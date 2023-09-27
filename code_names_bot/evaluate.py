import os
import yaml
import argparse
from collections import Counter

from config import CLUES_DIR
import json

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, required=True)
    parser.add_argument("-s", "--scenarios", type=str, required=True)
    args = parser.parse_args()
    return args.mode, args.scenarios

def evaluate(clues_name, mode):
    with open(os.path.join(CLUES_DIR, f"{clues_name}.yaml"), "r") as file:
        clues = yaml.safe_load(file.read())

    total_score = 0
    score_dist = Counter()
    attempt_dist = Counter()
    attempt_score = Counter()
    tokens = 0

    for _, clue_scenario in clues.items():
        if mode == "count_neg":
            guesses = clue_scenario["guesses"]
            pos_count = sum([ word in clue_scenario["pos"] for word in guesses])
            neg_count = sum([ word in clue_scenario["neg"] for word in guesses])
            score_dist[pos_count - neg_count] += 1
            clue_num = len(clue_scenario["words"])
            attempt_dist[clue_num] += 1
            score = pos_count - neg_count
            attempt_score[clue_num] += score
            total_score += score
            tokens += clue_scenario["details"]["tokens"]

    attempt_score = { num: score / attempt_dist[num] for num, score in attempt_score.items() }

    print(f"=== {clues_name} ===")
    print(f"Score: {total_score / len(clues)}")
    print("Scores:", json.dumps(score_dist, indent=4, sort_keys=True))
    print("Attempts:", json.dumps(attempt_dist, indent=4, sort_keys=True))
    print("Attempt scores:", json.dumps(attempt_score, indent=4, sort_keys=True))
    print("Tokens:", tokens / len(clues))
    print("\n")


def main():
    mode, scenarios = parse_args()

    clue_names = [ file_name.removesuffix(".yaml") for file_name in os.listdir(CLUES_DIR) ]
    clue_names = [ clue_name for clue_name in clue_names if clue_name.startswith(scenarios) ]
    for clue_name in clue_names:
        evaluate(clue_name, mode)


if __name__ == "__main__":
    main()