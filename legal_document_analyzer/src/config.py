
import yaml
from pathlib import Path

class AppConfig:
    def __init__(self, path: str | Path = 'config.yaml'):
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Config file not found: {p}")
        with open(p, 'r', encoding='utf-8') as f:
            self._cfg = yaml.safe_load(f)

    def get(self, *keys, default=None):
        d = self._cfg
        for k in keys:
            if isinstance(d, dict) and k in d:
                d = d[k]
            else:
                return default
        return d

CONFIG = AppConfig()
