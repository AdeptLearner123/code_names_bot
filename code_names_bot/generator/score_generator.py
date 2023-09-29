import random

from code_names_bot.util.caches import get_cache, put_cache
from code_names_bot.util.prompts import read_prompt, get_words_msg
from code_names_bot.util.completions import get_completion_as_dict

cache = get_cache("scores")
prompt = read_prompt("score")

def get_scores(words, clue):
    system_msg = prompt.replace("###", clue)
    user_msg = get_words_msg(words)
    scores, tokens = get_completion_as_dict(system_msg, user_msg)
    return scores, tokens