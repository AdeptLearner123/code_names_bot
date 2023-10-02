def get_clue_words_scores(scores, pos_words, neg_words):
    max_neg_score = max([ scores[word] for word in neg_words ])
    clue_words = [ word for word in pos_words if scores[word] > max_neg_score ]

    if len(clue_words) == 0:
        pos_neg_gap = 0
    else:
        pos_neg_gap = min([ scores[word] - max_neg_score for word in clue_words ])

    return clue_words, (len(clue_words), pos_neg_gap)