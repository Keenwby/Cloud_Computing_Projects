#!/usr/bin/env python
# Filename: sample.py
import re
from operator import itemgetter, attrgetter
rule = re.compile(r'(Media:|Special:|Talk:|User:|User_talk:|Project:|Project_talk:|File:|File_talk:|MediaWiki:|MediaWiki_talk:|Template:|Template_talk:|Help:|Help_talk:|Category:|Category_talk:|Portal:|Wikipedia:|Wikipedia_talk:|^[a-z]|404_error/:|Main_Page|Hypertext_Transfer_Protocol:|Favicon.ico:|Search:|.jpg|.gif|.png|.JPG|.GIF|.PNG|.txt|.ico)',re.X)
fi = open("pagecounts-20140701-000000",'r')
fo = open("test_1.txt",'w')
lines = fi.readlines()
List = []
for line in lines:
    [project_name, page_title, access_number, total_data] = line.split(" ", 3)
    if project_name == "en":
        match = rule.search(page_title)
        if not match:
            List.append((page_title,int(access_number)))
List_sorted = sorted(List, key=itemgetter(1))
for elem in List_sorted:
    fo.writelines('%s\t%s\n' %(elem[0],elem[1]))
fo.close()
fi.close()
