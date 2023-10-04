import yaml

def main():
    with open("full-boards_propose-10-score.yaml", "r") as file:
        clues = yaml.safe_load(file.read())
    
    for clue_item in clues.items():
        pos = clue_item["pos"]
        neg = clue_item["neg"]
        guesses = clue_item["guesses"]
        score = sum([ word in pos for word in guesses ]) - sum([ word in neg for word in guesses ])


if __name__ == "__main__":
    main()