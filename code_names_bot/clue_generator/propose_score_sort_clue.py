from code_names_bot.generator.proposal_generator import get_proposals
from code_names_bot.generator.score_generator import get_scores
from code_names_bot.generator.compare_generator import compare
from code_names_bot.util.propose_rank import select_clue

def _compare(word1, word2, proposal, neg_words):
    comparison = compare(proposal, word1, word2)

    if comparison == 0:
        return int(word1 in neg_words) - int(word2 in neg_words)

    return comparison

def _get_sorted_words(pos_words, neg_words, proposal):
    print("Processing", proposal)
    words = pos_words + neg_words
    scores, tokens = get_scores(words, proposal)
    total_tokens = tokens

    # Sort by score ascending. Negative words appear after positive words if equal. Then sort by alphabet.
    sorted_words = sorted(words, key=lambda word: (scores[word], word in neg_words, word))
    initial_sort = list(sorted_words)

    # Insertion sort
    for i in range(1, len(sorted_words)):
        word = sorted_words[i]
        print("Sorting: ", word)
        for j in range(i - 1, -1, -1):
            print("Comparing", word, sorted_words[j])
            comparison, compare_tokens = _compare(word, sorted_words[j], proposal, neg_words)
            total_tokens += compare_tokens

            if comparison >= 0:
                break

            sorted_words[j + 1] = sorted_words[j]
            sorted_words[j] = word

    return sorted_words, total_tokens, initial_sort


def propose_score_sort_clue(pos_words, neg_words):
    proposals, token_count = get_proposals(pos_words, neg_words, 10)
    total_tokens = token_count

    proposal_details = {}
    proposal_ranked_words = {}

    for proposal in proposals:
        sorted_words, tokens, initial_sort = _get_sorted_words(pos_words, neg_words, proposal)
        total_tokens += tokens
        proposal_details[proposal] = {
            "initial_sort": initial_sort,
            "sorted": sorted_words
        }
        proposal_ranked_words[proposal] = list(reversed(sorted_words))

    clue, words = select_clue(proposal_ranked_words, pos_words)
    details = {
        "proposals": proposal_details,
        "tokens": total_tokens
    }

    return clue, words, details