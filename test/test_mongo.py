# -*- coding: utf-8 -*-
import os
import sys
import codecs
import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson.timestamp import Timestamp
import xlrd, xlwt
import json
import math
import re
from pydash import py_ as _
from pinyin import PinYin

gPinYin = None
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
    db = client['kmgd']
    collection = db['network']
    ret = list(collection.find({
        '$or': [
            {'properties.py': {'$regex': u'^.*ql.*$'}},
            {'properties.name': {'$regex': u'^.*ql.*$'}}
        ],
        'properties.name':
            {
                '$in': [
                    u'\u8349\u6d77\u7ebf',
                    u'\u4e03\u7f57II\u56de',
                    u'\u4e03\u7f57I\u56de',
                    u'\u5382\u4e0aI\u3001II\u56de',
                    u'\u5382\u4e2d\u7ebf',
                    u'\u6606\u8f66I\u56de',
                    u'\u6606\u8f66II\u56de',
                    u'\u4e03\u4e1cII\u56de',
                    u'\u4e03\u4e1cI\u56de',
                    u'\u4e03\u677eI\u3001II\u56de',
                    u'\u6743\u9a6cII\u56de',
                    u'\u4e1c\u5927\u7ebf',
                    u'\u9752\u77f3\u8def\u7ebf',
                    u'\u4e03\u82b1I\u56de',
                    u'\u82b1\u9752II\u56de'
                ]
            },
        'properties.webgis_type':u'polyline_line'

    }))
    return ret
def query5():
    client = MongoClient('yncaiyun.com', 27017)
    db = client['chat']
    # print(db.collection_names())
    collection = db['groups']
    ret = list(collection.find({'description': {'$regex':'^.*' + u'描' + '.*$'}}))
    # ret = list(collection.find({'group_name':  Regex('^.*' + u'描述' + '.*$')}))
    # ret = list(collection.find({'group_name': re.compile(u'^.*' + u'描述' + u'.*$')}))
    # ret = list(collection.find({'group_name': re.compile(u'^.*' + u'a' + u'.*$')}))
    return ret
def query6():
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

def test_combine():
    client = MongoClient('localhost', 27017)
    db = client['kmgd']
    collection = db['network']
    others = []
    nodes = []
    others.append(collection.find_one({'properties.name':u'10kV龙马路线'}))
    others.append(collection.find_one({'properties.name':u'10kV州城Ⅴ回线39号杆T康井路北段'}))
    others.append(collection.find_one({'properties.name':u'10kV州城Ⅴ回线39号杆T康井路南段线'}))
    others.append(collection.find_one({'properties.name':u'10kV金家边线T10kV太极路线'}))
    others.append(collection.find_one({'properties.name':u'10kV州城Ⅴ回线52号杆塔T太极路'}))
    others.append(collection.find_one({'properties.name':u'10kV州城Ⅴ回线57号塔T徐百户屯'}))
    zc = collection.find_one({'properties.name':u'10kV州城Ⅴ回线'})
    for other in others:
        for node in other['properties']['nodes']:
            if not nodes in nodes:
                nodes.append(node)
    for i in nodes:
        if not i in zc['properties']['nodes']:
            zc['properties']['nodes'].append(i)
    collection.save(zc)
    print (len(nodes))

