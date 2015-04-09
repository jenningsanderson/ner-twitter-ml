#Named Entity Recognition on Twitter
###Machine Learning Project

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

####Example Data Structure of tweets.json
{
key: u'95119995'
domain: u'Wildfire'
disaster: u'Colorado Wildfires June 2012'
{u'text': u'Feel', u'features': [], u'annotations': u''}
{u'text': u'bad', u'features': [], u'annotations': u''}
{u'text': u'for', u'features': [], u'annotations': u''}
{u'text': u'reporter', u'features': [], u'annotations': u'Person'}
{u'text': u'trying', u'features': [], u'annotations': u'Person'}
{u'text': u'to', u'features': [], u'annotations': u'Person'}
{u'text': u'describe', u'features': [], u'annotations': u'Person'}
{u'text': u'evacuation', u'features': [], u'annotations': u'Person'}
{u'text': u'/', u'features': [], u'annotations': u''}
{u'text': u'allowed', u'features': [], u'annotations': u''}
{u'text': u'back', u'features': [], u'annotations': u''}
{u'text': u'situation', u'features': [], u'annotations': u''}
{u'text': u'.', u'features': [], u'annotations': u''}
{u'text': u'Gosh', u'features': [], u'annotations': u''}
{u'text': u',', u'features': [], u'annotations': u''}
{u'text': u'Colorado', u'features': [], u'annotations': u'Location Facility'}
{u'text': u'Springs', u'features': [], u'annotations': u'Location Facility'}
{u'text': u'roads', u'features': [], u'annotations': u'Facility'}
{u'text': u'are', u'features': [], u'annotations': u''}
{u'text': u'confusing', u'features': [], u'annotations': u''}
{u'text': u'!', u'features': [], u'annotations': u''}
{u'text': u'#', u'features': [], u'annotations': u''}
{u'text': u'WaldoCanyonFire', u'features': [], u'annotations': u''}
}