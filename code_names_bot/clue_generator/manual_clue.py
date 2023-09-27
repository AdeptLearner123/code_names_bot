from code_names_bot.util.select_words import select_words

def manual_clue(pos_words, neg_words):
    print("Pos:", ", ".join(pos_words))
    print("Neg:", ", ".join(neg_words))
    clue = input("Clue: ")
    words = select_words(pos_words)
    return clue, words, { "tokens": 0 }
