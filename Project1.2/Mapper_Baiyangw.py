#!/usr/bin/env python
# Filename: Mapper_Baiyangw.py
import re
import sys
import os
#Filter
rule = re.compile(r'(Media:|Special:|Talk:|User:|User_talk:|Project:|Project_talk:|File:|File_talk:|MediaWiki:|MediaWiki_talk:|Template:|Template_talk:|Help:|Help_talk:|Category:|Category_talk:|Portal:|Wikipedia:|Wikipedia_talk:|^[a-z]|404_error/:|Main_Page|Hypertext_Transfer_Protocol:|Favicon.ico:|Search:|.jpg|.gif|.png|.JPG|.GIF|.PNG|.txt|.ico)',re.X)
List = []
#Get filename
file_path = os.environ["map_input_file"]
file_name = os.path.split(file_path)[-1]
[name, date, hour] = file_name.split("-",2)
for line in sys.stdin:
    line = line.strip() #Strip any leading or trailing whitespace in line
    [project_name, page_title, access_number, total_data] = line.split(" ", 3)
    if project_name == "en":
        match = rule.search(page_title)
        if not match:
            List.append((page_title,int(access_number)))
for elem in List:
#Append date info to the value of pairs
    string = str(elem[1])+'-'+ date
#Output the pairs
    print '%s\t%s' %(elem[0],string)