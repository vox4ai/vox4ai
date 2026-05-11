import os
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def _config_dir() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / "vox4ai"
    return Path.home() / ".config" / "vox4ai"


def _config_path() -> Path:
    return _config_dir() / "config.yaml"


_DEFAULTS: dict[str, Any] = {
    "engine": "",
    "model": "",
    "server_url": "",
    "style_id": None,
    "speed": 1.0,
    "volume": None,
    "pitch": None,
}


def defaults() -> dict[str, Any]:
    return dict(_DEFAULTS)


def load() -> dict[str, Any]:
    """Load ~/.config/vox4ai/config.yaml, falling back to defaults."""
    cfg = defaults()
    path = _config_path()
    if not path.exists():
        return cfg
    if yaml is None:
        return cfg
    try:
        raw = yaml.safe_load(path.read_text())
        if isinstance(raw, dict):
            for k in cfg:
                if k in raw:
                    cfg[k] = raw[k]
    except Exception:
        pass
    return cfg


def show() -> str:
    path = _config_path()
    if not path.exists():
        return "(no config file)"
    return path.read_text().strip() or "(empty)"


def merge_cli(cfg: dict[str, Any], args) -> dict[str, Any]:
    """CLI args override config values. Returns merged copy."""
    merged = dict(cfg)
    cli_map = {
        "engine": "engine",
        "model": "model",
        "server_url": "server_url",
        "style_id": "style_id",
        "speed": "speed",
        "volume": "volume",
        "pitch": "pitch",
    }
    for cli_attr, cfg_key in cli_map.items():
        val = getattr(args, cli_attr, None)
        if val is not None and val != "":
            merged[cfg_key] = val
    return merged