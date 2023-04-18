import json
from pathlib import Path

# TODO: Gestion des erreurs

CURRENT_FILE = Path(__file__)
SETTINGS_FILE = CURRENT_FILE.parent / "settings.json"


def getConfig(params: str) -> dict:
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
        return settings[params]
