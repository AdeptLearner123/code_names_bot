def select_words(words, count = None):
    print("Count", count)
    options = { idx: word for idx, word in enumerate(words) }
    selected = []

    while count is None or len(selected) < count:
        for i, word in options.items():
            print(f"[{i}] {word}")
        idx = input("Input: ")

        if len(idx) == 0:
            return selected
        
        idx = int(idx)
        selected_word = options[idx]
        selected.append(selected_word)
        options.pop(idx)
    
    return selected