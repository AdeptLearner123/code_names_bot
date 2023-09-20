from config import PROMPTS_DIR

import os

def read_prompt(name):
    with open(os.path.join(PROMPTS_DIR, name), "r") as file:
        return file.read()


def get_scenario_str(pos_words, neg_words):
    pos_words_str = ", ".join(pos_words)
    neg_words_str = ", ".join(neg_words)
    return f"Positive words: {pos_words_str}\nNegative words:{neg_words_str}"


def get_words_msg(words):
    words_str = ", ".join(words)
    return f"Words: {words_str}"