import osm_api
import overpy
import cPickle
import json

data = cPickle.load(open("sample_tweets.p"))

osm_dict = {}
count = 0

for tweet_key in data.keys():
    count += 1
    print str(count) + " of " + str(len(data.keys()))
    if count % 100 == 0:
        sys.exit()
                                      
    tweet = data[tweet_key]
    for i in range(0,len(tweet.words)):
        if tweet.words[i] not in osm_dict:
            ways = osm_api.getWays(tweet.words[i].text)
            if ways:
                osm_dict[tweet.words[i].text] = [w for w in ways if ways[w] >= 5]
json.dump(osm_dict, open("osm_dict.json", "w"))
#        print tweet.words[i].text + " " + str(len(ways)) + " " + str(len(nodes)) + " " + str(len(relations))
#    for i in range(1, len(tweet.words)):
#        ways,nodes,relations = osm_api.getWays(tweet.words[i-1].text + " " + tweet.words[i].text)
#        print tweet.words[i].text + " : " + str(len(ways)) + " " + str(len(nodes)) + " " + str(len(relations))
