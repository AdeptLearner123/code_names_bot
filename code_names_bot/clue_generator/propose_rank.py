from code_names_bot.util.read_prompt import read_prompt
from code_names_bot.util.get_completion import get_completion

import json
import random

proposal_prompt = read_prompt("propose-rank_propose")
rank_prompt = read_prompt("propose-rank_rank")

def _get_proposals(pos_words, neg_words):
    pos_words_str = ", ".join(pos_words)
    neg_words_str = ", ".join(neg_words)
    user_msg = f"Positive words: {pos_words_str}\nNegative words:{neg_words_str}"
    completion, token_count = get_completion(proposal_prompt, user_msg)
    proposals = completion.split(", ")
    proposals = [ proposal.upper() for proposal in proposals ]
    return proposals, token_count


def _get_guessable_words(words_ranked, pos_words):
    for i, word in enumerate(words_ranked):
        if word not in pos_words:
            return words_ranked[:i]
    return words_ranked


def _get_proposal_ranked_words(pos_words, neg_words, proposal):
    words = pos_words + neg_words
    random.Random(0).shuffle(words)
    words_str = ", ".join(words)
    user_msg = f"Clue: {proposal}\nWords: {words_str}"
    completion, token_count = get_completion(rank_prompt, user_msg)
    words_ranked = completion.split(", ")

    details = {
        "words_ranked": words_ranked,
        "tokens": token_count
    }
    return words_ranked, details

def propose_rank_clue(pos_words, neg_words):
    proposals, token_count = _get_proposals(pos_words, neg_words)

    details = {
        "proposals": proposals,
        "proposal_word_details": {},
        "tokens": token_count
    }
    best_clue = None
    clue_words = None

    for proposal in proposals:
        words_ranked, proposal_word_details = _get_proposal_ranked_words(pos_words, neg_words, proposal)

        details["proposal_word_details"][proposal] = proposal_word_details
        details["tokens"] += proposal_word_details["tokens"]

        proposal_words = _get_guessable_words(words_ranked, pos_words)

        if best_clue is None or len(clue_words) < len(proposal_words):
            best_clue = proposal
            clue_words = proposal_words

    return best_clue, clue_words, details