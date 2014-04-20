#!/usr/bin/python
# -*- coding: utf-8 -*-.
import os
import sys
import commands
from BeautifulSoup import BeautifulSoup as Soup
from io import open
import sys
import getopt
reload(sys)
sys.setdefaultencoding("utf-8")


def _add_array_item(adict, key, value):
    if adict.has_key(key):
        adict[key].append(value)
    else:
        adict[key] = [value]

def _retrieve_saving(one_form, line, flag):
    line = line.strip()
    if line != "" and line.count(u':') == 1:
        total_amount = line.replace(" ","").split(":")[-1].replace(u'元)',"")
        _add_array_item(one_form, u'存款總金額', total_amount)
    if line != "":
        _default_line_process(one_form, line, flag)
    



def _retrieve_land(one_form, line, flag):
    land = u'(一) 不動產'
    line = line.strip()
    if line != "" and len(line) >= 3:
        _default_line_process(one_form, line, flag)

def _retrieve_stock(one_form, line, flag):
    keys = [u'股票',u'票券',u'債券',u'其他有價證券']
    to_remove_words= ["(總價額:","元)" ]
    _default_line_process(one_form, line, flag)


def _process_meta_org(one_form, line, flag):
    if line.strip() != "" and line.count(".")  == 1:
        org = line.strip().split(".")[-1]
        _add_array_item(one_form, u'服務機關', org)

def _process_meta_date(one_form, line, flag):
    line = line.strip()
    if line != "":
        one_form[u'申報日期'] = line

def _default_line_process(one_form, line, flag):
    line = line.strip()
    if line != "" and len(line) >= 3 :
        _add_array_item(one_form, flag, line)


def dump_form(one_form):
    print "===== dump one ===="
    for k in one_form.keys():
        print k 
        value = one_form[k]
        if isinstance(value, list):
            for item in value:
                print " **---> " + str(item)
        else:
            print "---> " + str(value)


def retrieve_info(sunshine_file, is_run_once=True):
    ignore_start = u'選舉擬參選人' 
    ignore_end = u'上表逕依申報人所載資料公告'
    form_start = [u'公職人員財產申報表', 
                  u'公職人員信託財產申報表',
                  u'公職人員變動財產申報表']
    form_end = [u'願負法律責任',u'特此聲明',u'本人係依法誠實申']
    meta_name = [u'申報人姓名',u'擬參選人：']
    meta_org =  u'服務機關'
    meta_date = u'申報日'
    section_orders = [u'存款',u'有價證券',u'.土地',u'.建物',u'外幣',u'債權',u'債務',u'事業投資',u'其他具有相當價值之財產',u'汽',u'其他財產',u'船舶',u'航空器']
    sections = { u'存款': _retrieve_saving, \
                 u'有價證券':_retrieve_stock, \
                 u'.土地':_default_line_process, \
                 u'.建物':_default_line_process, \
                 u'外幣':_default_line_process, \
                 u'債權':_default_line_process, \
                 u'債務':_default_line_process, \
                 u'事業投資':_default_line_process, \
                 u'其他具有相當價值之財產':_default_line_process, \
                 u'船舶': _default_line_process, \
                 u'其他財產':_default_line_process, \
                 u'汽' : _default_line_process , \
                 u'航空器' :_default_line_process, \
                }

    
    result = {}
    f = open(sunshine_file, encoding="UTF-8")
    flag = None # possible flag None, 'in', sections key name
    one_form = {}
    people_count = 0
    for line in f:
        if flag == None:
            for form_start_key in form_start:
                if line.replace(' ','').count(form_start_key) ==1:
                    print "=== form start ==="
                    flag = 'in' # means a new form
                    one_form = {}
                    break
            if line.count(ignore_start) >= 1:
                flag = 'ignore' # means an ignore form
                one_form = {}

        if flag == 'ignore' :
            if line.count(ignore_end) >= 1:
                flag = None # means leave an ignore form
                print "leave an ignore form"
            continue

        if flag != None:
            for form_end_key in form_end:
                if line.count(form_end_key) == 1:
                    print "=== form end ==="
                    flag = None # means a new form
                    dump_form(one_form)
                    people_count += 1
                    flag = None
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
                        tmp_name = parts[1]
                    flag = 'meta_name'
                    one_form[u'姓名'] = tmp_name
                    break

            if line.count(meta_org) == 1:
                flag = 'meta_org'
                _process_meta_org(one_form, line, flag)
                # print "flag changes " + flag
 
            if line.replace(' ','').count(meta_date) >= 1:
                flag = 'meta_date'
                print "handle meta date"
                _process_meta_date(one_form, line, flag)


            for key in section_orders:
                if line.count(key) >= 1:
                    flag = key
                    #print "flag changes for sections... " + flag
#                    sections[flag](one_form, line, flag)
                    break

            if flag in section_orders:
                sections[flag](one_form, line, flag)

        
           


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

