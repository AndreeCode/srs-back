BEGIN;

ALTER TABLE users ADD COLUMN IF NOT EXISTS blocked_at TIMESTAMPTZ;
ALTER TABLE users ADD COLUMN IF NOT EXISTS blocked_by UUID REFERENCES users(id) ON DELETE SET NULL;

ALTER TABLE devices ADD COLUMN IF NOT EXISTS block_scope VARCHAR(20);
ALTER TABLE devices ADD COLUMN IF NOT EXISTS blocked_reason TEXT;
ALTER TABLE devices ADD COLUMN IF NOT EXISTS blocked_at TIMESTAMPTZ;
ALTER TABLE devices ADD COLUMN IF NOT EXISTS blocked_by UUID REFERENCES users(id) ON DELETE SET NULL;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'devices_block_scope_check') THEN
        ALTER TABLE devices ADD CONSTRAINT devices_block_scope_check
            CHECK (block_scope IS NULL OR block_scope IN ('account', 'browser'));
    END IF;
END;
$$;

CREATE INDEX IF NOT EXISTS idx_devices_hash ON devices(device_hash);

CREATE OR REPLACE FUNCTION stamp_block()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_actor UUID := NULLIF(current_setting('app.user_id', true), '')::uuid;
    v_now_blocked BOOLEAN;
    v_was_blocked BOOLEAN;
BEGIN
    IF TG_TABLE_NAME = 'users' THEN
        v_now_blocked := NEW.blocked;
        v_was_blocked := OLD.blocked;
    ELSE
        v_now_blocked := NOT NEW.trusted;
        v_was_blocked := NOT OLD.trusted;
    END IF;

    IF v_now_blocked AND NOT v_was_blocked THEN
        NEW.blocked_at := NOW();
        NEW.blocked_by := v_actor;
    ELSIF NOT v_now_blocked AND v_was_blocked THEN
        NEW.blocked_at := NULL;
        NEW.blocked_by := NULL;
        NEW.blocked_reason := NULL;
        IF TG_TABLE_NAME = 'devices' THEN
            NEW.block_scope := NULL;
        END IF;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_users_stamp_block ON users;
CREATE TRIGGER trg_users_stamp_block
BEFORE UPDATE OF blocked ON users
FOR EACH ROW EXECUTE FUNCTION stamp_block();

DROP TRIGGER IF EXISTS trg_devices_stamp_block ON devices;
CREATE TRIGGER trg_devices_stamp_block
BEFORE UPDATE OF trusted ON devices
FOR EACH ROW EXECUTE FUNCTION stamp_block();

CREATE OR REPLACE FUNCTION revoke_sessions_of_blocked_user()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.blocked AND NOT OLD.blocked THEN
        UPDATE sessions SET revoked = true, revoked_reason = 'user_blocked'
        WHERE user_id = NEW.id AND NOT revoked;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_users_revoke_on_block ON users;
CREATE TRIGGER trg_users_revoke_on_block
AFTER UPDATE OF blocked ON users
FOR EACH ROW EXECUTE FUNCTION revoke_sessions_of_blocked_user();

CREATE TABLE IF NOT EXISTS security_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    kind VARCHAR(30) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    device_hash VARCHAR(64),
    detail JSONB NOT NULL DEFAULT '{}'::jsonb,

    status VARCHAR(20) NOT NULL DEFAULT 'open',
    resolution TEXT,
    resolved_by UUID REFERENCES users(id) ON DELETE SET NULL,
    resolved_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT security_alerts_kind_check CHECK (kind IN ('shared_device', 'many_devices')),
    CONSTRAINT security_alerts_status_check CHECK (status IN ('open', 'resolved', 'dismissed'))
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_security_alerts_open ON security_alerts(kind, subject) WHERE status = 'open';
CREATE INDEX IF NOT EXISTS idx_security_alerts_status ON security_alerts(status, updated_at);

DROP TRIGGER IF EXISTS trg_security_alerts_updated_at ON security_alerts;
CREATE TRIGGER trg_security_alerts_updated_at BEFORE UPDATE ON security_alerts
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

DROP TRIGGER IF EXISTS trg_audit_security_alerts ON security_alerts;
CREATE TRIGGER trg_audit_security_alerts AFTER INSERT OR UPDATE OR DELETE ON security_alerts
FOR EACH ROW EXECUTE FUNCTION audit_changes();

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'sicna_app') THEN
        GRANT SELECT, INSERT, UPDATE, DELETE ON security_alerts TO sicna_app;
    END IF;
END;
$$;

COMMIT;
