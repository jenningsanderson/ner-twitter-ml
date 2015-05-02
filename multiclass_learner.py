#
#
# This will use the logic from binary_learner and combine them all into a binary learner
#
#

clf_artifact = svm.LinearSVC(C=C[k]) # for all (nlp+metadata) features 
clf_artifact.fit(X_train_artifact, Y_train_artifact)
predictions_artifact = clf_artifact.predict(X_valid_artifact)          


# This part create a probability as input + y-label : 

dis_fun= clf_artifact.decision_function(X_train_artifact[0])[0]
            probs_train_artifact = [1/(1+math.exp(-dis_fun[0])), 1/(1+math.exp(-dis_fun[1])), 1/(1+math.exp(-dis_fun[2]))]
            for i in range(1,len(Y_train_artifact)):
                dis_fun= clf_artifact.decision_function(X_train_artifact[i])[0]
                probs_train_artifact= numpy.vstack((probs_train_artifact,[1/(1+math.exp(-dis_fun[0])), 1/(1+math.exp(-dis_fun[1])), 1/(1+math.exp(-dis_fun[2]))]))


# then add all these output together : 
X_probs_train = numpy.hstack((probs_train_artifact,probs_train_person,...))
Y_train = numpy.hstack((Y_train_artifact,Y_train_person,...))