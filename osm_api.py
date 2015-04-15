# To help resolve place issues, this will hit OSM
# and learn more about the data
#
import overpy

api = overpy.Overpass()

query_string = '''way(50.746,7.154,50.748,7.157) ["highway"];
    (._;>;);
    out body;'''

query_2 = """way["name"="Highway 6"];out body;"""

# fetch all ways and nodes
result = api.query(query_2)

print "Ways: %d" %(len(result.ways))
print "Nodes: %d" %(len(result.nodes))
print "Relations: %d" %(len(result.relations))


for way in result.ways[0:10]:
    print("Name: %s" % way.tags.get("name", "n/a"))
    print("Tags: %s" % way.tags)