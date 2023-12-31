import argparse
import yaml
import os
from config import SCENARIOS_DIR, CLUES_DIR

from .clue_generator.manual_clue import manual_clue
from .clue_generator.target_all_clue import target_all_clue
from .clue_generator.immediate_clue import immediate_clue
from .clue_generator.propose_rank_clue import propose_rank_clue
from .clue_generator.propose_filter_rank_clue import propose_filter_rank_clue
from .clue_generator.propose_rank_vote_clue import propose_rank_vote
from .clue_generator.propose_score_clue import propose_5_score_clue, propose_10_score_clue
from .clue_generator.propose_for_count_score_clue import propose_for_count_score_clue
from .clue_generator.propose_score_sort_clue import propose_score_sort_clue
from .clue_generator.propose_score_multi_clue import propose_score_multi_clue

yaml.Dumper.ignore_aliases = lambda *args: True

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
    if generator == "propose-filter-rank":
        return propose_filter_rank_clue
    if generator == "propose-rank-vote":
        return propose_rank_vote
    if generator == "propose-5-score":
        return propose_5_score_clue
    if generator == "propose-10-score":
        return propose_10_score_clue
    if generator == "propose-for-count-score":
        return propose_for_count_score_clue
    if generator == "propose-score-sort":
        return propose_score_sort_clue
    if generator == "propose-score-multi":
        return propose_score_multi_clue


def main():
    scenarios_name, generator_name, scenario_id = parse_args()
    path = os.path.join(SCENARIOS_DIR, f"{scenarios_name}.yaml")
    output_path = os.path.join(CLUES_DIR, f"{scenarios_name}_{generator_name}.yaml")

    with open(path, "r") as file:
        scenarios = yaml.safe_load(file.read())

    if os.path.isfile(output_path):
        with open(output_path, "r") as file:
            clues = yaml.safe_load(file.read())
    else:
        clues = {}
    
    generator = get_generator(generator_name)

    if scenario_id is not None:
        scenario_items = [(scenario_id, scenarios[scenario_id])]
    else:
        scenario_items = scenarios.items()

    for i, (scenario_id, scenario) in enumerate(scenario_items):
        print(f"=== {i} / {len(scenarios)} ===")

        if scenario_id in clues:
            continue

        clue, clue_words, details = generator(scenario["pos"], scenario["neg"])
        output = {
            "pos": scenario["pos"],
            "neg": scenario["neg"],
            "clue": clue,
            "words": clue_words
        }

        print("Output", output)

        if details is not None:
            output["details"] = details
        
        clues[scenario_id] = output

        with open(output_path, "w+") as file:
            file.write(yaml.dump(clues, default_flow_style=None, sort_keys=False))


if __name__ == "__main__":
    main()