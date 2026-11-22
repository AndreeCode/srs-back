BEGIN;

-- A08: SHA-256 de cada evidencia al subirla; se verifica antes de entregarla. Las evidencias previas
-- (NULL) reciben su hash en la primera descarga.
ALTER TABLE claim_evidences ADD COLUMN IF NOT EXISTS sha256 CHAR(64);

COMMIT;
