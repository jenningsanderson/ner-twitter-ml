from numpy import array
import numpy as np
import copy, math

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.feature_extraction import DictVectorizer
from sklearn.utils.multiclass import unique_labels
from sklearn import cross_validation

import re
import random

def pretty_print_performance(final_performance, labels=["Artifact", "Facility", "Location", "None", "Organization", "Person"]):
    '''
    From metrics.classification_report
    '''
    labels = np.asarray(labels)
    digits = 4

    last_line_heading = 'avg / total'

    width = len(last_line_heading)
    target_names = ['%s' % l for l in labels]

    headers = ["precision", "recall", "f1-score", "support"]
    fmt = '%% %ds' % width  # first column: class name
    fmt += '  '
    fmt += ' '.join(['% 9s' for _ in headers])
    fmt += '\n'

    headers = [""] + headers
    report = fmt % tuple(headers)
    report += '\n'

    p, r, f1, s = np.mean(final_performance, axis=0)

    for i, label in enumerate(labels):
        values = [target_names[i]]
        for v in (p[i], r[i], f1[i]):
            values += ["{0:0.{1}f}".format(v, digits)]
        values += ["{0:0.{1}f}".format(s[i], 1)]
        report += fmt % tuple(values)

    report += '\n'

    # compute averages
    values = [last_line_heading]
    for v in (np.average(p, weights=s),
              np.average(r, weights=s),
              np.average(f1, weights=s)):
        values += ["{0:0.{1}f}".format(v, digits)]
    values += ['{0}'.format(np.sum(s))]
    report += fmt % tuple(values)
    
    print report

class Entity:

    def build_features(self, features):
        self.ngrams = ['n-2','n-1','n+2','n+1']
        self.word = ['Word']
        self.texttype = ['Caps','POS','Dep_rel','Dep_head']

        self.all_liwc = ['Abbreviations','Emoticons','Pronoun','I','We',
                            'Self','You','Other','Negate','Assent','Article','Preps','Number','Affect','Posemo','Posfeel','Optim','Negemo',
                            'Anx','Anger','Sad','Cogmech','Cause','Insight','Discrep','Inhib','Tentat','Certain','Senses','See','Hear', 'Feel',
                            'Social','Comm','Othref','Friends','Family','Humans','Time','Past','Present','Future','Space','Up','Down','Incl',
                            'Excl','Motion','Occup','School','Job','Achieve','Leisure','Home','Sports','TV','Music','Money','Metaph','Relig',
                            'Death','Physcal','Body','Sexual','Eating','Sleep','Groom', 'Swear','Nonfl','Fillers',  'Period','Comma','Colon',
                            'SemiC','QMark','Exclam','Dash','Quote','Apostro','Parenth','OtherP']

        self.keys_to_featurize = []

        if features is not None:
            for f in features:
                for ff in self.__dict__[f]:
                    self.keys_to_featurize.append(ff)

    def featurize(self, features):
        to_return = {}

        for key, value in features.iteritems():
            if key in self.keys_to_featurize:
                to_return[key] = value

        return to_return

    def import_full_feature(self, args):
        '''
        Imports and shuffles all of the data for the SVM classifier

        If test_set is set to True, then this is the test set that's being imported.
        '''
        self.all_data = copy.deepcopy(args['all_data'])
        random.shuffle(self.all_data)
        self.iterations = args['iterations']
        self.not_nones = []
        self.nones = []
        for data in self.all_data:
            if data[self.name] == self.name:
                self.not_nones.append({'features':data,'text':data['Word'],'label':self.name})
            else:
                self.nones.append({'features':data,'text':data['Word'],'label':'None'})

        if args['limitNones']:
            self.nones = self.nones[:len(self.not_nones)]
    
        self.data = self.not_nones + self.nones
        random.shuffle(self.data)

        if args['test_set']:
            self.x_test_arr = [ self.v.transform( [ self.featurize( self.data[i]['features'] ) for i in range(len(self.data)) ] ) ]
            self.y_test_arr = [ [ self.data[i]['label'] for i in range(len(self.data)) ]  ]

        
        #This builds x_train_arr and y_train_arr...
        if args['build_and_separate']:
            self.build_and_separate_features(args['makeTest'])


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


    def build_and_separate_features(self, makeTest=True):
        '''
        Using a DictVectorizer and a cross validation shuffle splitter, split the data into training and test
        '''
        self.v = DictVectorizer()

        if makeTest:
            self.cv = cross_validation.ShuffleSplit(len(self.data), n_iter=self.iterations, test_size=0.25, random_state=0)
        else:
            self.cv = cross_validation.ShuffleSplit(len(self.data), n_iter=self.iterations, test_size=0.0, random_state=0)
       
        self.x_train_arr = []
        self.y_train_arr = []
        
        if makeTest:
            self.x_test_arr =  []
            self.y_test_arr =  []

        self.x_train_originals_arr = []

        for train_index, test_index in self.cv:

            self.x_train_arr.append( self.v.fit_transform( [ self.featurize( self.data[i]['features'] ) for i in train_index ] ) )
            
            if makeTest:
                self.x_test_arr.append(  self.v.transform(     [ self.featurize( self.data[i]['features'] ) for i in test_index  ] ) )   
            
            self.y_train_arr.append( [ self.data[i]['label'] for i in train_index ] )
            
            if makeTest:
                self.y_test_arr.append(  [ self.data[i]['label'] for i in test_index ]  )

            self.x_train_originals_arr.append( [self.data[i] for i in train_index] )

    def do_full_svm(self):

        self.accuracies = [0]*self.iterations

        this_round = []

        for i in range(self.iterations):
            self.clf = LinearSVC()
            self.clf.fit(self.x_train_arr[i], self.y_train_arr[i])
            svm_prediction = self.clf.predict(self.x_test_arr[i])

            this_round.append( metrics.precision_recall_fscore_support(y_true=self.y_test_arr[i], y_pred=svm_prediction) )

            self.accuracies[i] = metrics.accuracy_score(self.y_test_arr[i], svm_prediction)

            self.labels =  unique_labels(self.y_test_arr[i], svm_prediction)
            print ".",
    
        self.performance = np.mean(this_round, axis=0)
        print ""

    def pretty_print_entity_performance():
        pretty_print_performance(self.performance, self.labels)


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
