import yaml
from collections import defaultdict

from code_names_bot.clue_generator.propose_score_clue import _get_clue_words, _get_max_neg_scores

def main():
    with open("clues/full-boards_propose-10-score.yaml", "r") as file:
        clues = yaml.safe_load(file.read())
    
    attempt_comparisons = defaultdict(lambda: [])

    for clue_item in clues.values():
        pos = clue_item["pos"]
        neg = clue_item["neg"]
        details = clue_item["details"]
        proposal_scores = details["proposal_scores"]
        attempt_count = len(clue_item["words"])
        clue = clue_item["clue"]
        guesses = clue_item["guesses"]
        score = sum([ word in pos for word in guesses ]) - sum([ word in neg for word in guesses ])

        other_proposals = [ proposal for proposal in proposal_scores if proposal != clue ]
        other_proposal_clue_words = [ len(_get_clue_words(proposal_scores[proposal], pos, _get_max_neg_scores(proposal_scores[proposal], neg))) for proposal in other_proposals ]
        print(clue, attempt_count)
        print(attempt_count, other_proposal_clue_words, score)

        used_gap = any([ clue_count == attempt_count for clue_count in other_proposal_clue_words ])
        attempt_comparisons[attempt_count].append(used_gap)
    
    for num, value in attempt_comparisons.items():
        print(f"{num}: {sum(value)} / {len(value)} = {sum(value) / len(value)}")



if __name__ == "__main__":
    main()