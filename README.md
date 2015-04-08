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

####Example Data Structure
```tweets.json```:
	
	["94537339",
	 {"tweet_id"=>"94537339",
	  "domain"=>"Wildfire",
	  "disaster"=>"Colorado Wildfires June 2012",
	  "words"=>
	   [["The", "Location"],
	    ["entire", "Location"],
	    ["state", "Location"],
	    ["of", "Location"],
	    ["Colorado", "Location"],
	    ["is", ""],
	    ["on", ""],
	    ["fire", ""],
	    ["right", ""],
	    ["now", ""],
	    [".", ""],
	    ["CNN", "Organization"],
	    ["is", ""],
	    ["playing", ""],
	    ["an", ""],
	    ["Amy", ""],
	    ["Winehouse", ""],
	    ["story", ""],
	    [".", ""],
	    ["#", ""],
	    ["WaldoCanyonFire", ""]],
	  "text"=>
	   "The entire state of Colorado is on fire right now . CNN is playing an Amy Winehouse story . # WaldoCanyonFire"}]
