# -*- coding: utf-8 -*-
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def calculate_score(seg_list, sentiment_words, negative_words, degree_words):
    '''
    Function to compute sentiment score of a comment(segment list)

    seg_list: list; segment result of one comment
    sentiment_words: dict; keys are sentiment words and values are list of polarity and sentiment score
    negative_words: list; negative words
    degree_words: dict; keys are words and values are degree scores
    '''
    # initialize variable
    polarity = 1
    sentiment_score = 0
    degree_scrore = 1
    negative_score = 1
    negative_word_idx = -1
    degree_word_idx = -1
    final_score = 0
    try:
        # compute the sentiment score ignore negative words and degree words
        for word in seg_list:
            if word in sentiment_words:
                line = sentiment_words[word]
                polarity = line[0]
                sentiment_score = line[1]
                final_score += polarity * sentiment_score
        # adjust sentiment score for degree words and negative words
        if final_score:
            for i in range(len(seg_list)):
                if seg_list[i] in negative_words:
                    negative_score *= -1
                    negative_word_idx = i
                if seg_list[i] in degree_words:
                    degree_scrore *= degree_words[seg_list[i]]
                    degree_word_idx = i
        # only consider last idx of degree word and negative word
        if negative_word_idx >= 0 and degree_word_idx >= 0:
            if negative_word_idx > degree_word_idx:
                final_score = -(final_score * degree_scrore * negative_score)/2
            else:
                final_score = final_score * degree_scrore * negative_score
        elif negative_word_idx >= 0 and degree_word_idx < 0:
            final_score = (final_score * negative_score)/2
        elif negative_word_idx < 0 and degree_word_idx >= 0:
            final_score = final_score * degree_scrore 
    except Exception as e:
        logging.info("sentiment score computation error {} happen!".format(e))
    return final_score
