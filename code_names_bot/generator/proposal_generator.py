from code_names_bot.util.prompts import read_prompt, get_scenario_str
from code_names_bot.util.completions import get_completion_as_word_list
from code_names_bot.util.caches import get_cache, put_cache, get_scenario_key

cache = get_cache("proposals")
prompt = read_prompt("propose_5")

def get_proposals(pos_words, neg_words, num):
    scenario_key = get_scenario_key(pos_words, neg_words)
    if scenario_key not in cache:
        cache[scenario_key] = {}
    
    if str(num) in cache[scenario_key]:
        return cache[scenario_key][str(num)]

    scenario_str = get_scenario_str(pos_words, neg_words)
    proposals = get_completion_as_word_list(prompt.replace("###", num), scenario_str)

    cache[scenario_key][str(num)] = proposals
    put_cache("proposals", cache)

    return proposals