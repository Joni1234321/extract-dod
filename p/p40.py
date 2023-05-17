import json
from datetime import date
import re

# Returns description
def get_description(p40):
    for row in p40:
        if (row[0] == None):
            continue
        res = re.match(r"Description", row[0])
        if res:
            return row[0]
        
    return ""


# P40 JSON
def p40_to_json (p40, file_name, file_date, page, item_name, item_number):

   # resource_summary =  

    description = get_description(p40)

    res = {
        "schema_version": 1,
        "file_name": file_name,
        "file_date": file_date,
        "generation_date": date.today(), 
        "page": page,
        "item_name": item_name,
        "item_number": item_number,

        "description": description,

        "resource_summary":{
            
        }

        }

    return res