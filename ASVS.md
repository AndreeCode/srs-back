# SICNA / signa frente a OWASP ASVS 5.0, nivel 2

Este documento cubre el sistema completo: `SICNA-backend` (FastAPI), `signa-frontend` (Next.js) y la lectura del HIS-MINSA (SQL Server). El nivel objetivo es el **2**, porque el sistema maneja datos de salud de niños y de sus padres. Los requisitos de documentación (los `V*.1.*`) se responden primero; después viene la matriz por capítulo.

Estados: **Cumple** · **N/A** (el sistema no tiene esa función) · **Operación** (depende del despliegue, ver la nota).

## Documentación exigida

### Plazos de corrección de componentes (V15.1.1)

| Severidad (CVSS / GHSA) | Plazo |
|---|---|
| Crítica | 72 horas |
| Alta | 7 días |
| Media | 30 días |
| Baja | En la siguiente actualización programada (máximo 90 días) |

Fuentes de aviso: `pip-audit` y `bun audit` (en cada push y cada lunes), Dependabot (cooldown de 7 días) y el SBOM. Si se ignora un aviso, va de forma explícita en el workflow y con su motivo (hoy solo `GHSA-mrhx-c7xc-m3w5`: `zod@3`, que solo usa la CLI de shadcn en desarrollo).

### Inventario de componentes (V15.1.2)

`requirements.in` y `requirements.txt` (lock con hashes) en el back, `package.json` y `bun.lock` en el front. El job `sbom` de `.github/workflows/dependency-audit.yml` genera un SBOM **CycloneDX** (`sbom.cdx.json`) en cada ejecución y lo guarda 90 días.

### Operaciones costosas (V15.1.3 y V2.4.1)

| Operación | Defensa |
|---|---|
| Login y segundo factor | `LOGIN_RATE_LIMIT` por minuto por IP y bloqueo de la cuenta tras `LOGIN_MAX_ATTEMPTS`. Los usuarios inexistentes siguen la misma secuencia |
| Reautenticación (configurar el MFA, cerrar sesiones, cambiar la contraseña) | Cada fallo cuenta para el bloqueo de la cuenta, y el bloqueo cierra sus sesiones |
| Consultas al HIS (`/his/children/lookup`, `/his/children/{dni}`, `/his/guardians/{id}`) | 60 cada 10 min por usuario (`core/security/throttle.py`), además de `command_timeout` |
| Subir evidencias (personal y portal) | 30 y 10 cada 10 min por usuario, 10 MB por archivo, con tope de evidencias por reclamo |
| Descargar evidencias | 60 cada 10 min por usuario |
| Vincular hijos desde el portal | `portal_link_attempts`: 5 por niño cada 24 h, 10 por IP cada hora, 5 por cuenta cada 24 h |
| Reclamos abiertos desde el portal | 3 como máximo por niño |
| Verificar la cadena de auditoría | 6 cada 10 min por usuario |
| Llamadas de signa al back | `AbortSignal.timeout` (15 s, 30 s y 2 min) |

Los límites en memoria son por proceso.

### Reglas de autorización (V8.1.1 y V8.1.2)

- Cada ruta declara su permiso con `require_permission("<modulo>.<verbo>")`. El catálogo está en `permission_catalog.py` y los roles son `admin`, `health_staff` y `guardian`.
- Un `guardian` (portal) solo ve a sus hijos con vínculo **verificado**. Los vínculos pendientes se muestran enmascarados y nunca con el nombre del niño. Las descargas del portal verifican que la evidencia sea de un reclamo propio.
- El personal se asigna a una o varias micro redes (`user_region`).
- El reset de contraseña, el bloqueo o la desactivación de un usuario cierran todas sus sesiones al instante (ver `CLAUDE.md` de srs).
- signa nunca autoriza a partir de la cookie `session_role`: el rol sale de `/auth/me`.

### Tipos de archivo permitidos (V5.1.1)

