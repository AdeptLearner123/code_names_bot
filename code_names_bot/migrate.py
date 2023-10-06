import os
import yaml
import json
from collections import defaultdict, Counter
import openai

from code_names_bot.util.caches import get_cache, put_cache

openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    response = openai.Completion.create(
        model="gpt-4",
        temperature = 0,
        prompt="Is PLAYGROUND more related to SLIP or TRIP? (SLIP, TRIP, EQUAL):"
    )

    print(json.dumps(response))