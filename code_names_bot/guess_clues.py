import argparse
import yaml
import os
import random

from config import CLUES_DIR
from code_names_bot.util.select_words import select_words


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--clues", type=str, required=True)
    args = parser.parse_args()
    return args.clues


def main():
    clues_name = parse_args()
    clues_path = os.path.join(CLUES_DIR, f"{clues_name}.yaml")

    with open(clues_path, "r") as file:
        clues = yaml.safe_load(file.read())

    for i, (scenario_id, clue_item) in enumerate(clues.items()):
        print(f"=== {i} / {len(clues)} ===")
        words = clue_item["pos"] + clue_item["neg"]
        random.shuffle(words)

        clue = clue_item["clue"]
        num = len(clue_item["words"])

        print(f"Clue: {clue} {num}")
        print(f"Words: {', '.join(words)}")
        guess_words = select_words(words, num)

        clue_item["guesses"] = guess_words
        clues[scenario_id] = clue_item
    
    with open(clues_path, "w") as file:
        file.write(yaml.dump(clues, default_flow_style=None, sort_keys=False))


if __name__ == "__main__":
    main()