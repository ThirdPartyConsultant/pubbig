#!/bin/python

from BeautifulSoup import BeautifulSoup as soup
from io import open
import pymongo
import commands
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# The original list
#http://sunshine.cy.gov.tw/GipOpenWeb/wSite/lp?ctNode=442&mp=2&nowPage=1&pagesize=300
#retrieve detail pdf... this at least pdf files
# wget http://sunshine.cy.gov.tw/GipOpenWeb/wSite/public/Attachment/f1397102568527.pdf

site="http://sunshine.cy.gov.tw/GipOpenWeb/wSite/"

def build_metadata(filename): 
    list_html_file =  open(filename,encoding="UTF-8")

    keyword="public/Attachment"
    for line in list_html_file:
        if line.count(keyword) > 0:
            html_line = soup(line)
            print html_line.a['href']
            print html_line.a.img['title']
            wget_pdf(html_line)

    list_html_file.close()

#the atag is a soup like <a><img></img></a>
def wget_pdf(atag):
    cmd = "wget "+ site + atag.a['href']
    print cmd
#    commands.getoutput(cmd)



build_metadata("sunshine_open_data_list2.htm")

