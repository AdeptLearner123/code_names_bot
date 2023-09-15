from config import PROMPTS_DIR

import os

def read_prompt(name):
    with open(os.path.join(PROMPTS_DIR, name), "r") as file:
        return file.read()