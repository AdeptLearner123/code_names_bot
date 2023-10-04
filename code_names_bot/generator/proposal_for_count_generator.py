from code_names_bot.util.prompts import read_prompt, get_words_msg
from code_names_bot.util.completions import get_completion_as_dict
from code_names_bot.util.caches import get_cache, put_cache, get_words_list_key

cache = get_cache("proposal_for_count")
prompt = read_prompt("propose_for_count")

def _get_sys_message(word_count, num):
    word_format = ", ".join([ f"<word {i + 1}>" for i in range(word_count)])
    output_format = "\n".join([ f"<clue {i + 1}>: {word_format}" for i in range(num)])
    return prompt.replace("###", str(num)).replace("???", str(word_count)).replace("!!!", output_format)


def get_proposals_for_count(words, word_count, num):
    words_key = get_words_list_key(words)
    if words_key not in cache:
        print("Missing word key")
        cache[words_key] = {}
    if str(word_count) not in cache[words_key]:
        print("Missing word count")
        cache[words_key][str(word_count)] = {}
    if str(num) in cache[words_key][str(word_count)]:
        print("Found cached num")
        cache_item = cache[words_key][str(word_count)][str(num)]
        return cache_item["proposals"], cache_item["tokens"]

    sys_message = _get_sys_message(word_count, num)
    print("Sys message", sys_message)
    user_message = get_words_msg(words)
    proposal_words, tokens = get_completion_as_dict(sys_message, user_message)
    proposal_words = { proposal: words.split(", ") for proposal, words in proposal_words.items() }

    cache[words_key][str(word_count)][str(num)] = {
        "proposals": proposal_words,
        "tokens": tokens
    }
    put_cache("proposal_for_count", cache)

    return proposal_words, tokens