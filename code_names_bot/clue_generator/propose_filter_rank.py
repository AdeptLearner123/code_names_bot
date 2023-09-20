from code_names_bot.util.prompts import read_prompt, get_words_msg
from code_names_bot.util.completions import get_completion_as_word_list
from code_names_bot.util.propose_rank import get_proposals, get_ranked_words, select_clue
from code_names_bot.util.dict import split_by_column, merge
from code_names_bot.util.list import count_matches

import random

filter_prompt = read_prompt("filter")

def _get_related_words(words, proposal):
    system_msg = filter_prompt.replace("###", proposal)
    user_msg = get_words_msg(words)
    return get_completion_as_word_list(system_msg, user_msg)


def rank_words_if_necessary(words, proposal, pos_words, neg_words):
    has_pos_word = any([word in pos_words for word in words])
    has_neg_word = any([word in neg_words for word in words])
    
    if has_pos_word and has_neg_word:
        return get_ranked_words(words, proposal)
    return words, 0


def get_proposal_related_words(proposals, words, pos_words):
    proposal_related_words = {}
    proposal_tokens = {}

    for proposal in proposals:
        related_words, tokens = _get_related_words(words, proposal)
        proposal_related_words[proposal] = related_words
        proposal_tokens[proposal] = tokens

        if set(related_words) == set(pos_words):
            break
    return proposal_related_words, proposal_tokens


def propose_filter_rank_clue(pos_words, neg_words):
    proposals, token_count = get_proposals(pos_words, neg_words)
    words = pos_words + neg_words
    random.Random(0).shuffle(words)

    proposal_related_words, proposal_related_words_tokens = get_proposal_related_words(proposals, words, pos_words)
    filtered_proposals = proposal_related_words.keys()
    proposal_num_neg = { proposal: count_matches(proposal_related_words[proposal], neg_words) for proposal in filtered_proposals }
    proposal_num_pos = { proposal: count_matches(proposal_related_words[proposal], pos_words) for proposal in filtered_proposals }
    proposal_min_score = { proposal: 0 if proposal_num_neg[proposal] > 0 else proposal_num_pos[proposal] for proposal in filtered_proposals }
    proposal_max_score = proposal_num_pos

    print(proposal_related_words)
    print(proposal_num_neg)
    print(proposal_num_pos)
    print(proposal_min_score)
    max_min_score_proposal = max(proposal_min_score, key=proposal_min_score.get)
    max_min_score = proposal_min_score[max_min_score_proposal]
    candidate_proposals = [max_min_score_proposal] + [ proposal for proposal in filtered_proposals if proposal_max_score[proposal] > max_min_score ]

    proposal_ranked_words = {
        proposal: rank_words_if_necessary(proposal_related_words[proposal], proposal, pos_words, neg_words)
        for proposal in candidate_proposals
    }
    proposal_ranked_words, proposal_ranked_words_tokens = split_by_column(proposal_ranked_words)
    
    token_count += sum(proposal_related_words_tokens.values()) + sum(proposal_ranked_words_tokens.values())

    print(candidate_proposals)
    print(proposal_ranked_words)

    clue, clue_words = select_clue(proposal_ranked_words, pos_words)

    details = {
        "proposals": proposals,
        "words": words,
        "proposal_related_words": proposal_related_words,
        "proposal_related_words_tokens": proposal_related_words_tokens,
        "proposal_min_score": proposal_min_score,
        "proposal_max_score": proposal_max_score,
        "candidate_proposals": candidate_proposals,
        "proposal_ranked_words": proposal_ranked_words,
        "proposal_ranked_words_tokens": proposal_ranked_words_tokens,
        "tokens": token_count
    }

    return clue, clue_words, details
