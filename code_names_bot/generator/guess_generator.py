import random

from code_names_bot.util.select_words import select_words
from code_names_bot.util.caches import get_cache, put_cache

cache = get_cache("guesses")

def _get_words_key(pos_words, neg_words):
    pos_str = ",".join(pos_words)
    neg_str = ",".join(neg_words)
    return pos_str + "|" + neg_str


def _get_clue_key(clue, num):
    return f"{clue}_{num}"


def generate_guess(pos_words, neg_words, clue, num):
    words_key = _get_words_key(pos_words, neg_words)
    clue_key = _get_clue_key(clue, num)

    if words_key not in cache:
        cache[words_key] = {}

    if clue_key in cache[words_key]:
        return cache[words_key]

    words = pos_words + neg_words
    random.shuffle(words)
    guesses = select_words(words, num)

    cache[words_key][clue_key] = guesses

    put_cache("guesses", cache)
