import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# String pattern for checking street name anomalies
street_type_re = re.compile(r'(\S*)+\.?', re.I)
# +: at least one match of the previous symbol 
# *: at least 0 match of the previous symbol 
# ?: 0 or 1 occurrences of the previous symbol


num_line_street_re = re.compile(r'\d0?(st|nd|rd|th|)\s(Line)$', re.IGNORECASE) 

# List of expected street names
expected = ["Via", "Corso", "Viale", "Vicolo", "Piazza","Piazzetta", 
            "Piazzale", "Calle","Dorsoduro","Rio","Giudecca","Sotoportego",
            "Campo","Campiello","Fondamenta","Crosera","Salizada","Rotonda",
            "Riviera","Ponte","Corte","Cannaregio","San","Santa","Piscina","Borgo"]

# Map of corrections for street names
mapping_street = { "Campazzo": "Campo",
                   "Dorsorduro": "Dorsoduro",
                   "Fondamente": "Fondamenta",
                   "Gallion": "Calle Gallion",
                   "salizada": "Salizada",
                   "via": "Via",
                   "cannaregio": "Cannaregio",
                   "santa": "Santa",
                   "Sestiere": "",
                   "Carbonera": "",
                   "Forte": "Via Forte"}


def audit_street_type(street_types, street_name):
    """
    Add to the dictionary of unexpected street types a new unexpected street type.
    Args:
                street_types (dict): dictionary with unexpected street types
                street_name (str): street name   
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit_street(osmfile):
    
    """
    Open OSM file, find and call auditing function for every tag with street names.
    Args:
                osmfile (string): file path
    Returns:
                dict: dictionary with unexpected street types
    
    """
    
    osm_file = open(osmfile, encoding="utf8")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def correct_street_name(name, mapping):
    
    """
         Correct error in the street name
         Args:
                   name (string): street name
                   mapping (dict): dictionary with map of corrections 
         Returns:
                   name_correct (string): correct street name
    """
    
    name_correct = name
    
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type =='Isola':
            name_correct = re.sub("Nuova", "Nova",name)
        elif street_type =='Lista':
            name_correct = 'Rio Terà ' + name
            name_correct = re.sub(r'(\n)+', "", name_correct)
        elif street_type =='Stazione':
            name_correct = 'Cannaregio'
        elif street_type == 'Dorsoduro,':
            name_correct = re.sub(r'(\,+\D+)', "", name)
        elif street_type == 'La':
            name_correct = 'Fondamenta Sant Eufemia'
        elif street_type in mapping:
            name_correct = street_type_re.sub(mapping[street_type], name, count = 1)
            
            if street_type == 'Sestiere' or street_type == 'Carbonera':
                name_correct = re.sub(r'\s+',"", name_correct, count = 1)
            elif street_type == 'salizada':
                name_correct = re.sub(r'(samuele)+\D+[0-9]+','Samuele', name_correct, count = 1)

    return name_correct

