Deliverable 1
=============

First Deliverable (April 10, 2015)

###Goals
1. Establish a Baseline
2. Use LIWC to create new features for classification


###Results
Two different baselines are presented for named entity recognition. One is a Conditional Random Field (CRF) model, trained and tested using 5-fold cross validation. The other is the "distantly supervised" model provided by Ritter 2010.

CRF Model
The baseline CRF model uses very basic features.
Lexical : the word itself is used as a feature
Context : two words before and two words after are also features
Capitalization : whether the word is capitalized is split into a quadrary feature. The classes are no caps, initial caps, all caps, and mixed caps

The results reported are for randomized 5-fold cross validation.
Precision : For each instance predicted as a named entity, was that entity actually a named entity.
Recall : For each instance that is actual a named entity, was it predicted as a named entity.
F1 : Harmonic mean of Precision and Recall

The evaluations done here were based on partial matches. That is, if any word in an entity span was tagged correctly, the entire span is marked correct. For example, if the sentence is :

Word		Gold Tag       Pred Tag
The 		Loc<br>
entire		Loc<br>
state		Loc<br>
of		Loc<br>
Colorado	Loc		Loc<br>
is<br>
on<br>
fire<br>
right<br>
now<br>
.<br>
CNN		Org		Org<br>
is<br>
playing<br>
an<br>
Amy		Per		Per<br>
winehouse	Per		Per<br>
story<br>

If the predicted annotation only marks "Colorado" as Loc, it counts the entire span "The entire state of Colorado" as correct. In the above data, this sentence would have 3 total spans, and 3 spans correct. Exact spans are much harder to match.

![alt text](https://github.com/jenningsanderson/ner-twitter-ml/blob/master/deliverable_1/caps_by_domain.png "caps by domain, partial match")