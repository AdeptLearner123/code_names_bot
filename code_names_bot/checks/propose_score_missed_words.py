from collections import Counter

import yaml

def main():
    with open("clues/full-boards_propose-10-score.yaml", "r") as file:
        clues = yaml.safe_load(file.read())
    
    missed_word_scores = []
    missed_guess_scores = []

    for clue_item in clues.values():
        pos_words = clue_item["pos"]
        neg_words = clue_item["neg"]
        clue = clue_item["clue"]
        scores = clue_item["details"]["proposal_scores"][clue]
        words = clue_item["words"]
        guesses = clue_item["guesses"]

        missed_word_scores += [ scores[word] for word in words if word not in guesses ]
        missed_guess_scores += [ scores[guess] for guess in guesses if guess not in words ]

    print("Missed word score ", sum(missed_word_scores) / len(missed_word_scores))
    print("Missed guess score ", sum(missed_guess_scores) / len(missed_guess_scores))
    print("Missed word scores ", dict(Counter(missed_word_scores)))
    print("Missed guess scores ", dict(Counter(missed_guess_scores)))