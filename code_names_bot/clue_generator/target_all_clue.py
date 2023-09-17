from code_names_bot.util.prompts import read_prompt, get_scenario_str
from code_names_bot.util.completions import get_completion

prompt = read_prompt("target-all")

def target_all_clue(pos_words, neg_words):
    scenario_str = get_scenario_str(pos_words, neg_words)
    completion, tokens = get_completion(prompt, scenario_str)
    clue = completion.splitlines()[0].removeprefix("Clue: ").upper()
    details = {
        "tokens": tokens
    }
    return clue, pos_words, details
