import random

from code_names_bot.util.cache import get_cache_list, put_cache_list

CACHE_NAME = "scores"
cache = get_cache_list(CACHE_NAME)


def _get_key(pos_words, neg_words, clue):
    pos_str = ",".join(pos_words)
    neg_str = ",".join(neg_words)
    return pos_str + "|" + neg_str + "|" + clue


def generate_scores(pos_words, neg_words, clue):
    key = _get_key(pos_words, neg_words, clue)
    if key in cache:
        return cache[key]

    words = pos_words + neg_words
    random.shuffle(words)
    guesses = select_words(words, num)

    cache[key] = guesses
    put_cache_list(CACHE_NAME, cache)