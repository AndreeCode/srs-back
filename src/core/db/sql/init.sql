BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

DROP FUNCTION IF EXISTS auditar_cambios() CASCADE;
DROP FUNCTION IF EXISTS actualizar_timestamp() CASCADE;
DROP TYPE IF EXISTS rol_tipo;
DROP TYPE IF EXISTS estado_control;
DROP TYPE IF EXISTS resultado_tipo;
DROP TYPE IF EXISTS unidad_tipo;

DO $$
DECLARE
    t TEXT;
    n BIGINT;
BEGIN
    IF to_regclass('public.age_packages') IS NULL THEN
        RETURN;
    END IF;

    FOREACH t IN ARRAY ARRAY['child_controls', 'child_guardian', 'children', 'age_packages'] LOOP
        IF to_regclass('public.' || t) IS NOT NULL THEN
            EXECUTE format('SELECT count(*) FROM %I', t) INTO n;
            IF n > 0 THEN
                RAISE EXCEPTION
                    'Table % has % rows and its structure changed. Migrate that data before running init.sql.', t, n;
            END IF;
        END IF;
    END LOOP;

    DROP TABLE IF EXISTS child_controls, child_guardian, children, age_packages CASCADE;
END;
$$;

DROP TYPE IF EXISTS unit_type;

DROP VIEW IF EXISTS v_children, child_service_status;
DROP TABLE IF EXISTS schema_migrations;

DO $$
BEGIN
    IF to_regtype('role_type') IS NULL THEN
        CREATE TYPE role_type AS ENUM ('guardian', 'health_staff', 'admin');
    END IF;

    IF to_regtype('control_status') IS NULL THEN
        CREATE TYPE control_status AS ENUM ('pending', 'completed', 'overdue', 'not_applicable');
    END IF;

    IF to_regtype('result_type') IS NULL THEN
        CREATE TYPE result_type AS ENUM ('successful', 'failed', 'blocked');
    END IF;

    IF to_regtype('birth_condition') IS NULL THEN
        CREATE TYPE birth_condition AS ENUM ('none', 'premature', 'low_weight', 'premature_low_weight');
    END IF;

    IF to_regtype('claim_status') IS NULL THEN
        CREATE TYPE claim_status AS ENUM ('pending', 'in_review', 'resolved', 'rejected');
    END IF;
END;
$$;

CREATE TABLE IF NOT EXISTS roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name role_type NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

UPDATE roles SET is_active = TRUE WHERE is_active IS NULL;
ALTER TABLE roles ALTER COLUMN is_active SET DEFAULT TRUE;
ALTER TABLE roles ALTER COLUMN is_active SET NOT NULL;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,

    role_id UUID NOT NULL REFERENCES roles(id),

    full_name VARCHAR(200) NOT NULL,
    dni VARCHAR(20),
    phone VARCHAR(30),
    email VARCHAR(255),

    terms_accepted BOOLEAN NOT NULL DEFAULT FALSE,
    terms_version VARCHAR(50),
    terms_accepted_at TIMESTAMPTZ,

    active BOOLEAN NOT NULL DEFAULT TRUE,
    blocked BOOLEAN NOT NULL DEFAULT FALSE,
    blocked_reason TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS role_permission (
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS regions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    health_network VARCHAR(150) NOT NULL DEFAULT 'Huamanga Health Network'
);

ALTER TABLE regions ADD COLUMN IF NOT EXISTS active BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE regions ALTER COLUMN health_network SET DEFAULT 'Huamanga Health Network';
UPDATE regions SET health_network = 'Huamanga Health Network' WHERE health_network = 'Red de Salud Huamanga';

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'regions_name_unique') THEN
        ALTER TABLE regions ADD CONSTRAINT regions_name_unique UNIQUE (name);
    END IF;
END;
$$;

CREATE TABLE IF NOT EXISTS health_facilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(250) NOT NULL UNIQUE,
    region_id UUID NOT NULL REFERENCES regions(id),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS user_region (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    region_id UUID NOT NULL REFERENCES regions(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, region_id)
);

