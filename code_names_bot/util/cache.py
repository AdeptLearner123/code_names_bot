import os

from config import CACHES

def get_cache_list(cache_name):
    cache = get_cache(cache_name)
    cache = { key : value.split(",") for key, value in cache.items() }


def put_cache_list(cache_name, cache):
    cache = { key : ",".join(value) for key, value in cache.items() }
    put_cache(cache_name, cache)


def get_cache(cache_name):
    path = os.path.join(CACHES, f"{cache_name}.yaml")
    
    if os.path.isfile(path):
        with open(path, "r") as file:
            lines = file.read().splitlines()
            lines_split = [ line.split(":") for line in lines ]
            return { parts[0] : parts[1] for parts in lines_split }
    
    return {}


def put_cache(cache_name, cache):
    path = os.path.join(CACHES, f"{cache_name}.yaml")

    with open(path, "w+") as file:
        lines = [ key + ":" + value for key, value in cache.items() ]
        file.write("\n".join(lines))