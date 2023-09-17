from .prompts import read_prompt, get_scenario_str, get_clue_words_str
from .completions import get_completion_as_word_list

proposal_prompt = read_prompt("propose_5")
rank_prompt = read_prompt("rank")

def get_proposals(pos_words, neg_words):
    scenario_str = get_scenario_str(pos_words, neg_words)
    return get_completion_as_word_list(proposal_prompt, scenario_str)


def get_ranked_words(words, proposal):
    clue_words_str = get_clue_words_str(proposal, words)
    return get_completion_as_word_list(rank_prompt, clue_words_str)


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