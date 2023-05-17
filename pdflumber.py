import pdfplumber
import pandas as pd
import re
import os
import glob
from p.p40 import p40_to_json

name = "pdf/m.pdf"
name = "pdf/MSLS_FY_2022_PB_Missile_Procurement_Army - Copy.pdf"
file_name = name.split("/")[-1].split(".")[0]

# reads pdfs pages and returns them in tables
def get_table(name, pages = "all"):
    with pdfplumber.open(name) as pdf:
        tables = []
        if pages == "all":
            pages = range(len(pdf.pages))

        for i in pages:
            page = pdf.pages[i]
            t = page.extract_tables()
            if (len(t) == 0):
                continue
            table = t[0]
            tables.append(table)
    return tables

def replace_newline(table): 
    return [[col.replace('\n', ' ') if col != None else None for col in row] for row in table]

# return the p-xx type from the table, if it is in box 0,0
def get_type(table):
    pattern = r"(P-\d+),"
    res = re.search(pattern, table[0][0])
    if res:
        return res.group(1).replace(","," -")
    return "404"

# return the name of the item in the table, it is given by the following of p-1
def get_name(table):
    pattern = r"P-1.*: (.*)"
    for row in table:
        for col in row: 
           if (col == None):
               continue
           res = re.match(pattern, col)
           if res:
               return res.group(1).replace("/", "-")
    return "404"


# Duplication handle
previous_type = ""
previous_item = ""
duplicate = 2

def create_file(file_name, item_name, page_type):
    global duplicate
    global previous_item
    global previous_type
    # Create out
    if not os.path.exists("out"):
        os.mkdir("out")

    # Path
    directory = "out/{}/{}".format(file_name, item_name)
    path = "{}/{}.csv".format(directory, page_type)

    # Make directory if it doesnt exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Handle duplicate
    if previous_item == item_name and previous_type == page_type:
        p, ext = path.split(".")
        path = "{} ({}).{}".format(p, duplicate, ext)
        duplicate += 1
    else:
        duplicate = 2
        previous_item = item_name
        previous_type = page_type

    # Make as CSV file
    df = pd.DataFrame(table)
    df.to_csv('{}'.format(path), index=False, header=False)
    #print(df)




# Remove contents of out
tables = get_table(name, range(20, 230))
#20 230

# Create CSV files
for table in tables:
    # Format
    table = replace_newline(table) 

    # Content 
    page_type = get_type(table)
    item_name = get_name(table)

    create_file(file_name, item_name, page_type)
    if (page_type != "P-40"):
        continue
    p40json = p40_to_json(table, file_name, 2020, 20, item_name, 1)
    print(p40json)
