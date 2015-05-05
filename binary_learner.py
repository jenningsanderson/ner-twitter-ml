import loader as loader
from entity import *
from learner import Entity
import threading
import numpy as np

if __name__ == "__main__":

    limit       = 10000  #Limit of rows to load from the CSV
    iterations  = 5     #Number of iterations for the cross validation
    outer_iterations = 5

    words = loader.load_csv_tweets('./data/LIWC2001 Results_5class_new.csv', limit=limit)

    big_recall = {} 
    big_percision = {}
    big_accuracies ={}
    big_F1 = {}
    
    entity_names =['Artifact','Person','Location','Facility','Organization']
    
    for ent in entity_names:
        big_recall[ent]=[]
        big_percision[ent] = []
        big_accuracies[ent] =[]
        big_F1 [ent] = []    
    
    for itx in range(outer_iterations):
        print "Outer Iteration: " + str(itx+1)
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
            """
            print ent.name + "\n---------------------------"
            print "Accuracy:  "+  str(ent.accuracies) + "; average: " + str(np.average(ent.accuracies) )
            print "Recall:    "+  str(ent.recalls)    + "; average: " + str(np.average(ent.recalls)    )
            print "Precision: "+  str(ent.precisions) + "; average: " + str(np.average(ent.precisions) )
            print "F1-Score:  "+  str(ent.f1s)        + "; average: " + str(np.average(ent.f1s)        )
            print "==========================="
            """
            big_accuracies[ent.name].append(np.average(ent.accuracies))
            big_recall[ent.name].append(np.average(ent.recalls))
            big_percision[ent.name].append(np.average(ent.precisions))
            big_F1[ent.name].append(np.average(ent.f1s))
            

    for ent in entities:
        print ent.name + "s\n---------------------------"
        print "Accuracy: " + str(np.average(big_accuracies[ent.name]))
        print "Recall: "   + str(np.average(big_recall[ent.name]))
        print "Percision: " + str(np.average(big_percision[ent.name]))
        print "F1 Score: " + str(np.average(big_F1[ent.name]))
    print "==========================="
