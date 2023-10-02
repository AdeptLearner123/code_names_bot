from collections import Counter, defaultdict

import yaml

def main():
    with open("clues/full-boards_propose-10-score.yaml", "r") as file:
        clues = yaml.safe_load(file.read())
    
    correct_gap = 0
    correct_dist = Counter()
    correct_attempt_dist = defaultdict(lambda: [])
    incorrect_gap = 0
    incorrect_dist = Counter()
    incorrect_attempt_dist = defaultdict(lambda: [])

    for clue_item in clues.values():
        pos_words = clue_item["pos"]
        neg_words = clue_item["neg"]
        words = clue_item["words"]
        clue = clue_item["clue"]
        scores = clue_item["details"]["proposal_scores"][clue]
        guesses = clue_item["guesses"]

        correct = all([ guess in pos_words for guess in guesses ])
        min_pos = min(scores[word] for word in words)
        max_neg = max(scores[word] for word in neg_words)
        gap = min_pos - max_neg

        if correct:
            correct_gap += gap
            correct_dist[gap] += 1
            correct_attempt_dist[len(words)].append(gap)
        else:
            incorrect_gap += gap
            incorrect_dist[gap] += 1
            incorrect_attempt_dist[len(words)].append(gap)
    
    print("Correct gap: ", correct_gap / sum(correct_dist.values()))
    print("Correct dist: ", correct_dist)
    print("Correct attempt dist: ", correct_attempt_dist)
    print("Incorrect gap: ", incorrect_gap / sum(incorrect_dist.values()))
    print("Incorrect dist: ", incorrect_dist)
    print("Incorrect attempt dist: ", incorrect_attempt_dist)


if __name__ == "__main__":
    main()