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
      key: '95119995'
      domain: 'Wildfire'
      disaster: 'Colorado Wildfires June 2012'
      {'text': 'Feel', 'features': [], 'annotations': ''}
      {'text': 'bad', 'features': [], 'annotations': ''}
      {'text': 'for', 'features': [], 'annotations': ''}
      {
        'text': 'reporter',
        'features': [],
        'annotations': 'Person'
      }
      {
        'text': 'trying',
        'features': [],
        'annotations': 'Person'
      }
      {
        'text': 'to',
        'features': [],
        'annotations': 'Person'
      }
      {
        'text': 'describe',
        'features': [],
        'annotations': 'Person'
      }
      {
        'text': 'evacuation', 'features': [], 'annotations': 'Person'
      }
      {'text': '/', 'features': [], 'annotations': ''}
      {'text': 'allowed', 'features': [], 'annotations': ''}
      {'text': 'back', 'features': [], 'annotations': ''}
      {'text': 'situation', 'features': [], 'annotations': ''}
      {'text': '.', 'features': [], 'annotations': ''}
      {'text': 'Gosh', 'features': [], 'annotations': ''}
      {'text': ',', 'features': [], 'annotations': ''}
      {
        'text': 'Colorado',
        'features': [],
        'annotations': 'Location Facility'
      }
      {
        'text': 'Springs',
        'features': [],
        'annotations': 'Location Facility'
      }
      {
        'text': 'roads',
        'features': [],
        'annotations': 'Facility'
      }
      {'text': 'are', 'features': [], 'annotations': ''}
      {'text': 'confusing', 'features': [], 'annotations': ''}
      {'text': '!', 'features': [], 'annotations': ''}
      {'text': '#', 'features': [], 'annotations': ''}
      {'text': 'WaldoCanyonFire', 'features': [], 'annotations': ''}
    }
