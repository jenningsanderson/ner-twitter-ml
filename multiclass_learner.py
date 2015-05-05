from numpy import array
import numpy as np
import copy

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.feature_extraction import DictVectorizer
from sklearn import cross_validation

import re
import random
import loader as loader
from learner import Entity, pretty_print_performance
from entity import *
import threading


def find_the_none_nones(words, types):
    nones = []
    for feature in words:
        good = True
        for ent in types:
            if feature[ent.name] == ent.name:
                good=False

        if good:
            nones.append({'text': feature['Word'], 'features': feature, 'label': 'None'})

    return nones



def featurize(features):
    return {"Word": features['Word'], 'Caps':features['Caps'],'POS':features['POS'],'Dep_rel':features['Dep_rel'],'Dep_head':features['Dep_head'],
            'n-2':features['n-2'], 'n-1':features['n-1'], 'n+2':features['n+2'], 'n+1':features['n+1']}


if __name__ == "__main__":

    limit       = 5000  #Limit of rows to load from the CSV
    iterations  = 3      #Number of iterations for the cross validation
    outer_iters= 2      #Number of outer iterations

    words = loader.load_csv_tweets('./data/LIWC2001 Results_5class_new.csv', limit=limit)
    random.shuffle(words) #Shuffle the words here

    final_performance   = []
    final_accuracies    = []

    for jj in range(outer_iters):
        print 'Outer Iteration ' + str(jj) + ' of ' + str(outer_iters)

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
            t = threading.Thread(target=task, args=(words,iterations,False))
            t.start()
            t.join()

        nones = find_the_none_nones(words, entities) #Get all of the none values
        random.shuffle(nones)

        multiclass_data = []
        count = 0
        for ent in entities:
            for data in ent.not_nones:
                count+=1
                multiclass_data.append(data)

        multiclass_data += nones[:count]

        #Build a dictvectorizer and start the crossvalidation options
        v = DictVectorizer()

        # #Separate
        cv = cross_validation.ShuffleSplit(len(multiclass_data), n_iter=iterations, test_size=0.25, random_state=0)

        x_train_arr = []
        y_train_arr = []
        x_test_arr =  []
        y_test_arr =  []

        for train_index, test_index in cv:
            x_train_arr.append( v.fit_transform( [ featurize( multiclass_data[i]['features'] ) for i in train_index ] ) )
            x_test_arr.append(  v.transform(     [ featurize( multiclass_data[i]['features'] ) for i in test_index  ] ) )   

            y_train_arr.append( [ multiclass_data[i]['label'] for i in train_index ] )
            y_test_arr.append(  [ multiclass_data[i]['label'] for i in test_index ]  )


        accuracies = [0]*iterations
        this_round = []
 
        for i in range(iterations):
            clf = LinearSVC()
            clf.fit(x_train_arr[i], y_train_arr[i])
            svm_prediction = clf.predict(x_test_arr[i])

            accuracies[i] = metrics.accuracy_score(y_test_arr[i], svm_prediction)
            # print metrics.classification_report(y_true=y_test_arr[i], y_pred=svm_prediction)
            this_round.append( metrics.precision_recall_fscore_support(y_true=y_test_arr[i], y_pred=svm_prediction) )

        final_performance.append(np.mean(this_round, axis=0))
        final_accuracies.append(np.mean(accuracies))

    #Print performance results
    pretty_print_performance(final_performance)
    print "Final Accuracy: " + str(np.mean(final_accuracies))


