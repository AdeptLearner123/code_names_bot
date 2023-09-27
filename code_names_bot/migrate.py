import os
import yaml
import json

from code_names_bot.util.cache import get_cache, put_cache
from code_names_bot.generator.guess_generator import _get_key

guess_cache = get_cache("guesses")


def main():
    with open("caches/guesses", "w") as file:
        lines = [ key + ":" + ",".join(value) for key, value in guess_cache.items() ]
        cache_str = "\n".join(lines)
        file.write(cache_str)
