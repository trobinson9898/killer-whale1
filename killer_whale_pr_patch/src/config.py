import json, pathlib
BASE = pathlib.Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE / "config" / "config.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)
