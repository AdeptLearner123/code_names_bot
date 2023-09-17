from code_names_bot.util.prompts import read_prompt, get_clue_words_str
from code_names_bot.util.completions import get_completion_as_word_list
from code_names_bot.util.propose_rank import get_proposals, get_ranked_words, select_clue
from code_names_bot.util.dict import split_by_column, merge

import random

filter_prompt = read_prompt("filter")

def _get_related_words(words, proposal):
    clue_words_str = get_clue_words_str(proposal, words)
    return get_completion_as_word_list(filter_prompt, clue_words_str)


def propose_filter_rank_clue(pos_words, neg_words):
    proposals, token_count = get_proposals(pos_words, neg_words)
    words = pos_words + neg_words
    random.Random(0).shuffle(words)
    proposal_related_words = { proposal: _get_related_words(words, proposal) for proposal in proposals }
    proposal_related_words, proposal_related_words_tokens = split_by_column(proposal_related_words)
    proposal_ranked_words = {
        proposal: get_ranked_words(related_words, proposal)
        for proposal, related_words in proposal_related_words.items()
    }
    proposal_ranked_words, proposal_ranked_words_tokens = split_by_column(proposal_ranked_words)
    proposal_details = merge(
        ("related_words", proposal_related_words), ("related_words_tokens", proposal_related_words_tokens),
        ("ranked_words", proposal_ranked_words), ("ranked_words_tokens", proposal_ranked_words_tokens)
    )
    token_count += sum(proposal_related_words_tokens.values()) + sum(proposal_ranked_words_tokens.values())
    clue, clue_words = select_clue(proposal_ranked_words, pos_words)

    details = {
        "proposals": proposals,
        "words": words,
        "proposal_details": proposal_details,
        "tokens": token_count
    }

    return clue, clue_words, details