def test_add_field():
    XLS_FILE = ur'D:\2014项目\配电网故障定位\20151128\节点数据.xls'
    book = xlrd.open_workbook(XLS_FILE)
    startrowidx = 1
    namelist = []
    for sheet in book.sheets():
        for row in range(startrowidx, sheet.nrows):
            name = sheet.cell_value(row, 0)
            code = sheet.cell_value(row, 1)
            namelist.append({'name':name, 'code':code})
        break

    names = _.pluck(namelist, 'name')
    print(len(names))
    client = MongoClient('localhost', 27017)
    db = client['kmgd']
    collection = db['features']
    l = list(collection.find({'properties.name':{'$in':names}}))
    # print(len(l))
    # # name_code_mapping = []
    # for i in l:
    #     code = _.result(_.find(namelist,  {'name':i['properties']['name']}), 'code')
    #     # cl.append(code)
    #     i['properties']['code_name'] = code
    #     # o = {}
    #     # o['name'] = code
    #     # o['_id'] = str(i['_id'])
    #     # name_code_mapping.append(o)
    #     collection.save(i)
    # # print(json.dumps(name_code_mapping, ensure_ascii=True, indent=4))

    # ids = []
    # for i in l:
    #     ids.append(i['_id'])
    # collection = db['edges']
    # tids = set()
    # for id in ids:
    #     ll = list(collection.find({'$or':[{'properties.start':id},{'properties.end':id}]}))
    #     for ii in ll:
    #         if ii['properties']['start'] == id:
    #             tids.add(ii['properties']['end'])
    #         if ii['properties']['end'] == id:
    #             tids.add(ii['properties']['start'])
    # tids = list(tids)
    # ids.extend(tids)
    # ids = list(set(ids))
    linename = u'10kV州城Ⅴ回线'
    collection = db['network']
    zc = collection.find_one({'properties.name':linename})
    if not ObjectId('5657b187d8b95a18a48c4a62') in zc['properties']['nodes']:
        zc['properties']['nodes'].append(ObjectId('5657b187d8b95a18a48c4a62'))
    if not ObjectId('5656aa13d8b95a0a485fbaa7') in zc['properties']['nodes']:
        zc['properties']['nodes'].append(ObjectId('5656aa13d8b95a0a485fbaa7'))
    collection.save(zc)

def test_add_edge():
    XLS_FILE = ur'D:\2014项目\配电网故障定位\20151128\节点数据.xls'
    book = xlrd.open_workbook(XLS_FILE)
    startrowidx = 1
    codelist = []
    sheet = book.sheet_by_index(1)
    startrowidx = 1
    for row in range(startrowidx, sheet.nrows):
        codelist.append({'start':sheet.cell_value(row, 0).strip(), 'end':sheet.cell_value(row, 2).strip()})
    print(codelist)

    client = MongoClient('localhost', 27017)
    db = client['kmgd']
    collection_edges = db['edges']
    collection_features = db['features']
    for pair in codelist:
        starts = list(collection_features.find({'properties.code_name':pair['start']}))
        ends = list(collection_features.find({'properties.code_name':pair['end']}))
        if len(starts) and len(ends):
            for start in starts:
                for end in ends:
                    edge = collection_edges.find_one({'properties.start':start['_id'], 'properties.end':end['_id']})
                    if edge is None:
                        edge = {'properties':{'webgis_type':'edge_dn','start':start['_id'], 'end':end['_id']}}
                        print('add %s->%s' % (pair['start'], pair['end']))
                        collection_edges.save(edge)

def test_filter_tower():
    client = MongoClient('localhost', 27017)
    db = client['kmgd']
    collection = db['network']
    collection_features = db['features']
    linename = u'10kV州城Ⅴ回线'
    zc = collection.find_one({'properties.name':linename})
    ids = []
    for id in zc['properties']['nodes']:
        t = collection_features.find_one({'_id':id})
        if t:
            if not t['properties']['webgis_type'] == 'point_tower':
                ids.append(id)
    zc['properties']['nodes'] = ids
    collection.save(zc)
    # print(len(ids))

def geodistance(origin, destination):
    lon1, lat1 = origin
    lon2, lat2 = destination
    radius = 6371.0 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

