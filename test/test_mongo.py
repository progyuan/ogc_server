# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import os
import sys
import datetime
import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient


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
    

if __name__ == '__main__':
    ret1 = query1()
    #print(ret)
    print(len(ret1))
    ret2 = query2()
    #print(ret)
    print(len(ret2))
    ret3 = query3()
    print(ret3)
    #print(testdb.collection_names())
    
    
    