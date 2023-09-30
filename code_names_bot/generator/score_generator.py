import random

from code_names_bot.util.caches import get_cache, put_cache, get_words_list_key
from code_names_bot.util.prompts import read_prompt, get_words_msg
from code_names_bot.util.completions import get_completion_as_dict

cache = get_cache("scores")
prompt = read_prompt("score")

def format_scores(raw_scores):
    return { word: int(raw_scores[word].split(" ")[0]) for word in raw_scores }


def get_scores(words, clue):
    scenario_key = get_words_list_key(words)

    if scenario_key not in cache:
        cache[scenario_key] = {}

    if clue in cache[scenario_key]:
        cache_item = cache[scenario_key][clue]
        return format_scores(cache_item["scores"]), cache_item["tokens"]

    system_msg = prompt.replace("###", clue)
    words = sorted(words)
    random.Random(0).shuffle(words)
    user_msg = get_words_msg(words)
    scores, tokens = get_completion_as_dict(system_msg, user_msg)

    cache[scenario_key][clue] = {
        "scores": scores,
        "tokens": tokens
    }
    put_cache("scores", cache)

    return format_scores(scores), tokens