def test_calc_distance():
    XLS_FILE = ur'D:\2014项目\配电网故障定位\20151128\节点数据.xls'
    book = xlrd.open_workbook(XLS_FILE)
    startrowidx = 1
    codelist = []
    sheet = book.sheet_by_index(1)
    startrowidx = 1
    for row in range(startrowidx, sheet.nrows):
        codelist.append({'start':sheet.cell_value(row, 0).strip(), 'end':sheet.cell_value(row, 2).strip()})
    print(codelist)

    client = MongoClient('localhost', 27017)
    db = client['kmgd']
    collection_edges = db['edges']
    collection_features = db['features']
    for pair in codelist:
        start = collection_features.find_one({'properties.code_name':pair['start'],
                                              'properties.webgis_type':'point_dn'})
        end = collection_features.find_one({'properties.code_name':pair['end'],  'properties.webgis_type':'point_dn'})
        if start and end:
            lng1, lat1 = start['geometry']['coordinates'][0], start['geometry']['coordinates'][1]
            lng2, lat2 = end['geometry']['coordinates'][0], start['geometry']['coordinates'][1]
            d = geodistance((lng1, lat1),(lng2, lat2))
            print('%s,%s,%d' % (start['properties']['code_name'], end['properties']['code_name'], int(d*1000)))

def test_add_ht7():
    client = MongoClient('localhost', 27017)
    db = client['kmgd']
    collection = db['network']
    linename = u'10kV州城Ⅴ回线'
    zc = collection.find_one({'properties.name':linename})
    if not ObjectId('564e953cd8b95a144c6c2172') in zc['properties']['nodes']:
        print('not in ')
        zc['properties']['nodes'].append(ObjectId('564e953cd8b95a144c6c2172'))
    collection.save(zc)

def test_build_map():
    client = MongoClient('localhost', 27017)
    db = client['kmgd']
    collection = db['network']
    collection_fea = db['features']
    linename = u'10kV州城Ⅴ回线'
    zc = collection.find_one({'properties.name':linename})
    l = list(collection_fea.find({'_id':{'$in':zc['properties']['nodes']}}))
    # print(len(l))
    name_code_mapping = []
    for i in l:
        if i['properties'].has_key('code_name'):
            o = {}
            o['idx'] = i['properties']['code_name']
            o['name'] = i['properties']['code_name']
            o['_id'] = str(i['_id'])
            name_code_mapping.append(o)
    #     collection.save(i)
    print(json.dumps(name_code_mapping, ensure_ascii=True, indent=4))

