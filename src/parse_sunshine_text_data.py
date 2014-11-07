#!/usr/bin/python
# -*- coding: utf-8 -*-.
import os
import sys
import commands
from BeautifulSoup import BeautifulSoup as Soup
from io import open
import sys
import getopt
sys.path.append('web_server/DA')
reload(sys)
sys.setdefaultencoding("utf-8")

from couchbase import Couchbase
import pprint
import uuid
titlemeta = {}

class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)



def addToCouchbase(key, doc):
    couchbucket = Couchbase.connect(bucket='sunshine', host='localhost')
    ruuid = str(uuid.uuid4())
    couchbucket.set(key+ruuid,doc);


def post_process_form(aform):
    if(aform[u'姓名'] == u''):
        for elem in aform['source'][u'text']:
            if elem.startswith(u'申報人：') or elem.startswith(u'申報人:'):
                possibleName = elem.split(":")[-1].split(u'：')[-1]
                aform[u'姓名'] = possibleName
                break

    #adjust URL to site site="http://sunshine.cy.gov.tw/GipOpenWeb/wSite/"
    site="http://sunshine.cy.gov.tw/GipOpenWeb/wSite/public/Attachment/"
    url = aform['source']['url']
    originalname = url.replace("row_data/text/","").replace(".txt","")
    title = ''
    global titlemeta
    for key in titlemeta.keys():
        if key.count(originalname) > 0 :
            title = titlemeta[key]['title']
    url = site + originalname
    aform['source']['url'] = url
    aform['source']['title'] = title

def dump_form(aform):
    post_process_form(aform)
    akey = aform['source']['title']+u':'+aform[u'姓名']
    addToCouchbase(akey, aform)
    # MyPrettyPrinter().pprint(aform)  
   # if(aform[u'姓名'] == u''):
   #     MyPrettyPrinter().pprint(aform)  

def retrieve_info(sunshine_file, is_run_once=True):
    ignore_start = u'選舉擬參選人' 
    ignore_end = u'上表逕依申報人所載資料公告'
    form_start = [u'公職人員財產申報表', u'申報人姓名',
                  u'公職人員信託財產申報表',
                  u'公職人員變動財產申報表']
    form_end = [u'申報人:',u'申報人：']
    meta_name = [u'申報人姓名',u'擬參選人：']
    
    result = {}
    f = open(sunshine_file, encoding="UTF-8")
    flag = None # possible flag None, 'in', sections key name
    one_form = {}
    people_count = 0
    extra_count = 0
    shorttext = u''
    for line in f:
        line = line.strip()
        line = line.replace(" ","")
        if len(shorttext) <= 3 and  len(line) <=2 : 
             shorttext =  shorttext + line
             continue 
        else: 
             line = shorttext + line
             shorttext = u''

        if flag == None:
            for form_start_key in form_start:
                if line.replace(' ','').count(form_start_key) ==1:
                    print "=== form start ===" + form_start_key
                    flag = 'in' # means a new form
                    one_form = {}
                    one_form['source'] = {}
                    one_form['source']['url'] = sunshine_file
                    one_form['source']['text'] = []
                    one_form[u'姓名'] = ''
                    break
            if line.count(ignore_start) >= 1:
                flag = 'ignore' # means an ignore form
                one_form = {}

        if flag == 'in' :
            one_form['source']['text'].append(line)


        if flag == 'ignore' :
            shorttext = ''
            if line.count(ignore_end) >= 1:
                flag = None # means leave an ignore form
                print "leave an ignore form"
            continue


        if flag != None:
            for form_end_key in form_end:
                if line.count(form_end_key) == 1:
                    print "=== form end ==="+form_end_key
                    flag = None # means a new form
                    dump_form(one_form)
                    people_count += 1
                    flag = None
                    break



    print people_count
 


def build_metadata(filename):
    list_html_file =  open(filename,encoding="UTF-8")

    fullhtmlsoup = Soup(open(filename))

    keyword="public/Attachment"
    meta_source = {}
    for line in list_html_file:
        if line.count(keyword) > 0:
            html_line = Soup(line)
            sourcelink= html_line.a['href']
            meta_source[sourcelink] = {}
            meta_source[sourcelink]['title'] = html_line.a.img['title'].replace(".pdf","")

    list_html_file.close()
    return meta_source



def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)

    is_run_once = True
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)

    sunshine_file = args[0]

    global titlemeta 
    titlemeta  = build_metadata("row_data/list_of_report_part.html")
    retrieve_info(sunshine_file, is_run_once=False)
    


if __name__ == "__main__":
    main()




