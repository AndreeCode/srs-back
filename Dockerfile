# syntax=docker/dockerfile:1
# Imagen base fijada por versión y digest (A03): Dependabot la actualiza (ecosistema docker).
FROM python:3.15.2-slim-trixie@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928 AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

FROM base AS deps
COPY requirements.txt /tmp/requirements.txt
# El lock tiene hashes SHA-256: pip rechaza cualquier paquete que no coincida.
RUN python -m venv /opt/venv \
 && /opt/venv/bin/pip install --require-hashes -r /tmp/requirements.txt

FROM base AS runtime
RUN useradd --system --uid 10001 --home-dir /app --shell /usr/sbin/nologin app
WORKDIR /app
COPY --from=deps /opt/venv /opt/venv
COPY main.py ./
COPY scripts ./scripts
COPY src ./src
# El código queda de root y solo lectura para la app; solo /app/uploads es escribible.
RUN mkdir -p /app/uploads && chown app:app /app/uploads && chmod 700 /app/uploads
ENV PATH=/opt/venv/bin:$PATH \
    UPLOAD_DIR=/app/uploads
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api', timeout=4)"]
# --no-proxy-headers: la IP real la resuelve la app con TRUSTED_PROXIES (client_ip.py).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header", "--no-proxy-headers"]
