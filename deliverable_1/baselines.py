import sys
sys.path.append( '..' )

from loader import * #Import the helper load functions

if __name__ == '__main__':
    x = load_json_tweets('../tweets.json', 100)
    print "Loaded %d Tweets" %( len(x) )
