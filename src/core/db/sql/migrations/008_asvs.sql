-- ASVS 5.0 V16.3.2: los accesos denegados (403) se registran en audit_log como ACCESS_DENIED.
-- Reemplaza log_auth_event de 006 agregando la accion; el resto queda igual.
CREATE OR REPLACE FUNCTION log_auth_event(p_action TEXT, p_user_id UUID, p_result result_type, p_details JSONB)
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
DECLARE
    v_device_id UUID;
    v_ip_address INET;
    v_user_agent TEXT;
BEGIN
    IF p_action NOT IN ('LOGIN', 'LOGIN_FAILED', 'LOGOUT', 'PASSWORD_CHANGED', 'ACCOUNT_LOCKED', 'MFA_ENABLED',
                        'MFA_DISABLED', 'MFA_RESET', 'MFA_FAILED', 'SESSION_IDLE', 'SESSION_REVOKED',
                        'ACCESS_DENIED') THEN
        RAISE EXCEPTION 'Accion de autenticacion no permitida: %', p_action;
    END IF;

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

    INSERT INTO audit_log (user_id, device_id, action, affected_table, record_id, record_key,
                           ip_address, user_agent, result, details)
    VALUES (p_user_id, v_device_id, p_action, 'users', p_user_id,
            CASE WHEN p_user_id IS NULL THEN NULL ELSE jsonb_build_object('id', p_user_id) END,
            v_ip_address, v_user_agent, p_result, p_details);
END;
$$;
