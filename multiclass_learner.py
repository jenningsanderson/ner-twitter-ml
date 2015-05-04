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
from learner import Entity
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

    limit       = 10000  #Limit of rows to load from the CSV
    iterations  = 5     #Number of iterations for the cross validation

    words = loader.load_csv_tweets('./data/LIWC2001 Results_5class_new.csv', limit=limit)
    random.shuffle(words) #Shuffle the words here


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

    print cv

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
    precisions = [0]*iterations
    recalls    = [0]*iterations
    f1s        = [0]*iterations
    for i in range(iterations):
        clf = LinearSVC()
        clf.fit(x_train_arr[i], y_train_arr[i])
        svm_prediction = clf.predict(x_test_arr[i])

        precisions[i] = metrics.precision_score(y_true=y_test_arr[i], y_pred=svm_prediction, pos_label=None)
        recalls[i]    = metrics.recall_score(y_true=y_test_arr[i], y_pred=svm_prediction, pos_label=None)
        f1s[i]        = metrics.f1_score(y_true=y_test_arr[i], y_pred=svm_prediction, pos_label=None)
        accuracies[i] = metrics.accuracy_score(y_test_arr[i], svm_prediction)

        print "Metrics Classification for round: " + str(i)
        print metrics.classification_report(y_true=y_test_arr[i], y_pred=svm_prediction)


    print "Cross Validation for "+str(iterations)+" rounds."
    print "Accuracy:  "+ str(np.average(accuracies) )
    print "Recall:    "+ str(np.average(recalls)    )
    print "Precision: "+ str(np.average(precisions) )
    print "F1-Score:  "+ str(np.average(f1s)        )
    print "==========================="



