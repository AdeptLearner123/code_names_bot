from code_names_bot.util.read_prompt import read_prompt
from code_names_bot.util.get_completion import get_completion

prompt = read_prompt("immediate")

def immediate_clue(pos_words, neg_words):
    pos_words_str = ", ".join(pos_words)
    neg_words_str = ", ".join(neg_words)
    user_msg = f"Positive words: {pos_words_str}\nNegative words:{neg_words_str}"
    completion, tokens = get_completion(prompt, user_msg)

    lines = completion.splitlines()
    clue = lines[0].removeprefix("Clue: ").upper()
    words = lines[1].removeprefix("Words: ").split(", ")
    details = {
        "tokens": tokens
    }
    return clue, words, details