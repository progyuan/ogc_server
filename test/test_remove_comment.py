# -*- coding: utf-8 -*-

import os,sys
import db_util
import json
from bson.objectid import ObjectId
from bson import BSON

JSONFILE = ur'D:\2014项目\km_towers.json'
JSONFILE1 = ur'D:\2014项目\km_towers1.json'
JSONFILE2 = ur'D:\2014项目\km_line.json'

def remove_comment():
    l = []
    with open(JSONFILE) as f:
        l = f.readlines()
        #print(len(l))
    ll = []
    for i in l:
        if '/*' in i:
            continue
        ll.append(i)
    s = ''.join(ll)
    with open(JSONFILE1, 'w') as f:
        f.write(s)

def flatten():
    def get_vol_name(towerid, lines, codes):
        ret = ''
        for line in lines:
            if towerid in line['properties']['nodes']:
                c = line['properties']['voltage']
                if codes['voltage_level'].has_key(c):
                    ret = codes['voltage_level'][c]
                    break
        return ret    
        
    db_util.init_global()
    towers = db_util.mongo_find('kmgd', 'features', conditions={"properties.webgis_type":"point_tower", "geometry2d.type":"Point"})
    lines = db_util.mongo_find('kmgd', 'network', conditions={"properties.webgis_type":"polyline_line"})
    codes = db_util.mongo_find_one('kmgd', 'codes', {})
    ll = []
    #print(len(l))
    for i in towers:
        o = {}
        tower_id = i['_id']
        
        o['_id'] = ObjectId(tower_id)
        o['lng'] = i['geometry']['coordinates'][0]
        o['lat'] = i['geometry']['coordinates'][1]
        o['name'] = i['properties']['name']
        o['voltage'] = get_vol_name(tower_id, lines, codes)
        ll.append(unicode(o).replace(' u', ''))
    s = '\n'.join(ll)
    with open(JSONFILE1, 'w') as f:
        f.write(s)
        
def flatten2():
    db_util.init_global()
    l = db_util.mongo_find('kmgd', 'network', conditions={"properties.webgis_type":"polyline_line"})
    
    ll = []
    print(len(l))
    for i in l:
        o = {}
        o['nodes'] = i['properties']['nodes']
        lll = [ObjectId(ii) for ii in o['nodes']]
        o['nodes'] = lll
        o['name'] = i['properties']['name']
        ll.append(unicode(o).replace(' u', ''))
    s = '\n'.join(ll)
    with open(JSONFILE2, 'w') as f:
        f.write(s)
        
        
if __name__=="__main__":
    flatten()
    
    
    