# SICNA — Backend

API en **FastAPI** + **PostgreSQL**.

## Requisitos

- Python 3.10 o superior
- PostgreSQL
- [uv](https://docs.astral.sh/uv/) (opcional)

## 1. Crear la base de datos

```bash
psql -U postgres -c "CREATE DATABASE sicna;"
```

## 2. Configurar el `.env`

Copia el ejemplo:

```bash
cp .env.example .env
```

Y pon tu contraseña de `postgres`:

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=sicna
DB_USER=postgres
DB_PASSWORD=tu_password

DB_ADMIN_USER=postgres
DB_ADMIN_PASSWORD=tu_password

JWT_SECRET=cambia-esto-por-una-clave-larga
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

COOKIE_SECURE=false
UPLOAD_DIR=uploads
```

## 3. Instalar y ejecutar

### Opción A: con uv

```bash
uv venv
uv pip install -r requirements.txt

uv run python -m scripts.migrate    # crea las tablas
uv run python -m scripts.seed       # carga datos de prueba
uv run uvicorn main:app --reload
```

### Opción B: con venv

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m scripts.migrate           # crea las tablas
python -m scripts.seed              # carga datos de prueba
uvicorn main:app --reload
```

Abre:

- API: <http://127.0.0.1:8000/api>
- Documentación: <http://127.0.0.1:8000/docs>

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `Admin123!` | Administrador |
| `coordinador` | `Coord123!` | Coordinador |
| `usuario` | `Usuario123!` | Padre |

## Seguridad (OWASP ASVS 5.0 nivel 2)

La matriz de cumplimiento del sistema (back + signa + HIS), con la documentación que exige el estándar, está en [`ASVS.md`](ASVS.md). Para aplicar la migración `008` (`ACCESS_DENIED` en la auditoría): `python -m scripts.migrate`.

## Comandos útiles

```bash
python -m scripts.fresh --seed      # borra todo, recrea las tablas y carga los datos
python -m scripts.reset             # vacía las tablas
```

Con uv, antepón `uv run` a cada comando.

## Docker

```bash
docker build -t sicna-backend .
```

La imagen corre uvicorn en `:8000` como usuario sin privilegios; las variables van por entorno (o `*_FILE` para secretos). Para levantar back + front juntos, usar `compose.yaml` en la raíz del proyecto (`../compose.yaml`).
