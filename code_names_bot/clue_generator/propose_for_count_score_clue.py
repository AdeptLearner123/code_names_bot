from code_names_bot.generator.proposal_for_count_generator import get_proposals_for_count
from code_names_bot.generator.score_generator import get_scores
from code_names_bot.util.propose_score import get_clue_words_scores
from code_names_bot.util.dict import split_by_column

MAX_TARGET = 5

def propose_for_count_score_clue(pos_words, neg_words):
    words = pos_words + neg_words
    total_tokens = 0
    all_proposals = {}
    all_proposal_scores = {}
    all_proposal_clue_words = {}
    all_proposal_clue_scores = {}

    for i in range(MAX_TARGET, 0, -1):
        proposal_words, tokens = get_proposals_for_count(pos_words, i, 5)
        total_tokens += tokens
        proposals = list(proposal_words.keys())
        all_proposals[i] = proposal_words

        proposal_scores = { proposal: get_scores(words, proposal) for proposal in proposals }
        proposal_scores, proposal_tokens = split_by_column(proposal_scores)
        total_tokens += sum(proposal_tokens.values())
        proposal_clue_words_scores = { proposal: get_clue_words_scores(proposal_scores[proposal], pos_words, neg_words) for proposal in proposals }
        proposal_clue_words, proposal_clue_scores = split_by_column(proposal_clue_words_scores)

        all_proposal_scores.update(proposal_scores)
        all_proposal_clue_words.update(proposal_clue_words)
        all_proposal_clue_scores.update(proposal_clue_scores)

        print(max(all_proposal_clue_scores.values()))
        top_score, _ = max(all_proposal_clue_scores.values())
        if top_score >= i:
            break

    clue = max(proposal_clue_scores, key=proposal_clue_scores.get)
    clue_words = all_proposal_clue_words[clue]

    details = {
        "proposals": all_proposals,
        "proposal_scores": all_proposal_scores,
        "proposal_clue_scores": all_proposal_clue_scores,
        "tokens": total_tokens
    }

    return clue, clue_words, details