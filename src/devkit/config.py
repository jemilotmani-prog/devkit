import json
from pathlib import Path

CONFIG_FILE = Path.home() / '.devkit' / 'config.json'

DEFAULTS = {
    'ai_tool': 'gh-copilot',
    'default_repo': '',
    'theme': 'dark',
    'show_spinner': True,
}

def load_config() -> dict:
    if CONFIG_FILE.exists():
        return {**DEFAULTS, **json.loads(CONFIG_FILE.read_text())}
    return DEFAULTS

def save_config(cfg: dict):
    CONFIG_FILE.parent.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))