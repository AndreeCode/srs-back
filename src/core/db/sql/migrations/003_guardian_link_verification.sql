BEGIN;

-- A06: el vinculo que crea el propio padre (registro publico o portal) queda pendiente hasta que
-- el personal lo verifica en persona. DEFAULT TRUE: los vinculos existentes y los que registra
-- el personal siguen verificados.
ALTER TABLE child_guardian ADD COLUMN IF NOT EXISTS verified BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE child_guardian ADD COLUMN IF NOT EXISTS requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW();
ALTER TABLE child_guardian ADD COLUMN IF NOT EXISTS verified_by UUID REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE child_guardian ADD COLUMN IF NOT EXISTS verified_at TIMESTAMPTZ;

ALTER TABLE guardian_his_children ADD COLUMN IF NOT EXISTS verified BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE guardian_his_children ADD COLUMN IF NOT EXISTS verified_by UUID REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE guardian_his_children ADD COLUMN IF NOT EXISTS verified_at TIMESTAMPTZ;

CREATE INDEX IF NOT EXISTS idx_child_guardian_pending ON child_guardian (requested_at) WHERE NOT verified;
CREATE INDEX IF NOT EXISTS idx_guardian_his_children_pending ON guardian_his_children (created_at) WHERE NOT verified;

-- Intentos de vincular un nino desde el registro publico o el portal (limite contra adivinar la
-- fecha de nacimiento). identifier_hash = HMAC-SHA256 del DNI / codigo de padron: no se guarda en claro.
CREATE TABLE IF NOT EXISTS portal_link_attempts (
    id BIGSERIAL PRIMARY KEY,
    identifier_hash CHAR(64) NOT NULL,
    ip_address INET,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    success BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_portal_link_attempts_identifier ON portal_link_attempts (identifier_hash, created_at);
CREATE INDEX IF NOT EXISTS idx_portal_link_attempts_ip ON portal_link_attempts (ip_address, created_at);
CREATE INDEX IF NOT EXISTS idx_portal_link_attempts_user ON portal_link_attempts (user_id, created_at);

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'sicna_app') THEN
        GRANT SELECT, INSERT, DELETE ON portal_link_attempts TO sicna_app;
        GRANT USAGE, SELECT ON SEQUENCE portal_link_attempts_id_seq TO sicna_app;
    END IF;
END;
$$;

COMMIT;
