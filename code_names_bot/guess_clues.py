import argparse
import yaml
import os
import random

from config import SCENARIOS_DIR, CLUES_DIR, GUESSES_DIR
from code_names_bot.util.select_words import select_words


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--clues", type=str, required=True)
    args = parser.parse_args()
    return args.clues


def main():
    clues_name = parse_args()
    scenarios_name = clues_name.split("_")[0]
    clues_path = os.path.join(CLUES_DIR, f"{clues_name}.yaml")
    scenarios_path = os.path.join(SCENARIOS_DIR, f"{scenarios_name}.yaml")

    with open(clues_path, "r") as file:
        clues = yaml.safe_load(file.read())

    with open(scenarios_path, "r") as file:
        scenarios = yaml.safe_load(file.read())

    guesses = {}

    for i, (scenario_id, item) in enumerate(clues.items()):
        print(f"=== {i} / {len(clues)} ===")
        scenario = scenarios[scenario_id]
        words = scenario["pos"] + scenario["neg"]
        random.shuffle(words)

        clue = item["clue"]
        num = len(item["words"])

        print(f"Clue: {clue} {num}")
        print(f"Words: {', '.join(words)}")
        guess_words = select_words(words, num)

        guesses[scenario_id] = guess_words
    
    guesses_path = os.path.join(GUESSES_DIR, f"{clues_name}.yaml")
    with open(guesses_path, "w+") as file:
        file.write(yaml.dump(guesses, default_flow_style=None))


if __name__ == "__main__":
    main()