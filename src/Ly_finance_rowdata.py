#!/bin/python
# -*- coding: utf-8 -*-.
import os
import sys
import commands
from BeautifulSoup import BeautifulSoup as Soup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

path = u'row_data'

def retrieve_detail(filename):
    cmd = "./wget_finance.detail.sh"
    print filename
    for_parse = open(filename).read()
    soup = Soup(for_parse)
    ly_name = filename[17:]
    for item in soup.findAll('a', title=ly_name):
        if item['href'] != "javascript:redirectFileDownload('Y')":
            print item['href'][31:][1:-1]
            pdf_id = item['href'][31:][1:-1]
            get_pdf_cmd = cmd + " "+ pdf_id + " "+ filename+"_"+pdf_id+".pdf"
            print commands.getoutput(get_pdf_cmd.encode('utf-8'))



for f in os.listdir(path):
    if f[:8] == u'finance_' :
        retrieve_detail(path+"/"+f)


