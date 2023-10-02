from code_names_bot.generator.proposal_generator import get_proposals
from code_names_bot.generator.score_generator import get_scores
from code_names_bot.util.dict import split_by_column
from code_names_bot.util.propose_score import get_clue_words_scores


def _propose_score_clue(pos_words, neg_words, propose_count):
    proposals, token_count = get_proposals(pos_words, neg_words, propose_count)
    words = pos_words + neg_words
    proposal_scores = { proposal: get_scores(words, proposal) for proposal in proposals }
    proposal_scores, proposal_tokens = split_by_column(proposal_scores)
    proposal_clue_words_scores = { proposal: get_clue_words_scores(proposal_scores[proposal], pos_words, neg_words) for proposal in proposals }
    proposal_clue_words, proposal_clue_scores = split_by_column(proposal_clue_words_scores)

    clue = max(proposal_clue_scores, key=proposal_clue_scores.get)
    token_count += sum(proposal_tokens.values())

    details = {
        "words": words,
        "proposal_scores": proposal_scores,
        "tokens": token_count
    }

    return clue, proposal_clue_words[clue], details


def propose_5_score_clue(pos_words, neg_words):
    return _propose_score_clue(pos_words, neg_words, 5)


def propose_10_score_clue(pos_words, neg_words):
    return _propose_score_clue(pos_words, neg_words, 10)
