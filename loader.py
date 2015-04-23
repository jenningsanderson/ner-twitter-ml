import json

def load_json_tweets(file, limit=None):
    """
    Load the JSON file of tweets

    :param file:  The location of the json file as a string
    :param limit: Only return the first <n> tweets
    """
    tweets = []

    i = 0
    for id, tweet in json.load( open(file) ).iteritems():
        if i<limit or limit==None:
            tweets.append(tweet)
            i+=1

    return tweets

def tweet_to_vectors(tweet):
    x = []
    y = []
   
    for w in tweet['words']:
        if w['annotations']:
            x.append(w['text'])
            y.append(w['annotations'])
    return x,y


if __name__ == '__main__':
    tweets = load_json_tweets('data/tweets.json', limit=10)
    print "Loaded %d Tweets" %( len(tweets) )

    x = [] 
    y = []

    for tweet in tweets:
        (a,b) = tweet_to_vectors(tweet)
        x += a
        y += b

    



