import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# We are following exactly the same procedure as in the audit_street_type.py
# script, but this time we will audit and update city names

osmfile = "liverpool_england.osm"
city_name_re = re.compile(r'\b\S+')
city_names = defaultdict(set)

expected_city_name = ["Liverpool"]
			
def audit_city_names(city_names, city):
    k = city_name_re.search(city)
    if k:
        city_name = k.group()
        if city_name not in expected_city_name:
        	city_names[city_name].add(city)

def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")

def audit_city():
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    audit_city_names(city_names, tag.attrib['v'])
    pprint.pprint(dict(city_names))

city_name_mapping = {
                    "Balliol road": "Bootle", 
                    "Liverpol": "Liverpool", 
                    "prescot": "Prescot"
                    }
                      
def update_city_names(name):
    for city in city_name_mapping:
        if city in name:
            name = re.sub(city, city_name_mapping[city], name)
    return name


if __name__ == '__main__':
    audit_city()