def test_algorithm():
    def find_next_by_node(features, collection_edges, alist=[], id=None):
        if isinstance(id, str):
            id = add_mongo_id(id)
        l = _.deep_pluck(list(collection_edges.find({'properties.start':id})),'properties.end')
        for i in l:
            obj = _.find(features, {'_id': i})
            if obj and obj.has_key('properties'):
                if obj['properties'].has_key('devices'):
                    alist.append(obj['_id'])
                else:
                    alist = find_next_by_node(features, collection_edges, alist, obj['_id'])
        return alist
    def find_chain(features, collection_edges, alist=[], id=None):
        _ids = find_next_by_node(features, collection_edges, [], id)
        for _id in _ids:
            obj = _.find(features, {'_id':_id})
            if obj :
                from_index = _.find_index(features, {'_id':id})
                to_index = _.find_index(features, {'_id':_id})
                if obj.has_key('properties') and obj['properties'].has_key('devices'):
                    alist.append({
                        'lnbr_idx': len(alist) + 1,
                        'from_id': add_mongo_id(id),
                        'to_id': obj['_id'],
                        # 'from_idx': from_index,
                        # 'to_idx': to_index,
                    })
                alist = find_chain(features, collection_edges, alist, obj['_id'])
        return alist


    def find_prev(collection_edges, id):
        ret = None
        one = collection_edges.find_one({'properties.end': id})
        if one:
            ret = one['properties']['start']
        return ret


    def find_next(collection_edges, id):
        ret = None
        one = collection_edges.find_one({'properties.start': id})
        if one:
            ret = one['properties']['end']
        return ret


    def find_first(collection_edges, alist):
        ids = _.pluck(alist, '_id')
        id = alist[0]['_id']
        prev_id = None
        while id and id in ids:
            prev_id = id
            id = find_prev(collection_edges, prev_id)
        return prev_id

    def write_excel_lnbr(features_all, chains, filename):
        wb = xlwt.Workbook()
        # print(dir(wb))
        for chain in chains:
            ws = wb.add_sheet(str(len(wb._Workbook__worksheets) + 1))
            columns = [
                '_001_LnBR',
                '_002_Bus_from',
                '_003_Bus_to',
                '_004_R',
                '_005_X',
                '_006_B_1_2',
                '_007_kVA',
                '_008_State',
            ]
            for col in columns:
                ws.write(0, columns.index(col), col)
            for i in chain:
                row = chain.index(i) + 1
                ws.write(row, 0, str(i['lnbr_idx']))
                from_obj = _.find(features_all, {'_id':i['from_id']})
                to_obj = _.find(features_all, {'_id':i['to_id']})
                from_name = from_obj['properties']['name']
                from_id = remove_mongo_id(from_obj['_id'])
                # from_idx = i['from_idx']
                to_name = to_obj['properties']['name']
                to_id = remove_mongo_id(to_obj['_id'])
                # to_idx = i['to_idx']
                # ws.write(row, 1, from_name)
                # ws.write(row, 2, to_name)
                ws.write(row, 1, from_id)
                ws.write(row, 2, to_id)
        wb.save(filename)
    def write_excel_bus(features_all, chains, filename):
        wb = xlwt.Workbook()
        # print(dir(wb))
        for chain in chains:
            ws = wb.add_sheet(str(len(wb._Workbook__worksheets) + 1))
            columns = [
                '_001_No',
                '_002_Type',
                '_003_MW',
                '_004_Mvar',
                '_005_GS',
                '_006_Bs',
                '_007_Mag',
                '_008_Deg',
            ]
            for col in columns:
                ws.write(0, columns.index(col), col)
            for i in chain:
                row = chain.index(i) + 1
                obj = _.find(features_all, {'_id': i['from_id']})
                # name = obj['properties']['name']
                id = obj['_id']
                # from_idx = i['from_idx']
                # ws.write(row, 0, name)
                ws.write(row, 0, remove_mongo_id(id))
                # ws.write(row, 0, from_idx)
                if row == 1:
                    ws.write(row, 1, 3)
                else:
                    ws.write(row, 1, 1)
                if row == len(chain):
                    obj1 = _.find(features_all, {'_id': i['to_id']})
                    # name1 = obj1['properties']['name']
                    id1 = obj1['_id']
                    # to_idx = i['to_idx']
                    # ws.write(row+1, 0, name1)
                    ws.write(row + 1, 0, remove_mongo_id(id1))
                    # ws.write(row + 1, 0, to_idx)
                    ws.write(row+1, 1, 1)
        wb.save(filename)

    client = MongoClient('localhost', 27017)
    db = client['kmgd_pe']
    collection_network = db['network']
    collection_fea = db['features']
    collection_edges = db['edges']

    # line_ids = ['570ce0c1ca49c80858320619', '570ce0c1ca49c8085832061a']
    # 坪掌寨线
    ids0 = collection_network.find_one({'_id':add_mongo_id('570ce0c1ca49c8085832061a')})['properties']['nodes']
    features_all = list(collection_fea.find({'_id':{'$in':ids0}}))
    line_ids = _.pluck(list(collection_network.find({'$and':[{'properties.py': {'$regex': '^pzzx.*$'}}, {'properties.py': {'$not': re.compile('^pzzx$')}}]})), '_id')
    # print(line_ids)
    chains = []
    for i in line_ids:
        line = collection_network.find_one({'_id':i})
        if line and line['properties'].has_key('nodes'):
            features = list(collection_fea.find({'_id':{'$in':add_mongo_id(line['properties']['nodes'])}}))
            first_id = find_first(collection_edges, features)
            if first_id:
                first =  _.find(features, {'_id': first_id})
                if first:
                    chain = find_chain(features, collection_edges, [], first_id)
                    print(first['properties']['name'])
                    print(len(chain))
                    chains.append(chain)
    write_excel_lnbr(features_all, chains, 'data_lnbr_pzz.xls')
    write_excel_bus(features_all, chains, 'data_bus_pzz.xls')
    # chains = []
    # line = collection_network.find_one({'_id': add_mongo_id('570ce0c1ca49c8085832061a')})
    # if line and line['properties'].has_key('nodes'):
    #     first_id = add_mongo_id('570ce0b7ca49c8085832018f')
    #     chain = find_chain(features_all, collection_edges, [], first_id)
    #     chains.append(chain)
    # write_excel_lnbr(features_all, chains, 'data_lnbr_pzz0.xls')






    # first = ['570ce0b7ca49c8085832018f', '570ce0c1ca49c8085832031b']
    #酒房丫口线
    chains = []
    ids0 = collection_network.find_one({'_id': add_mongo_id('570ce0c1ca49c80858320619')})['properties']['nodes']
    features_all = list(collection_fea.find({'_id': {'$in': ids0}}))
    line_ids = _.pluck(list(collection_network.find( {'$and': [{'properties.py': {'$regex': '^jfykx.*$'}}, {'properties.py': {'$not': re.compile('^jfykx$')}}]})), '_id')
    # print(line_ids)
    for i in line_ids:
        line = collection_network.find_one({'_id': i})
        if line and line['properties'].has_key('nodes'):
            features = list(collection_fea.find({'_id': {'$in': add_mongo_id(line['properties']['nodes'])}}))
            first_id = find_first(collection_edges, features)
            if first_id:
                first = _.find(features, {'_id': first_id})
                if first:
                    chain = find_chain(features, collection_edges, [], first_id)
                    print(first['properties']['name'])
                    print(len(chain))
                    chains.append(chain)
    write_excel_lnbr(features_all, chains, 'data_lnbr_jfyk.xls')
    write_excel_bus(features_all, chains, 'data_bus_jfyk.xls')
    # chains = []
    # line = collection_network.find_one({'_id': add_mongo_id('570ce0c1ca49c80858320619')})
    # if line and line['properties'].has_key('nodes'):
    #     first_id = add_mongo_id('570ce0c1ca49c8085832031b')
    #     chain = find_chain(features_all, collection_edges, [], first_id)
    #     chains.append(chain)
    # write_excel_lnbr(features_all, chains, 'data_lnbr_jfyk0.xls')

