import sys
sys.path.append( '..' )

from loader import *

if __name__ == '__main__':
    x = load_json_tweets('../tweets.json', 100)
    print "Loaded %d Tweets" %( len(x) )
