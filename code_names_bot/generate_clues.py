import argparse
import yaml
import os
from config import SCENARIOS_DIR, CLUES_DIR

from .clue_generator.manual_clue import manual_clue
from .clue_generator.target_all_clue import target_all_clue
from .clue_generator.immediate_clue import immediate_clue
from .clue_generator.propose_rank import propose_rank_clue

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scenarios", type=str, required=True)
    parser.add_argument("-g", "--generator", type=str, required=True)
    parser.add_argument("-i", "--scenario-id", type=str, required=False)
    args = parser.parse_args()
    return args.scenarios, args.generator, args.scenario_id


def get_generator(generator):
    if generator == "manual":
        return manual_clue
    if generator == "target-all":
        return target_all_clue
    if generator == "immediate":
        return immediate_clue
    if generator == "propose-rank":
        return propose_rank_clue


def main():
    scenarios_name, generator_name, scenario_id = parse_args()
    path = os.path.join(SCENARIOS_DIR, f"{scenarios_name}.yaml")

    with open(path, "r") as file:
        scenarios = yaml.safe_load(file.read())

    clues = {}
    generator = get_generator(generator_name)

    if scenario_id is not None:
        scenario_items = [(0, (scenario_id, scenarios[scenario_id]))]
    else:
        scenario_items = enumerate(scenarios.items())

    for i, (scenario_id, scenario) in scenario_items:
        print(f"=== {i} / {len(scenarios)} ===")

        clue, clue_words, details = generator(scenario["pos"], scenario["neg"])
        output = {
            "clue": clue,
            "words": clue_words
        }

        print("Output", output)

        if details is not None:
            output["details"] = details
        
        clues[scenario_id] = output

    
    output_path = os.path.join(CLUES_DIR, f"{scenarios_name}_{generator_name}.yaml")

    with open(output_path, "w+") as file:
        file.write(yaml.dump(clues, default_flow_style=None))


if __name__ == "__main__":
    main()