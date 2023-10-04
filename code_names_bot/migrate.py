import os
import yaml
import json
from collections import defaultdict, Counter

from code_names_bot.util.caches import get_cache, put_cache

def main():
    cache = get_cache("scores")
    for key, subcache in cache.items():
        for subkey in subcache:
            