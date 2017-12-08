# Wrangle OpenStreetMap Data

## Map Area

[Liverpool, England, Uk](https://en.wikipedia.org/wiki/Liverpool)

[https://mapzen.com/data/metro-extracts/metro/liverpool_england/](https://mapzen.com/data/metro-extracts/metro/liverpool_england/)

I completed my postgraduate studies in the UK, so this project is a good chance to explore the hometown 
of Beatles and Liverpool FC. 

## Methodology

As a first step in exploring the data, I ran the [audit_street_type.py](/audit_street_type.py) script against the 300 MB Liverpool OpenStreetMap dataset. The output of the script revealed that some street type addresses needed to be fixed. I modified the script to tackle with these issues. The same approach was used with the other audit scripts that were created to copy with issues found in bus stations street names and amenity types. 

Then I revised the [data.py](/data.py) script by importing the update functions into it. I created a small sample of the dataset with the [sample_region.py](/sample_region.py) and I tested the data.py against this sample. As long as the data.py produced the desired results in the csv samples, I proceed and ran the script against the whole Liverpool dataset to create the appropiate csv files.

In the last step of this project I imported the csv files into the SQL using the [data_wrangling_schema.sql](/data_wrangling_schema.sql) and I ran several queries to provide a statistical overview of the dataset.

## Problems Encountered in the Map

### Incosistent Street Names

As noted above the initial audit revealed some incosistencies in the street type addresses. More specifically: 

	<tag k="addr:street" v="International Business Park, Estuary Blvd"/>
	<tag k="addr:street" v="Overton St"/> 
	<tag k="addr:street" v="Allerton road"/>

For example the first element has the street type *Blvd* which I changed to Boulevard in order to be consisent with other boulevard names found in the dataset. The same method was applied to the next  two elements which have *St* and *road* as street types, which I modifiied them to Street and Road. Before doing this I also modified any capitalized street names in the appropriate form. For example in this tag:....

	<tag k="addr:street" v="Wallasey VIllage"/>
	
.....*VIllage* was modified to Village before writing it into the csv.

 Below is a part of the [audit_street_type.py](/audit_street_type.py) script that deals with these issues:

	street_type_re = re.compile(r'\b\S+\.?$')
	
	def is_street_name(elem):
   	    return (elem.attrib['k'] == "addr:street")
	
	mapping = {
	    		"Blvd": "Boulevard", 
	    		"road": "Road",
	    		"St": "Street" 
	          }
	
	def update_street_type(name, mapping):
	    new_name = name.title()
	    for street_type in mapping:
	        if street_type in new_name:
	            # Matching and replacing the unexpected street types. This regex will replace
	            # the erroneous street type only if it is at the end of the street name
	            # (as it is expected with street types).
	            new_name = re.sub(r'\b' + re.escape(street_type) + r'$', mapping[street_type], new_name)
	    return new_name
	    
### Incosistent and Incorrect Bus Station Street Names
	    
In [this OpenStreetMap wiki article](http://wiki.openstreetmap.org/wiki/NaPTAN) we are informed that "NaPTAN and NPTG are UK official datasets for bus stops and places which the UK Department for Transport and Traveline have offered to make available to OpenStreetMap project". I checked the bus stations street names and I found that the majority of bus stations street names where imported into the dataset in capital letters and that some street types were incosistent. For example: 

	<tag k="naptan:Street" v="BROADGREEN HOSPITA"/>
	<tag k="naptan:Street" v="ENDBUTT LAN"/>

So I followed the same procedure as in the incosistent street names section to fix the incosistent and incorrect bus station names (the code that follows is part of the [audit_bus_stations.py](/audit_bus_stations.py)):

	bus_street_name_re = re.compile(r'\b\S+\.?$')
	
	def is_bus_street_name(elem):
	    return (elem.attrib['k'] == "naptan:Street")
	    
	  mapping_street_buses = {
	                        "Hospita": "Hospital", 
	                        "Lan": "Lane",
	                        "Rd": "Road", 
	                        "Sreet": "Street",
	                        "Steet": "Street",
	                        "St": "Street"
	                        }
	
	def update_bus_street_names(name, mapping_street_buses):
	    new_name = name.title()
	    for bus in mapping_street_buses:
	        if bus in new_name:
	            new_name = re.sub(r'\b' + re.escape(bus) + r'$', mapping_street_buses[bus], new_name) 
	    return new_name 

### Incosistent and Incorrect Amenity Types 

I also checked the amenities type names. I found few erroneous entries related to amenities and city names which I document below:....

	# Note that all amenity types consisting of two words are seperated with an 
	# underscore in the dataset
	<tag k="amenity" v="clubhouse"/>
	<tag k="amenity" v="Fish and Ships"/>
	<tag k="amenity" v="police; council"/>
		
...and I also present bits of the code that I used to tackle with them:  (the code that follows is part of [audit_amenities.py](/audit_amenities.py))

	amenity_re = re.compile(r'\S+(\s\S+)*')
	
	def is_amenity(elem):
	    return (elem.attrib['k'] == "amenity")
	
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

## Overview of the Data

This section contains basic statistics about the dataset and the SQL queries used to gather them.


### File sizes
	liverpool_england.osm	301.3 MB
	liverpol.db		164.3 MB
	nodes.csv		106.6 MB
	nodes_tags.csv		  4.0 MB
	ways.csv		 15.3 MB
	ways_tags.csv		 18.4 MB
	way_nodes.csv		 43.9 MB

### Number of nodes
	sqlite> SELECT COUNT(*) FROM nodes;
	1296280
### Number of ways
	sqlite> SELECT COUNT(*) FROM ways;
	258001	
### Number of unique users
	sqlite> SELECT COUNT(DISTINCT(e.uid))
	   ...> FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
	816
### Top 10 contributing users
	sqlite> SELECT e.user, COUNT(*) as num
	   ...> FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
	   ...> GROUP BY e.user
	   ...> ORDER BY num DESC
	   ...> LIMIT 10;
	   
	daviesp12	1055137
	jrdx		  50628
	khbritish	  38805
	UniEagle	  33522
	Dyserth		  26694
	F1rst_Timer	  21084
	xj25vm		  20245
	duxxa		  20024
	alterain	  16164
	thewilk		  16118

### Top 10 appearing amenities

	sqlite> SELECT value, COUNT(*) as num
	   ...> FROM nodes_tags
	   ...> WHERE key='amenity'
	   ...> GROUP BY value
	   ...> ORDER BY num DESC
	   ...> LIMIT 10;
	   
	post_box			543
	pub				454
	restaurant			225
	fast_food			196
	place_of_worship		194
	parking				176
	cafe				139
	telephone			128
	taxi				127
	pharmacy			 79

### Banks with the most branches

	sqlite> SELECT nodes_tags.value, COUNT(*) as num
	   ...> FROM nodes_tags
	   ...> JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='bank') i
	   ...> ON nodes_tags.id=i.id
	   ...> WHERE nodes_tags.key='name'
	   ...> GROUP BY nodes_tags.value
	   ...> ORDER BY num DESC
	   ...> LIMIT 5;
	
	HSBC		9
	Barclays	8
	Santander	6
	NatWest		5
	Halifax		3

### Largest fast food restaurant chains 

	sqlite> SELECT nodes_tags.value, COUNT(*) as num
	   ...> FROM nodes_tags
	   ...> JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='fast_food') i
	   ...> ON nodes_tags.id=i.id
	   ...> WHERE nodes_tags.key='name'
	   ...> GROUP BY nodes_tags.value
	   ...> ORDER BY num DESC
	   ...> LIMIT 5;
	
	Subway		15
	McDonald's	 8
	KFC		 5
	Burger King	 3
	Dominos		 3

## Additional Ideas

As I was running several queries like the ones above, I thought it would be interesting to check if the openstreetmap dataset for Liverpool provides website info for restaurants or pubs. So I run the query below in sqlite:

	sqlite> SELECT nodes_tags.value, COUNT(*) as num
	   ...> FROM nodes_tags
	   ...> JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE key='website') i
	   ...> ON nodes_tags.id=i.id
	   ...> WHERE nodes_tags.key='amenity'
	   ...> GROUP BY  nodes_tags.value
	   ...> ORDER BY num DESC ;
	
	restaurant	21
	pub		18
	......

Then I checked how many restaurants... 

	sqlite> SELECT COUNT(*)
	   ...> FROM nodes_tags
	   ...> WHERE value='restaurant';
	225

......and pubs are present in the dataset:
	
	sqlite> SELECT COUNT(*)
	   ...> FROM nodes_tags
	   ...> WHERE value='pub';
	454
			
So the dataset has website info for only 9% of restaurants and 4% of pubs in Liverpool. Those percentages are quite low but we must not forget that probably not all restaurants or pubs have a website. Nevertheless, it seems that there are a lot of missing websites from the Liverpool dataset. In my opinion adding an external link, even if it just a facebook page (which is a cheap and common way to have presence on the Internet nowdays) will give extra value in the openstreet map. This is certainly not an easy task for each user that voluntarily adds info on the map manually. But I think its not difficult to web scrap addresses as long as you already have the name of the restaurant or pub and the city name and have some programming experience. So for the interested openstreetmap volunteer this could be a very interesting task to accomplish.
