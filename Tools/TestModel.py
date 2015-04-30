import json
import subprocess
import os
import random
import numpy
import sys
import string
import re
import glob

import numpy as np

from sklearn.svm import SVC
from operator import add

import Features

#features = []
features = [Features.liwc]

caps_template = "templates/capsTemplate"
null_template = "templates/nullTemplate"
trigram_template = "templates/trigramTemplate"

tags = ["Person", "Location", "Organization", "Facility", "Artifact"]

domains = ["Blizzard", "Flood", "Wildfire", "Earthquake", "Tornado", "Hurricane"]

current_template = caps_template
output_location = "/home/kevin/Documents/Epic/NER/Algorithms/CRF/output/caps_by_domain/"
model_location = "models/"

def add_features(list_of_tweets):
    for f in features:
        f(list_of_tweets)

def split_data(data, split_type):
    result = []
    if split_type == "cv":
        data = data.keys()
        split_data = chunks(data, 5)
        for tweet_list in split_data:
            current_chunk = []
            for tweet in tweet_list:
                current_chunk.append(tweet)
            result.append(current_chunk)
        return result
    elif split_type == "domain":
        split_data = [[] for _ in domains]
        for tweet_key in data:
            index = domains.index(data[tweet_key].domain)
            split_data[index].append(tweet_key)
        return split_data
    elif split_type == "event":
        split_data = {}

        for tweet_key in [tk for tk in data if data[tk].domain == "Wildfire"]:
            if data[tweet_key].disaster not in split_data:
                split_data[data[tweet_key].disaster] = [tweet_key]
            else:
                split_data[data[tweet_key].disaster].append(tweet_key)
        result = [[] for _ in split_data.keys()]
        b = 0
        for key in split_data:
            result[b] = split_data[key]
            b += 1
        sys.exit()
        return result
    return None

def chunks(l, n):
    newn = int(len(l)/n)
    for i in xrange(0, n-1):
        yield l[i*newn:i*newn+newn]
    yield l[n*newn-newn:]    

def run_model(tweets, data_split, output_dir, classifier):
    tag_results = {}
    for tag in tags:
        results = ""
        #split data:
        total_weights = []
        for i in range(len(data_split)):
            test_data = [tweets[t] for t in data_split[i]]
            train_data = []

            for split in data_split:
                if split != data_split[i]:
                    train_data += [tweets[t] for t in split]

            #train model
            X_train = []
            y_train = []

            for t in train_data:
                for w in t["words"]:
                    X_train.append(np.array(w["features"]))
                    if tag in w["annotations"]:
                        y_train.append(1)
                    else:
                        y_train.append(0)

            print "Training classifier..."
            classifier.fit(X_train[0:5000], y_train[0:5000])
            print "Done training!"
            if total_weights == []:
                total_weights = classifier.coef_
            else:
                map(add, total_weights, classifier.coef_)
            #run model on test data
            '''
            X_test = []
            for t in test_data:
                for w in t["words"]:
                    X_test.append(np.array(w["features"]))
                   
            results = classifier.predict(X_test)

            i = 0
            for j in range(len(test_data)):
                for w in test_data[j]["words"]:
                    if results[i] == 1:
                        print w["text"] + " " + str(w["annotations"]) + str(results[i])
                    i += 1
            #print results
        '''
        print tag + " done"
        print total_weights
        tag_results[tag] = list(total_weights[0]/5.)
    json.dump(tag_results, open("feature_weights.json", "w"))

def run():
    types = ["Facility", "Organization", "Person", "Location", "Artifact"]
    
    all_tweets = json.load(open("../data/sample_tweets.json"))

    add_features(all_tweets)

    data_split = split_data(all_tweets, "cv")

    classifier = SVC(kernel="linear")

    run_model(all_tweets, data_split, output_location, classifier)

r = []

run()
