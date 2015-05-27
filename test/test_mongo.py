# -*- coding: utf-8 -*-
# from gevent import monkey; monkey.patch_all()
import os
import sys
import datetime
import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson.regex import Regex
import re


def query1():
    client = MongoClient('192.168.1.8', 27017)
    kmgd = client['kmgd']
    collection = kmgd['features']
    ret = []
    #cur = collection.find({"properties.metals.type":u"超声波驱鸟装置"})
    cur = collection.find({"properties.webgis_type":"point_tower","properties.metals.type":u"防振锤"})
    for i in cur:
        ret.append(i)
    #print(ret)
    return ret
def query2():
    client = MongoClient('192.168.1.8', 27017)
    kmgd = client['kmgd']
    collection = kmgd['features']
    ret = []
    #cur = collection.find({"properties.metals.type":u"超声波驱鸟装置"})
    cur = collection.find({
        "properties.webgis_type":"point_tower",
        "properties.metals":{
            "$elemMatch":{
                "type":u"超声波驱鸟装置",
                "imei":"861001005073727"
            }
        }
    })
    for i in cur:
        ret.append(i)
    return ret
def query3():
    client = MongoClient('192.168.1.8', 27017)
    kmgd = client['kmgd']
    collection = kmgd['features']
    ret = []
    #cur = collection.find({"properties.metals.type":u"超声波驱鸟装置"})
    cur = collection.find({
        "_id":ObjectId('533e88cbca49c8156025a895'),
    })
    for i in cur:
        ret.append(i)
    return ret
    
def query4():
    client = MongoClient('localhost', 27017)
    db = client['chat']
    collection = db['users']
    ret = list(collection.find({}))
    return ret
def query4():
    client = MongoClient('yncaiyun.com', 27017)
    db = client['chat']
    # print(db.collection_names())
    collection = db['groups']
    ret = list(collection.find({'description': {'$regex':'^.*' + u'描' + '.*$'}}))
    # ret = list(collection.find({'group_name':  Regex('^.*' + u'描述' + '.*$')}))
    # ret = list(collection.find({'group_name': re.compile(u'^.*' + u'描述' + u'.*$')}))
    # ret = list(collection.find({'group_name': re.compile(u'^.*' + u'a' + u'.*$')}))
    return ret

if __name__ == '__main__':
    ret = query4()
    print(ret)
    # print(re.compile(u'^.*' + u'描述' + u'.*$').findall(u'描述aaaa'))