| Flujo | Tipos | Tamaño | Validación |
|---|---|---|---|
| Evidencias de reclamo | JPG, PNG y PDF | 10 MB | Tipo detectado por *magic bytes*, no por la extensión ni el `Content-Type`. Nombre generado por el servidor, archivo `0600` en una carpeta `0700`, fuera del webroot (`UPLOAD_DIR`) |
| Descarga de evidencias | Las mismas, como `attachment` | — | SHA-256 verificado (409 si cambió el archivo) |
| Export CSV (signa) | `text/csv` | — | `toCsv()` neutraliza fórmulas |

### Clasificación de datos (V14.1.1 y V14.1.2)

| Nivel | Datos | Protección |
|---|---|---|
| **Secreto** | Hash de contraseña, secreto TOTP, códigos de respaldo, tokens, claves (`JWT_SECRET`, `AUDIT_CHAIN_KEY`, `MFA_ENCRYPTION_KEY`), credenciales del HIS | Argon2, AES-GCM, SHA-256 o HMAC. No se devuelven ni se registran en el log. Se leen del `.env` o de `*_FILE` |
| **Sensible (salud, menores)** | Padrón de niños, controles y vacunas, evidencias, datos del HIS, DNI de padres | Permisos, vínculo verificado, auditoría, `Cache-Control: no-store`, `Clear-Site-Data` al salir, DNI por `POST` (no en la URL), identificador del niño en los intentos guardado como HMAC |
| **Interno** | Usuarios, establecimientos, micro redes, auditoría y alertas | Permisos y auditoría |
| **Público** | `GET /api` | — |

### Inventario de criptografía y claves (V11.1.1 y V11.1.2)

| Uso | Algoritmo | Clave | Rotación |
|---|---|---|---|
| Contraseñas | Argon2id, se re-hashea al iniciar sesión si cambian los parámetros | — | Automática |
| JWT de sesión y de MFA | HMAC-SHA256/384/512 con `iss=sicna`, `iat`, `exp` y `sid` | `JWT_SECRET` (32 caracteres o más) | Cambiarla cierra todas las sesiones e invalida los HMAC de `portal_link_attempts` |
| Tokens en BD | SHA-256 | — | — |
| Secreto TOTP | AES-256-GCM con AAD `mfa:<user_id>` | `MFA_ENCRYPTION_KEY` | Para cambiarla hay que resetear el MFA de todos |
| Cadena de auditoría | HMAC-SHA256 encadenado | `AUDIT_CHAIN_KEY` | **No se puede cambiar** una vez creada la cadena |
| Integridad de evidencias | SHA-256 | — | — |
| TLS hacia PostgreSQL y el HIS | `DB_SSLMODE` y `MSSQL_ENCRYPTION` | — | — |
| Aleatoriedad | `secrets` y `crypto.randomUUID()` (nonce de la CSP) | — | — |

### Comunicaciones (V13.1.1 y V12)

| Origen → destino | Protocolo | Autenticación |
|---|---|---|
| Navegador → signa | HTTPS (proxy TLS; HSTS lo envía Next) | Cookie `__Host-access_token` |
| signa → back | HTTP por loopback o red interna, nunca expuesto | Cookie reenviada. `X-Forwarded-For` solo se acepta desde `TRUSTED_PROXIES` |
| Back → PostgreSQL | TCP con `DB_SSLMODE` (`require` o más si la BD es remota) | `sicna_app` con privilegios mínimos |
| Back → HIS-MINSA (SQL Server) | TDS con `MSSQL_ENCRYPTION=require` | Usuario de **solo lectura**, con una guarda de solo lectura en `sqlserver_fetch`. FreeTDS cifra pero no valida el certificado: usar una red privada |
| `scripts/migrate` → PostgreSQL | Igual | Dueño del esquema |

**Operación**: el proxy TLS (fuera del repositorio) debe usar TLS 1.2 o 1.3 con AEAD, un certificado válido y redirigir HTTP a HTTPS.

