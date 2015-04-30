import Tools

import re
import string
import json
import numpy as np

from sets import Set

from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix

from sklearn.feature_extraction import DictVectorizer

LIWC_DICT = "../data/liwc_dict.json"

def unigram(tweets):
    tweet_words = []
    for tweet_id in tweets.keys():
        word_dict = {}
        for word in tweets[tweet_id]["words"]:
            word = Tools.convert([word["text"]])[0]
            word_dict[word] = 1
        tweet_words.append(word_dict)

    vec = DictVectorizer()

    vec.fit(tweet_words)

    for tweet_id in tweets.keys():
        for word in tweets[tweet_id]["words"]:
            one_hot = csr_matrix((len(vec.get_feature_names()), 1))
            one_hot[vec.get_feature_names().index(word["text"]), 0] = 1
            word["features"] = one_hot

def liwc(tweets):
    def ispunct(s):
        return all(c in string.punctuation for c in s)

    liwc_dict = json.load(open(LIWC_DICT))
    for tweet_id in tweets.keys():
        for word in tweets[tweet_id]["words"]:
            text = Tools.convert([word["text"]])[0]
            if text in liwc_dict.keys():
                liwc_features = liwc_dict[text]
            elif ispunct(text):
                liwc_features = [0]*83 + [500]
            else:
                liwc_features = [0]*84
            feat = np.array(word["features"], dtype=float)
            word["features"] = np.append(feat, np.array(liwc_features, dtype=float))
            
