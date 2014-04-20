# -*- coding: utf-8 -*-. 
from BeautifulSoup import BeautifulSoup as soup
from io import open
import pymongo
import commands
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

legislator = {}


def handle_ly(filename, orderno):
    site = "http://www.ly.gov.tw"

    htmlfile = open(filename,encoding='UTF-8')
    start_keystring = u'屆　立法委員名單'
    end_keystring = u'查詢結果共'
    state = "none" # none, inline
    print u'第' + str(orderno) + u'屆 清單'
    state = "none" # none, inline
    cnt = 0
    for line in htmlfile:
        if line.count(start_keystring) >= 1:
            state = "inline"
        if line.count(end_keystring)  and state == "inline" >= 1:
            state = "none"

        if state == "inline":
            cnt+= 1
            html_line = soup(line, fromEncoding="UTF-8")
            for tag in html_line.findAll('a', {'href': True}) :
                if(tag.string != None and tag['href'] != None ):
                    url = site + tag['href']
                    legislator_name = tag.string.encode('UTF-8')
               #     print type(legislator_name.encode("UTF-8"))
                    inject_legislator_tag(legislator_name, url, orderno) 

            
# result in legislator dict
def inject_legislator_tag(name, url, orderno):
    #print name
    if legislator.has_key(name):

        if legislator[name].has_key(u'屆'):
            legislator[name][u'屆'].append(orderno)
        else:
            legislator[name][u'屆'] = []
            legislator[name][u'屆'].append(orderno)

        if legislator[name].has_key(u'url'):
            legislator[name][u'url'].append(url)
        else:
            legislator[name][u'url'] = []
            legislator[name][u'url'].append(url)
    else:
        legislator[name] = {}
        legislator[name][u'屆'] = []
        legislator[name][u'屆'].append(orderno)
        legislator[name][u'url'] = []
        legislator[name][u'url'].append(url)




filename_prefix="row_data/legList.action_"
for i in range(2,9):
    filename = filename_prefix+str(i)+"th"
    handle_ly(filename, i)


print legislator
mongo_connection = pymongo.Connection('localhost',27017)
mongo_legislator_db = mongo_connection['legislator_db']

collection_legislator_list = mongo_legislator_db['legislator_list']
collection_legislator_list.insert(legislator)


#Insert in to mongodb 
#db -> legislator
#collection -> member_list
#document (single document)


#f = open("all_legislator.json","w", encoding="UTF-8")
#print json.dumps(legislator, encoding="UTF-8")
#f.close()

#gather finance report to row data
#for name in legislator.keys():
#    cmd = "sh wget_finance.sh \"" + name +"\" \"row_data/finance_"+name+"\""
#    print cmd
#    print commands.getoutput(cmd.encode('utf-8'))
