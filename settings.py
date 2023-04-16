import json

# TODO: Gestion des erreurs


SETTINGS_FILE = "/Users/guillaume/Code/database/settings.json"


def getConfig(params: str) -> dict:
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
        return settings[params]
