from config import CLUES_DIR

import os
import yaml

PATH = "scenarios/pairs-small.yaml"

def main():
    files = os.listdir(CLUES_DIR)
    
    with open(PATH, "r") as file:
        scenarios = yaml.safe_load(file.read())

    for filename in files:
        clues_path = os.path.join(CLUES_DIR, filename)
        with open(clues_path, "r") as file:
            clue_items = yaml.safe_load(file.read())
    
        for scenario_id, clue_item in clue_items.items():
            clue = clue_item["clue"]
            words = clue_item["words"]
            guesses = clue_item.pop("guesses")

            if "guesses" not in scenarios[scenario_id]:
                scenarios[scenario_id]["guesses"] = {}
            
            scenarios[scenario_id]["guesses"][f"{clue}_{len(words)}"] = guesses

        with open(clues_path, "w") as file:
            file.write(yaml.dump(clue_items, default_flow_style=None, sort_keys=False))
    
    with open(PATH, "w") as file:
        file.write(yaml.dump(scenarios, default_flow_style=None, sort_keys=False))


if __name__ == "__main__":
    main()