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
<table>
  <tr><td>Word</td><td>Gold Tag</td><td>Pred Tag</td></tr>
  <tr><td>The</td><td>Location</td><td></td></tr>
  <tr><td>entire</td><td>Location</td><td></td></tr>
  <tr><td>state</td><td>Location</td><td></td></tr>
  <tr><td>of</td><td>Location</td><td></td></tr>
  <tr><td>Colorado</td><td>Location</td><td>Location</td></tr>
  <tr><td>is</td><td></td><td></td></tr>
  <tr><td>on</td><td></td><td></td></tr>
  <tr><td>fire</td><td></td><td></td></tr>
  <tr><td>right</td><td></td><td></td></tr>
  <tr><td>now</td><td></td><td></td></tr>
  <tr><td>.</td><td></td><td></td></tr>
  <tr><td>CNN</td><td>Organization</td><td>Organization</td></tr>
  <tr><td>is</td><td></td><td></td></tr>
  <tr><td>playing</td><td></td><td></td></tr>
  <tr><td>an</td><td></td><td></td></tr>
  <tr><td>Amy</td><td>Person</td><td>Person</td></tr>
  <tr><td>Winehouse</td><td>Person</td><td>Person</td></tr>
  <tr><td>story</td><td></td><td></td></tr>
</table>

If the predicted annotation only marks "Colorado" as Loc, it counts the entire span "The entire state of Colorado" as correct. In the above data, this sentence would have 3 total spans, and 3 spans correct. Exact spans are much harder to match.

<b>Partial Match</b><br>
CRF Model with all features, with results sorted by entity type
![alt text](https://github.com/jenningsanderson/ner-twitter-ml/blob/master/deliverable_1/caps_summary.png "caps by entity, partial match")

CRF Model with all features, with results sorted by disaster type
![alt text](https://github.com/jenningsanderson/ner-twitter-ml/blob/master/deliverable_1/caps_by_domain.png "caps by domain, partial match")

<b>Exact Match</b><br>
CRF Model with all features, with results sorted by entity type
![alt text](https://github.com/jenningsanderson/ner-twitter-ml/blob/master/deliverable_1/caps_entity_exact.png "caps by entity, exact match")

CRF Model with all features, with results sorted by disaster type
![alt text](https://github.com/jenningsanderson/ner-twitter-ml/blob/master/deliverable_1/caps_domain_exact.png "caps by domain, exact match\
")

