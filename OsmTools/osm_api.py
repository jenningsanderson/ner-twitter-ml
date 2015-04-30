# To help resolve place issues, this will hit OSM
# and learn more about the data
#
import overpy
import string

api = ""
usa_bounds = ["18.911720", "-179.150558", "71.441048", "-66.940643"]

def getWays(query_string):
    def sterilize(s):
        data = s.split()
        result = [""]*len(data)
        for i in range(len(data)):
            if ispunct(data[i]):
                result[i] = ""
            else:
                result[i] = data[i]
        return " ".join(result).strip()

    def ispunct(s):
        return all(c in string.punctuation for c in s)

    global api
    if not api:
        print "LOADING API..."
        api = overpy.Overpass()
    #query_string = '''way(50.746,7.154,50.748,7.157) ["highway"];
    #    (._;>;);
    #    out body;'''
    size = len(query_string.split())
    query_string = sterilize(query_string)
    if query_string and len(query_string.split()) >= size:
        query_string = "way[\"name\"=\"" + query_string + "\"](" + ",".join(usa_bounds) + ");out body;"

        result = api.query(query_string)
        data = {}
        if len(result.ways) > 5:
            for way in result.ways[0:25]:
                for tag in way.tags:
                    if tag not in data:
                        data[tag] = 1
                    else:
                        data[tag] += 1

            if len(result.nodes) > 0 or len(result.relations) > 0 :
                print result.nodes
                print result.relations
                sys.exit()

        return (data)
        '''
        for way in result.ways[0:10]:
            print("Name: %s" % way.tags.get("name", "n/a"))
            print("Tags: %s" % way.tags)
        '''
    else:
        return ({})
