#Named Entity Recognition on Twitter
###Machine Learning Project


##Use
Do one-aginst-all classification in parallel:

  python binary_learner.py

Or do multiclass clssification:

  python multiclass_learner.py


##Available Features
  limit       = 10000  #Limit of rows to load from the CSV
    iterations  = 10     #Number of iterations for the cross validation
    outer_iterations = 15

    out_file = "./output/ngrams_texttype.csv"

    features = ['ngrams','word','texttype']


##Resources
1. [Google Drive](https://drive.google.com/a/colorado.edu/#folders/0BxQ6tqeOTfwBMzdXaVdxd3VSSlk)
2. [LIWC](http://liwc.net)
3. [Brendan O'Connor's pipelines for NLP on Twitter](http://brenocon.com/blog/2011/09/end-to-end-nlp-packages/)


###Entities in which we are interested:
 - Location
 - Person
 - Facility
 - Organization
 - Artifact

###Data
Annotated Tweets from various disasters: floods, hurricanes, tornadoes, etc.
