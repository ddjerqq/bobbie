import os
import sys
import toml

PATH = os.path.dirname(os.path.abspath(__file__))

cfg = toml.load(os.path.join(PATH, "bobbie.toml"))
cfg["bot"]["testing"] = "--test" in sys.argv

with open(os.path.join(PATH, "bobbie.toml"), "w", encoding="utf-8") as f:
    toml.dump(cfg, f)
