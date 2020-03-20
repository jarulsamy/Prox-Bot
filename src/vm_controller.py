import os
import time

from dotenv import load_dotenv
from mc_api import MC
from tshock_api import Terraria

load_dotenv()
m = MC("nu.lan", 25565, timeout=10)

t = Terraria(
    os.getenv("TERRARIA_USER"),
    os.getenv("TERRARIA_PASS"),
    "http://nu.lan:7878",
    timeout=10,
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
