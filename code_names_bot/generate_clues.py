import argparse
import yaml
import os
from config import SCENARIOS_DIR, CLUES_DIR

from .clue_generator.manual_generator import ManualGenerator

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scenarios", type=str, required=True)
    parser.add_argument("-g", "--generator", type=str, required=True)
    args = parser.parse_args()
    return args.scenarios, args.generator


def get_generator(generator):
    if generator == "manual":
        return ManualGenerator()


def main():
    scenarios_name, generator_name = parse_args()
    path = os.path.join(SCENARIOS_DIR, f"{scenarios_name}.yaml")

    with open(path, "r") as file:
        scenarios = yaml.safe_load(file.read())

    clues = {}
    generator = get_generator(generator_name)

    for i, (scenario_id, scenario) in enumerate(scenarios.items()):
        print(f"=== {i} / {len(scenarios)} ===")

        clue, clue_words = generator.give_clue(scenario["pos"], scenario["neg"])
        clues[scenario_id] = {
            "clue": clue,
            "words": clue_words
        }
    
    output_path = os.path.join(CLUES_DIR, f"{scenarios_name}_{generator_name}.yaml")

    with open(output_path, "w+") as file:
        file.write(yaml.dump(clues, default_flow_style=None))


if __name__ == "__main__":
    main()