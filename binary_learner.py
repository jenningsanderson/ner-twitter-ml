from numpy import array
import numpy as np

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.feature_extraction import DictVectorizer

# #NLTK:
# from nltk.corpus import stopwords
# from nltk.stem.porter import PorterStemmer

import re
import random

import loader as loader
from entity import *
import threading

class Entity:
    def import_data(self, tweets):
        print "Loading "+self.name+"....",
        self.data = []
        for tweet in tweets:
            self.data += loader.tweet_to_vectors(tweet, self.name)
        print "Finished {0}".format(self.name)


    def import_full_feature(self, all_data):
        random.shuffle(all_data)
        self.not_nones = []
        self.nones = []
        for data in all_data:
            if data[self.name] == self.name:
                self.not_nones.append({'features':data,'text':data['Word'],'label':self.name})
            else:
                self.nones.append({'features':data,'text':data['Word'],'label':'None'})

        self.nones = self.nones[:len(self.not_nones)]

        self.data = self.not_nones + self.nones


    def trim_none_values_to_match(self):
        random.shuffle(self.data)
        self.not_nones = []
        self.nones    = []
        for x in self.data:
            if x['label']!="None":
                self.not_nones.append(x)
            else:
                self.nones.append(x)
            
        self.nones = self.nones[:len(self.not_nones)]

        self.data = self.not_nones + self.nones
        random.shuffle(self.data)


    def build_features(self, percent=80):
        self.v = DictVectorizer()

        #Separate
        limit = int((percent/100.0)*len(self.data))
        self.train_set = self.data[:limit]
        self.test_set  = self.data[limit+1:]

        #Vectorize
        self.x_train   = self.v.fit_transform([self.featurize(x['features']) for x in self.train_set])
        self.x_test    = self.v.transform([self.featurize(x['features']) for x in self.test_set])

        #Save Labels
        self.y_train   = [x['label'] for x in self.train_set]
        self.y_test    = [x['label'] for x in self.test_set]


    def featurize(self, features):
        return {"Word": features['Word']}

    def train_lr_classifier(self):
        self.lr = SGDClassifier(loss='log', penalty='l2', shuffle=True)
        self.lr.fit(self.x_train, self.y_train)

    def train_svm_classifier(self):
        self.clf = SVC()
        self.clf.fit(self.x_train, self.y_train)

    def test_svm(self):
        self.svm_predictions = self.clf.predict(self.x_test)

    def test_lr(self):
        self.lr_predictions = self.lr.predict(self.x_test)

    def report_svm(self):
        print metrics.classification_report(y_true=self.y_test, y_pred=self.svm_predictions)

    def report_lr(self):
        print metrics.classification_report(y_true=self.y_test, y_pred=self.lr_predictions)
        print self.name + ": "+str(metrics.accuracy_score(self.y_test, self.lr_predictions))
    def do_full_svm(self):
        self.build_features()
        self.train_svm_classifier()
        self.test_svm()
        self.report_svm()

    def do_full_lr(self):
        self.build_features()
        self.train_lr_classifier()
        self.test_lr()
        self.report_lr()



if __name__ == "__main__":

    limit       = None

    # tweets = loader.load_json_tweets('./data/tweets.json', limit=limit)

    words = loader.load_csv_tweets('./data/LIWC2001Results_5class.csv', limit=limit)

    artifacts       = Artifact()
    persons         = Person()
    locations       = Location()
    facilities      = Facility()
    organizations   = Organization()

    entities = [artifacts, persons, locations, facilities, organizations]

    #import_tasks = [ent.import_data for ent in entities]

    import_tasks = [ent.import_full_feature for ent in entities]

    for task in import_tasks:
        t = threading.Thread(target=task, args=(words,))
        t.start()
        t.join()

    #Run all the classifiers in parallel:
    for task in [ent.do_full_lr for ent in entities]:
        t = threading.Thread(target=task, args=())
        t.start()
