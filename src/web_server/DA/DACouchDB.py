import couchdb

class DACouchDB:
    def __init__(self,dbName,collectionName):
        self.host = 'localhost'
        self.port = 5984
        #self.connection = Connection(self.host, self.port)
        self.server = couchdb.Server()
        print dir(self.server)
        print dbName
        self.db = self.server.create(dbName)
        self.collection = collectionName # to sastify a collection catagory
                        
    def insert(self, obj=None, key=None):
        self.db.save(obj)
        print dir(self.collection)
        return objId

    def delete(self, obj):
        self.collection.remove(obj)

    def select(self, obj):
        return self.collection.find(obj)

    def update(self, oriObj, newObj ):
        self.collection.update(oriObj, newObj)


if __name__ == '__main__':
    dataAccess = DACouchDB('theboss',"person")
    dir(dataAccess.db)
    
