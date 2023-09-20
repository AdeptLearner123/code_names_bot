import yaml

def main():
    with open("clues/pairs-small_propose-filter-rank.yaml", "r") as file:
        clues = yaml.safe_load(file.read())
    
    for _, clue_item in clues.items():
        details = clue_item["details"]
        proposals = details["proposals"]

        for proposal in proposals:
            ranked_words = details["proposal_details"][proposal]["ranked_words"]
            related_words = details["proposal_details"][proposal]["related_words"]
            if proposal in ranked_words:
                print("Proposal in ranked words", proposal)
            if set(ranked_words) != set(related_words):
                print("Ranked words unequal to words", ranked_words, related_words)


if __name__ == "__main__":
    main()