def sortlist(collection_edges, alist):
    def find_prev(id):
        ret = None
        one = collection_edges.find_one({'properties.end':id})
        if one:
            ret = one['properties']['start']
        return ret
    def find_next(id):
        ret = None
        one = collection_edges.find_one({'properties.start':id})
        if one:
            ret = one['properties']['end']
        return ret
    def find_first(alist):
        ids = _.pluck(alist, '_id')
        id = alist[0]['_id']
        prev_id = None
        while id and id in ids:
            prev_id = id
            id = find_prev(prev_id)
        return prev_id
    def find_chain(alist, obj):
        ids = _.pluck(alist, '_id')
        chainlist = []
        while obj:
            chainlist.append(obj)
            nst_id = find_next(obj['_id'])
            if nst_id:
                obj = _.find(alist, {'_id': nst_id})
            else:
                obj = None
        return chainlist
    first_id =  find_first(alist)
    # ids = _.map_(_.pluck(alist, '_id'), lambda x:remove_mongo_id(x))
    # print(ids)
    # print(_.index_of(ids, remove_mongo_id(first_id)))
    first = _.find(alist, {'_id': first_id})
    chainlist = []
    if first:
        chainlist = find_chain(alist, first)
    return chainlist





def test_pzzx():#坪掌寨线
    piny = get_pinyin_data()
    client = MongoClient('localhost', 27017)
    db = client['kmgd_pe']
    collection_fea = db['features']
    collection_network = db['network']
    collection_edges = db['edges']
    one = collection_network.find_one({'_id':add_mongo_id('570ce0c1ca49c8085832061a')})
    branches = []
    print(len(one['properties']['nodes']))
    l = list(collection_fea.find({'properties.py': {'$regex': '^.*sslzx.*$'}})) #松山林支线
    # print(len(l))
    l = sortlist(collection_edges, l)
    branches.extend(_.pluck(l, '_id'))
    s = ','.join(_.deep_pluck(l, 'properties.name'))
    print(u'松山林支线%d, [%s]' % (len(l), s))
    name = u'坪掌寨线松山林支线'
    o = {'properties': {
        'name': name,
        'py': piny.hanzi2pinyin_first_letter(
            name.replace('#', '').replace('II', u'二').replace('I', u'一').replace(u'Ⅱ', u'二').replace(u'Ⅰ', u'一')),
        'voltage': '12',
        'webgis_type': 'polyline_dn',
        'nodes': _.pluck(l, '_id')
    }}
    # print(o)
    collection_network.insert(o)
    l = list(collection_fea.find({'properties.py': {'$regex': '^.*mdszx.*$'}}))  # 忙肚山支线
    l = sortlist(collection_edges, l)
    branches.extend(_.pluck(l, '_id'))
    s = ','.join(_.deep_pluck(l, 'properties.name'))
    print(u'忙肚山支线%d, [%s]' % (len(l), s))
    name = u'坪掌寨线忙肚山支线'
    o = {'properties': {
        'name': name,
        'py': piny.hanzi2pinyin_first_letter(
            name.replace('#', '').replace('II', u'二').replace('I', u'一').replace(u'Ⅱ', u'二').replace(u'Ⅰ', u'一')),
        'voltage': '12',
        'webgis_type': 'polyline_dn',
        'nodes': _.pluck(l, '_id')
    }}
    # print(o)
    collection_network.insert(o)
    l = list(collection_fea.find({'properties.py': {'$regex': '^.*mdszx.*$'}}))  # 大河边支线
    l = sortlist(collection_edges, l)
    branches.extend(_.pluck(l, '_id'))
    s = ','.join(_.deep_pluck(l, 'properties.name'))
    print(u'大河边支线%d, [%s]' % (len(l), s))
    name = u'坪掌寨线大河边支线'
    o = {'properties': {
        'name': name,
        'py': piny.hanzi2pinyin_first_letter(
            name.replace('#', '').replace('II', u'二').replace('I', u'一').replace(u'Ⅱ', u'二').replace(u'Ⅰ', u'一')),
        'voltage': '12',
        'webgis_type': 'polyline_dn',
        'nodes': _.pluck(l, '_id')
    }}
    # print(o)
    collection_network.insert(o)
    l = list(collection_fea.find({'properties.py': {'$regex': '^.*xdtzx.*$'}}))  #下大田支线
    l = sortlist(collection_edges, l)
    branches.extend(_.pluck(l, '_id'))
    s = ','.join(_.deep_pluck(l, 'properties.name'))
    print(u'下大田支线%d, [%s]' % (len(l), s))
    name = u'坪掌寨线下大田支线'
    o = {'properties': {
        'name': name,
        'py': piny.hanzi2pinyin_first_letter(
            name.replace('#', '').replace('II', u'二').replace('I', u'一').replace(u'Ⅱ', u'二').replace(u'Ⅰ', u'一')),
        'voltage': '12',
        'webgis_type': 'polyline_dn',
        'nodes': _.pluck(l, '_id')
    }}
    # print(o)
    collection_network.insert(o)
    l = list(collection_fea.find({'properties.py': {'$regex': '^pzzxN.*$'}}))
    ids = _.pluck(l, '_id')
    main_ids = _.difference(ids, branches)
    print('len(main_ids)=%d' % len(main_ids))
    l = list(collection_fea.find({'_id': {'$in': main_ids}}))  # 坪掌寨线
    l = sortlist(collection_edges, l)
    s = ','.join(_.deep_pluck(l, 'properties.name'))
    print(u'坪掌寨线%d, [%s]' % (len(l), s))
    name = u'坪掌寨线主线'
    o = {'properties': {
        'name': name,
        'py': piny.hanzi2pinyin_first_letter(
            name.replace('#', '').replace('II', u'二').replace('I', u'一').replace(u'Ⅱ', u'二').replace(u'Ⅰ', u'一')),
        'voltage': '12',
        'webgis_type': 'polyline_dn',
        'nodes': _.pluck(l, '_id')
    }}
    collection_network.insert(o)