CREATE TABLE IF NOT EXISTS children (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    padron_code VARCHAR(50) NOT NULL UNIQUE,
    medical_record_code VARCHAR(100),
    dni VARCHAR(20),

    first_names VARCHAR(150) NOT NULL,
    last_names VARCHAR(150) NOT NULL,
    birth_date DATE NOT NULL,
    gender CHAR(1),
    birth_condition birth_condition NOT NULL DEFAULT 'none',

    mother_name VARCHAR(200),
    mother_dni VARCHAR(20),
    address VARCHAR(300),
    contact_phone VARCHAR(50),
    insurance VARCHAR(100),

    health_facility_id UUID NOT NULL REFERENCES health_facilities(id),

    active BOOLEAN NOT NULL DEFAULT TRUE,
    registered_by UUID REFERENCES users(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT children_gender_check CHECK (gender IS NULL OR gender IN ('M', 'F')),
    CONSTRAINT children_dni_check CHECK (dni IS NULL OR dni ~ '^[0-9]{8}$')
);

CREATE TABLE IF NOT EXISTS guardians (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    full_name VARCHAR(200) NOT NULL,
    dni VARCHAR(20) NOT NULL UNIQUE,
    phone VARCHAR(50),
    email VARCHAR(255),

    user_id UUID UNIQUE REFERENCES users(id) ON DELETE SET NULL,

    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT guardians_dni_check CHECK (dni ~ '^[0-9]{8}$')
);

CREATE TABLE IF NOT EXISTS child_guardian (
    child_id UUID NOT NULL REFERENCES children(id) ON DELETE CASCADE,
    guardian_id UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
    relationship VARCHAR(50) NOT NULL DEFAULT 'Guardian',
    PRIMARY KEY (child_id, guardian_id)
);

CREATE TABLE IF NOT EXISTS care_packages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    description VARCHAR(500),

    min_age_days INTEGER NOT NULL,
    max_age_days INTEGER NOT NULL,

    at_risk_newborn_only BOOLEAN NOT NULL DEFAULT FALSE,

    sort_order INTEGER NOT NULL DEFAULT 1,
    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT care_packages_code_check CHECK (code ~ '^[A-Z0-9_]{2,50}$'),
    CONSTRAINT care_packages_age_check CHECK (min_age_days >= 0 AND min_age_days <= max_age_days)
);

CREATE TABLE IF NOT EXISTS care_services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    package_id UUID NOT NULL REFERENCES care_packages(id) ON DELETE CASCADE,

    code VARCHAR(80) NOT NULL,
    name VARCHAR(300) NOT NULL,

    group_name VARCHAR(150) NOT NULL DEFAULT 'DIRECT',
    group_order INTEGER NOT NULL DEFAULT 1,
    sort_order INTEGER NOT NULL DEFAULT 1,

    min_age_days INTEGER NOT NULL,
    max_age_days INTEGER NOT NULL,
    min_interval_days INTEGER NOT NULL DEFAULT 0,

    active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT care_services_package_code_unique UNIQUE (package_id, code),
    CONSTRAINT care_services_code_check CHECK (code ~ '^[A-Z0-9_]{2,80}$'),
    CONSTRAINT care_services_age_check CHECK (min_age_days >= 0 AND min_age_days <= max_age_days),
    CONSTRAINT care_services_interval_check CHECK (min_interval_days >= 0)
);

