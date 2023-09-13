from abc import ABC, abstractmethod

class ClueGenerator(ABC):
    @abstractmethod
    def give_clue(self, pos_words, neg_words):
        pass