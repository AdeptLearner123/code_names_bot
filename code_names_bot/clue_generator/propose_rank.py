from code_names_bot.util.propose_rank import get_proposals, get_ranked_words, select_clue
from code_names_bot.util.dict import split_by_column, merge

import random

def propose_rank_clue(pos_words, neg_words):
    proposals, token_count = get_proposals(pos_words, neg_words)    
    words = pos_words + neg_words
    random.Random(0).shuffle(words)
    proposal_ranked_words = { proposal: get_ranked_words(words, proposal) for proposal in proposals }
    proposal_ranked_words, proposal_tokens = split_by_column(proposal_ranked_words)
    proposal_details = merge(("ranked_words", proposal_ranked_words), ("tokens", proposal_tokens))
    token_count += sum(proposal_tokens.values())
    clue, clue_words = select_clue(proposal_ranked_words, pos_words)

    details = {
        "proposals": proposals,
        "words": words,
        "proposal_details": proposal_details,
        "tokens": token_count
    }

    return clue, clue_words, details
