import yaml
import random
import argparse
import uuid
import os

from config import CARD_WORDS, SCENARIOS_DIR

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, required=True)
    parser.add_argument("-n", "--name", type=str, required=True)
    parser.add_argument("--num-pos", type=int, required=True)
    parser.add_argument("--num-neg", type=int, required=True)
    args = parser.parse_args()
    return args.count, args.name, args.num_pos, args.num_neg


def main():
    count, name, num_pos, num_neg = parse_args()

    with open(CARD_WORDS, "r") as file:
        card_words = file.read().splitlines()

    scenarios = {}

    for _ in range(count):
        sample = random.sample(card_words, num_pos + num_neg)
        pos_words = sample[:num_pos]
        neg_words = sample[num_pos:]

        scenarios[str(uuid.uuid4())] = {
            "pos": pos_words,
            "neg": neg_words
        }
    
    path = os.path.join(SCENARIOS_DIR, f"{name}.yaml")
    with open(path, "w+") as file:
        file.write(yaml.dump(scenarios, default_flow_style=None))


if __name__ == "__main__":
    main()