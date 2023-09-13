from .clue_generator import ClueGenerator

class ManualGenerator(ClueGenerator):
    def give_clue(self, pos_words, neg_words):
        print("Pos:", ", ".join(pos_words))
        print("Neg:", ", ".join(neg_words))
        clue = input("Clue: ")
        return clue, pos_words
