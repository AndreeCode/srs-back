BEGIN;

DROP TABLE IF EXISTS guardian_sisnat_children;

CREATE TABLE IF NOT EXISTS guardian_his_children (
    guardian_id UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
    document_number VARCHAR(15) NOT NULL,
    birth_date DATE NOT NULL,
    child_name VARCHAR(150),
    relationship VARCHAR(50) NOT NULL DEFAULT 'Guardian',
    linked_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (guardian_id, document_number),
    CONSTRAINT guardian_his_children_document_check CHECK (document_number ~ '^[0-9]{8}$')
);

CREATE INDEX IF NOT EXISTS idx_guardian_his_children_document ON guardian_his_children(document_number);

CREATE TABLE IF NOT EXISTS his_service_rules (
    id SERIAL PRIMARY KEY,
    his_code VARCHAR(20) NOT NULL,
    dose_id INT,
    lab_value VARCHAR(10),
    service_id UUID NOT NULL REFERENCES care_services(id) ON DELETE CASCADE,
    priority INT NOT NULL DEFAULT 0,
    CONSTRAINT uq_his_service_rules UNIQUE NULLS NOT DISTINCT (his_code, dose_id, lab_value, service_id)
);

CREATE INDEX IF NOT EXISTS idx_his_service_rules_code ON his_service_rules(his_code);

DROP TRIGGER IF EXISTS trg_audit_guardian_his_children ON guardian_his_children;
CREATE TRIGGER trg_audit_guardian_his_children
AFTER INSERT OR UPDATE OR DELETE ON guardian_his_children
FOR EACH ROW EXECUTE FUNCTION audit_changes('guardian_id', 'document_number');

DROP TRIGGER IF EXISTS trg_audit_his_service_rules ON his_service_rules;
CREATE TRIGGER trg_audit_his_service_rules
AFTER INSERT OR UPDATE OR DELETE ON his_service_rules
FOR EACH ROW EXECUTE FUNCTION audit_changes('id');

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'sicna_app') THEN
        GRANT SELECT, INSERT, UPDATE, DELETE ON guardian_his_children, his_service_rules TO sicna_app;
        GRANT USAGE, SELECT ON SEQUENCE his_service_rules_id_seq TO sicna_app;
    END IF;
END;
$$;

COMMIT;
