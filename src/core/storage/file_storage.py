import asyncio
from pathlib import Path

from ..config.config import config


def resolve_path(relative_path: str) -> Path:
    base = Path(config.upload_dir).resolve()
    path = (base / relative_path).resolve()

    if not path.is_relative_to(base):
        raise ValueError(f"Ruta fuera del directorio de subida: {relative_path}")

    return path


def _write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


async def save_file(relative_path: str, content: bytes) -> None:
    await asyncio.to_thread(_write, resolve_path(relative_path), content)


async def delete_file(relative_path: str) -> None:
    await asyncio.to_thread(resolve_path(relative_path).unlink, True)
