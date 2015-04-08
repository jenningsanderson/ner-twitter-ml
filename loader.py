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

if __name__ == '__main__':
    x = load_json_tweets('tweets.json')
    print "Loaded %d Tweets" %( len(x) )
