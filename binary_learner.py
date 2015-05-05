import loader as loader
import writer as writer
from entity import *
from learner import Entity, pretty_print_performance
import threading, time
import numpy as np

if __name__ == "__main__":
    start = time.clock()

    limit               = None  #Limit of rows to load from the CSV
    iterations          = 10     #Number of iterations for the cross validation
    outer_iterations    = 1
    use_test_data       = False
    out_file            = "./output/not_limiting_nones.csv"

    features            = ['ngrams','word','texttype','liwc']



    words = loader.load_csv_tweets('./data/LIWC2001 Results_5class_new.csv', limit=limit)

    #Defaults
    args = {'all_data'           : words, 
            'iterations'         : iterations, 
            'build_and_separate' : True,
            'limitNones'         : True,
            'test_set'           : False, 
            'makeTest'           : True}



    if use_test_data:
        test_data = loader.load_csv_tweets('./data/test_set.csv', limit=limit)
        test_args = {'all_data'  : test_data, 
            'iterations'         : iterations, 
            'build_and_separate' : True,
            'limitNones'         : True,
            'test_set'           : False, 
            'makeTest'           : False}
        args['makeTest'] = False


    #Logging
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
            t = threading.Thread(target=task, args=(args,))
            t.start()
            t.join()

        
        #Are we using test data?
        if use_test_data:
            import_test_tasks = [ent.import_full_feature for ent in entities]
            for task in import_test_tasks:
                t = threading.Thread(target=task, args=(test_args,))
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
