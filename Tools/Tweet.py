import re
import string
import sys

from sets import Set

import FixCharacters

chars = r""+string.letters + "_0-9"
web_punct = r"([^" + chars + "/])+"
punct = r"([^" + chars + "]+)"
not_punct = r"([" + chars + "]+)"

data_domains = {
    "redriver09":("Red River 2009", "Flood"), "redriver10":("Red River 2010", "Flood"),
    "sandy_":("Hurricane Sandy User Streams", "Hurricane"), "HurricaneSandy":("Hurricane Sandy Random Tweets", "Hurricane"),
    "ColoradoWildFiresJune2012":("Colorado Wildfires June 2012", "Wildfire"), "HighParkFire":("High Park Fire", "Wildfire"), "LowerNorthForthFire":("Lower North Fork Fire", "Wildfire"), "NewMexicoFireJune2012":("New Mexico Fire June 2012", "Wildfire"), "okFiresSamplesForAnnot":("Oklahoma Fire", "Wildfire"),
    "DallasTornadoApril2012":("Dallas Tornado April 2012", "Tornado"),
    "haiti_curated":("Haiti Earthquake", "Earthquake"), "nz_sa_tweets_":("New Zealand Earthquake", "Earthquake"),
    "WinterStormNemo":("Winter Storm Nemo", "Blizzard")
    }

used_keys = []

class Tweet(object):
    def __init__(self, text, span_start, span_end, tweet_file, user="", populate_id=True, populate_words=True, populate_disaster_info=True):
        self.text = text
        self.span_start = span_start
        self.span_end = span_end
        self.tweet_file = tweet_file
        self.user = ""

        if populate_id:
            self.populate_tweet_id()
        if populate_words:
            self.populate_words()
        else:
            self.words = []
        if populate_disaster_info:
            self.populate_disaster_info()
        self.fix_text()

    def __str__(self):
        return self.text + " " + " ".join([str(w) for w in self.words])

    def __eq__(self, other):
        return self.tweet_id == other.tweet_id

    def __hash__(self):
        return hash(self.tweet_id)

    def populate_words(self):
        start = 0
        self.words = []
        for w in self.text.split():
            for token in tokenize(w).split():
                token = FixCharacters.fix_characters(token)
                length = len(token)

                if len(token.strip()) >= 1:
                    word = Word(token, start, start+length)
                    self.words.append(word)
                start += length
            start += 1
        self.fix_text()

    def fix_text(self):
        self.text = " ".join([w.text for w in self.words])

    def populate_disaster_info(self):
        for key in data_domains:
            if re.match(key, self.tweet_file.split("/")[-1]):
                self.disaster = data_domains[key][0]
                self.domain = data_domains[key][1]

    def populate_tweet_id(self):
        if re.match("^[0-9]{6,},.+", self.text):
            self.tweet_id = self.text.split(",")[0]
        elif re.match("^[0-9]{6,}[\s].+", self.text):
            self.tweet_id = self.text.split()[0]
        elif re.match("^.+[\s][0-9]{6,}$", self.text):
            self.tweet_id = self.text.split()[-1]
        elif re.match("^No_ID_[0-9]+.+$", self.text):
            self.tweet_id = self.text.split()[0]
        else:
            print self.text
            self.tweet_id = "No_ID_" + str(next_key())

    def to_crf_string(self, add_features=False, header=False, tag=None):
        result = ""
        part_1 = []
        part_2 = []
        part_3 = []
        for i in range(len(self.words)):
            word = self.words[i]
            part_1 = [word.text]
            if add_features:
                part_2 = word.features
            if tag:
                if "I-" + tag in word.annotations:
                    part_3 = ["I-" + tag]
                    if "O-none" in self.words[i-1].annotations:
                        print self.words
                        sys.exit()
                elif "B-" + tag in word.annotations:
                    part_3 = ["B-" + tag]
                else:
                    part_3 = ["O-none"]
            result += " ".join(part_1 + part_2 + part_3) + "\n"
        result += "\n"

#        print result

        return result

class Word(object):
    def __init__(self, text, span_start, span_end):
        self.text = text
        self.span_start = span_start
        self.span_end = span_end
        self.annotations = Set()
        self.features = []

    def __lt__(self, other):
        return self.span_start < other.span_start

    def __eq__(self, other):
        return (self.text == other.text and self.span_start == other.span_start and self.span_end == other.span_end and self.annotations == other.annotations)

    def __str__(self):
        return str(self.text) + " " + str(self.span_start) + " " + str(self.span_end) + " " + str(self.annotations) + " " + str(self.features)

    def add_annotation(self, tag):
        self.annotations.add(tag)

    def add_feature(self, feature):
        self.features.append(feature)

    def binarize_features(self):
        new_features = []
        for f in self.features:
            if f == 0:
                new_features.append(0)
            elif f > 0:
                new_features.append(1)
            else:
                print "CAN'T HAEVE NEGATIVE FEATURES : " + str(self.features)
                sys.exit(5)
    
class Annotation(object):
    ann_id = ""
    span_start = ""
    span_end = ""
    span_text = ""
    entity_type = ""
    source_file = ""

    tokens = []

    def get_tokens(self):
        if self.tokens == []:
            self.tokens = tokenize(self.span_text).split()
        return self.tokens

    def __str__(self):
        try:
            return self.source_file + " " + self.ann_id +" "+ str(self.span_start) + " " + str(self.span_end) + " " + self.span_text.decode("UTF-8") + " " + self.entity_type
        except :
            print "String can't be encoded..."

    def __lt__(self, other):
        return self.span_start < other.span_start

    def __eq__(self, other):
        if self.span_start == other.span_start and self.span_end == other.span_end and self.span_text == other.span_text:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.span_start, self.span_end, self.span_text))

def next_key():
    for i in range(200000):
        if i not in used_keys:
            used_keys.append(i)
            return i

def tokenize(word):
    word = word.strip()
    if len(word) < 1:
        return ""
    elif re.match(punct+"+$", word):
        return word
    elif "http:" in word or "www." in word or "https:" in word or ("http" in word and "//" in word):
        prefix_punct = ""
        suffix_punct = ""

        while re.match(web_punct, word[0]):
            prefix_punct += word[0]
            word = word[1:]
        while re.match(web_punct, word[-1]):
            suffix_punct += word[-1]
            word = word[:-1]
        result_word = prefix_punct + " " + word + " " + suffix_punct
        return result_word.strip()
    else:
        new_word = ""
        result = re.findall(not_punct + "|" + punct, word)

        for data in result:
            new_word += data[0] + data[1] + " "
        return new_word[:-1]
