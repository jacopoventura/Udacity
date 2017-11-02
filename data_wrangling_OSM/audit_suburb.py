# Audit city suburb name
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

mapping_city = {"Venice": "Venezia",
                "Marghera VE": "Marghera",
                "Venezia Mestre": "Mestre",
                "30173": "Tessera",
                "3073": "Tessera"
				}

expected_suburb = ['Venezia', 'Oriago', 'Mestre', 'Favaro Veneto','Tessera',
                   'Marghera', 'Zelarino', 'Campalto', 'Malcontenta','Marcon',
				   'Martellago','Mira','Olmo','Spinea']

def audit_city(osmfile):
    """
    Audit name of city suburb
         Args:
                   osmfile (str): OSM file path
         Returns:
                   suburb_list_wrong (dict): dictionary with wrong postal codes
    """
    suburb_list_wrong = defaultdict(set)
    city_file = open(osmfile, encoding="utf8")
    
    for event, elem in ET.iterparse(city_file, events=("start",)):
        
        if elem.tag == "node" or elem.tag == "way":
            
            for tag in elem.iter("tag"):
                
                if tag.attrib['k'] == 'addr:city':
                    
                    city = tag.attrib['v']
                    # province = re.sub(" ", "", tag.attrib['v'].strip())
                    if city not in expected_suburb:
                        
                        suburb_list_wrong[city].add(city)
                    
    city_file.close()
    return suburb_list_wrong
    
    
def correct_city_sub(name, mapping):
    """
    correct suburb name
    Arg:
        name (str): suburb name
        mapping (dict): list of corrections
        
    Return:
        name_correct (str): correct name
    
    """
    name_correct = name
    
    m = re.search(r'(\D*\d*)+',name)
    if m:
        suburb = m.group()
        if suburb not in expected_suburb:
            name_correct = mapping[suburb]
            
    return name_correct
