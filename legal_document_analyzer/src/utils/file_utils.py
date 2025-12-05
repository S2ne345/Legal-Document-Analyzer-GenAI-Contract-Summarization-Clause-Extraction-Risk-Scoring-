
from pathlib import Path
from typing import Optional


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_text(path: str | Path, content: str) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')
    return p


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding='utf-8')


def sniff_ext(path: str | Path) -> Optional[str]:
    p = Path(path)
    return p.suffix.lower().lstrip('.') if p.suffix else None
