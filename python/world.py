import json

# ------------------------------------------------------------------------------
# Load Config
# ------------------------------------------------------------------------------

CONFIG = ""

with open("./json/backendconfig.json", "r") as read_file:
    CONFIG = json.load(read_file)

if CONFIG['debug']['loadingJSON']: print(json.dumps(CONFIG, indent=4, sort_keys=True))
