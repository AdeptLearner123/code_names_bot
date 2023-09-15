import os
import yaml
import argparse

from config import GUESSES_DIR, SCENARIOS_DIR

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, required=True)
    args = parser.parse_args()
    return args.mode

def evaluate(guesses_name, mode):
    with open(os.path.join(GUESSES_DIR, f"{guesses_name}.yaml"), "r") as file:
        guesses = yaml.safe_load(file.read())
    
    scenarios_name = guesses_name.split("_")[0]
    with open(os.path.join(SCENARIOS_DIR, f"{scenarios_name}.yaml"), "r") as file:
        scenarios = yaml.safe_load(file.read())

    score = 0

    for scenario_id, guess_words in guesses.items():
        scenario = scenarios[scenario_id]

        if mode == "count_neg":
            pos_count = sum([ word in scenario["pos"] for word in guess_words])
            neg_count = sum([ word in scenario["neg"] for word in guess_words])
            score += pos_count - neg_count

    print(f"{guesses_name}: {score} / {len(guesses)} = {score / len(guesses)}")


def main():
    mode = parse_args()

    guesses_names = [ file_name.removesuffix(".yaml") for file_name in os.listdir(GUESSES_DIR) ]
    for guesses_name in guesses_names:
        evaluate(guesses_name, mode)


if __name__ == "__main__":
    main()