def get_pinyin_data():
    global gPinYin
    if gPinYin is None:
        pydatapath =  'pinyin_word.data'
        gPinYin =  PinYin(pydatapath)
        gPinYin.load_word()
    return gPinYin

def test_jfykx():#酒房丫口线
    piny = get_pinyin_data()
    client = MongoClient('localhost', 27017)
    db = client['kmgd_pe']
    collection_fea = db['features']
    collection_network = db['network']
    collection_edges = db['edges']
    one = collection_network.find_one({'_id': add_mongo_id('570ce0c1ca49c80858320619')})
    # print(len(one['properties']['nodes']))
    branches = []
    l = list(collection_fea.find({'properties.py': {'$regex': '^.*dhpzzx.*$'}}))  # 大河平掌支线
    l = sortlist(collection_edges, l)
    branches.extend(_.pluck(l, '_id'))
    s = ','.join(_.deep_pluck(l, 'properties.name'))
    print(u'大河平掌支线%d, [%s]' % (len(l), s))
    name = u'酒房丫口线大河平掌支线'
    o = {'properties':{
        'name':name,
        'py':piny.hanzi2pinyin_first_letter(name.replace('#','').replace('II',u'二').replace('I',u'一').replace(u'Ⅱ',u'二').replace(u'Ⅰ',u'一')),
        'voltage':'12',
        'webgis_type':'polyline_dn',
        'nodes':_.pluck(l, '_id')
    }}
    # print(o)
    collection_network.insert(o)
    l = list(collection_fea.find({'properties.py': {'$regex': '^.*bszzx.*$'}}))  # 控制半山寨支线
    l = sortlist(collection_edges, l)
    branches.extend(_.pluck(l, '_id'))
    s = ','.join(_.deep_pluck(l, 'properties.name'))
    print(u'控制半山寨支线%d, [%s]' % (len(l), s))
    name = u'酒房丫口线控制半山寨支线'
    o = {'properties': {
        'name': name,
        'py': piny.hanzi2pinyin_first_letter(
            name.replace('#', '').replace('II', u'二').replace('I', u'一').replace(u'Ⅱ', u'二').replace(u'Ⅰ', u'一')),
        'voltage': '12',
        'webgis_type': 'polyline_dn',
        'nodes': _.pluck(l, '_id')
    }}
    # print(o)
    collection_network.insert(o)
    l = list(collection_fea.find({'properties.py': {'$regex': '^.*mchzx.*$'}}))  # 控制马草河支线支线
    l = sortlist(collection_edges, l)
    branches.extend(_.pluck(l, '_id'))
    s = ','.join(_.deep_pluck(l, 'properties.name'))
    print(u'控制马草河支线%d, [%s]' % (len(l), s))
    name = u'酒房丫口线控制马草河支线'
    o = {'properties': {
        'name': name,
        'py': piny.hanzi2pinyin_first_letter(
            name.replace('#', '').replace('II', u'二').replace('I', u'一').replace(u'Ⅱ', u'二').replace(u'Ⅰ', u'一')),
        'voltage': '12',
        'webgis_type': 'polyline_dn',
        'nodes': _.pluck(l, '_id')
    }}
    # print(o)
    collection_network.insert(o)
    l = list(collection_fea.find({'properties.py': {'$regex': '^.*dpzzx.*$'}}))  # 大平掌支线
    l = sortlist(collection_edges, l)
    branches.extend(_.pluck(l, '_id'))
    s = ','.join(_.deep_pluck(l, 'properties.name'))
    print(u'大平掌支线%d, [%s]' % (len(l), s))
    name = u'酒房丫口线大平掌支线'
    o = {'properties': {
        'name': name,
        'py': piny.hanzi2pinyin_first_letter(
            name.replace('#', '').replace('II', u'二').replace('I', u'一').replace(u'Ⅱ', u'二').replace(u'Ⅰ', u'一')),
        'voltage': '12',
        'webgis_type': 'polyline_dn',
        'nodes': _.pluck(l, '_id')
    }}
    # print(o)
    collection_network.insert(o)
    l = list(collection_fea.find({'properties.py': {'$regex': '^.*bjzx.*$'}}))  # 碧鸡支线
    l = sortlist(collection_edges, l)
    branches.extend(_.pluck(l, '_id'))
    s = ','.join(_.deep_pluck(l, 'properties.name'))
    print(u'碧鸡支线%d, [%s]' % (len(l), s))
    name = u'酒房丫口线碧鸡支线'
    o = {'properties': {
        'name': name,
        'py': piny.hanzi2pinyin_first_letter(
            name.replace('#', '').replace('II', u'二').replace('I', u'一').replace(u'Ⅱ', u'二').replace(u'Ⅰ', u'一')),
        'voltage': '12',
        'webgis_type': 'polyline_dn',
        'nodes': _.pluck(l, '_id')
    }}
    # print(o)
    collection_network.insert(o)
    l = list(collection_fea.find({'properties.py': {'$regex': '^jfykxN.*$'}}))
    ids = _.pluck(l, '_id')
    main_ids = _.difference(ids, branches)
    print('len(main_ids)=%d' % len(main_ids))
    l = list(collection_fea.find({'_id': {'$in': main_ids}}))  # 酒房丫口线
    l = sortlist(collection_edges, l)
    s = ','.join(_.deep_pluck(l, 'properties.name'))
    print(u'酒房丫口线%d, [%s]' % (len(l), s))
    name = u'酒房丫口线主线'
    o = {'properties': {
        'name': name,
        'py': piny.hanzi2pinyin_first_letter(
            name.replace('#', '').replace('II', u'二').replace('I', u'一').replace(u'Ⅱ', u'二').replace(u'Ⅰ', u'一')),
        'voltage': '12',
        'webgis_type': 'polyline_dn',
        'nodes': _.pluck(l, '_id')
    }}
    collection_network.insert(o)

def test_trim():
    client = MongoClient('localhost', 27017)
    db = client['kmgd_pe']
    collection_fea = db['features']
    collection_network = db['network']
    collection_edges = db['edges']
    nodes = []
    collection_network.remove({'_id': {'$nin': add_mongo_id(['570ce0c1ca49c80858320619', '570ce0c1ca49c8085832061a'])}})
    # l = list(collection_network.find({'_id':{'$nin':add_mongo_id(['570ce0c1ca49c80858320619', '570ce0c1ca49c8085832061a'])}}))
    # for i in l:
    #     if i['properties'].has_key('nodes'):
    #         nodes.extend(i['properties']['nodes'])
    # print(len(nodes))
    collection_fea.remove({'_id':{'$in':nodes}})
    collection_edges.remove({'$or':[{'properties.start':{'$in':nodes}}, {'properties.end':{'$in':nodes}}]})
    # ll = list(collection_edges.find({'$or': [{'properties.start': {'$in': nodes}}, {'properties.end': {'$in': nodes}}]}))
    # print(len(ll))

if __name__ == '__main__':
    # pass
    # test_algorithm()
    # pass
    # test_pzzx()
    # test_jfykx()
    # test_trim()
    for i in query4():
        print(i['properties']['name'])

