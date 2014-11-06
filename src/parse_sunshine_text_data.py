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

import pprint

class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)



def dump_form(aform):
    if(aform[u'姓名'] == u''):
        MyPrettyPrinter().pprint(aform)  

def retrieve_info(sunshine_file, is_run_once=True):
    ignore_start = u'選舉擬參選人' 
    ignore_end = u'上表逕依申報人所載資料公告'
    form_start = [u'公職人員財產申報表', u'申報人姓名',
                  u'公職人員信託財產申報表',
                  u'公職人員變動財產申報表']
    form_end = [u'願負法律責任',u'申報人:',u'特此聲明',u'本人係依法誠實申',u'申報人：']
    meta_name = [u'申報人姓名',u'擬參選人：']
    
    result = {}
    f = open(sunshine_file, encoding="UTF-8")
    flag = None # possible flag None, 'in', sections key name
    one_form = {}
    people_count = 0
    extra_count =0
    for line in f:
        line = line.strip()
        line = line.replace(" ","")
        if flag == None:
            for form_start_key in form_start:
                if line.replace(' ','').count(form_start_key) ==1:
                    print "=== form start ===" + form_start_key
                    flag = 'in' # means a new form
                    one_form = {}
                    one_form['text'] = []
                    break
            if line.count(ignore_start) >= 1:
                flag = 'ignore' # means an ignore form
                one_form = {}
        if flag == 'in' and len(line)>=3:
            one_form['text'].append(line)

        if flag == 'ignore' :
            if line.count(ignore_end) >= 1:
                flag = None # means leave an ignore form
                print "leave an ignore form"
            continue


        if flag != None:
            for form_end_key in form_end:
                if line.count(form_end_key) == 1:
                    print "=== form end ==="+form_end_key
                    flag = None # means a new form
                    if one_form.has_key(u'姓名') and one_form[u'姓名'].strip !="" :
                        dump_form(one_form)
                        people_count += 1
                        flag = None
                    else: # do search extra 3 lines
                        flag = 'extra_meta_name'
                        extra_count == 0
                    break


            if flag == None and is_run_once:
                break

            for possible_name in meta_name:
                if line.count(possible_name) == 1 :
                    tmp_name = ""
                    if line.count(u'：') >= 1:
                        parts = line.split(u'：')
                        tmp_name = parts[1]
                    else:
                        parts = line.split(" ")
                        if len(parts) == 2:
                            tmp_name = parts[1]
                    one_form[u'姓名'] = tmp_name
                    break

    print people_count
 



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
    print sunshine_file

    retrieve_info(sunshine_file, is_run_once=False)
    

if __name__ == "__main__":
    main()

