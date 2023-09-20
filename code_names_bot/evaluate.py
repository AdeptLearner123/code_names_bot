import os
import yaml
import argparse
from collections import Counter

from config import CLUES_DIR

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, required=True)
    args = parser.parse_args()
    return args.mode

def evaluate(clues_name, mode):
    with open(os.path.join(CLUES_DIR, f"{clues_name}.yaml"), "r") as file:
        clues = yaml.safe_load(file.read())

    score = 0
    score_dist = Counter()
    tokens = 0

    for _, clue_scenario in clues.items():
        if mode == "count_neg":
            guesses = clue_scenario["guesses"]
            pos_count = sum([ word in clue_scenario["pos"] for word in guesses])
            neg_count = sum([ word in clue_scenario["neg"] for word in guesses])
            score_dist[pos_count - neg_count] += 1
            score += pos_count - neg_count
            tokens += clue_scenario["details"]["tokens"]

    print(f"{clues_name}: {score} / {len(clues)} = {score / len(clues)}")
    print("Scores:", score_dist)
    print("Tokens:", tokens / len(clues))


def main():
    mode = parse_args()

    guesses_names = [ file_name.removesuffix(".yaml") for file_name in os.listdir(CLUES_DIR) ]
    for guesses_name in guesses_names:
        evaluate(guesses_name, mode)


if __name__ == "__main__":
    main()