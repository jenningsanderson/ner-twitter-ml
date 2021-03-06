from csv import DictReader, DictWriter

from numpy import array

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC

#NLTK:
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

import re
import random

import loader as loader


# We need to be able to tag things with multiple labels.
# Easiest to do 5 different categories.

#
# Will do this manually for each of the category
#

#
# Rewrite the analyzer to look up the text
#


class Analyzer:
    def __init__(self, name):
        print "Initialized an Analyzer named: %s" %(name) #Just trying to remember how Python works

    def __call__(self, text):

        #Simplest, just yield the word itself as a feature
        yield text

        if text[0].isupper():
            yield "capitalized"

        #Could potentially also yield all of the LIWC features -- but perhaps not.





class Featurizer:
    def __init__(self, analyzer):
        self.vectorizer = CountVectorizer(
            analyzer=analyzer,
            max_features=2500000
            )

    def train_feature(self, examples):
        return self.vectorizer.fit_transform(examples)

    def test_feature(self, examples):
        return self.vectorizer.transform(examples)



if __name__ == "__main__":
    analyzer = Analyzer('Simplest case')
    feat = Featurizer(analyzer=analyzer)

    data = []

    for tweet in loader.load_json_tweets('./data/tweets.json', limit=5000):
        for labeled in loader.tweet_to_vectors(tweet):
            data.append(labeled)

    random.shuffle(data)

    train = data[:4000]
    test  = data[4001:]

    x_train = feat.train_feature( [t['text'] for t in train] )
    x_test = feat.test_feature( [t['text'] for t in test] )

    print "Number of Features: %d" %(len(feat.vectorizer.get_feature_names()))

    y_train = [t['label'] for t in train]


    # Train classifier
    lr = SGDClassifier(loss='log', penalty='l2', shuffle=True)
    lr.fit(x_train, y_train)

    # Train an SVM?
    # clf = SVC()
    # clf.fit(x_train, y_train)

    #Write out Predictions
    predictions = lr.predict(x_test)
    # predictions = clf.predict(x_test)

    print metrics.classification_report(y_true=[t['label'] for t in test], y_pred=predictions)
