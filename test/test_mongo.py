# -*- coding: utf-8 -*-
import os
import sys
import codecs
import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson.timestamp import Timestamp
from pydash import py_ as _

ENCODING = 'utf-8'
ENCODING1 = 'gb18030'
def dec(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
    text, length = gb18030_decode(aStr, 'replace')
    return text
def enc(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
    text, length = gb18030_encode(aStr, 'replace')
    return text
def dec1(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING1)
    text, length = gb18030_decode(aStr, 'replace')
    return text
def enc1(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING1)
    text, length = gb18030_encode(aStr, 'replace')
    return text

def add_mongo_id(obj, objidkeys = ['_id', u'_id',]):
    if isinstance(obj, str) or isinstance(obj, unicode):
        try:
            if len(obj) == 24:
                obj = ObjectId(obj)
        except:
            pass

        d = None
        try:
            d = datetime.datetime.strptime(obj, "%Y-%m-%d %H:%M:%S.%F")
        except:
            try:
                d = datetime.datetime.strptime(obj, "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    d = datetime.datetime.strptime(obj, "%Y-%m-%d")
                except:
                    d = None
        if d:
            obj = d
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            if k in objidkeys and obj[k] is None:
                obj[k] = ObjectId()
            obj[k] = add_mongo_id(obj[k])

    elif isinstance(obj, list):
        for i in obj:
            obj[obj.index(i)] = add_mongo_id(i)
    return obj

def remove_mongo_id(obj):
    if isinstance(obj, ObjectId):
        obj = str(obj)
    elif isinstance(obj, Timestamp):
        obj = obj.as_datetime().strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, datetime.datetime):
        obj = obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = remove_mongo_id(obj[k])
    elif isinstance(obj, list):
        for i in obj:
            obj[obj.index(i)] = remove_mongo_id(i)
    return obj

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
    client = MongoClient('localhost', 27017)
    kmgd = client['kmgd']
    collection = kmgd['network']
    ret = list(collection.find({}))
    ret = remove_mongo_id(ret)
    properties = _.pluck(ret, 'properties')
    # print(names)
    for i in properties:
        if i.has_key('edges') and len(i['edges']):
            print (enc(i['name']))
    # collection = kmgd['network']
    # ret = list(collection.find({'properties.edges':{'$elemMatch':ObjectId('53f306efca49c822ece76641')}}))
    # ret = remove_mongo_id(ret)
    # print(ret)
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
def query5():
    client = MongoClient('yncaiyun.com', 27017)
    db = client['kmgd']
    collection = db['features']
    ret = list(
        collection.find({
            "properties.webgis_type":"point_tower",
            "properties.metals":{
                "$elemMatch":{
                    "type":u"超声波驱鸟装置",
                },
                "$size": 2
            }
            # "properties.metals":{"$size": 3},
        })
    )
    return ret


if __name__ == '__main__':
    query3()