### Inventario de registros (V16.1.1)

| Evento | Dónde |
|---|---|
| Cambios en tablas (antes y después, actor, IP, dispositivo) | `audit_log` (trigger) |
| `LOGIN`, `LOGIN_FAILED` (con el motivo, incluido `reauth_bad_password`), `ACCOUNT_LOCKED`, `LOGOUT`, `PASSWORD_CHANGED`, `MFA_ENABLED`, `MFA_DISABLED`, `MFA_RESET`, `MFA_FAILED`, `SESSION_IDLE`, `SESSION_REVOKED` | `audit_log` (`log_auth_event`) |
| `ACCESS_DENIED`: cualquier 403 de una petición autenticada (método y ruta) | `audit_log` (migración `008`, `AuthMiddleware`) |
| Alertas `brute_force_account`, `brute_force_ip`, `shared_device`, `many_devices` y `audit_chain_broken` | `security_alerts` y el dashboard de signa |
| 4xx y 5xx | stdout (sin el cuerpo de la petición) |

Los timestamps del log van en UTC ISO-8601 y en la BD como `TIMESTAMPTZ`. Nunca se registran contraseñas ni tokens. El log escapa `\r` y `\n`.

## Matriz por capítulo

### V1 Codificación y saneamiento
| Req. | Estado | Evidencia |
|---|---|---|
| 1.2.x Inyección (HTML, SQL, OS) | Cumple | React escapa por defecto. Postgres con `$n`, SQL Server con `%s` (`placeholders()`) y la guarda de solo lectura. `reset.py` usa `quote_ident()` |
| 1.2.10 Inyección CSV | Cumple | `toCsv()` en `lib/sisnat/logic.ts` |
| 1.3.x SSRF y HTML del usuario | N/A | |
| 1.5.x Deserialización | Cumple | Solo JSON (Pydantic) y multipart |

