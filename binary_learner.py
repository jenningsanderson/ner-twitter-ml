import loader as loader
import writer as writer
from entity import *
from learner import Entity, pretty_print_performance
import threading, time
import numpy as np

if __name__ == "__main__":

    limit       = 10000  #Limit of rows to load from the CSV
    iterations  = 10     #Number of iterations for the cross validation
    outer_iterations = 15

    out_file = "./output/all_liwc.csv"

    features = ['all_liwc']

    start = time.clock()

    words = loader.load_csv_tweets('./data/LIWC2001 Results_5class_new.csv', limit=limit)

    final_performances = {} 
    final_accuracies = {}

    entity_names =['Artifact','Person','Location','Facility','Organization']
    
    for ent in entity_names:
        final_accuracies[ent] =[]
        final_performances[ent] = [] 

    
    
    for itx in range(outer_iterations):
        print "Outer Iteration: " + str(itx+1)
        #Make a class for each piece
        artifacts       = Artifact(     features )
        persons         = Person(       features )
        locations       = Location(     features )
        facilities      = Facility(     features )
        organizations   = Organization( features )
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

        #Store the results of this round
        for ent in entities:
            final_performances[ent.name].append(ent.performance)
            final_accuracies[ent.name].append(np.mean(ent.accuracies))
      
    #Results
    to_csv = []        
    for ent in entities:
        print "\n====================================================================="
        print "-----------------------     " + ent.name.upper() + "     -----------------------"
        print "---------------------------------------------------------------------"
        pretty_print_performance(final_performances[ent.name], ent.labels)
        to_csv.append({'title': ent.name, 
            'data': np.mean(final_performances[ent.name], axis=0), 
            'labels': ent.labels,
            'accuracy':np.mean(final_accuracies[ent.name])})
        print "Accuracy: " + "{0:0.{1}f}".format(np.mean(final_accuracies[ent.name]), 4)
    print "=====================================================================\n"

    writer.write_final_performance(out_file, to_csv, meta={'features':features, 'limit': limit, 'outer_iterations':outer_iterations, 'iterations':iterations })

    end= time.clock()
    print "Using {} features:".format(limit)
    print "Ran {} rounds with {}-fold cross validation in {:.2f} seconds".format(outer_iterations, iterations, (end-start))
