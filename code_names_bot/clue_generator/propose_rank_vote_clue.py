from code_names_bot.generator.proposal_generator import get_proposals
from code_names_bot.util.propose_rank import select_clue
from code_names_bot.util.dict import split_by_column, merge
from code_names_bot.util.propose_rank import get_word_scores, word_scores_to_sorted_list


ROUNDS = 3


def propose_rank_vote(pos_words, neg_words):
    proposals, token_count = get_proposals(pos_words, neg_words)
    words = pos_words + neg_words
    proposal_word_scores = { proposal: get_word_scores(words, proposal, ROUNDS) for proposal in proposals }
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