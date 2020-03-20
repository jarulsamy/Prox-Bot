import os
import time
from pprint import pprint

import requests
from dotenv import load_dotenv


class Terraria(object):
    def __init__(self, username, password, host, timeout=1800):
        super().__init__()

        if "https" in host:
            raise ValueError("HTTPS endpoint not supported!")

        self.host = host
        self.timeout = timeout

        resp = requests.post(
            f"{self.host}/v2/token/create?username={username}&password={password}"
        )

        data = resp.json()
        if data["status"] != "200":
            pprint(data)
            raise Exception(f"Token creation failed, status code: {data['status']}")

        self.token = data["token"]
        self.last_player_time = time.time()
        self._get_status()
        self._kill = False
        self._expire = False

    @property
    def expire(self):
        self._get_status()
        return self._expire

    @expire.setter
    def expire(self, val):
        self._expire = val

    def _get_status(self):
        resp = requests.get(f"{self.host}/status", data={"token": self.token})
        resp = resp.json()
        self.uptime = resp["uptime"]
        self.playercount = resp["playercount"]

        if self.playercount > 0:
            self.last_player_time = time.time()
            self.expire = False
        else:
            self.time_since_last_player = time.time() - self.last_player_time
            if self.time_since_last_player > self.timeout:
                self.expire = True


if __name__ == "__main__":
    load_dotenv()
    USER = os.getenv("TERRARIA_USER")
    PASS = os.getenv("TERRARIA_PASS")
    t = Terraria(USER, PASS, "http://nu.lan:7878")
