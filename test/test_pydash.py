# -*- coding: utf-8 -*-

import os, sys
import codecs
import json
import pymongo
from pydash import py_ as _

STATICRESOURCE_DIR = ur'F:\work\html\webgis'

def get_collection(collection):
    ret = None
    client = pymongo.MongoClient('192.168.1.8', 27017)
    # client = pymongo.MongoClient('localhost', 27017)
    db = client['kmgd']
    if not collection in db.collection_names(False):
        ret = db.create_collection(collection)
    else:
        ret = db[collection]
    return ret

def get_occur_p(line_name, name, value=None):
    ret = 0.0
    collection = get_collection('state_examination')
    l = list(collection.find({'line_name':line_name}))
    totalcnt = len(l)
    cnt = 0
    if totalcnt>0:
        for i in l:
            if len(name)>4 and name[:5] == 'unit_':
                if i.has_key(name) and i[name] == value:
                    cnt += 1
            if len(name)>8 and name[:8] == 'unitsub_':
                id = name[8:]
                if i.has_key('unitsub'):
                    for j in i['unitsub']:
                        if j['id'] == id:
                            cnt += 1
        ret = float(cnt)/float(totalcnt)
    return ret

def check_has_subunit(alist, line_name, unit):
    ret = []
    children = _.result(_.find(alist, {'unit':unit}), 'children')
    ids = _.pluck(children, 'id')
    ids = _.map(ids, lambda x:'unitsub_' + x)
    for id in ids:
        p = get_occur_p(line_name, id)
        if p>0:
            ret.append(id)
    return ret

def get_template_v(alist, unit, id, key):
    ret = None
    children = _.result(_.find(alist, {'unit':unit}), 'children')
    if children:
        p0 = _.result(_.find(children, {'id':id}), key)
        if p0:
            ret = p0
    return ret

def testjson():
    ret = []
    with codecs.open(ur'd:\testjson.json', 'r',  'utf-8-sig') as f:
        ret = json.loads(f.read())
    return ret

def getlvl(unit, total_score):
    ret = 'I'
    if unit == 'unit_1' or  unit == 'unit_4':
        if total_score <= 10:
            ret = 'I'
        if total_score >= 12 and  total_score <= 24:
            ret = 'II'
        if total_score >= 30 and total_score <= 32:
            ret = 'II'
        if total_score == 40:
            ret = 'IV'
    if unit == 'unit_2' or unit == 'unit_6' or unit == 'unit_8':
        if total_score <= 10:
            ret = 'I'
        if total_score >= 12 and  total_score <= 24:
            ret = 'II'
        if total_score >= 30 and  total_score <= 32:
            ret = 'III'
        if total_score == 40:
            ret = 'IV'
    if unit == 'unit_3':
        if total_score <= 10:
            ret = 'I'
        if total_score >= 12 and  total_score <= 24:
            ret = 'II'
        if total_score >= 30 and total_score <= 32:
            ret = 'III'
        if total_score == 40:
            ret = 'IV'

    if unit == 'unit_5' or unit == 'unit_7':
        if total_score <= 10:
            ret = 'I';
        if total_score >= 12 and total_score <= 24:
            ret = 'II'
        if total_score >= 30 and total_score <= 32:
            ret = 'III'
        if total_score == 40:
            ret = 'IV'
    return ret

def test1(line_name):
    standard_template = []
    with codecs.open(os.path.join(STATICRESOURCE_DIR, 'standard_template2009.json'), 'r', 'utf-8-sig') as f:
        standard_template = json.loads(f.read())
    ret = testjson()
    for linestate in ret:
        idx0 = ret.index(linestate)
        line_state = linestate['line_state']
        for res in linestate['result']:
            idx = linestate['result'].index(res)
            if res['name'][:8] == 'unitsub_':
                id = res['name'][8:]
                unit = res['name'][8:14]
                p0 = get_template_v(standard_template, unit, id, 'p0')
                total_score = int(get_template_v(standard_template, unit, id, 'total_score'))
                if p0:
                    # res['p'] = p0[getlvl(unit, total_score)] * get_occur_p(line_name, res['name']) * 10.0
                    res['p'] = p0[line_state] * get_occur_p(line_name, res['name']) * 10.0
                    if res['p'] > 1.0:
                        res['p'] = 1.0
                linestate['result'][idx] = res
        ret[idx0] = linestate
    with codecs.open(ur'd:\testjson1.json', 'w', 'utf-8-sig') as f:
        f.write(json.dumps(ret, ensure_ascii=True, indent=4))






def test():
    standard_template = []
    with codecs.open(os.path.join(STATICRESOURCE_DIR, 'standard_template2009.json'), 'r', 'utf-8-sig') as f:
        standard_template = json.loads(f.read())
    units = _.pluck(standard_template, 'unit')
    for un in units:
        print (check_has_subunit(standard_template, u'东大茨线', un))


if __name__ == '__main__':
    test1(u'东大茨线')
    