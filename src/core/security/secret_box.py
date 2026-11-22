import base64
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PREFIX = "v1:"


def seal(key: bytes, plaintext: str, context: str) -> str:
    nonce = os.urandom(12)
    sealed = AESGCM(key).encrypt(nonce, plaintext.encode(), context.encode())
    return PREFIX + base64.urlsafe_b64encode(nonce + sealed).decode()


def open_sealed(key: bytes, token: str, context: str) -> str:
    if not token.startswith(PREFIX):
        raise ValueError("Formato de secreto cifrado desconocido")
    raw = base64.urlsafe_b64decode(token[len(PREFIX):])
    try:
        return AESGCM(key).decrypt(raw[:12], raw[12:], context.encode()).decode()
    except InvalidTag as err:
        raise ValueError("No se pudo descifrar el secreto (clave incorrecta o dato alterado)") from err
