from code_names_bot.util.prompts import read_prompt, get_scenario_str
from code_names_bot.util.completions import get_completion

prompt = read_prompt("immediate")

def immediate_clue(pos_words, neg_words):
    scenario_str = get_scenario_str(pos_words, neg_words)
    completion, tokens = get_completion(prompt, scenario_str)

    lines = completion.splitlines()
    clue = lines[0].removeprefix("Clue: ").upper()
    words = lines[1].removeprefix("Words: ").split(", ")
    details = {
        "tokens": tokens
    }
    return clue, words, details