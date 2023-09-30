import json
import os

from config import CACHES

def get_scenario_key(pos_words, neg_words):
    pos_str = ",".join(pos_words)
    neg_str = ",".join(neg_words)
    return pos_str + "|" + neg_str


def get_words_list_key(words):
    return ",".join(sorted(words))


def get_cache(cache_name):
    path = os.path.join(CACHES, f"{cache_name}.json")

    if os.path.isfile(path):
        with open(path) as file:
            return json.loads(file.read())
    return {}


def put_cache(cache_name, cache):
    path = os.path.join(CACHES, f"{cache_name}.json")

    with open(path, "w+") as file:
        file.write(json.dumps(cache, indent=4))