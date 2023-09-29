import os
import yaml
import json

from code_names_bot.util.cache import get_cache, put_cache


def get_key(pos, neg):
    return str(hash(",".join(sorted(pos)) + "|" + ",".join(sorted(neg))))


def main():
    with open("caches/guesses_old.yaml", "r") as file:
        old_cache = yaml.safe_load(file.read())

    new_cache = {}
    for key, item in old_cache.items():
        new_key = ",".join(item["pos"]) + "_" + ",".join(item["neg"])

        new_cache[new_key] = {}

        for guess_key, guesses in item["guesses"].items():
            new_cache[new_key][guess_key] = guesses

    with open("caches/guesses.yaml", "w+") as file:
        file.write(json.dumps(new_cache, indent=4))