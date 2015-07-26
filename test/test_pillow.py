# -*- coding: utf-8 -*-
import os, sys
import  datetime
import time
from PIL import Image
import pymongo
import gridfs

from bson.objectid import ObjectId
from bson.timestamp import Timestamp


ROOT_DIR = ur'F:\work\html\webgis\img\birds'
OUT_DIR = os.path.join(ROOT_DIR,'crop')
OUT_DIR = ur'J:\bird\cropfiles'
OUT_DIR1 = ur'J:\bird\cropfiles1'

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

def get_ext(path):
    return path[path.rindex('.'):]

def crop_one(path, option):
    # print(u'%s: left[%d] top[%d] width[%d] height[%d]' % (path, option['left'],option['top'],option['width'],option['height']))
    im = Image.open(path)
    w, h = im.size
    if option['left'] + option['width'] > w:
        print ('width over large:(%d, %d)' % (w, h))
        return
    if option['top'] + option['height'] > h:
        print ('height over large:(%d, %d)' % (w, h))
        return
    right, bottom = option['left'] + option['width'], option['top'] + option['height']
    im = im.crop((option['left'], option['top'], right, bottom))
    im = im.resize((30, 30), Image.BICUBIC)
    # ext = get_ext(path)
    ext = '.jpg'
    # p = '%s_%d_%d_%d_%d%s' % (os.path.basename(path).replace(ext, ''), option['left'],option['top'],option['width'],option['height'], ext)
    p = '%s_%d_%d_%d_%d_%d%s' % (option['_id'], option['idx'], option['left'],option['top'],option['width'],option['height'], ext)
    p = os.path.join(OUT_DIR, p)
    print ('generating %s...' % p)
    im.save(p, im.format)

def build_options(dirpath):
    ret = []
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
    for i in os.listdir(dirpath):
        path = os.path.join(ROOT_DIR, i)
        if os.path.isfile(path):
            ret.append({'path':path,'option':{'left':50,'top':50,'width':100,'height':100}})
    return ret


def crop_many(dirpath):
    options = build_options(dirpath)
    for i in options:
        crop_one(i['path'], i['option'])


def extract():
    client = pymongo.MongoClient('localhost', 27017)
    db = client['bird']
    collection = db['logs']
    l = list(collection.find({'hasBird':True}))
    # print(len(l))
    data = {}
    for i in l:
        if i.has_key('picture'):
            if len(i['picture']) == 1 and i.has_key('select0'):
                id = str(i['picture'][0])
                data[id] = i['select0']
            if len(i['picture']) == 2 and i.has_key('select0') and i.has_key('select1'):
                id = str(i['picture'][0])
                data[id] = i['select0']
                id = str(i['picture'][1])
                data[id] = i['select1']
    keys = [ObjectId(i) for i in data.keys()]
    # print (keys)
    fs = gridfs.GridFS(db, collection='log')
    cur = fs.find({'_id':{'$in':keys}})
    for f in cur:
        _id = str(f._id)
        for i in data[_id]:
            idx = data[_id].index(i)
            option = {'_id':_id, 'idx':idx}
            option['left'] = i['x']
            option['top'] = i['y']
            option['width'] = i['w']
            option['height'] = i['w']
            try:
                f.seek(0)
                crop_one(f, option)
                # time.sleep(0.5)
            except:
                print ('error in %s-%d:' % (_id, idx))
    client.close()

def random_extract(num):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['bird']
    collection = db['tmp']
    l1 = list(collection.find({}))
    collection1 = db['tmp1']
    l2 = list(collection1.find({}))
    l = []
    l.extend(l1)
    l.extend(l2)
    ids = []
    for i in l:
        ids.extend(i['picture'][-num:])
    ids1 = [ObjectId(i) for i in ids]
    fs = gridfs.GridFS(db, collection='log')
    cur = fs.find({'_id':{'$in':ids1}})
    cnt = 0
    success = 0
    failed = []
    for f in cur:
        cnt += 1
        try:
            f.seek(0)
            im = Image.open(f)
            p = '%s.jpg' % str(f._id)
            if not os.path.exists(OUT_DIR1):
                os.mkdir(OUT_DIR1)
            p = os.path.join(OUT_DIR1, p)
            # print(p)
            im.save(p, im.format)
            success += 1
        except Exception,e:
            failed.append(str(f._id))
            print('failed id = %s' % str(f._id))
    print('total:%d, success:%d' % (cnt, success))
    print('failed:%s' % str(failed))

    client.close()




if __name__=="__main__":
    # crop_many(ROOT_DIR)
    random_extract(50)
