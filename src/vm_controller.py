import time

from config_loader import load
from mc_api import MC
from tshock_api import Terraria

# TODO: Add argparse for filename selection
config = load("config.json")
m = MC(config["minecraft"]["host"], int(config["minecraft"]["port"]))

t = Terraria(
    config["terraria"]["username"],
    config["terraria"]["password"],
    config["terraria"]["host"],
)

while True:
    try:
        if m.expire and t.expire:
            print("SHUTDOWN")
        else:
            print("NOT YET")
        time.sleep(10)
    except KeyboardInterrupt:
        exit(0)
