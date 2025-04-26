import json
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / ".config" / "notes"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_NOTES_DIR = Path.home() / "notes"


def load_config(config_path: Path = CONFIG_FILE):
    """Load the configuration from a JSON file."""
    if not config_path.exists():
        return {"notes_dir": str(DEFAULT_NOTES_DIR)}

    with open(config_path, "r") as f:
        config = json.load(f)

    return config


def save_config(config: dict[str, Any]):
    """Save the configuration to a JSON file."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
