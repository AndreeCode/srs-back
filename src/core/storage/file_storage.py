import asyncio
import os
from pathlib import Path

from ..config.config import config


def upload_root() -> Path:
    return Path(config.upload_dir).resolve()


def resolve_path(relative_path: str) -> Path:
    base = upload_root()
    path = (base / relative_path).resolve()

    if not path.is_relative_to(base):
        raise ValueError(f"Ruta fuera del directorio de subida: {relative_path}")

    return path


def _make_private_dirs(path: Path) -> None:
    base = upload_root()
    base.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    current = path
    while current != base and current.is_relative_to(base):
        os.chmod(current, 0o700)
        current = current.parent
    os.chmod(base, 0o700)


def _write(path: Path, content: bytes) -> None:
    _make_private_dirs(path.parent)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as out:
        out.write(content)
    os.chmod(path, 0o600)


def secure_existing_files() -> None:
    base = upload_root()
    if not base.is_dir():
        return
    os.chmod(base, 0o700)
    for root, dirs, files in os.walk(base):
        for name in dirs:
            os.chmod(Path(root) / name, 0o700)
        for name in files:
            os.chmod(Path(root) / name, 0o600)


async def save_file(relative_path: str, content: bytes) -> None:
    await asyncio.to_thread(_write, resolve_path(relative_path), content)


async def delete_file(relative_path: str) -> None:
    await asyncio.to_thread(resolve_path(relative_path).unlink, True)
