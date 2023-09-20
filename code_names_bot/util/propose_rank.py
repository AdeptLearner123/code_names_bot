from .prompts import read_prompt, get_scenario_str, get_words_msg
from .completions import get_completion_as_word_list
from .dict import split_by_column

import random
from collections import Counter

proposal_prompt = read_prompt("propose_5")
rank_prompt = read_prompt("rank")

def get_proposals(pos_words, neg_words):
    scenario_str = get_scenario_str(pos_words, neg_words)
    return get_completion_as_word_list(proposal_prompt, scenario_str)


def get_ranked_words(words, proposal):
    user_msg = get_words_msg(words)
    system_msg = rank_prompt.replace("###", proposal)
    return get_completion_as_word_list(system_msg, user_msg)


def _get_guessable_words(words_ranked, pos_words):
    for i, word in enumerate(words_ranked):
        if word not in pos_words:
            return words_ranked[:i]
    return words_ranked


def select_clue(proposal_ranked_words, pos_words):
    proposal_guessable_words = { 
        proposal: _get_guessable_words(ranked_words, pos_words) 
        for proposal, ranked_words in proposal_ranked_words.items()
    }

    proposal_score = {
        proposal: len(guessable_words)
        for proposal, guessable_words in proposal_guessable_words.items()
    }

    clue = max(proposal_score, key=proposal_score.get)
    return clue, proposal_guessable_words[clue]


def ranked_list_to_scores(ranked_words):
    # Counter only keeps keys with positive values, so add 1 to make all indexes positive.
    word_scores = { word: idx + 1 for idx, word in enumerate(ranked_words) }
    return Counter(word_scores)


def get_word_scores(words, proposal, rounds):
    seeds = range(rounds)
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