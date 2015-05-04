from numpy import array
import numpy as np
import copy

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.feature_extraction import DictVectorizer

from sklearn import cross_validation

# #NLTK:
# from nltk.corpus import stopwords
# from nltk.stem.porter import PorterStemmer

import re
import random

import loader as loader
from entity import *
import threading

class Entity:
    def featurize(self, features):
        #Default featurizer -- override these in the entity classes
        return {"Word": features['Word']}

    def import_full_feature(self, all_data, iterations):
        self.all_data = copy.deepcopy(all_data)
        random.shuffle(self.all_data)
        self.iterations = iterations
        self.not_nones = []
        self.nones = []
        for data in self.all_data:
            if data[self.name] == self.name:
                self.not_nones.append({'features':data,'text':data['Word'],'label':self.name})
            else:
                self.nones.append({'features':data,'text':data['Word'],'label':'None'})

        self.nones = self.nones[:len(self.not_nones)]
        self.data = self.not_nones + self.nones

        random.shuffle(self.data)

        #This builds x_train_arr and y_train_arr...
        self.build_and_separate_features()

    def build_and_separate_features(self):
        self.v = DictVectorizer()

        # #Separate
        self.cv = cross_validation.ShuffleSplit(len(self.data), n_iter=self.iterations, test_size=0.25, random_state=0)

        self.x_train_arr = []
        self.y_train_arr = []
        self.x_test_arr = []
        self.y_test_arr = []

        for train_index, test_index in self.cv:

            self.x_train_arr.append( self.v.fit_transform( [ self.featurize( self.data[i]['features'] ) for i in train_index ] ) )
            self.x_test_arr.append(  self.v.transform(     [ self.featurize( self.data[i]['features'] ) for i in test_index  ] ) )   
            
            self.y_train_arr.append( [ self.data[i]['label'] for i in train_index ] )
            self.y_test_arr.append(  [ self.data[i]['label'] for i in test_index ]  )

    def do_full_svm(self):
        self.accuracies = [0]*self.iterations
        self.precisions = [0]*self.iterations
        self.recalls    = [0]*self.iterations
        self.f1s        = [0]*self.iterations
        for i in range(self.iterations):
            self.clf = LinearSVC()
            self.clf.fit(self.x_train_arr[i], self.y_train_arr[i])
            self.svm_prediction = self.clf.predict(self.x_test_arr[i])

            self.precisions[i] = metrics.precision_score(y_true=self.y_test_arr[i], y_pred=self.svm_prediction, pos_label=None)
            self.recalls[i]    = metrics.recall_score(y_true=self.y_test_arr[i], y_pred=self.svm_prediction, pos_label=None)
            self.f1s[i]        = metrics.f1_score(y_true=self.y_test_arr[i], y_pred=self.svm_prediction, pos_label=None)
            self.accuracies[i] = metrics.accuracy_score(self.y_test_arr[i], self.svm_prediction)

            print "Metrics Classification for " + self.name + "; Round: " + str(i)
            print metrics.classification_report(y_true=self.y_test_arr[i], y_pred=self.svm_prediction)
            

if __name__ == "__main__":

    limit       = 3000  #Limit of rows to load from the CSV
    iterations  = 5     #Number of iterations for the cross validation

    words = loader.load_csv_tweets('./data/LIWC2001Results_5class.csv', limit=limit)

    #Make a class for each piece
    artifacts       = Artifact()
    persons         = Person()
    locations       = Location()
    facilities      = Facility()
    organizations   = Organization()
    entities = [artifacts, persons, locations, facilities, organizations]

    #Import the data
    import_tasks = [ent.import_full_feature for ent in entities]
    for task in import_tasks:
        t = threading.Thread(target=task, args=(words,iterations))
        t.start()
        t.join()

    #This is where we actually run a classifier
    #Run all the classifiers in parallel:
    for task in [ent.do_full_svm for ent in entities]:
        t = threading.Thread(target=task, args=())
        t.start()
        t.join()

    #Print the results
    for ent in entities:
        print ent.name + "\n---------------------------"
        print "Accuracy:  "+  str(ent.accuracies) + "; average: " + str(np.average(ent.accuracies) )
        print "Recall:    "+  str(ent.recalls)    + "; average: " + str(np.average(ent.recalls)    )
        print "Precision: "+  str(ent.precisions) + "; average: " + str(np.average(ent.precisions) )
        print "F1-Score:  "+  str(ent.f1s)        + "; average: " + str(np.average(ent.f1s)        )
        print "==========================="
