import base64
import copy
import json
import re


def load(filename: str):
    """
    Load json config, with base64 password salting
    """
    with open(filename) as f:
        data = json.loads(f.read())
    base_64 = re.findall(
        "^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$",
        data["terraria"]["password"],
    )
    if not base_64:
        to_encode = copy.deepcopy(data)
        to_encode["terraria"]["password"] = base64.b64encode(
            data["terraria"]["password"].encode("utf-8")
        ).decode("utf-8")
        with open(filename, "w") as f:
            json.dump(to_encode, f, indent=4)
    else:
        data["terraria"]["password"] = base64.b64decode(
            data["terraria"]["password"]
        ).decode("utf-8")
    return data