### V2 Validación y lógica de negocio
| Req. | Estado | Evidencia |
|---|---|---|
| 2.1.1 Reglas documentadas | Cumple | `CLAUDE.md` de srs (esquema y reglas) |
| 2.2.x Validación en el servidor | Cumple | Pydantic, validaciones de cada servicio y triggers (fechas de control) |
| 2.3.x Lógica de negocio | Cumple | Los vínculos creados por el padre quedan pendientes, hay tope de reclamos abiertos, y la contraseña temporal y el MFA son obligatorios antes de usar la app |
| 2.4.1 Anti-automatización | Cumple | Ver [Operaciones costosas](#operaciones-costosas-v1513-y-v241) |

### V3 Seguridad del front web
| Req. | Estado | Evidencia |
|---|---|---|
| 3.2.x Interpretación del contenido | Cumple | `nosniff` y descargas como `attachment` |
| 3.3.x Cookies | Cumple | `__Host-` en producción, `HttpOnly`, `Secure` y `SameSite=Lax` (`lib/cookie-names.ts`) |
| 3.4.1 HSTS | Cumple | `next.config.ts` y el back en producción |
| 3.4.3 CSP | Cumple | Nonce + `strict-dynamic`, `object-src 'none'` y `frame-ancestors 'none'` (`lib/csp.ts`, `proxy.ts`) |
| 3.4.4 a 3.4.8 Otras cabeceras | Cumple | `Referrer-Policy`, `X-Frame-Options`, COOP, CORP en el back y `Permissions-Policy` |
| 3.5.x CSRF | Cumple | Server Actions (Next valida `Origin`), `SameSite`, descargas `GET` sin efectos. El back no es accesible desde el navegador |

### V4 API
| Req. | Estado | Evidencia |
|---|---|---|
| 4.1.1 `Content-Type` | Cumple | JSON, y archivos con su tipo detectado |
| 4.1.2 Solo HTTPS | Operación | Proxy TLS con HSTS |
| 4.1.3 Cabeceras de proxy | Cumple | `TRUSTED_PROXIES` |
| 4.2.x Mensajes HTTP | Cumple | Métodos limitados y tope de tamaño del cuerpo |
| 4.3 y 4.4 GraphQL y WebSocket | N/A | |

### V5 Archivos
| Req. | Estado | Evidencia |
|---|---|---|
| 5.2.1 Tamaño | Cumple | 10 MB (`MAX_EVIDENCE_BYTES`) |
| 5.2.2 Tipo real | Cumple | *Magic bytes* (JPG, PNG y PDF) |
| 5.3.1 a 5.3.3 Almacenamiento | Cumple | `file_storage.py` rechaza rutas fuera de `UPLOAD_DIR`, el nombre lo genera el servidor, permisos `0600`/`0700`, se descarga como `attachment` y no se ejecuta |

### V6 Autenticación
| Req. | Estado | Evidencia |
|---|---|---|
| 6.1.1 Anti-automatización documentada | Cumple | Ver arriba |
| 6.1.2 Palabras de contexto | Cumple | `password_policy`: rechaza las que contengan el usuario, el DNI, el nombre, el correo o «sicna», «signa» o «sisnat» |
| 6.2.x Contraseñas | Cumple | De 8 a 128 caracteres, sin reglas de composición, lista de contraseñas comunes. Cambiarla pide la actual |
| 6.3.1 Fuerza bruta | Cumple | Por IP y por cuenta, con el mismo trato y el mismo tiempo para usuarios inexistentes |
| 6.3.2 Cuentas por defecto | Cumple | En producción el seed genera contraseñas aleatorias |
| 6.3.3 MFA | Cumple | TOTP obligatorio para `MFA_ROLES` (`admin` y `health_staff`) en producción |
| 6.3.4 Vías de acceso | Cumple | Login único. El registro público está apagado por defecto (`PUBLIC_REGISTRATION`) |
| 6.4.x Contraseñas temporales | Cumple | Vencen a las `TEMP_PASSWORD_HOURS` y se deben cambiar en el primer ingreso (migración `007`) |
| 6.4.4 Reset del MFA | Cumple | Lo hace otra persona con permiso, queda auditado y cierra las sesiones |
| 6.5.x TOTP y códigos de respaldo | Cumple | RFC 6238, sin reutilizar pasos, códigos de respaldo de un solo uso como SHA-256 |
| 6.6 a 6.8 | N/A | |

### V7 Sesiones
| Req. | Estado | Evidencia |
|---|---|---|
| 7.2.x Validación en el servidor y token nuevo | Cumple | Sesión en BD en cada petición |
| 7.3.1 y 7.3.2 Inactividad y expiración absoluta | Cumple | `SESSION_IDLE_MINUTES` (30) y `JWT_EXPIRE_MINUTES` (60) |
| 7.4.1 y 7.4.2 Logout y desactivación | Cumple | Revocación en BD y `Clear-Site-Data` |
| 7.4.3 Cerrar otras sesiones al cambiar un factor | Cumple | Al cambiar la contraseña y al activar o desactivar el MFA |
| 7.4.5 El admin puede cerrar sesiones | Cumple | Gestión de sesiones y dispositivos |
| 7.5.1 Reautenticación antes de cambios sensibles | Cumple | Configurar o desactivar el MFA y cambiar la contraseña piden la contraseña (`auth_mfa_service.confirm_password`) |
| 7.5.2 Ver y cerrar sesiones propias | Cumple | `GET /auth/sessions`, y `POST /auth/sessions/{id}/revoke` y `/revoke-others` con contraseña (modal «Mis sesiones») |

### V8 Autorización
| Req. | Estado | Evidencia |
|---|---|---|
| 8.1.x Documentación | Cumple | Ver [Reglas de autorización](#reglas-de-autorización-v811-y-v812) |
| 8.2.x Funciones y datos (IDOR) | Cumple | `require_permission` y, en el portal, el filtro por vínculo verificado y por dueño del reclamo |
| 8.3.x Capa de confianza | Cumple | Todo lo valida el back. signa toma el rol de `/auth/me` |

### V9 Tokens
| Req. | Estado | Evidencia |
|---|---|---|
| 9.1.x y 9.2.x | Cumple | Lista fija de algoritmos HS*, y `exp`, `iat`, `iss`, `sub` y `sid` obligatorios. El token del paso de MFA es distinto y dura 5 min |

### V10 OAuth — N/A

### V11 Criptografía
| Req. | Estado | Evidencia |
|---|---|---|
| 11.1.x | Cumple | Ver [Inventario de criptografía](#inventario-de-criptografía-y-claves-v1111-y-v1112) |
| 11.2.x a 11.6.x | Cumple | AES-256-GCM, HMAC-SHA256, Argon2id y CSPRNG |

### V12 Comunicación
| Req. | Estado | Evidencia |
|---|---|---|
| 12.1.x y 12.2.x | Operación | Proxy TLS y HSTS |
| 12.3.x | Cumple / Operación | `DB_SSLMODE` y `MSSQL_ENCRYPTION` obligatorios en producción con servidores remotos. Al HIS, por una red privada |

### V13 Configuración
| Req. | Estado | Evidencia |
|---|---|---|
| 13.1.1 | Cumple | Ver [Comunicaciones](#comunicaciones-v1311-y-v12) |
| 13.2.x Mínimo privilegio | Cumple | `sicna_app` solo con `SELECT` en `audit_log`, y el HIS de solo lectura |
| 13.3.x Secretos | Cumple | `.env` o `*_FILE`, y `ensure_valid()` al arrancar |
| 13.4.x Depuración | Cumple | `/docs` apagado en producción y errores con mensajes fijos |

### V14 Datos
| Req. | Estado | Evidencia |
|---|---|---|
| 14.1.x | Cumple | Ver [Clasificación de datos](#clasificación-de-datos-v1411-y-v1412) |
| 14.2.1 Fuera de la URL | Cumple | `POST /his/children/lookup` (el DNI va en el cuerpo) |
| 14.2.2 Sin caché | Cumple | `Cache-Control: no-store` en el back |
| 14.3.1 Limpiar al salir | Cumple | `Clear-Site-Data` en `/signed-out` y `/session-expired` |
| 14.3.x Almacenamiento del navegador | Cumple | El token nunca llega al JS |

### V15 Código y arquitectura
| Req. | Estado | Evidencia |
|---|---|---|
| 15.1.x | Cumple | Ver arriba |
| 15.2.x Componentes, disponibilidad y cadena de suministro | Cumple | Auditorías, límites y timeouts, lock con hashes, actions fijadas por SHA, `minimumReleaseAge` |
| 15.3.x Asignación masiva y fuga de campos | Cumple | Modelos Pydantic por operación y `to_dict()` sin `password_hash` |
| 15.4.x Concurrencia (escrituras de varios pasos) | Cumple | Validar antes de escribir y deshacer si falla (`guardianRepository.discard_new()`) |

### V16 Registro y errores
| Req. | Estado | Evidencia |
|---|---|---|
| 16.1.1 | Cumple | Ver [Inventario de registros](#inventario-de-registros-v1611) |
| 16.2.x Metadatos y hora UTC | Cumple | Actor, IP, dispositivo y resultado, con hora en UTC |
| 16.3.1 a 16.3.4 Autenticación, autorización, evasión y errores | Cumple | `LOGIN*`, `MFA*`, `ACCESS_DENIED`, 429 y alertas |
| 16.4.x Protección del log | Cumple | `audit_log` inmutable con cadena HMAC |
| 16.5.x Errores seguros | Cumple | Mensajes fijos y controles que fallan cerrados |

### V17 WebRTC — N/A
