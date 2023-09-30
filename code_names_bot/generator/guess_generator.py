import random

from code_names_bot.util.select_words import select_words
from code_names_bot.util.caches import get_cache, put_cache, get_words_list_key

cache = get_cache("guesses")

def _get_clue_key(clue, num):
    return f"{clue}_{num}"


def generate_guess(words, clue, num):
    words_key = get_words_list_key(words)
    clue_key = _get_clue_key(clue, num)

    if words_key not in cache:
        cache[words_key] = {}

    if clue_key in cache[words_key]:
        return cache[words_key][clue_key]

    random.shuffle(words)
    print("Clue: ", clue)
    guesses = select_words(words, num)

    cache[words_key][clue_key] = guesses
    put_cache("guesses", cache)

    return guesses
