from code_names_bot.util.prompts import read_prompt

import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_completion(system, user):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature = 0,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    )
    message = response["choices"][0]["message"]["content"]
    token_count = int(response["usage"]["total_tokens"])

    return message, token_count


def get_completion_as_word_list(system, user):
    completion, token_count = get_completion(system, user)
    words = completion.split(", ")
    words = [ word.upper() for word in words ]
    return words, token_count


def get_completion_as_dict(system, user):
    completion, token_count = get_completion(system, user)
    lines = completion.splitlines()
    lines_split = [ line.split(": ") for line in lines ]
    dictionary = { parts[0]: parts[1] for parts in lines_split }
    return dictionary, token_count