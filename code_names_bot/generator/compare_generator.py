import random

from code_names_bot.util.prompts import read_prompt
from code_names_bot.util.select_words import select_words
from code_names_bot.util.completions import get_completion
from code_names_bot.util.caches import get_cache, put_cache

prompt = read_prompt("compare")
cache = get_cache("compares")

def compare(clue, word1, word2):
    key = f"{clue}_{word1}|{word2}"
    if key in cache:
        return cache[key]

    sys = prompt.replace("!!!", clue).replace("###", word1).replace("???", word2)
    completion, tokens = get_completion(sys)

    if completion == word1:
        result = 1
    elif completion == word2:
        result = -1
    elif completion == "EQUAL":
        result = 0
    else:
        raise RuntimeError("Invalid comparison result: " + result)

    cache[key] = result
    put_cache("compares", cache)
    return result