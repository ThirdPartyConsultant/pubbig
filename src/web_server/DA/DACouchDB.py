#!/bin/python
# -*- coding: utf-8 -*-.
import os
import sys
import couchdb
reload(sys)
sys.setdefaultencoding("utf-8")


class DACouchDB:
    def __init__(self,dbName,collectionName):
        self.host = 'localhost'
        self.port = 5984
        #self.connection = Connection(self.host, self.port)
        self.server = couchdb.Server()
        if dbName in self.server:
            print dbName + " already there"
            self.db=self.server[dbName]
        else:
            print "create "+dbName
            self.db = self.server.create(dbName)
            self.collection = collectionName # to sastify a collection catagory

                        
    def insert(self, obj=None, key=None):
        (objId, rev) = self.db.save(obj)
        return objId

    def delete(self, doc):
        self.db.delete(doc)

    def select(self, objId):
        return self.db.get(objId)

    def query(self, map_fun,key=None):
        return self.db.query(map_fun, key=key)

    def update(self, oriObj, newObj ):
        self.db.update([oriObj])


if __name__ == '__main__':

    dataAccess = DACouchDB('boss',"person")
    testdoc = {u'姓名':u'馬小九', 'name':u'馬小酒', 'tel':['23939889','020020202','02020202020'] }
    testdoc2 = {u'姓名':u'馬小九', 'name':u'馬小久', 'tel':['23939889','020020202','02020202020'] }
    objId = dataAccess.insert(obj=testdoc)
    print "new doc id: "+ str(objId)
    
    doc = dataAccess.select(objId)  
    print "get the doc"
    print doc
    print "delete the doc ... "
    doc = dataAccess.delete(doc)  
    print "select the same doc again ... "
    doc = dataAccess.select(objId)  
    print doc
    objId = dataAccess.insert(obj=testdoc2)
    print "insert new doc id: "+ str(objId)
   
    doc = dataAccess.select(objId)  
    print "going to update the doc..."
    print doc
    print "going to update the doc to"
    doc[u'姓名'] = u'馬英九'
    dataAccess.update(doc, doc)

    doc = dataAccess.select(objId)
    print "select again the update result..."
    print doc

    map_fun = ''' function(doc){ 
        emit(doc.name ,doc);
    } 
   '''
    results = dataAccess.query(map_fun, key=u'馬小久')
    for i in results:
        print i.key

    print "delete again the doc ... "
    doc = dataAccess.delete(doc)  
