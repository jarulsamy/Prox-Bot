import json
import os

import requests
from dotenv import load_dotenv


class VM(object):
    def __init__(self, name=None, id=None, status=None):
        super().__init__()
        self.name = name
        self.id = id
        self.running = status

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, val):
        if val == "running":
            self._running = True
        else:
            self._running = False

    def __str__(self):
        data = {"id": self._id, "name": self._name, "running": self._running}
        return json.dumps(data, indent=4)


class Prox(object):
    def __init__(self, user, password, host, node_name):
        super().__init__()

        # Payload to login
        self.user_payload = {"username": f"{user}@pam", "password": password}

        self.host = host
        self.node_name = node_name
        # Complete login
        resp = requests.post(
            f"{self.host}/access/ticket", verify=False, data=self.user_payload
        )

        resp = resp.json()
        token = resp["data"]["CSRFPreventionToken"]
        ticket = resp["data"]["ticket"]

        # Prepare cookies and headers for future requests.
        self.cookies = {"PVEAuthCookie": ticket}

        self.headers = {"CSRFPreventionToken": token}

        self.vm_ids = ["100"]
        self.vm_list = {"vms": "".join(self.vm_ids), "force": 1}
        print(self.vm_list)
        self.load_vms()

    def load_vms(self):
        resp = requests.get(
            f"{self.host}/nodes/{self.node_name}/qemu",
            verify=False,
            headers=self.headers,
            cookies=self.cookies,
        )
        resp = resp.json()
        resp = resp["data"]
        self._vms = []
        for vm in resp:
            if vm["vmid"] in self.vm_ids:
                self._vms.append(
                    VM(name=vm["name"], id=vm["vmid"], status=vm["status"])
                )

    def start_vms(self):
        resp = requests.post(
            f"{self.host}/nodes/{self.node_name}/startall",
            verify=False,
            headers=self.headers,
            cookies=self.cookies,
            data=self.vm_list,
        )
        return resp.status_code

    def get_vms(self):
        self.load_vms()
        return self._vms


if __name__ == "__main__":
    load_dotenv()

    prox = Prox(
        os.getenv("PROX_USER"),
        os.getenv("PROX_PASS"),
        os.getenv("PROX_HOST"),
        os.getenv("PROX_NODE_NAME"),
    )
    for i in prox.get_vms():
        print(str(i))
