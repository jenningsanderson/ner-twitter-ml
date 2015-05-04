import re
import random

import loader as loader
from Entity import *
from learner import Entity
import threading



if __name__ == "__main__":

    limit       = 2000  #Limit of rows to load from the CSV
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
    # for task in [ent.do_full_svm for ent in entities]:
    #     t = threading.Thread(target=task, args=())
    #     t.start()
    #     t.join()

    # # then add all these output together : 
    # X_probs_train = numpy.hstack((probs_train_artifact,probs_train_person,...))
    # Y_train = numpy.hstack((Y_train_artifact,Y_train_person,...))


    # for ent in entities:
    #     print ent.name + "\n---------------------------"
    #     print "Accuracy:  "+ str(np.average(ent.accuracies) )
    #     print "Recall:    "+ str(np.average(ent.recalls)    )
    #     print "Precision: "+ str(np.average(ent.precisions) )
    #     print "F1-Score:  "+ str(np.average(ent.f1s)        )
    #     print "==========================="
