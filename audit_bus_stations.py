import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# We are following exactly the same procedure as in the audit_street_type.py
# script, but this time we will audit and update bus street types.

osmfile = "liverpool_england.osm"
bus_street_name_re = re.compile(r'\b\S+\.?$')
bus_street_names = defaultdict(set)

# We are going to use the same keyword letters in our expected dictionary as 
# in the audit_street_type.py
expected = ["Avenue", "Boulevard", "Close", "Court", "Crescent", "Drive", \
            "East", "Gardens", "Grove", "Lane", "Mews", "North", "Parade", \
            "Park", "Place", "Road", "South", "Square", "Street", "Terrace", \
            "View", "Village", "Walk", "Way"]


def audit_bus(bus_street_names, bus_street_name):
    p = bus_street_name_re.search(bus_street_name)
    if p:
        bus_full_name = p.group()
        if bus_full_name not in expected:
            bus_street_names[bus_full_name].add(bus_street_name)

def is_bus_street_name(elem):
    return (elem.attrib['k'] == "naptan:Street")

def audit_bus_street_names():
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_bus_street_name(tag):
                    audit_bus(bus_street_names, tag.attrib['v'])
    pprint.pprint(dict(bus_street_names))

# After running the audit_bus_street_names() function we clearly notice that the
# majority of bus street names data has been entered in capital letters in the
# OpenStreetMap dataset. So we need to fix this issue along with the unexpected 
# street enties that we found during our audit. As in the other audit scripts we
# will create a dictionary that keeps track of the changes needed to be done   
# to fix the unexpected bus street types.  

mapping_street_buses = {
                        "Hospita": "Hospital", 
                        "Lan": "Lane",
                        "Rd": "Road", 
                        "Sreet": "Street",
                        "Steet": "Street",
                        "St": "Street",
                        } 

def update_bus_street_names(name, mapping_street_buses):
    new_name = name.title()
    for bus in mapping_street_buses:
        if bus in new_name:
            new_name = re.sub(r'\b' + re.escape(bus) + r'$', mapping_street_buses[bus], new_name) 
    return new_name 

if __name__ == '__main__':
    audit_bus_street_names()