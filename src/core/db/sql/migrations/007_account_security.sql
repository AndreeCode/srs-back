BEGIN;

-- ASVS V6/V7: MFA con TOTP y cierre de sesion por inactividad.
-- mfa_secret / mfa_pending_secret van cifrados con AES-GCM por la app (MFA_ENCRYPTION_KEY), y
-- mfa_recovery_codes guarda solo SHA-256 de los codigos de respaldo. Ninguno se copia a audit_log.
ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_secret TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_pending_secret TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_last_step BIGINT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_recovery_codes TEXT[] NOT NULL DEFAULT '{}';
ALTER TABLE users ADD COLUMN IF NOT EXISTS mfa_enabled_at TIMESTAMPTZ;

ALTER TABLE sessions ADD COLUMN IF NOT EXISTS last_activity_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

-- ASVS V6.4: las contrasenas que asigna el personal son temporales y vencen (TEMP_PASSWORD_HOURS).
ALTER TABLE users ADD COLUMN IF NOT EXISTS must_change_password BOOLEAN NOT NULL DEFAULT FALSE;

COMMIT;
