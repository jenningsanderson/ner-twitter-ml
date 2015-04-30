import json
import operator

data = json.load(open("feature_weights.json"))

totals = {}

all_lists = [data[i] for i in data.keys()]

abs_totals = [abs(a)+abs(b)+abs(c)+abs(d)+abs(e) for a,b,c,d,e in zip(all_lists[0], all_lists[1], all_lists[2], all_lists[3], all_lists[4])]

sorted_abs = sorted(range(len(abs_totals)), key=lambda k:abs_totals[k], reverse=True)


'''    
for key in data:    
    for i in range(len(data[key])):
        if i not in totals.keys():
            totals[i] = data[key][i]
        else:
            totals[i] += data[key][i]
'''
#sorted_x = sorted(totals.items(), key=operator.itemgetter(1))
print ", ".join([str(x) for x in sorted_abs[0:20]])
    
