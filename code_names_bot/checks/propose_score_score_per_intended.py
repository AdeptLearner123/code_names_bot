import os
import yaml
import json
from collections import defaultdict, Counter

from code_names_bot.util.caches import get_words_list_key
from code_names_bot.clue_generator.propose_score_clue import _get_clue_words, _get_max_neg_scores
from code_names_bot.generator.guess_generator import generate_guess

def main():
    with open("clues/full-boards_propose-5-score.yaml", "r") as file:
        clues = yaml.safe_load(file.read())
    
    with open("clues/full-boards_propose-10-score.yaml", "r") as file:
        clues_2 = yaml.safe_load(file.read())
    
    intent_clues = defaultdict(lambda: [])
    intent_scores = Counter()
    
    for scenario_id, clue_item in clues.items():
        details = clue_item["details"]
        pos = clue_item["pos"]
        neg = clue_item["neg"]
        proposal_scores = details["proposal_scores"] | clues_2[scenario_id]["details"]["proposal_scores"]
        for proposal in proposal_scores:
            max_neg_score = _get_max_neg_scores(proposal_scores[proposal], neg)
            clue_words = _get_clue_words(proposal_scores[proposal], pos, max_neg_score)
            clue_num = len(clue_words)
            intent_clues[clue_num].append((scenario_id, proposal))

            if clue_num >= 3:
                guesses = generate_guess(pos + neg, proposal, clue_num)
                score = sum([ word in pos for word in guesses ]) - sum(word in neg for word in guesses)
                intent_scores[clue_num] += score
    
    print({ num: score / len(intent_clues[num]) for num, score in intent_scores.items() })
    print({ num: len(values) for num, values in intent_clues.items() })