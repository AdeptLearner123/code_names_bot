import os
import yaml
import json


def main():
    with open("clues/pairs-small_propose-filter-rank.yaml", "r") as file:
        clues = yaml.safe_load(file.read())
    
    with open("caches/proposals.json", "r") as file:
        cache = json.loads(file.read())

    for scenario_id, clue in clues.items():
        pos = clue["pos"]
        neg = clue["neg"]
        proposals = clue["details"]["proposals"]
        
        related_words_tokens = sum(clue["details"]["proposal_related_words_tokens"].values())
        ranked_words_tokens = sum(clue["details"]["proposal_ranked_words_tokens"].values())
        total_tokens = clue["details"]["tokens"]

        propsoals_tokens = total_tokens - related_words_tokens - ranked_words_tokens

        cache[",".join(pos) + "|" + ",".join(neg)] = {
            str(len(proposals)): {
                "proposals": proposals,
                "tokens": propsoals_tokens
            }
        }
    
    with open("caches/proposals.json", "w+") as file:
        file.write(json.dumps(cache, indent=4))