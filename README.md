#Named Entity Recognition on Twitter
###CSCI 5622: Machine Learning Final Project

Jennings Anderson<br>
Mahnaz Roshenaei<br>
Kevin Stowe


##Command Line Use
Do one-aginst-all classification in parallel:

	$ python binary_learner.py

Or do multiclass clssification:

	$ python multiclass_learner.py

###Available Flags (set in the python file)
	limit       = 10000   #Limit of rows to load from the CSV
  	iterations  = 10      #Number of iterations for the cross validation
  	outer_iterations = 15 
	out_file = "./output/ngrams_texttype.csv" #Where to write the performance stats
	
	#Define the features to use:
	features = ['ngrams','word','texttype']

###Available Features
1. **word** - Simply the word as a feature
2. **ngrams** - The words at position ```+1,+2,-1,-2``` in context.
3. **texttype** - Syntactical details: capitalization, POS, etc.
4. **liwc** - Specific features from liwc as determined per class in the ```entities.py``` file.
5. **all_liwc** - Use all the liwc features for every class, not specific features (worse)



###Data
Annotated Tweets from various disasters: floods, hurricanes, tornadoes, etc.
