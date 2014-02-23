# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import os
import sys
import datetime
import pymongo
from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    print(client.database_names())
    testdb = client['test']
    print(testdb.collection_names())
    #print(client.database_names())
    collection = testdb['test_collection']
    print(collection.find_one())
    #post = {"author": u"测试作者",
    #"text": u"中文测试",
    #"tags": ["mongodb", "python", "pymongo"],
    #"date": datetime.datetime.now()}
    #id = collection.insert(post)
    #print(id)
    #print(testdb.collection_names())
    
    
    