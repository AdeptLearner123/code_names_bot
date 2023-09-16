from code_names_bot.util.read_prompt import read_prompt
from code_names_bot.util.get_completion import get_completion

prompt = read_prompt("target-all")

def target_all_clue(pos_words, neg_words):
    pos_words_str = ", ".join(pos_words)
    neg_words_str = ", ".join(neg_words)
    user_msg = f"Positive words: {pos_words_str}\nNegative words:{neg_words_str}"

    completion, tokens = get_completion(prompt, user_msg)
    clue = completion.splitlines()[0].removeprefix("Clue: ").upper()
    details = {
        "tokens": tokens
    }
    return clue, pos_words, details
