import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# This script checks for incosistent and erroneous street types in the Liverpool
# openstreet map
osmfile = "liverpool_england.osm"
street_type_re = re.compile(r'\b\S+\.?$')
street_types = defaultdict(set)

# We create a list with the street types that we expect to see in our dataset
expected = ["Avenue", "Boulevard", "Close", "Court", "Crescent", "Drive", \
			"East", "Gardens", "Grove", "Lane", "Mews", "North", "Parade", \
			"Park", "Place", "Road", "South", "Square", "Street", "Terrace", \
			"View"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           , "Village", "Walk", "Way"]
			
# We create a function that will audit for non expected street types
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
        	street_types[street_type].add(street_name)

# We define which element attrib our script will audit
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit():
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                	# We audit the data to check if there are street types 
                	# that aren't present in the expected list 
                    audit_street_type(street_types, tag.attrib['v'])
                    # Then we print the results in order to identify 
                    # potential unexpected street types in the dataset.
    pprint.pprint(dict(street_types))


# We create a dictionary that keeps track of the changes needed to be done   
# to fix the unexpected street types. 
mapping = {
    		"Blvd": "Boulevard", 
    		"road": "Road",
    		"St": "Street", 
            }

# Now its time to create the function that will fix the erroneous street types.
# We will use it in the data.py script to create the final dictionaries that would 
# be used to write the appropriate .csv files. Before doing this we will also use 
# the title method to modify any capitalize street type.
def update_street_type(name, mapping):
    new_name = name.title()
    for street_type in mapping:
        if street_type in new_name:
            # Matching and replacing the unexpected street types. This regex will replace
            # the erroneous street type only if it is at the end of the street name
            # (as it is expected with street types).
            new_name = re.sub(r'\b' + re.escape(street_type) + r'$', mapping[street_type], new_name)
    return new_name


if __name__ == '__main__':
    audit()