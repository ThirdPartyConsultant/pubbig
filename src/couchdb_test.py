#!/usr/bin/python
# -*- coding: utf-8 -*-.

from couchdb import Server

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

s = Server(url='http://172.16.32.128:5984')
db = s['sunshine']

doc = {
      "_id":"_design/testview",
      "language": "javascript",
      "views":
      {
        "all": {
          "map": "function(doc) { if (doc) {emit(null, doc);} }"
        },
       "by_lastname": {
         "map": "function(doc) {   emit(doc.姓名, doc); }"
       },
       }
   }

#a = db.save(doc)
#print a
docs = db.view("_design/testview/_view/by_lastname",startkey=u'馬英九', endkey=u'馬英九')
cnt = 0
print docs
for row in docs.rows:
    doc = row.value
    cnt += 1
    for k in doc.keys():
        print k 
        if k == u'有價證券':
            for item in doc[k]:
                print item


print("total:"+str(cnt))

