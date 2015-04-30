import sys
import csv
import json

reader = csv.reader(open("LIWC2001 Results_6class.csv"))

liwc_dict = {}

count = 0
for line in reader:
    if line[0] != "Filename":
        word = line[-7].lower()
        features = line[5:-8]
        if word not in liwc_dict.keys():
            liwc_dict[word] = features

            
json.dump(liwc_dict, open("liwc_dict.json", "w"))
