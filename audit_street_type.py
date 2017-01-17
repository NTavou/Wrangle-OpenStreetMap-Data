import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

osmfile = "liverpool_england.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

# We create a list with the street types that we expect to see in our dataset
expected = ["Avenue", "Boulevard", "Close", "Court", "Crescent", "Drive", \
			"East", "Gardens", "Grove", "Lane", "Mews", "North", "Parade", \
			"Park", "Place", "Road", "South", "Square", "Street", "Terrace", \
			"View", "Village", "Walk", "Way"]
			

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
        	street_types[street_type].add(street_name)

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
# to fix the unexpected street types 
mapping = {
    		"Blvd": "Boulevard", 
    		"Road, ": "Road", 
    		"road": "Road",
    		"St": "Street", 
    		"VIllage": "Village"
    		}

# Now its time to create the function that will fix the erroneous street types.
# We will use it along with the mapping dictionary in the data.py script to
# create the final dictionaries that would be used to write the appropriate
# .csv files.
def update_street_type(name):
    for street_type in mapping:
        if street_type in name:
            name = re.sub(r'(?!Street)'+ street_type, mapping[street_type], name)
    return name


if __name__ == '__main__':
    audit()