import json
import os

from config import CACHES

def get_cache(cache_name):
    path = os.path.join(CACHES, f"{cache_name}.json")

    if os.path.isfile(path):
        with open(path) as file:
            return json.load(file.read())
    return {}


def put_cache(cache_name, cache):
    path = os.path.join(CACHES, f"{cache_name}.json")

    with open(path, "w+") as file:
        file.write(json.dumps(cache, indent=4))