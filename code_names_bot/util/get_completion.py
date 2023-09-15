from code_names_bot.util.read_prompt import read_prompt

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
