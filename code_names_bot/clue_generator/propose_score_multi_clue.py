from code_names_bot.generator.proposal_generator import get_proposals
from code_names_bot.generator.score_generator import get_scores

ROUNDS = 3

def _get_proposal_score(proposal, pos_words, neg_words):
    words = pos_words + neg_words
    scores_list = [ get_scores(words, proposal, i) for i in range(ROUNDS) ]
    scores_list, tokens_list = list(zip(*scores_list))
    total_tokens = sum(tokens_list)

    # How much above the maximum negative word a word is
    pos_word_scores = { word: 99 for word in pos_words }
    details = {}

    for i, scores in enumerate(scores_list):
        max_neg_score = max([ scores[word] for word in neg_words ])

        for pos_word in pos_words:
            pos_word_scores[pos_word] = min(pos_word_scores[pos_word], scores[pos_word] - max_neg_score)
        
        max_neg_clue = max(neg_words, key=lambda word: scores[word])
        details[i] = {}
        details[i][max_neg_clue] = max_neg_score
        for pos_word in pos_words:
            details[i][pos_word] = scores[pos_word]
    
    clue_words = [ word for word in pos_words if pos_word_scores[word] > 0 ]
    
    if len(clue_words) == 0:
        return [], 0, {}, total_tokens

    return clue_words, min([ pos_word_scores[word] for word in clue_words]), details, total_tokens


def propose_score_multi_clue(pos_words, neg_words):
    proposals, tokens = get_proposals(pos_words, neg_words, 10)
    total_tokens = tokens
    proposal_results = [ _get_proposal_score(proposal, pos_words, neg_words) for proposal in proposals ]
    proposal_clue_words, proposal_gaps, proposal_details, proposal_tokens = list(zip(*proposal_results))
    total_tokens += sum(proposal_tokens)
    proposal_details = { proposal: details for proposal, details in zip(proposals, proposal_details) }
    proposal_clue_words = { proposal: clue_words for proposal, clue_words in zip(proposals, proposal_clue_words) }
    proposal_gaps = { proposal: gap for proposal, gap in zip(proposals, proposal_gaps) }

    print(proposal_clue_words)
    clue = max(proposals, key=lambda proposal: (len(proposal_clue_words[proposal]), proposal_gaps[proposal]))
    clue_words = proposal_clue_words[clue]

    details = {
        "proposals": proposal_details,
        "tokens": total_tokens
    }

    return clue, clue_words, details