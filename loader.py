import json

def load_json_tweets(file, limit=None):
    """
    Load the JSON file of tweets

    :param file:  The location of the json file as a string
    :param limit: Only return the first <n> tweets
    """
    tweets = []

    print "Loading tweets from {0} with limit: {1}".format(file, limit)

    i = 0
    for id, tweet in json.load( open(file) ).iteritems():
        if i<limit or limit==None:
            tweets.append(tweet)
            i+=1

    return tweets


# UPDATE THIS TO INCLUDE NONE VALUES
def tweet_to_vectors(tweet, entity='Location'):
    """
    :param tweet: A tweet in JSON as read from tweets.json

    :returns an array of hashes: {word, annotation}
    """

    labeled = []

    for w in tweet['words']:
        if entity in w['annotations'].split(' '):
            labeled.append( {'text': w['text'], 'label': entity } )
        else:
            labeled.append( {'text': w['text'], 'label': "None" })

    return labeled


if __name__ == '__main__':
    tweets = load_json_tweets('data/tweets.json', limit=10)
    print "Loaded %d Tweets" %( len(tweets) )

    vals = []

    for tweet in tweets:
        vals += tweet_to_vectors(tweet)

    print vals
