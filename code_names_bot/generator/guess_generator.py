from config import CACHES
import random

from code_names_bot.util.select_words import select_words
from code_names_bot.util.cache import get_cache_list, put_cache_list

CACHE_NAME = "guesses"
cache = get_cache_list(CACHE_NAME)


def _get_key(pos_words, neg_words, clue, clue_num):
    pos_str = ",".join(pos_words)
    neg_str = ",".join(neg_words)
    clue_str = f"{clue}_{clue_num}"
    return pos_str + "|" + neg_str + "|" + clue_str


def generate_guess(pos_words, neg_words, clue, num):
    key = _get_key(pos_words, neg_words, clue, num)
    if key in cache:
        return cache[key]

    words = pos_words + neg_words
    random.shuffle(words)
    guesses = select_words(words, num)

    cache[key] = guesses
    put_cache_list(CACHE_NAME, cache)