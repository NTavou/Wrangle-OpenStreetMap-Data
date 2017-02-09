import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# We are following the same procedure as in the audit_street_type.py
# script, but this time we will audit and update amenities. The only difference
# with the audit_street_type.py script is that we won't use the title method
# because the amenities names are found in lowercase letters in the OpenStreetMap
# dataset.

osmfile = "liverpool_england.osm"
amenity_re = re.compile(r'\S+(\s\S+)*')
amenities = defaultdict(set)

expected_amenities = ["ambulance_station", "arts_center", "atm", "bank", "bar",
                        "beauty salon", "bowling club", "bus_station", "cafe",
                        "car_rental", "casino", "cinema","club", "club_house", 
                        "college","dentist", "doctors", "fast_food",
                        "fire_station", "fuel", "hospital", "nightclub", "park", 
                        "pharmacy", "police", "post_office", "pub", 
                        "restaurant", "school", "taxi", "telephone", "taxi", 
                        "theatre", "university"]

			
def audit_amenities(amenities, amenity_name):
    n = amenity_re.search(amenity_name)
    if n:
        amenity_found = n.group()
        if amenity_found not in expected_amenities:
        	amenities[amenity_found].add(amenity_name)

def is_amenity(elem):
    return (elem.attrib['k'] == "amenity")

def audit_amenity():
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_amenity(tag):
                    audit_amenities(amenities, tag.attrib['v'])
    pprint.pprint(dict(amenities))

amenity_mapping = {
                    "clubhouse": "club_house", 
                    "Fish and Ships": "restaurant",
                    "police; council": "police" 
    		      }
                      
def update_amenity(name, amenity_mapping):
    for amenity in amenity_mapping:
        if amenity in name:
            name = re.sub(r'\b' + re.escape(amenity), amenity_mapping[amenity], name)
    return name


if __name__ == '__main__':
    audit_amenity()