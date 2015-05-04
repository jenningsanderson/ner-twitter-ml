from numpy import array
import numpy as np
import copy, math

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.feature_extraction import DictVectorizer

from sklearn import cross_validation

import re
import random



class Entity:
    def featurize(self, features):
        #Default featurizer -- override these in the entity classes
        return {"Word": features['Word']}

    def import_full_feature(self, all_data, iterations, build_and_separate=True):
        '''
        Imports and shuffles all of the data for the SVM classifier
        '''
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
        if build_and_separate:
            self.build_and_separate_features()

    def import_static_x_vector(self, all_data):
        '''
        Imports self.data to be the same for all subclasses
        '''
        self.iterations = 1
        self.not_nones = []
        self.nones = []
        for i in range(len(all_data)):
            data = all_data[i]
            if data[self.name] == self.name:
                self.not_nones.append({'features':data, 'text':data['Word'], 'label':self.name, 'all_data_index':i})
            else:
                self.nones.append({'features':data, 'text':data['Word'], 'label':'None', 'all_data_index':i})

        self.nones = self.nones[:len(self.not_nones)]
        self.data = self.not_nones + self.nones

        self.build_and_separate_features()


    def build_and_separate_features(self):
        '''
        Using a DictVectorizer and a cross validation shuffle splitter, split the data into training and test
        '''
        self.v = DictVectorizer()

        # #Separate
        self.cv = cross_validation.ShuffleSplit(len(self.data), n_iter=self.iterations, test_size=0.25, random_state=0)

        self.x_train_arr = []
        self.y_train_arr = []
        self.x_test_arr =  []
        self.y_test_arr =  []

        self.x_train_originals_arr = []

        for train_index, test_index in self.cv:

            self.x_train_arr.append( self.v.fit_transform( [ self.featurize( self.data[i]['features'] ) for i in train_index ] ) )
            self.x_test_arr.append(  self.v.transform(     [ self.featurize( self.data[i]['features'] ) for i in test_index  ] ) )   
            
            self.y_train_arr.append( [ self.data[i]['label'] for i in train_index ] )
            self.y_test_arr.append(  [ self.data[i]['label'] for i in test_index ]  )

            self.x_train_originals_arr.append( [self.data[i] for i in train_index] )

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

            print metrics.classification_report(y_true=self.y_test_arr[i], y_pred=self.svm_prediction)
    
    
    def get_feature_probabilities(self, iteration=0):
        "Print Starting the Decision Fusion Probabilities for ", self.name
        self.decision_clf = LinearSVC(C=1)
        self.decision_clf.fit(self.x_train_arr[iteration], self.y_train_arr[iteration])

        dis_fun = self.decision_clf.decision_function(self.x_train_arr[iteration][0])[0]
        probs_train = [1/(1+math.exp(-dis_fun))]
        for j in range(1,len(self.y_train_arr[iteration])):
            dis_fun= self.decision_clf.decision_function(self.x_train_arr[iteration][j])[0]
            probs_train = np.vstack((probs_train,[1/(1+math.exp(-dis_fun))]))

        print self.name
        print np.shape(self.x_train_arr[iteration])
        print np.shape(probs_train)

        self.probs_train = probs_train
        # for x in range(len(self.x_train_originals_arr[iteration])):
        #     print self.name + ": "+ self.x_train_originals_arr[iteration][x]['text'] + " " +str(probs_train[x])
