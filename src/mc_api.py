import time

from mcstatus import MinecraftServer


class MC(MinecraftServer):
    def __init__(self, host, port, timeout=1800):
        super().__init__(host, port)
        self.timeout = timeout
        self._expire = False
        self.last_player_time = time.time()
        self._get_status()

    @property
    def expire(self):
        self._get_status()
        return self._expire

    @expire.setter
    def expire(self, val):
        self._expire = val

    def _get_status(self):
        stat = super().status()
        self.player_count = stat.players.online

        if self.player_count > 0:
            self.last_player_time = time.time()
            self.expire = False
        else:
            self.time_since_last_player = time.time() - self.last_player_time
            if self.time_since_last_player > self.timeout:
                self.expire = True


if __name__ == "__main__":
    m = MC("nu.lan", 25565)
    num_players = m.num_players()
