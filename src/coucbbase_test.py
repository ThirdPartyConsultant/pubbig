#!/usr/bin/env python
#trial generate large scale database

from couchbase import Couchbase


couchbucket = Couchbase.connect(bucket='sunshine', host='localhost')
print couchbucket

global total
total = 0