CREATE TABLE IF NOT EXISTS child_controls (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    child_id UUID NOT NULL REFERENCES children(id) ON DELETE CASCADE,
    service_id UUID NOT NULL REFERENCES care_services(id) ON DELETE CASCADE,

    status control_status NOT NULL DEFAULT 'pending',
    scheduled_date DATE,
    completed_date DATE,

    health_facility_id UUID REFERENCES health_facilities(id),

    batch_number VARCHAR(100),
    book_page VARCHAR(100),
    book_record VARCHAR(100),
    notes TEXT,

    registered_by UUID REFERENCES users(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT child_controls_unique UNIQUE (child_id, service_id),
    CONSTRAINT child_controls_completed_check
        CHECK ((status = 'completed') = (completed_date IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    child_id UUID NOT NULL REFERENCES children(id) ON DELETE CASCADE,
    requester_user_id UUID NOT NULL REFERENCES users(id),

    requester_dni VARCHAR(20) NOT NULL,
    child_dni VARCHAR(20),
    child_identifier VARCHAR(100) NOT NULL,

    health_facility_id UUID REFERENCES health_facilities(id),
    service_id UUID REFERENCES care_services(id) ON DELETE SET NULL,
    attention_date DATE,

    message TEXT NOT NULL,

    status claim_status NOT NULL DEFAULT 'pending',
    response TEXT,
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT claims_requester_dni_check CHECK (requester_dni ~ '^[0-9]{8}$')
);

CREATE TABLE IF NOT EXISTS claim_evidences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    claim_id UUID NOT NULL REFERENCES claims(id) ON DELETE CASCADE,

    original_name VARCHAR(255) NOT NULL,
    storage_path TEXT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    size_bytes INTEGER NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT claim_evidences_mime_check
        CHECK (mime_type IN ('image/jpeg', 'image/png', 'application/pdf')),
    CONSTRAINT claim_evidences_size_check
        CHECK (size_bytes > 0 AND size_bytes <= 10485760)
);

CREATE TABLE IF NOT EXISTS devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    device_hash VARCHAR(64) NOT NULL,
    user_agent TEXT,

    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    trusted BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT devices_user_hash_unique UNIQUE (user_id, device_hash)
);

CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_id UUID NOT NULL REFERENCES devices(id) ON DELETE CASCADE,

    token_hash VARCHAR(128) NOT NULL UNIQUE,
    ip_address INET,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,

    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    revoked_reason VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID REFERENCES users(id),
    device_id UUID REFERENCES devices(id),

    action VARCHAR(100) NOT NULL,
    affected_table VARCHAR(100),

    record_id UUID,
    record_key JSONB,

    ip_address INET,
    user_agent TEXT,

    result result_type NOT NULL DEFAULT 'successful',
    details JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION audit_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
DECLARE
    v_user_id UUID;
    v_device_id UUID;
    v_ip_address INET;
    v_user_agent TEXT;

    v_row JSONB;
    v_old JSONB;
    v_new JSONB;
    v_record_id UUID;
    v_record_key JSONB;
    v_details JSONB;
    v_col TEXT;
BEGIN
    BEGIN
        v_user_id := NULLIF(current_setting('app.user_id', true), '')::UUID;
    EXCEPTION WHEN OTHERS THEN
        v_user_id := NULL;
    END;

    BEGIN
        v_device_id := NULLIF(current_setting('app.device_id', true), '')::UUID;
    EXCEPTION WHEN OTHERS THEN
        v_device_id := NULL;
    END;

    BEGIN
        v_ip_address := NULLIF(current_setting('app.ip_address', true), '')::INET;
    EXCEPTION WHEN OTHERS THEN
        v_ip_address := NULL;
    END;

    v_user_agent := NULLIF(current_setting('app.user_agent', true), '');

    IF TG_OP IN ('UPDATE', 'DELETE') THEN
        v_old := to_jsonb(OLD);
    END IF;
    IF TG_OP IN ('INSERT', 'UPDATE') THEN
        v_new := to_jsonb(NEW);
    END IF;
    v_row := COALESCE(v_new, v_old);

    IF TG_NARGS = 0 THEN
        v_record_id := (v_row ->> 'id')::UUID;
        v_record_key := jsonb_build_object('id', v_row -> 'id');
    ELSE
        v_record_key := '{}'::JSONB;
        FOREACH v_col IN ARRAY TG_ARGV LOOP
            v_record_key := v_record_key || jsonb_build_object(v_col, v_row -> v_col);
        END LOOP;
    END IF;

    v_old := v_old - 'password_hash' - 'token_hash';
    v_new := v_new - 'password_hash' - 'token_hash';

    IF TG_OP = 'UPDATE' AND (v_old - 'updated_at') = (v_new - 'updated_at') THEN
        RETURN NEW;
    END IF;

    v_details := CASE TG_OP
        WHEN 'INSERT' THEN jsonb_build_object('new', v_new)
        WHEN 'DELETE' THEN jsonb_build_object('old', v_old)
        ELSE jsonb_build_object('old', v_old, 'new', v_new)
    END;

    INSERT INTO audit_log (
        user_id, device_id, action, affected_table, record_id, record_key,
        ip_address, user_agent, result, details
    )
    VALUES (
        v_user_id, v_device_id, TG_OP, TG_TABLE_NAME, v_record_id, v_record_key,
        v_ip_address, v_user_agent, 'successful', v_details
    );

    RETURN COALESCE(NEW, OLD);
END;
$$;

CREATE OR REPLACE FUNCTION check_child_control_dates()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_birth DATE;
BEGIN
    IF NEW.completed_date IS NULL THEN
        RETURN NEW;
    END IF;

    SELECT birth_date INTO v_birth FROM children WHERE id = NEW.child_id;

    IF NEW.completed_date < v_birth OR NEW.completed_date > CURRENT_DATE THEN
        RAISE EXCEPTION 'Attention date (%) must be between the birth date (%) and today', NEW.completed_date, v_birth
            USING ERRCODE = 'check_violation';
    END IF;

    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION check_claim_evidence_limit()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF (SELECT count(*) FROM claim_evidences WHERE claim_id = NEW.claim_id) >= 5 THEN
        RAISE EXCEPTION 'A claim can have at most 5 evidence files'
            USING ERRCODE = 'check_violation';
    END IF;
    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION check_guardian_user_role()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.user_id IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM users u JOIN roles r ON r.id = u.role_id
        WHERE u.id = NEW.user_id AND r.name = 'guardian'
    ) THEN
        RAISE EXCEPTION 'The user linked to a guardian must have the guardian role'
            USING ERRCODE = 'check_violation';
    END IF;
    RETURN NEW;
