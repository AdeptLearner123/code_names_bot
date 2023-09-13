from .clue_generator import ClueGenerator
from .clue_generator import ClueGenerator

import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

class SimpleGptGenerator(ClueGenerator):
    def give_clue(self, pos_words, neg_words):
        pos_words_str = ", ".join(pos_words)
        neg_words_str = ", ".join(neg_words)

        print("Calling")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature = 0,
            messages=[
                {"role": "system", "content": "Generate a single-world clue that is related to the positive words, but not the negative words. Explain."},
                {"role": "user", "content": f"Positive words: {pos_words_str}\nNegative words:{neg_words_str}"},
            ]
        )

        print("Response " + json.dumps(response))
        message = response["choices"][0]["message"]["content"]
        clue = message.splitlines()[0].removeprefix("Clue:")
        return clue, pos_words, json.dumps(response)