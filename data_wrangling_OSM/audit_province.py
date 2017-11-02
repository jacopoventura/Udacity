import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# Audit province information
def correct_province(name):
    
    if name=='VE':
        name = 'Venezia'
        
    return name


    
def audit_prov(osmfile):
    """
    Check province information
    Args:
        osmfile (str): file path
    """
    province_list = []
    province_file = open(osmfile, encoding="utf8")
    for event, elem in ET.iterparse(province_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == 'addr:province':
                    province = correct_province(re.sub(" ", "", tag.attrib['v'].strip()))
                    if province not in province_list:
                        province_list.append(province)
                    
                    
    province_file.close()