END;
$$;

DO $$
DECLARE
    t TEXT;
BEGIN
    FOREACH t IN ARRAY ARRAY['users', 'children', 'guardians', 'care_packages', 'care_services', 'child_controls', 'claims'] LOOP
        EXECUTE format('DROP TRIGGER IF EXISTS trg_%1$s_updated_at ON %1$I', t);
        EXECUTE format('CREATE TRIGGER trg_%1$s_updated_at BEFORE UPDATE ON %1$I
                        FOR EACH ROW EXECUTE FUNCTION update_timestamp()', t);
    END LOOP;

    FOREACH t IN ARRAY ARRAY[
        'roles', 'users', 'permissions', 'regions', 'health_facilities',
        'children', 'guardians', 'care_packages', 'care_services', 'child_controls',
        'claims', 'claim_evidences', 'devices', 'sessions'
    ] LOOP
        EXECUTE format('DROP TRIGGER IF EXISTS trg_audit_%1$s ON %1$I', t);
        EXECUTE format('CREATE TRIGGER trg_audit_%1$s AFTER INSERT OR UPDATE OR DELETE ON %1$I
                        FOR EACH ROW EXECUTE FUNCTION audit_changes()', t);
    END LOOP;
END;
$$;

DROP TRIGGER IF EXISTS trg_audit_user_region ON user_region;
CREATE TRIGGER trg_audit_user_region
AFTER INSERT OR UPDATE OR DELETE ON user_region
FOR EACH ROW EXECUTE FUNCTION audit_changes('user_id', 'region_id');

DROP TRIGGER IF EXISTS trg_audit_child_guardian ON child_guardian;
CREATE TRIGGER trg_audit_child_guardian
AFTER INSERT OR UPDATE OR DELETE ON child_guardian
FOR EACH ROW EXECUTE FUNCTION audit_changes('child_id', 'guardian_id');

DROP TRIGGER IF EXISTS trg_audit_role_permission ON role_permission;
CREATE TRIGGER trg_audit_role_permission
AFTER INSERT OR UPDATE OR DELETE ON role_permission
FOR EACH ROW EXECUTE FUNCTION audit_changes('role_id', 'permission_id');

DROP TRIGGER IF EXISTS trg_child_controls_dates ON child_controls;
CREATE TRIGGER trg_child_controls_dates
BEFORE INSERT OR UPDATE OF completed_date, child_id ON child_controls
FOR EACH ROW EXECUTE FUNCTION check_child_control_dates();

DROP TRIGGER IF EXISTS trg_claim_evidences_limit ON claim_evidences;
CREATE TRIGGER trg_claim_evidences_limit
BEFORE INSERT ON claim_evidences
FOR EACH ROW EXECUTE FUNCTION check_claim_evidence_limit();

DROP TRIGGER IF EXISTS trg_guardians_user_role ON guardians;
CREATE TRIGGER trg_guardians_user_role
BEFORE INSERT OR UPDATE OF user_id ON guardians
FOR EACH ROW EXECUTE FUNCTION check_guardian_user_role();

CREATE INDEX IF NOT EXISTS idx_users_role ON users(role_id);
CREATE INDEX IF NOT EXISTS idx_user_region_region ON user_region(region_id);
CREATE INDEX IF NOT EXISTS idx_health_facilities_region ON health_facilities(region_id);

CREATE INDEX IF NOT EXISTS idx_children_facility ON children(health_facility_id);
CREATE INDEX IF NOT EXISTS idx_children_birth_date ON children(birth_date);
CREATE INDEX IF NOT EXISTS idx_children_registered_by ON children(registered_by);
CREATE INDEX IF NOT EXISTS idx_children_medical_record ON children(medical_record_code);
CREATE INDEX IF NOT EXISTS idx_children_active ON children(active) WHERE active;
CREATE UNIQUE INDEX IF NOT EXISTS uq_children_dni ON children(dni) WHERE dni IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_children_name
    ON children (lower(last_names), lower(first_names));

CREATE INDEX IF NOT EXISTS idx_child_guardian_guardian ON child_guardian(guardian_id);

CREATE INDEX IF NOT EXISTS idx_care_services_package ON care_services(package_id, group_order, sort_order);

CREATE INDEX IF NOT EXISTS idx_child_controls_child ON child_controls(child_id);
CREATE INDEX IF NOT EXISTS idx_child_controls_service ON child_controls(service_id);
CREATE INDEX IF NOT EXISTS idx_child_controls_status ON child_controls(status);
CREATE INDEX IF NOT EXISTS idx_child_controls_scheduled_date ON child_controls(scheduled_date);
CREATE INDEX IF NOT EXISTS idx_child_controls_completed_date ON child_controls(completed_date);
CREATE INDEX IF NOT EXISTS idx_child_controls_registered_by ON child_controls(registered_by);

CREATE INDEX IF NOT EXISTS idx_claims_child ON claims(child_id);
CREATE INDEX IF NOT EXISTS idx_claims_requester ON claims(requester_user_id);
CREATE INDEX IF NOT EXISTS idx_claims_status ON claims(status, created_at);
CREATE INDEX IF NOT EXISTS idx_claim_evidences_claim ON claim_evidences(claim_id);

CREATE INDEX IF NOT EXISTS idx_devices_user ON devices(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_user_revoked ON sessions(user_id, revoked);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at);

CREATE INDEX IF NOT EXISTS idx_audit_log_user_date ON audit_log(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action);
CREATE INDEX IF NOT EXISTS idx_audit_log_table_record ON audit_log(affected_table, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_date ON audit_log(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_log_record_key ON audit_log USING GIN(record_key);

DROP INDEX IF EXISTS idx_children_region;
DROP INDEX IF EXISTS idx_children_guardian;
DROP INDEX IF EXISTS idx_children_dni;

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'sicna_app') THEN
        GRANT SELECT, INSERT, UPDATE, DELETE ON
            roles, users, permissions, role_permission,
            regions, health_facilities, user_region,
            children, guardians, child_guardian,
            care_packages, care_services, child_controls,
            claims, claim_evidences, devices, sessions
        TO sicna_app;

        GRANT SELECT ON audit_log TO sicna_app;
        REVOKE INSERT, UPDATE, DELETE ON audit_log FROM sicna_app;

    END IF;
END;
$$;

COMMIT;
