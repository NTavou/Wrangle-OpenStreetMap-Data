import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# We are following exactly the same procedure as in the audit_street_type.py
# script, but this time we will audit and update max speeds

osmfile = "liverpool_england.osm"
maxspeed_re = re.compile(r'\d+\s\S+')
maxspeeds = defaultdict(set)

expected_maxspeed = ["5 mph","10 mph", "15 mph", "20 mph", "25 mph", "30 mph", 
                    "35 mph", "40 mph", "45 mph", "50 mph", "55 mph", "60 mph", 
                    "65 mph", "70 mph"]
			
def audit_maxspeeds(maxspeeds, maxspeed):
    l = maxspeed_re.search(maxspeed)
    if l:
        maxspeed_found = l.group()
        if maxspeed_found not in expected_maxspeed:
        	maxspeeds[maxspeed_found].add(maxspeed)

def is_maxspeed(elem):
    return (elem.attrib['k'] == "maxspeed")

def audit_maxspeed():
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_maxspeed(tag):
                    audit_maxspeeds(maxspeeds, tag.attrib['v'])
    pprint.pprint(dict(maxspeeds))

max_speed_mapping = { 
                    '85 mph': '70 mph',
                    '90 mph': '70 mph'
    		          }
                      
def update_maxspeeds(name):
    for maxspeed in max_speed_mapping:
        if maxspeed in name:
            name = re.sub(maxspeed, max_speed_mapping[maxspeed], name)
    return name


if __name__ == '__main__':
    audit_maxspeed()