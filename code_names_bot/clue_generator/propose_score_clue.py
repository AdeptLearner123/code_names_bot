from code_names_bot.generator.proposal_generator import get_proposals
from code_names_bot.generator.score_generator import get_scores
from code_names_bot.util.dict import split_by_column

import random

def _get_max_neg_scores(scores, neg_words):
    return max([ scores[word] for word in neg_words ])


def _get_clue_words(scores, pos_words, max_neg_score):
    return [ word for word in pos_words if scores[word] > max_neg_score ]


def _get_clue_scores(scores, clue_words, max_neg_score):
    if len(clue_words) == 0:
        pos_neg_gap = 0
    else:
        pos_neg_gap = min([ scores[word] - max_neg_score for word in clue_words ])

    return len(clue_words), pos_neg_gap


def propose_score_clue(pos_words, neg_words):
    proposals, token_count = get_proposals(pos_words, neg_words, 5)
    words = pos_words + neg_words
    random.Random(0).shuffle(words)

    proposal_scores = { proposal: get_scores(words, proposal) for proposal in proposals }
    proposal_scores, proposal_tokens = split_by_column(proposal_scores)
    proposal_max_neg = { proposal: _get_max_neg_scores(proposal_scores[proposal], neg_words) for proposal in proposals }
    proposal_clue_words = { proposal: _get_clue_words(proposal_scores[proposal], pos_words, proposal_max_neg[proposal]) for proposal in proposals }
    proposal_clue_scores = { proposal: _get_clue_scores(proposal_scores[proposal], proposal_clue_words[proposal], proposal_max_neg[proposal]) for proposal in proposals }
    
    clue = max(proposal_clue_scores, key=proposal_clue_scores.get)
    token_count += sum(proposal_tokens.values())

    details = {
        "words": words,
        "proposal_scores": proposal_scores,
        "tokens": token_count
    }

    return clue, proposal_clue_words[clue], details
