from code_names_bot.util.propose_rank import get_proposals, get_ranked_words, select_clue
from code_names_bot.util.dict import split_by_column, merge

import random
from collections import Counter

ROUNDS = 3

def ranked_list_to_scores(ranked_words):
    # Counter only keeps keys with positive values, so add 1 to make all indexes positive.
    word_scores = { word: idx + 1 for idx, word in enumerate(ranked_words) }
    return Counter(word_scores)


def get_word_scores(words, proposal):
    seeds = range(ROUNDS)
    seed_words = { seed: random.Random(seed).sample(words, len(words)) for seed in seeds }
    seed_ranked_words = { seed: get_ranked_words(seed_words[seed], proposal) for seed in seeds }
    seed_ranked_words, seed_tokens = split_by_column(seed_ranked_words)
    seed_word_scores = { seed: ranked_list_to_scores(seed_ranked_words[seed]) for seed in seeds }
    print(seed_word_scores)
    word_scores = sum(seed_word_scores.values(), Counter())
    word_scores = dict(word_scores)
    tokens = sum(seed_tokens.values())

    return word_scores, tokens


def word_scores_to_sorted_list(word_scores, pos_words):
    # Sort words by their score. For the same score, positive words should appear after negative words.
    return list(sorted(word_scores.keys(), key=lambda word: (word_scores[word], word in pos_words)))


def propose_rank_vote(pos_words, neg_words):
    proposals, token_count = get_proposals(pos_words, neg_words)
    words = pos_words + neg_words
    proposal_word_scores = { proposal: get_word_scores(words, proposal) for proposal in proposals }
    proposal_word_scores, proposal_tokens = split_by_column(proposal_word_scores)
    proposal_ranked_words = { proposal: word_scores_to_sorted_list(proposal_word_scores[proposal], pos_words) for proposal in proposals }
    proposal_details = merge(("word_scores", proposal_word_scores), ("ranked_words", proposal_ranked_words), ("tokens", proposal_tokens))
    token_count += sum(proposal_tokens.values())
    clue, clue_words = select_clue(proposal_ranked_words, pos_words)

    details = {
        "proposals": proposals,
        "words": words,
        "proposal_details": proposal_details,
        "tokens": token_count
    }

    return clue, clue_words, details