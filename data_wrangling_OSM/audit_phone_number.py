# Audit phone number  
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
  
PHONENUM = re.compile(r'\+39\s\d{3}\s\d{6,7}')

def correct_phone_num(phone_num):
    """
    Correct the phone number to ensure the same format
    
    Args:
        phone_num (str): phone number
        
    Returns:
        str: correct phone number
    """
    # Check for valid phone number format
    m = PHONENUM.match(phone_num)
    if m is None:
        
        # remove postal code 
        if re.match(r'\d{5}', phone_num) is not None:
            if re.match(r'\d{6}', phone_num) is None:
                return None
        
        # Convert all dashes to spaces
        if "-" in phone_num:
            phone_num = re.sub("-", " ", phone_num)
         
        # remove space between + and 39
        if re.match(r'\+ 3',phone_num[:3]) is not None:
            phone_num = re.sub(" ", "", phone_num, count=1)
            
        # Substitute 00 with +
        if phone_num[:2]=='00':
            phone_num = '+' + phone_num[2:]
            
        # Add coutry code
        if re.match(r'\+39|39',phone_num) is None:
            phone_num = "+39" + phone_num
            
        # Remove whitespaces
        if " " in phone_num:
            phone_num = re.sub(" ", "", phone_num)
            
        # Add + in country code
        if re.match(r'39\d{3,}', phone_num) is not None:
            phone_num = "+" + phone_num
            
        # Check number in the 4th position
        if phone_num[3]=='4':
            phone_num = phone_num[:3]+'0'+phone_num[3:]
            
        if phone_num[3:5]=='03':
            phone_num = phone_num[:3]+phone_num[5:]
            
      
        # Space phone number
        phone_num = phone_num[:3] + " " + phone_num[3:6] + " " + phone_num[6:]

    return phone_num


def audit_phone(osmfile):
    """
    Check phone numbers and correct for the right format
    Args:
        osmfile (str): file path
    """
    phone_list = []
    phone_file = open(osmfile, encoding="utf8")
    counter = 0
    counter_max = 5
    print('Corrected phone numbers (first 5):\n') 
    for event, elem in ET.iterparse(phone_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == 'phone':
                    old_phone_num = tag.attrib['v']
                    new_phone = correct_phone_num(old_phone_num)
                    if counter<counter_max:  
                        if old_phone_num!=new_phone:
                            print(old_phone_num + '-->' + new_phone)
                            counter = counter + 1
                   # if phone_num not in phone_list:
                    #    phone_list.append(phone_num)
                    
    phone_file.close()