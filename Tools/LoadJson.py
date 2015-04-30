import sys
import getopt
import json

import Tools
import Features

features = [Features.liwc]

def add_features(tweets):
    for f in features:
        f(tweets)

#Main method as suggested by van Rossum, simplified
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:], "h", ["help"])
    except:
        print "Error in args : " + str(argv[1:])
        return 2

    #Use opts and args here
    # ....
    tweets = json.load(open(args[0]))
    
    add_features(tweets)

if __name__ == "__main__":
    sys.exit(main())
