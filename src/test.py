# -*- coding: utf-8 -*-. 
from io import open
from BeautifulSoup import BeautifulSoup as soup


site = "http://www.ly.gov.tw"
def handle_ly():
    htmlfile = open('legList.action',encoding='UTF-8')
    start_keystring = u'屆　立法委員名單'
    end_keystring = u'查詢結果共'
    state = "none" # none, inline
    cnt = 0
    for line in htmlfile:
        if line.count(start_keystring) >= 1:
            state = "inline"
        if line.count(end_keystring)  and state == "inline" >= 1:
            state = "none"

        if state == "inline":
            cnt+= 1
            html_line = soup(line)
            for tag in html_line.findAll('a', {'href': True}) :
                if(tag.string != None and tag['href'] != None ):
                    url = site + tag['href']
                    print tag.string + "URL->"+ url

    print cnt

handle_ly()
