import os
import yaml
import json

from code_names_bot.util.caches import get_words_list_key

def main():
    with open("caches/scores_v2.json", "r") as file:
        cache = json.loads(file.read())
    
    new_cache = {}

    for key, value in cache.items():
        words = key.replace("_", ",").split(",")
        print(words)
        new_cache[get_words_list_key(words)] = value
    
    with open("caches/scores.json", "w+") as file:
        file.write(json.dumps(new_cache, indent=4))