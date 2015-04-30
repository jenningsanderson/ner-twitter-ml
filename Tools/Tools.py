import re
import nltk

from sets import Set

def convert(list_of_tweet_texts):
    web_pattern = re.compile(r".*www\.|http:|https:.*")
    num_pattern = re.compile("[0-9]+")

    for i in range(len(list_of_tweet_texts)):
        tweet_text = list_of_tweet_texts[i]
        new_text = ""
        for word in tweet_text.split():
            word = word.lower()
            if num_pattern.match(word):
                word = "[NUM]"
            elif web_pattern.match(word):
                word = "[WEB]"
            elif "{?}" in word:
                word = "{?}"
            new_text += word + " "
        list_of_tweet_texts[i] = new_text.strip()
    return list_of_tweet_texts

def to_dictionary(list_of_tweet_texts):
    print "building dict..."
    word_dict = Set()
    for text in list_of_tweet_texts:
        for word in text.split():
            word_dict.add(word)

    word_dict = sorted(list(word_dict))
    return word_dict

def to_bigrams(list_of_tweet_texts):
    bigrams = Set()
    for tweet_text in list_of_tweet_texts:
        for bigram in nltk.bigrams(tweet_text.split()):
            bigrams.add(bigram)
    return sorted(list(bigrams))
