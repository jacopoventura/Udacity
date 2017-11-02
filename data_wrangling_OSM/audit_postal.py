# Audit post code
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


mapping_postal_code = { "PontedeiPugni": "30123",
                        "Ponte dei Pugni": "30123",
                        "Venice30123": "30123",
                        "Venice 30123": "30123"}


POSTCODE = re.compile(r'[A-z]\d[A-z]\s?\d[A-z]\d')
min_code = 30121
max_code = 30176

def audit_postcode(osmfile):
    """
    Audit postal code
         Args:
                   osmfile (str): OSM file path
         Returns:
                   postal_code_wrong (dict): dictionary with wrong postal codes
    """

    postal_code_wrong = defaultdict(set)
    
    # loop through the OSM file to check postal codes
    post_file = open(osmfile, encoding="utf8")

    counter = 0
    print('Postal codes outside Mestre area (first 5):')
    for event, elem in ET.iterparse(post_file, events=("start",)):
        
        if elem.tag == "node" or elem.tag == "way":
            
            for tag in elem.iter("tag"):
                
                if tag.attrib['k'] == 'addr:postcode':
                    
                    post_code = re.sub(" ", "", tag.attrib['v'].strip())
                    m = POSTCODE.match(post_code)
                    if m is None:
                        
                        aa = [int(s) for s in post_code.split() if s.isdigit()]
                        if aa:
                            
                            if aa[0]<min_code or aa[0]>max_code:
                                
                                if counter<5:

                                    #if post_code not in postal_code_wrong
                                    print('%d' %aa[0])
                                    counter+=1
                        else:
                            postal_code_wrong[post_code].add(post_code)
    post_file.close()
    return postal_code_wrong

	
def correct_postal_code(name, mapping):
    """
         correct postal code
         Args:
                   name (str): postal code
                   mapping (list): list of corrections
         Returns:
                   code_correct (str): correct postal code
    """
    
    code_correct = name
    
    m = re.search(r'(\D+\d*)+',name)
    if m:
        code = m.group()
        code_correct = re.sub(r'(\D+\d*)+',mapping[code], name, count = 1)
        return code_correct
    
    return code_correct