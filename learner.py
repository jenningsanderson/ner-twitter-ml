from csv import DictReader, DictWriter

import numpy as np
from numpy import array

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier

#NLTK:
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

import re
import random



# 1. Vectorize our data
#
# 2. Run an SVM?
#
# 3. Check accuracy?

class Analyzer:
    def __init__(self, name):
        print "Initialized an Analyzer named: %s" %(name) #Just trying to remember how Python works
        print "Using English Stop words"
        self.stop_words = stopwords.words('english')

        #Add stop words specific to these documents.
        self.stop_words += ['points', 'name', 'ftp', 'pointsname', 'ten', 'fifteen']
        print "Number of Stop Words: %d" %( len(self.stop_words) )

        #Create a stemmer
        # self.stemmer = SnowballStemmer("english") #The PorterStemmer is better...
        print "Initializing a Porter Stemmer"
        self.stemmer = PorterStemmer()
        
    def __call__(self, text):
 
        #Keep numbers, words, and apostrophes
        all_words = re.findall("[a-zA-Z0-9\'\.]+", text)
        
        #Filter out all stop words
        words = [word for word in all_words if word.lower() not in self.stop_words]

        #Stem the words
        stemmed_words = [self.stemmer.stem(word) for word in words]

        #Learn about numbers in the sentences and then yield a more specific term
        for word in stemmed_words:
            if re.match("\d+$", word):
                year = int(word)
                if year > 100:
                    if year < 2000:
                        yield "numbers:old"
                    else:
                        yield "numbers:current"

            elif re.match("\d+\.\d+$", word):
                yield "numbers:float"
            elif re.match("\d+\.\d+[x]", word):
                yield "numbers:scientific"
            elif re.match("\d+\.\d+[A-z]", word):
                yield "numbers:different"
            # #Else, just yield the stemmed word
            else:
                yield word
      
        # #Store the length for quicker calculation
        num_words = len(words)

        #Yield both bigrams and trigrams with the original words
        for i in range(num_words):    
            if i<num_words-1:
                yield words[i]+"_"+words[i+1]

                if i<num_words-2:
                    yield words[i]+"_"+words[i+1]+"_"+words[i+2]



class Featurizer:
    def __init__(self, analyzer):
        self.vectorizer = CountVectorizer(
            analyzer=analyzer,
            max_features=2500000
            )

    def train_feature(self, examples):
        return self.vectorizer.fit_transform(examples)

    def test_feature(self, examples):
        return self.vectorizer.transform(examples)


    def show_top10(self, classifier, categories):
        feature_names = np.asarray(self.vectorizer.get_feature_names())
        for i, category in enumerate(categories):
            top10 = np.argsort(classifier.coef_[i])[-10:]
            print("%s: %s" % (category, " ".join(feature_names[top10])))

if __name__ == "__main__":


    analyzer = Analyzer('Descriptive Numbers, Stems, Bigrams & Trigrams')
    feat = Featurizer(analyzer=analyzer)

    x_train = feat.train_feature(x['text'] for x in train)
    x_test = feat.test_feature(x['text'] for x in test)

    print "Number of Features: %d" %(len(feat.vectorizer.get_feature_names()))

    y_train = array(list(labels.index(x['cat']) for x in train))


    # Train classifier
    lr = SGDClassifier(loss='log', penalty='l2', shuffle=True)
    lr.fit(x_train, y_train)

    # Show Top 10
    feat.show_top10(lr, labels)

    #Write out Predictions
    predictions = lr.predict(x_test)
    o = DictWriter(open("predictions.csv", 'w'), ["id", "cat"])
    o.writeheader()
    for ii, pp in zip([x['id'] for x in test], predictions):
        d = {'id': ii, 'cat': labels[pp]}
        o.writerow(d)


    #How about also printing out the training data...
    # Cast to list to keep it all in memory
    all_data = list(DictReader(open("train.csv", 'r')))
    
    #Shuffle the data so we don't get ordering affects, but perhaps we should use a seed?
    random.shuffle(all_data)

    #Train is the first 1000, test is the next 1200
    fake_test  = all_data[40001:50000]

    #Create a test_y_values set:
    test_y_values = {}
    # test_sentences = {}
    for row in fake_test:
        test_y_values[row['id']] = row['cat']
        # test_sentences[row['id']] = row['text']

    #Now actually run it on the data:
    x_test2 = feat.test_feature(x['text'] for x in fake_test)
    predictions2 = lr.predict(x_test2)
    correct = 0.0
    total   = 0.0
    for ii, pp in zip( [x['id'] for x in fake_test], predictions2):
        # print "Predicted", {'id': ii, 'cat': labels[pp]}
        # print "Actual:",   {'id': ii, 'cat': test_y_values[ii]}
        if labels[pp] == test_y_values[ii]:
            correct += 1
        # else:
        #     print labels[pp] + "||" + test_y_values[ii]
        #     print test_sentences[ii]
        #     print "================"

        total += 1.0
    print "Rate: %f" %(correct/total)