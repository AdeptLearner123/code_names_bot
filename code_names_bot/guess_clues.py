import argparse
import yaml
import os
import random

from config import CLUES_DIR, SCENARIOS_DIR
from code_names_bot.generator.guess_generator import generate_guess


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

    scenarios_name = clues_name.split("_")[0]
    scenarios_path = os.path.join(SCENARIOS_DIR, f"{scenarios_name}.yaml")
    with open(scenarios_path, "r") as file:
        scenarios = yaml.safe_load(file.read())

    for i, (scenario_id, clue_item) in enumerate(clues.items()):
        print(f"=== {i} / {len(clues)} ===")
        clue = clue_item["clue"]
        num = len(clue_item["words"])

        clue_item["guesses"] = generate_guess(clue_item["pos"] + clue_item["neg"], clue, num)
        clues[scenario_id] = clue_item
    
    with open(clues_path, "w") as file:
        file.write(yaml.dump(clues, default_flow_style=None, sort_keys=False))

    with open(scenarios_path, "w") as file:
        file.write(yaml.dump(scenarios, default_flow_style=None, sort_keys=False))
    

if __name__ == "__main__":
    main()