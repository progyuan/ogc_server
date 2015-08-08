# -*- coding: utf-8 -*-
import codecs
import os, sys, time, datetime
import traceback
import uuid
import math
import shutil
import subprocess

from collections import OrderedDict
import decimal
import json
import urllib
import urllib2
import StringIO
import re
import gzip
#import sqlite3
import base64
import random
from optparse import OptionParser
from collections import OrderedDict
import gevent


import configobj
from pymongo import MongoClient, ReadPreference
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
import gridfs
from module_locator import module_path, ENCODING, ENCODING1, dec, dec1, enc, enc1



try:
    import numpy as np
except:
    print('numpy import error')
try:
    from lxml import etree
except:
    print('lxml import error')

try:
    import catenary
except:
    print('catenary import error')

try:
    import pypyodbc
except:
    print('pypyodbc import error')

try:
    import shapefile
except:
    print('shapefile import error')
try:
    from PIL import Image
except :
    print('PIL import error')
try:
    from geventhttpclient import HTTPClient, URL
except:
    print('geventhttpclient import error')

try:
    import shapely
    import shapely.geometry
    import shapely.wkt
except:
    print('shapely import error')
try:
    import pyproj
except:
    print('pyproj import error')
try:
    import geojson
except:
    print('geojson import error')
try:
    from pinyin import PinYin
except:
    print('pinyin import error')
try:
    from pyquery import PyQuery as pq
except:
    print('pyquery import error')
try:
    import xlrd
    import xlwt
except:
    print('xlrd xlwt import error')
try:
    import psycopg2 as psycopg
    from psycopg2 import errorcodes
except:
    print('psycopg2 import error')

CONFIGFILE = None
gConfig = None
gClientMongo = {}
gClientMongoTiles = {}
gClientMetadata = {}
ODBC_STRING = {}
gPinYin = None
gFeatureslist = []
gIsSaveTileToDB = True
gHttpClient = {}

ARCGISTILEROOT = r'I:\geotiff'
GOOGLETILEROOT = r'I:\geotiff'
DIRTILEROOT = r'I:\geotiff\tiles'
TILEROOT = r'I:\geotiff'
ZEROID = '00000000-0000-0000-0000-000000000000'

MAXCOMMITRECORDS = 100
TILESIZE = 256
TILEFORMAT = 'png'
SHAPEROOT= ur'I:\云南省矢量数据'
#SHAPEROOT= ur'D:\work\云南省矢量数据'
JSONROOT= ur'I:\geotiff\kmgdgis\download'
SERVERJSONROOT= os.path.join(module_path(),'static', 'geojson')
SERVERGLTFROOT= os.path.join(module_path(),'static', 'gltf')

GEOJSONSHAPEMAPPING = {'hotel':u'宾馆酒店',
                       'restaurant':u'餐饮',
                       'mall':u'超市商城',
                       'speedway':u'城市快速路',
                       'exitentrance':u'出入口',
                       'village':u'村',
                       'building':u'大厦',
                       'island':u'岛',
                       'subcity':u'地级市',
                       'subway':u'地铁轻轨',
                       'heighway':u'高速',
                       'busstop':u'公交站',
                       'park':u'公园',
                       'nationalroad':u'国道',
                       'greenland':u'绿地',
                       'otherroad':u'其他路',
                       'otherinfo':u'其他信息',
                       'provinceroad':u'省道',
                       'provincecapital':u'省会',
                       'provinceborder':u'省界',
                       'cityborder':u'市界',
                       'rollstop':u'收费站',
                       'railway':u'铁路',
                       'parker':u'停车场',
                       'county':u'县',
                       'countyroad':u'县道',
                       'countyborder':u'县界',
                       'villageroad':u'乡镇村道',
                       'school':u'学校',
                       'chemistsshop':u'药店',
                       'hospital':u'医疗',
                       'bank':u'银行',
                       'ynadminborder':u'云南行政边界',
                       'town':u'镇',
                        'goverment':u'政府机构',
                        }
CODE_XLS_FILE = dec1(r'G:\work\csharp\kmgdgis\doc\电网设备信息分类与编码.xls')


def init_global():
    global CONFIGFILE, gConfig, gClientMongo, gClientMongoTiles, gClientMetadata, ODBC_STRING, gPinYin, gFeatureslist
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="config", action="store", default=os.path.join(module_path(), "ogc-config.ini"),
                      help="specify a config file to load")
    parser.add_option("--signcert_enable",
                      action="store_true", dest="signcert_enable", default=False,
                      help="generate ssl cert and key")
    parser.add_option("--signcert_directory",
                      action="store", dest="signcert_directory", default=module_path(),
                      help="specify the directory to store ssl cert and key file")
    parser.add_option("--signcert_year",
                      action="store", type="int", dest="signcert_year", default=10,
                      help="specify year to generate ssl cert")
    #parser.add_option("--ssl_enable",
                      #action="store_true", dest="ssl_enable", default=False,
                      #help="enable ssl mode")
    parser.add_option("--cluster_enable",
                      action="store_true", dest="cluster_enable", default=False,
                      help="enable cluster mode")
    parser.add_option("--batch_download_tile_enable",
                      action="store_true", dest="batch_download_tile_enable", default=False,
                      help="enable batch download tile mode")
    
    parser.add_option("--tiletype",
                      action="store", dest="tiletype", default=None,
                      help="batch download tile: specify tiletype")
    parser.add_option("--subtype",
                      action="store", dest="subtype", default=None,
                      help="batch download tile: specify subtype")
    parser.add_option("--west",
                      action="store", type="float", dest="west", default=None,
                      help="batch download tile: specify west longitude")
    parser.add_option("--east",
                      action="store", type="float", dest="east", default=None,
                      help="batch download tile: specify east longitude")
    parser.add_option("--south",
                      action="store", type="float", dest="south", default=None,
                      help="batch download tile: specify south latitude")
    parser.add_option("--north",
                      action="store", type="float", dest="north", default=None,
                      help="batch download tile: specify north latitude")
    parser.add_option("--zoom_min",
                      action="store", type="int", dest="zoom_min", default=1,
                      help="batch download tile: specify min zoom")
    parser.add_option("--zoom_max",
                      action="store", type="int", dest="zoom_max", default=17,
                      help="batch download tile: specify max zoom")
    parser.add_option("--num_cocurrent",
                      action="store", type="int", dest="num_cocurrent", default=5,
                      help="batch download tile: specify files number during cocurrent downloading")
    parser.add_option("--wait_sec",
                      action="store", type="int", dest="wait_sec", default=1,
                      help="batch download tile: specify wait seconds before cocurrent batch download begin")

    parser.add_option("--save_to_db",
                      action="store_true", dest="save_to_db", default=False,
                      help="batch download tile: save tile to database")

    
    (options, args) = parser.parse_args()    
    
    print('parsing %s...' % options.config)
    CONFIGFILE = options.config
    
        
    gConfig = configobj.ConfigObj(CONFIGFILE, encoding='UTF8')
    # gClientMongo = {'webgis':None, 'geofeature':None,}
    gClientMongoTiles = {}
    gClientMetadata = {}
    ODBC_STRING = {}
    if gConfig.has_key('odbc'):
        for k in gConfig['odbc'].keys():
            if not k in ['odbc_driver']:
                if len(gConfig['odbc'][k]['db_instance'])>0:
                    ODBC_STRING[k] = "DRIVER={SQL Server Native Client 10.0};server=%s\\%s;Database=%s;TrustedConnection=no;Uid=%s;Pwd=%s;" % (gConfig['odbc'][k]['db_server'], gConfig['odbc'][k]['db_instance'], gConfig['odbc'][k]['db_name'], gConfig['odbc'][k]['db_username'], gConfig['odbc'][k]['db_password'])
                else:
                    ODBC_STRING[k] = "DRIVER={SQL Server Native Client 10.0};server=%s;Database=%s;TrustedConnection=no;Uid=%s;Pwd=%s;" % (gConfig['odbc'][k]['db_server'],  gConfig['odbc'][k]['db_name'], gConfig['odbc'][k]['db_username'], gConfig['odbc'][k]['db_password'])
    gFeatureslist = []
    if gConfig.has_key('webgis') and gConfig['webgis'].has_key('analyze') and gConfig['webgis']['analyze'].has_key('feature_list'):
        for i in gConfig['webgis']['analyze']['feature_list']:
            gFeatureslist.append(str(i)) 
    return options

class DemExtrctor(object):
    """let you look up pixel value"""

    def __init__(self, tifname='test.tif'):
        """Give name of tif file (or other raster data?)"""

        # open the raster and its spatial reference
        self.ds = gdal.Open(tifname)
        srRaster = osr.SpatialReference(self.ds.GetProjection())

        # get the WGS84 spatial reference
        srPoint = osr.SpatialReference()
        srPoint.ImportFromEPSG(4326) # WGS84

        # coordinate transformation
        self.ct = osr.CoordinateTransformation(srPoint, srRaster)

        # geotranformation and its inverse
        gt = self.ds.GetGeoTransform()
        dev = (gt[1]*gt[5] - gt[2]*gt[4])
        gtinv = ( gt[0] , gt[5]/dev, -gt[2]/dev, 
                gt[3], -gt[4]/dev, gt[1]/dev)
        self.gt = gt
        self.gtinv = gtinv

        # band as array
        b = self.ds.GetRasterBand(1)
        self.arr = b.ReadAsArray()

    def lookup(self, lon, lat):
        """look up value at lon, lat"""

        # get coordinate of the raster
        xgeo,ygeo,zgeo = self.ct.TransformPoint(lon, lat, 0)

        # convert it to pixel/line on band
        u = xgeo - self.gtinv[0]
        v = ygeo - self.gtinv[3]
        # FIXME this int() is probably bad idea, there should be 
        # half cell size thing needed
        xpix =  int(self.gtinv[1] * u + self.gtinv[2] * v)
        ylin = int(self.gtinv[4] * u + self.gtinv[5] * v)

        # look the value up
        return self.arr[ylin,xpix]


                        
                        
                
        
    
    
def read_txt(filepath):
    ret = {}
    ret['line'] = []
    ret['tower'] = []
    with open(filepath) as f:
        for i in f:
            arr = i.split('\t')
            ret['tower'].append( ( arr[0] , arr[1].strip()) )
            #print("%s=%s" % (arr[0], arr[1].strip()) )
    return ret

def read_xls(filepath):
    ret = {}
    ret['line'] = []
    ret['tower'] = []
    
    book = xlrd.open_workbook(filepath)
    sheet_line = book.sheet_by_name('line')
    for i in range(sheet_line.nrows):
        #print("%s=%s" % (sheet_line.cell_value(i,0), sheet_line.cell_value(i,1)))
        ret['line'].append( (sheet_line.cell_value(i,0), sheet_line.cell_value(i,1)) )
    sheet_tower = book.sheet_by_name('tower')
    for i in range(sheet_tower.nrows):
        #print("%s=%s" % (sheet_tower.cell(i,0).value, sheet_tower.cell(i,1).value) )
        ret['tower'].append( (sheet_tower.cell_value(i,0), sheet_tower.cell_value(i,1), sheet_tower.cell_value(i,2)) )
    return ret

def read_code_xls(filepath):
    ret = {}
    book = xlrd.open_workbook(filepath)
    for sh in book.sheets():
        if not sh.name in [ 'mapping']:
            if sh.nrows>0:
                tbname = ('table_' + sh.name).upper()
                ret[tbname] = []
                for i in range(sh.nrows):
                    c, n = sh.cell_value(i,0), sh.cell_value(i,1)
                    if '(' in c:
                        #c = c[:c.index('(')]
                        c = c[c.index('(')+1:]
                        c = c.replace(')','')
                    if len(c.strip())>0:
                        ret[tbname].append( (c, n) )
    return ret


def kml_get_records(filepath):
    ret = []
    tree = etree.parse(filepath)
    if tree:
        root = tree.getroot()
        for child in root:
            for child1 in child:
                for child2 in child1:
                    #tag = child2.tag.replace('{http://www.opengis.net/kml/2.2}','')
                    #print(tag)
                    for child3 in child2:
                        tag = child3.tag.replace('{http://www.opengis.net/kml/2.2}','')
                        if tag in ['Folder']:
                            for item in child3:
                                tagname = item.tag.replace('{http://www.opengis.net/kml/2.2}','')
                                if tagname == 'Placemark':
                                    tower = {}
                                    tower['tower_name'] = item[0].text
                                    arr = item[2][2].text.split(',')
                                    tower['geo_x'] = float(arr[0])
                                    tower['geo_y'] = float(arr[1])
                                    ret.append(tower)
    return ret
    
def kml_to_geojson(filepath):
    ignorelines = [u'220kV厂金II回', u'220kV厂金I回', u'220kV七官I、II回',
                   u'500kV厂口曲靖I回', '500kV和平厂口I回', u'220kV草海线', 
                   u'500kV草和乙线', u'500kV厂口七甸I回线', 
                   u'500kV七罗II回',u'110kV郭南线',u'220kV马温海线',
                   u'500kV厂口曲靖II回', u'500kV草和甲线',u'500kV草宝乙线',
                   u'500kV和平厂口II回', u'500kV草宝甲线', u'500kV七罗I回',
                   u'500kV大宝I回', u'500kV宝七I回', u'110kV郭岔线',
                   u'500kV宝七II回'
                   ]
    lines = []
    towers = []
    edges = []
    piny = get_pinyin_data()
    tree = etree.parse(filepath)
    if tree:
        root = tree.getroot()
        for child in root:
            for child1 in child:
                #print(child1.tag)
                for child2 in child1:
                    line = {}
                    tag = child2.tag.replace('{http://www.opengis.net/kml/2.2}','')
                    #if tag in ['Folder']:
                    if tag in ['Document']:
                        linename = None
                        line = {}
                        voltage = None
                        for child3 in child2:
                            tagname = child3.tag.replace('{http://www.opengis.net/kml/2.2}','')
                            if tagname == 'name':
                                line['properties'] = {}
                                line['properties']['name'] = child3.text.replace(u'.kml', u'').replace(u'Ⅱ',u'II').replace(u'Ⅰ',u'I')
                                if line['properties']['name'] in ignorelines:
                                    break
                                if '500kV' in line['properties']['name'] or '500' in line['properties']['name']:
                                    voltage = '15'
                                    line['properties']['name'] = line['properties']['name'].replace('500kV', '').replace('500', '')
                                elif '220kV' in line['properties']['name'] or '220' in line['properties']['name']:
                                    voltage = '13'
                                    line['properties']['name'] = line['properties']['name'].replace('220kV', '').replace('220', '')
                                elif '110kV' in line['properties']['name']:
                                    voltage = '12'
                                    line['properties']['name'] = line['properties']['name'].replace('110kV', '')
                                elif '66kV' in line['properties']['name']:
                                    voltage = '11'
                                    line['properties']['name'] = line['properties']['name'].replace('66kV', '')
                                elif '35kV' in line['properties']['name']:
                                    voltage = '10'
                                    line['properties']['name'] = line['properties']['name'].replace('35kV', '')
                                elif '20kV' in line['properties']['name']:
                                    voltage = '09'
                                    line['properties']['name'] = line['properties']['name'].replace('20kV', '')
                                elif '10kV' in line['properties']['name']:
                                    voltage = '08'
                                    line['properties']['name'] = line['properties']['name'].replace('10kV', '')
                                line['properties']['name'] = line['properties']['name'].replace('#', '')
                                line['properties']['py'] = piny.hanzi2pinyin_first_letter(line['properties']['name'].replace('#','').replace('II',u'二').replace('I',u'一').replace(u'Ⅱ',u'二').replace(u'Ⅰ',u'一'))
                                line['properties']['webgis_type'] = 'polyline_line'
                                line['properties']['supervisor'] = None
                                line['properties']['decease_date'] = None
                                line['properties']['manage_length'] = None
                                line['properties']['designer'] = None
                                line['properties']['voltage'] = voltage
                                line['properties']['operator'] = None
                                line['properties']['category'] = u'架空线'
                                line['properties']['management'] = None
                                line['properties']['production_date'] = None
                                line['properties']['end_point'] = None
                                line['properties']['responsible'] = None
                                line['properties']['owner'] = None
                                line['properties']['maintenace'] = None
                                line['properties']['nodes'] = []
                                line['properties']['status'] = None
                                line['properties']['line_code'] = None
                                line['properties']['finish_date'] = None
                                line['properties']['team'] = None
                                line['properties']['investor'] = None
                                line['properties']['length'] = None
                                line['properties']['constructor'] = None
                                line['properties']['start_point'] = None
                            #if tagname == 'Region':
                                #line['box'] = {'north':float(item[0][0].text),'south':float(item[0][1].text),'east':float(item[0][2].text),'west':float(item[0][3].text)}
                            if tagname == 'Folder':
                                for child4 in child3:
                                    tagname1 = child4.tag.replace('{http://www.opengis.net/kml/2.2}','')
                                    if tagname1 == 'Placemark':
                                        tower = {}
                                        tower['_id'] = str(ObjectId())
                                        tower['geometry'] = {}
                                        tower['geometry2d'] = {}
                                        tower['properties'] = {}
                                        tower['properties']['name'] = child4[0].text.replace(u'Ⅱ',u'II').replace(u'Ⅰ',u'I')
                                        m = re.match(r'(\D+)(\d+\.?\d*)(#)', tower['properties']['name'])
                                        if m:
                                            g = m.groups()
                                            if len(g) == 3 and g[2] == u'#':
                                                tower['properties']['name'] = '%s%s%s' % (g[0], g[2], g[1])
                                        tower['properties']['grnd_resistance'] = None
                                        tower['properties']['tower_code'] = ''
                                        tower['properties']['webgis_type'] = 'point_tower'
                                        tower['properties']['metals'] = []
                                        tower['properties']['line_rotate'] = 0
                                        tower['properties']['building_level'] = None
                                        tower['properties']['rotate'] = 0
                                        tower['properties']['vertical_span'] = 0
                                        tower['properties']['py'] = piny.hanzi2pinyin_first_letter(tower['properties']['name'].replace('#','').replace('II',u'二').replace('I',u'一').replace(u'Ⅱ',u'二').replace(u'Ⅰ',u'一'))
                                        tower['properties']['model'] = {}
                                        tower['properties']['horizontal_span'] = 0
                                        tower['properties']['denomi_height'] = None
                                        tower['properties']['voltage'] = voltage
                                        tower['geometry']['type'] = 'Point'
                                        tower['geometry2d']['type'] = 'Point'
                                        arr = child4[2][2].text.split(',')
                                        alt = extract_one_altitude(float(arr[0]), float(arr[1]))
                                        tower['geometry']['coordinates'] = [float(arr[0]), float(arr[1]), alt]
                                        tower['geometry2d']['coordinates'] = [float(arr[0]), float(arr[1])]
                                        tower['type'] = 'Feature'
                                        towers.append(tower)
                                        line['properties']['nodes'].append(tower['_id'])
                                for idx in range(1, len(line['properties']['nodes'])):
                                    edge = {}
                                    edge['_id'] = str(ObjectId())
                                    edge['properties'] = {}
                                    edge['properties']['start'] = line['properties']['nodes'][idx - 1]
                                    edge['properties']['end'] = line['properties']['nodes'][idx]
                                    edge['properties']['webgis_type'] = 'edge_tower'
                                    edges.append(edge)
                                
                        if not line['properties']['name'] in ignorelines:
                            lines.append(line)
        #print(lines)
        #for line in lines:
            ##for k in line.keys():
            #print('%s=%s' % (line['name'],str(line['towers'])))
    return lines, towers, edges

def odbc_insert_line(lines):
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    #cur.execute('''SELECT * FROM TABLE_LINE  ''')
    #for d in cur.description: 
        #print (d[0])
    
    #print ('')   
    #for row in cur.fetchall():
        #for field in row: 
            #print (field )
        #print ('')        
    
    for line in lines:
        cur.execute('''INSERT INTO TABLE_LINE VALUES(?, ?, ?, ?, ?, ?, ?)''',(str(uuid.uuid4()).upper(), '', line['name'], line['box']['north'], line['box']['south'], line['box']['east'], line['box']['west']))
    cur.commit()
    
    cur.close()
    conn.close()
    
def odbc_insert_line_tower(lines):
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    
    for line in lines:
        lineid = str(uuid.uuid4()).upper()
        #cur.execute('''INSERT INTO TABLE_LINE VALUES(?, ?, ?, ?, ?, ?, ?)''',(lineid, '', line['name'], line['box']['north'], line['box']['south'], line['box']['east'], line['box']['west']))
        cur.execute('''INSERT INTO TABLE_LINE VALUES(?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?)''',(lineid, '', line['name'], line['box']['north'], line['box']['south'], line['box']['east'], line['box']['west'], '15','架空线',0,0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
        towerid, tower_startid, tower_endid = None, None, None
        for tower in line['towers']:
            idx = line['towers'].index(tower)
            tower_endid = towerid = str(uuid.uuid4()).upper()
            if idx   == len(line['towers']):#-1:
                tower_startid = None
            if tower_startid and tower_endid:
                cur.execute('''INSERT INTO TABLE_TOWER_RELATION VALUES(?, ?, ?, ?)''',(str(uuid.uuid4()).upper(), lineid, tower_startid,  tower_endid))
            rotate = 0.0
            #if idx>0 and idx<len(line['towers'])-1:
                #lat1, lgt1 = line['towers'][idx-1]['coordinates']['lat'], line['towers'][idx-1]['coordinates']['lgt']
                #lat2, lgt2 = tower['coordinates']['lat'], tower['coordinates']['lgt']
                #lat3, lgt3 = line['towers'][idx+1]['coordinates']['lat'], line['towers'][idx+1]['coordinates']['lgt']
                #rotate = get_ab1((lat1, lgt1), (lat2, lgt2), (lat3, lgt3))
            #print('towerid=%s, lineid=%s, rotate=%f' % (towerid, lineid, rotate))
            cur.execute('''INSERT INTO TABLE_TOWER VALUES(?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?)''',(towerid, lineid, None, tower['name'], tower['coordinates']['lgt'],tower['coordinates']['lat'], 0, rotate, None, 0, 0, 0, 0, 0))
            #for i in range(8):
                #attachid = str(uuid.uuid4()).upper()
                #offset_x = -65.0
                #offset_y = 0.0
                #if i>3:
                    #offset_x = 65.0
                #if i in [0, 4]:
                    #offset_y = 145.0
                #elif i in [1, 5]:
                    #offset_y = 125.0
                #elif i in [2, 6]:
                    #offset_y = 105.0
                #elif i in [3, 7]:
                    #offset_y = 85.0
                #cur.execute('''INSERT INTO TABLE_TOWER_ATTACH_POINT VALUES(?, ?, ?, ?, ?)''',(attachid, towerid,  i,  offset_x, offset_y))
            tower_startid = tower_endid    
    cur.commit()
    
    cur.close()
    conn.close()
    
def odbc_insert_line_tower1(lines):
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    
    for line in lines:
        lineid = str(uuid.uuid4()).upper()
        cur.execute('''INSERT INTO TABLE_LINE VALUES(?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?)''',(lineid, '', line['name'], line['box']['north'], line['box']['south'], line['box']['east'], line['box']['west'], '15','架空线',0,0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
        towerid, tower_startid, tower_endid = None, None, None
        for tower in line['towers']:
            idx = line['towers'].index(tower)
            tower_endid = towerid = str(uuid.uuid4()).upper()
            if idx   == len(line['towers']):
                tower_startid = None
            if tower_startid and tower_endid:
                cur.execute('''INSERT INTO TABLE_SEGMENT VALUES(?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL)''',(str(uuid.uuid4()).upper(), lineid, tower_startid,  tower_endid, 0,0,0,0))
            rotate = 0.0
            cur.execute('''INSERT INTO TABLE_TOWER VALUES(?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?)''',(towerid, lineid, None, tower['name'], str(uuid.UUID('0'*32)),   tower['coordinates']['lgt'],tower['coordinates']['lat'], 0, rotate, None, 0, 0, 0, 0, 0))
            tower_startid = tower_endid    
    cur.commit()
    
    cur.close()
    conn.close()



def odbc_get_records(table, condition='1=1', area=''):
    ret = []
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING[area])
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return ret
 

    try:
        sql = ''' SELECT * FROM %s WHERE %s ''' % (table, condition)
        cur.execute(sql )
        for row in cur.fetchall():
            d = row.cursor_description
            line = {}
            for i in range(len(d)):
                v = row[i]
                s = v
                if isinstance(s, decimal.Decimal):
                    s = float(v)
                elif isinstance(s, datetime.datetime):
                    try:
                        s = v.strftime('%Y-%m-%d')
                    except:
                        s = '1900-01-01'
                elif isinstance(s, str) or isinstance(s, unicode):
                    s = v.strip()
                
                #if d[row.index(v)][0] == 'end_geo_z':
                    #print('end_geo_z=%f' % s)
                line[d[i][0]] = s
                #if table=='VIEW_ATTACH_LINE_SEG':
                    #if not 'end_geo_z' in str(d):
                        #print(d)
            ret.append(line)
        
    except:
        print(sys.exc_info()[1])
        ret = []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return ret



def get_latest_3dd_stamp(stamp_format, area=''):
    p = os.path.abspath('static/3dd/yn.3dd')
    ret = []
    d = {}
    d['update_stamp'] = time.strftime(stamp_format, time.localtime(os.path.getmtime(p)))
    ret.append(d)
    return d

def get_latest_stamp(stamp_format, area=''):
    ret = []
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING[area])
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return ret
 

    try:
        cur.execute('''SELECT MAX(update_stamp) as update_stamp from TABLE_UPDATE_TIMESTAMP''' )
        for row in cur.fetchall():
            d = row.cursor_description
            line = {}
            for i in range(len(d)):
                v = row[i]
                s = v
                if isinstance(s, decimal.Decimal):
                    s = float(v)
                elif isinstance(s, datetime.datetime):
                    #'%Y-%m-%d %H:%M:%S'
                    s = v.strftime(stamp_format)
                elif isinstance(s, str) or isinstance(s, unicode):
                    s = v.strip()
                
                #if d[row.index(v)][0] == 'end_geo_z':
                    #print('end_geo_z=%f' % s)
                line[d[i][0]] = s
                #if table=='VIEW_ATTACH_LINE_SEG':
                    #if not 'end_geo_z' in str(d):
                        #print(d)
            ret.append(line)
        
    except:
        print(sys.exc_info()[1])
        ret = []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return ret
 


def odbc_insert_line_seg():
    conn = None
    cur = None
    #try:
        #conn = pypyodbc.connect(ODBC_STRING)
        #cur = conn.cursor()
    #except:
        #print(sys.exc_info()[1])
        #return 
    #print(len(lines))
    
    conn = pypyodbc.connect(ODBC_STRING)
    cur = conn.cursor()
    cur.execute('''DELETE FROM TABLE_LINE_SEG''')
    cur.commit()
    cur.close()
    conn.close()
    
    lines = odbc_get_records('TABLE_LINE', '1=1')
    
    for line in lines:
        #attas = get_records('VIEW_ATTACH_POS', "line_id='%s'" % line['id'])
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
        
        towers = odbc_get_sorted_tower_by_line(line['id'])
        
        
        start_tower_id, end_tower_id = None, None
        
        for tower in towers:
            end_tower_id = tower['id']
            #if towers.index(tower)==len(towers)-1:
                #break
            if start_tower_id and end_tower_id:
                print(tower['tower_name'])
                for i in range(8):
                    start_attas = odbc_get_records('VIEW_ATTACH_POS', "tower_id='%s' and point_index=%d" % (start_tower_id, i))
                    end_attas   = odbc_get_records('VIEW_ATTACH_POS', "tower_id='%s' and point_index=%d" % (end_tower_id,   i))
                    start_point_id, end_point_id = start_attas[0]['id'], end_attas[0]['id']
                    id = str(uuid.uuid4()).upper()
                    cur.execute('''INSERT INTO TABLE_LINE_SEG VALUES(?, ?, ?, ?, ?, ?, ?)''',(id, line['id'], start_point_id, end_point_id , 0.9, 0.001, '0,255,255' ))
                    #end_point_id = start_point_id
            start_tower_id = end_tower_id
                
        
    
        cur.commit()
        cur.close()
        conn.close()
        
def odbc_insert_segment():
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return 
    
    cur.execute('''DELETE FROM TABLE_SEGMENT''')
    
    lines = odbc_get_records('TABLE_LINE', '1=1')
    
    for line in lines:
        print(line['line_name'])
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
        towers = odbc_get_sorted_tower_by_line(line['id'])
        start_tower_id, end_tower_id = str(uuid.UUID('0'*32)).upper(), None
        
        for tower in towers:
            end_tower_id = tower['id']
            if start_tower_id and end_tower_id:
                print(tower['tower_name'])
                cur.execute('''INSERT INTO TABLE_SEGMENT VALUES(?, ?, ?, ?, NULL, NULL, NULL,NULL,NULL,NULL,NULL)''',(str(uuid.uuid4()).upper(), line['id'], start_tower_id, end_tower_id ))
            start_tower_id = end_tower_id
        end_tower_id = str(uuid.UUID('1'*32)).upper()
        print('end')
        cur.execute('''INSERT INTO TABLE_SEGMENT VALUES(?, ?, ?, ?, NULL, NULL, NULL,NULL,NULL,NULL,NULL)''',(str(uuid.uuid4()).upper(), line['id'], start_tower_id, end_tower_id ))
                
        cur.commit()
        cur.close()
        conn.close()

def odbc_get_sorted_tower_by_line(line_id, area):
    towers = odbc_get_records('TABLE_TOWER', "line_id='%s'" % line_id, area)
    towers_relation = odbc_get_records('VIEW_TOWER_RELATIONS', "line_id='%s'" % line_id, area)
    if len(towers)==0:
        return []
    towers = resort_towers_by_list(towers, towers_relation)
    return towers

    
    
    
def odbc_delete_from_table(table, condition):
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    
    cur.execute(''' DELETE FROM  %s where %s ''' % (table, condition))
    cur.commit()
    cur.close()
    conn.close()

    
def odbc_clear_table():
    odbc_delete_from_table('TABLE_CONTACT_POINT', '1=1')
    odbc_delete_from_table('TABLE_CROSS_POINT', '1=1')
    odbc_delete_from_table('TABLE_LINE', '1=1')
    #odbc_delete_from_table('TABLE_LINE_SEG', '1=1')
    odbc_delete_from_table('TABLE_SEGMENT', '1=1')
    odbc_delete_from_table('TABLE_SPECIAL_SECTION', '1=1')
    odbc_delete_from_table('TABLE_STRAIN_SECTION', '1=1')
    #odbc_delete_from_table('TABLE_TOWER_ATTACH_POINT', '1=1')
    odbc_delete_from_table('TABLE_TOWER_METALS', '1=1')
    odbc_delete_from_table('TABLE_TOWER_MODEL', '1=1')
    odbc_delete_from_table('TABLE_TOWER_MODEL', '1=1')
    odbc_delete_from_table('TABLE_TOWER', '1=1')
    #odbc_delete_from_table('TABLE_TOWER_RELATION', '1=1')
    
def import_from_kml():
    odbc_clear_table()
    data = read_kml(KML_FILE)
    #odbc_insert_line_tower(data)
    odbc_insert_line_tower1(data)
    odbc_update_towers_rotate(False)
    
    
def import_line_tower_code():
    ret = read_xls(XLS_FILE)
    #ret = read_txt(TXT_FILE)
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    
    for i in ret['line']:
        cur.execute(''' UPDATE  TABLE_LINE SET line_code=? WHERE line_name=?''', (i[1][:19], i[0]) )
    for i in ret['tower']:
        #print("%d %s=%s" % (ret['tower'].index(i), i[0], i[1]))
        cur.execute(''' UPDATE  TABLE_TOWER SET tower_code=?, model_code=? WHERE tower_name=?''', (i[1][:19], i[2], i[0]) )
        
    cur.commit()
    cur.close()
    conn.close()
    
def import_code_table():
    ret = read_code_xls(CODE_XLS_FILE)
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    for k in ret.keys():
        odbc_create_code_table(k)
        odbc_delete_from_table(k, '1=1')
        for i in ret[k]:
            cur.execute('''INSERT INTO %s VALUES(?, ?) ''' % k, (i[0], i[1]))
    cur.commit()
    cur.close()
    conn.close()
            

def odbc_table_exist(table):
    ret = False
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    sql = ''' SELECT  * FROM dbo.SysObjects WHERE ID = object_id(N'%s') AND OBJECTPROPERTY(ID, 'IsTable') = 1  ''' %  table
    cur.execute(sql)
    for row in cur.fetchall():
        ret = True
        
    #cur.commit()
    cur.close()
    conn.close()
    return ret

def odbc_drop_table(table):
    ret = False
    if not odbc_table_exist(table):
        return ret
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return ret
    sql = ''' DROP TABLE  %s  ''' %  table
    cur.execute(sql)
    cur.commit()
    cur.close()
    conn.close()
    return True
    
    
    
def odbc_create_code_table(table):
    ret = False
    if odbc_table_exist(table):
        return ret
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return ret
    sql = ''' CREATE TABLE  %s (
	      code  nvarchar(16) NOT NULL,
	      name  nvarchar(100) NULL
        )  ''' %  table
    cur.execute(sql)
    cur.commit()
    cur.close()
    conn.close()
    return True
    
def get_ab1((lat1,lgt1), (lat2,lgt2), (lat3,lgt3)):
    v1 = Vector(lat1,lgt1,0)
    v2 = Vector(lat2,lgt2,0)
    v3 = Vector(lat3,lgt3,0)
    xaxis = Vector(1, 0, 0)
    e1 = (v1-v2).normalized()
    e2 = (v3-v2).normalized()
    e = (e1+e2)/((e1+e2).mag())
    halfAngleABC = np.rad2deg(e.angle(xaxis))
    #print(halfAngleABC)
    #e1 = v1-v2
    #e2 = v3-v2
    angleAB= np.rad2deg(e1.angle(xaxis))
    angleBC = np.rad2deg(e2.angle(xaxis))
    #angleAB = (angleAB + 360) % 360
    #angleBC = (angleBC + 360) % 360
    #halfAngleABC = (angleAB + angleBC) / 2.0
    sita = np.abs(halfAngleABC - angleBC)
    deg = 0
    if sita > 90:
        deg = (halfAngleABC-90) % 360
    else:
        deg = (halfAngleABC+90) % 360
    deg = (180 - deg + 360) % 360
    return deg
    
def get_ab((lgt1, lat1), (lgt2, lat2), (lgt3, lat3)):
    v1 = Vector(lgt1, lat1,0)
    v2 = Vector(lgt2, lat2,0)
    v3 = Vector(lgt3, lat3,0)
    xaxis = Vector(1, 0, 0)
    e1 = (v1-v2).normalized()
    e2 = (v3-v2).normalized()
    e = (e1+e2)/((e1+e2).mag())
    
    deg = np.rad2deg(e.angle(xaxis))
    if deg > 90:
        deg = 270.0 - deg
        #deg = (deg-90) % 360
    else:
        deg = 90.0 + deg
        #deg = (deg+90) % 360
    if np.isnan(deg):
        deg = 0.0
    return deg

def get_ab2((lgt1, lat1), (lgt2, lat2), (lgt3, lat3)):
    v1 = Vector(lgt1, lat1,0)
    v2 = Vector(lgt2, lat2,0)
    v3 = Vector(lgt3, lat3,0)
    xaxis = Vector(1, 0, 0)
    e1 = (v1-v2).normalized()
    e2 = (v3-v2).normalized()
    e = (e1+e2)/((e1+e2).mag())
    deg = np.rad2deg(e.angle(xaxis))
    cr = np.cross(e1.get_array(), e2.get_array())
    if cr[2]<0:
        deg = deg * (-1)
    #if deg > 90:
        #deg = 270.0 - deg
        ##deg = (deg-90) % 360
    #else:
        #deg = 90.0 + deg
        ##deg = (deg+90) % 360
    if np.isnan(deg):
        deg = 0.0
    return deg

    
    
    
class Vector(object):
    def __init__(self, x, y=None, z=None):
        if y is None and z is None:
            # Array, list, tuple...
            if len(x)!=3:
                raise ValueError("Vector: x is not a  list/tuple/array of 3 numbers")
            self._ar=np.array(x, 'd')
        else:
            # Three numbers
            self._ar=np.array((x, y, z), 'd')

    def __repr__(self):
        x,y,z=self._ar
        return "<Vector %.2f, %.2f, %.2f>" % (x,y,z)

    def __neg__(self):
        "Return Vector(-x, -y, -z)"
        a=-self._ar
        return Vector(a)

    def __add__(self, other):
        "Return Vector+other Vector or scalar"
        if isinstance(other, Vector):
            a=self._ar+other._ar
        else:
            a=self._ar+np.array(other)
        return Vector(a)

    def __sub__(self, other):
        "Return Vector-other Vector or scalar"
        if isinstance(other, Vector):
            a=self._ar-other._ar
        else:
            a=self._ar-np.array(other)
        return Vector(a)

    def __mul__(self, other):
        "Return Vector.Vector (dot product)"
        return sum(self._ar*other._ar)

    def __div__(self, x):
        "Return Vector(coords/a)"
        a=self._ar/np.array(x)
        return Vector(a)

    def __pow__(self, other):
        "Return VectorxVector (cross product) or Vectorxscalar"
        if isinstance(other, Vector):
            a,b,c=self._ar
            d,e,f=other._ar
            c1=np.linalg.det(np.array(((b,c), (e,f))))
            c2=-np.linalg.det(np.array(((a,c), (d,f))))
            c3=np.linalg.det(np.array(((a,b), (d,e))))
            return Vector(c1,c2,c3)
        else:
            a=self._ar*np.array(other)
            return Vector(a)

    def __getitem__(self, i):
        return self._ar[i]

    def __setitem__(self, i, value):
        self._ar[i]=value

    def __contains__(self, i):
        return (i in self._ar)

    def norm(self):
        "Return vector norm"
        return np.sqrt(sum(self._ar*self._ar))

    def normsq(self):
        "Return square of vector norm"
        return abs(sum(self._ar*self._ar))

    def normalize(self):
        "Normalize the Vector"
        self._ar=self._ar/self.norm()

    def normalized(self):
        "Return a normalized copy of the Vector"
        v=self.copy()
        v.normalize()
        return v

    def angle(self, other):
        "Return angle between two vectors"
        n1=self.norm()
        n2=other.norm()
        c=(self*other)/(n1*n2)
        # Take care of roundoff errors
        #c=min(c,1)
        #c=max(-1,c)
        return np.arccos(c)

    def get_array(self):
        "Return (a copy of) the array of coordinates"
        return np.array(self._ar)

    def left_multiply(self, matrix):
        "Return Vector=Matrix x Vector"
        a=np.dot(matrix, self._ar)
        return Vector(a)

    def right_multiply(self, matrix):
        "Return Vector=Vector x Matrix"
        a=np.dot(self._ar, matrix)
        return Vector(a)
    def mag(self):
        return np.sqrt(self._ar.dot(self._ar))
    def copy(self):
        "Return a deep copy of the Vector"
        return Vector(self._ar)    


    


def resort_towers_by_list(towers, towers_relation):
    def getidx(tows, id):
        ret = -1
        for t in tows:
            if t['id']==id:
                return tows.index(t)
        return ret
    ret = []
    ret.append(towers[0])
    tower_id = towers[0]['id']
    done = []
    done.append(tower_id)
    while True:
        for tr in towers_relation:
            #print(towers_relation[id]['tower_start'] + "=" + tower_id)
            if tr['tower_start'] == tower_id:
                tower_id = tr['tower_end']
                break
        idx = getidx(towers, tower_id)
        if idx>-1 and not tower_id in done:
            ret.append(towers[idx])
            done.append(tower_id)
        else:
            break
            
    tower_id = towers[0]['id']
    
    while True:
        for tr in towers_relation:
            #print(towers_relation[id]['tower_start'] + "=" + tower_id)
            if tr['tower_end'] == tower_id:
                tower_id = tr['tower_start']
                break
        idx = getidx(towers, tower_id)
        if idx>-1 and not tower_id in done :
            ret.insert(0, towers[idx])
            done.append(tower_id)
        else:
            break
    
    #d = OrderedDict()
    #for i in ret:
        #d[i['id']] = i
    return ret        

    
    
    
        
        
    
def get_suitable_model_code(tower_info_list, model_code, line_position, area):
    ret = ''
    mclist = [i['model_code'] for i in tower_info_list]
    if model_code is None or len(model_code)==0 or model_code==u'NULL':
        ret = 'NZDH_D_48'
        if not line_position==u'单回':
            ret = 'NZSH_D_48'
    else:
        if not model_code in mclist:
            dh = model_code[model_code.rindex('_'):]
            ret = 'NZDH_D_48'
            if len(dh)>1:
                for mc in mclist:
                    if line_position==u'单回' and mc[:4] == 'NZDH' and dh in mc:
                        ret = mc
                        break
                    if not line_position==u'单回' and mc[:4] == 'NZSH' and dh in mc:
                        ret = mc
                        break
        else:
            l_1 = odbc_get_records('TABLE_CONTACT_POINT', " model_code='%s'  AND position='%s'" % (model_code, line_position), area)
            if len(l_1)==0:
                ret = 'NZDH_D_48'
                if not line_position==u'单回':
                    ret = 'NZSH_D_48'
            else:
                ret = model_code
    return ret

    
        
        
    

def resort_towers_by_dict(towers, towers_relation):
    ret = []
    tower_id = towers.keys()[0]
    ret.append(towers[tower_id])
    
    done = []
    done.append(tower_id)
    while True:
        for id in towers_relation.keys():
            #print(towers_relation[id]['tower_start'] + "=" + tower_id)
            if towers_relation[id]['tower_start'] == tower_id:
                tower_id = towers_relation[id]['tower_end']
                break
        if towers.has_key(tower_id) and not tower_id in done:
            ret.append(towers[tower_id])
            done.append(tower_id)
        else:
            break
            
    tower_id = towers.keys()[0]
    #done = []
    while True:
        for id in towers_relation.keys():
            #print(towers_relation[id]['tower_start'] + "=" + tower_id)
            if towers_relation[id]['tower_end'] == tower_id:
                tower_id = towers_relation[id]['tower_start']
                break
        if towers.has_key(tower_id) and not tower_id in done :
            ret.insert(0, towers[tower_id])
            done.append(tower_id)
        else:
            break
    
    d = OrderedDict()
    for i in ret:
        d[i['id']] = i
    return d        
            
def resort_towers_to_groups(towers, towers_relation,  exclude=[]):
    ret = []
    towers1 = resort_towers_by_dict(towers, towers_relation)
    groups = []
    keys = towers1.keys()
    
    extsortidx = []
    for i in exclude:
        if i in keys:
            extsortidx.append(keys.index(i))
    extsortidx.sort()
    
    extsort = []
    for i in extsortidx:
        extsort.append(keys[i])
    
    start, end = 0,  -1
    for i in extsort:
        arr = None
        end = keys.index(i)
        arr = keys[start:end]
        if len(arr)>0:
            groups.append(arr)
        start = end+1
    end = len(keys)
    
    if start != end:
        groups.append(keys[start:end])
    
    for g in groups:
        d = OrderedDict()
        for id in g:
            d[id] = towers[id]
        ret.append(d)    
    return ret        
                
                
                
        
        
    
    
    
def odbc_update_segment_by_start_end(segs, area):
    sqls = []
    for seg in segs: 
        obj = sqlize_data(seg)
        sql = """INSERT INTO TABLE_WIRE_SEGMENT VALUES(
                 %s,
                 %s,
                 %s,
                 %s,
                 %s,
                 %s
        )""" % (
              "'%s'" % str(uuid.uuid4()).upper(),
              obj['start_tower_id'],
              obj['end_tower_id'],
              obj['start_contact_id'],
              obj['end_contact_id'],
              obj['phase']
        )
        sqls.append(sql)
    
    odbc_execute_sqls(sqls, area)
    
    
    

def odbc_update_line_seg_color():
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    database = 'KMGD'
    colors = ['255,255,0','255,128,0','255,0,128','128,0,255','128,255,0','0,128,255','0,255,128', '0,255,255']
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    
    #for i in range(8):
        #cur.execute(""" UPDATE  TABLE_LINE_SEG SET line_color=? WHERE id=?""" , (ang, tower['id']) )
        
    lines = odbc_get_records('TABLE_LINE', "1=1" )
    for line in lines:
        segs = get_data_from_rdbms(kmgd, database, 'VIEW_ATTACH_LINE_SEG', " line_id='%s'  " % line['id'])
        print('%s=%d' % (line['line_name'],len(segs.keys())))
        for k in segs.keys():
            seg = segs[k]
            for i in range(8):
                cur.execute(""" UPDATE  TABLE_LINE_SEG SET line_color=? WHERE id=?""" , (colors[i], seg['id']) )
    cur.commit()
    cur.close()
    conn.close()


    
    

def ToGeographic(mercatorX_lon, mercatorY_lat):
    if abs(mercatorX_lon) < 180 and  abs(mercatorY_lat) < 90:
        return 0, 0
    if abs(mercatorX_lon) > 20037508.3427892 or abs(mercatorY_lat) > 20037508.3427892 :
        return 0, 0

    x = mercatorX_lon;
    y = mercatorY_lat;
    num3 = x / 6378137.0;
    num4 = num3 * 57.295779513082323;
    num5 = math.floor(float(num4 + 180.0) / 360.0)
    num6 = num4 - (num5 * 360.0)
    num7 = 1.5707963267948966 - (2.0 * math.atan(math.exp((-1.0 * y) / 6378137.0)))
    lon = num6
    lat = num7 * 57.295779513082323
    return lon, lat


def ToWebMercator(lon, lat):
    if abs(lon) > 180 or abs(lat) > 90:
        return 0, 0
    num = lon * 0.017453292519943295
    x = 6378137.0 * num
    a = lat * 0.017453292519943295

    mercatorX_lon = x
    mercatorY_lat = 3189068.5 * math.log((1.0 + math.sin(a)) / (1.0 - math.sin(a)))
    return mercatorX_lon, mercatorY_lat

                


    


def import_tower_model_code():
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    
    towers = odbc_get_records('TABLE_TOWER', '1=1')
    cods = set()
    for tower in towers:
        cod = tower['model_code']
        cods.add(cod)
    for cod in cods:
        cur.execute(''' INSERT INTO TABLE_TOWER_MODEL VALUES (? ,?, ?, ?, ?)''', (str(uuid.uuid4()).upper(), cod, 'test2.3ds','','') )
        
    cur.commit()
    
    cur.execute(''' UPDATE TABLE_TOWER_MODEL SET model_code='test2' WHERE  model_code='' ''' )
    cur.commit()
    
    cur.close()
    conn.close()
    
def import_tower_attach_points():
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    
    cur.execute(''' DELETE FROM  TABLE_TOWER_ATTACH_POINT''' )
    models = odbc_get_records('TABLE_TOWER_MODEL', '1=1')
    cods = set()
    for m in models:
        cod = m['model_code']
        cods.add(cod)
    for m in cods:
        model_code = m
        for i in range(8):
            attachid = str(uuid.uuid4()).upper()
            offset_x = -65.0
            offset_y = 0.0
            if i>3:
                offset_x = 65.0
            if i in [0, 4]:
                offset_y = 145.0
            elif i in [1, 5]:
                offset_y = 125.0
            elif i in [2, 6]:
                offset_y = 105.0
            elif i in [3, 7]:
                offset_y = 85.0
            cur.execute('''INSERT INTO TABLE_TOWER_ATTACH_POINT VALUES(?, ?, ?, ?, ?)''',(attachid, model_code,  i,  offset_x, offset_y))
        
        
        
    cur.commit()
    cur.close()
    conn.close()

            
def test_xml():
    r1 = etree.parse(r'D:\arcgisserver\sd\kmgdgis.xml')
    r2 = etree.parse(r'D:\arcgisserver\sd\kmgdgis1.xml')
    print(etree.tostring(r2.getroot(), pretty_print=True))




def gen_xls_report(line_names=[]):
    lines = odbc_get_records('TABLE_LINE', '1=1')
    for line in lines:
        #print(line['id'])
        #if line['id'].upper() == '241A57B9-40D6-41AD-A2C1-7670D58B0E98':#七罗I回
            #gen_xls_report_by_line_id(line)
            #break
        if line['line_name'] in line_names:
            print(line['line_name'])
            gen_xls_report_by_line_id(line)
    
def gen_xls_report_by_line_id(line):
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    towers = odbc_get_sorted_tower_by_line(line['id'])
    
    
    book = xlwt.Workbook()
    
    style = xlwt.XFStyle()
    style.num_format_str  = '@'
    
    #线路信息
    sheet = book.add_sheet(line['line_name'] + u'_线路信息')
    sheet.write(0, 0, u'线路名称')
    sheet.write(0, 1, u'线路代码(19位代码,中国南方电网公司信息分类和编码标准.doc)')
    sheet.write(0, 2, u'长度')
    sheet.write(0, 3, u'管辖长度')
    sheet.write(0, 4, u'线路起点')
    sheet.write(0, 5, u'线路终点')
    sheet.write(0, 6, u'线路状态')
    sheet.write(0, 7, u'运维单位')
    sheet.write(0, 8, u'管辖基层')
    sheet.write(0, 9, u'所属单位')
    sheet.write(0, 10, u'维护班组')
    sheet.write(0, 11, u'维护人')
    sheet.write(0, 12, u'建设单位')
    sheet.write(0, 13, u'设计单位')
    sheet.write(0, 14, u'监理单位')
    sheet.write(0, 15, u'施工单位')
    sheet.write(0, 16, u'运行单位')
    sheet.write(0, 17, u'投运日期')
    sheet.write(0, 18, u'投产日期')
    sheet.write(0, 19, u'退役日期')

    #sheet.write(1, 0, u'')
    #sheet.write(1, 1, u'19位代码(中国南方电网公司信息分类和编码标准.doc)')
    #sheet.write(1, 2, u'')
    #sheet.write(1, 3, u'')
    #sheet.write(1, 4, u'')
    #sheet.write(1, 5, u'')
    #sheet.write(1, 6, u'')
    #sheet.write(1, 7, u'')
    #sheet.write(1, 8, u'')
    #sheet.write(1, 9, u'')
    #sheet.write(1, 10, u'')
    #sheet.write(1, 11, u'')
    #sheet.write(1, 12, u'')
    #sheet.write(1, 13, u'')
    #sheet.write(1, 14, u'')
    #sheet.write(1, 15, u'')
    #sheet.write(1, 16, u'')
    #sheet.write(1, 17, u'')
    #sheet.write(1, 18, u'')

    #杆塔信息
    sheet = book.add_sheet(line['line_name'] + u'_杆塔信息')
    sheet.write(0, 0, u'杆塔id')
    sheet.write(0, 1, u'杆塔名称')
    sheet.write(0, 2, u'杆塔序号')
    sheet.write(0, 3, u'杆塔代码(19位代码,厂站功能位置编码,中国南方电网公司信息分类和编码标准.doc')
    sheet.write(0, 4, u'杆塔型号')
    sheet.write(0, 5, u'呼称高')
    sheet.write(0, 6, u'水平档距(单位米)')
    sheet.write(0, 7, u'垂直档距(单位米)')
    sheet.write(0, 8, u'施工基面(单位米)')
    sheet.write(0, 9, u'线路转角(单位度)')
    
    for tower in towers:
        sheet.write(towers.index(tower)+1, 0, tower['id'])
        sheet.write(towers.index(tower)+1, 1, tower['tower_name'])
        m = re.search('(\d+)', tower['tower_name'])
        idx = ''
        if m:
            idx = m.group(0)
        sheet.write(towers.index(tower)+1, 2, idx)
        
        
    #杆塔附件信息    
    sheet = book.add_sheet(line['line_name'] + u'_杆塔附件信息')
    sheet.write(0, 0, u'杆塔id')
    sheet.write(0, 1, u'杆塔名称')
    sheet.write(0, 2, u'杆塔序号')
    #sheet.write(0, 2, u'附件类型attach_type(取值：防震锤、绝缘子串、接地装置、基础)')
    #sheet.write(0, 3, u'附件子类型attach_subtype(取值：防震锤：导线大号侧、导线小号侧、地线大号侧、地线小号侧；绝缘子串：导线绝缘子、跳线绝缘子、地线绝缘子、OPGW绝缘子串；基础：A腿、B腿、C腿、D腿)')
    #sheet.write(0, 4, u'型号规格specification')
    #sheet.write(0, 5, u'串数strand(绝缘子串数,防震锤个数)')
    #sheet.write(0, 6, u'片数slice(绝缘子:每串片数)')
    #sheet.write(0, 7, u'实数value1(防震锤：每线防震锤安装距离)')
    
    #绝缘子串-导线绝缘子串最多4
    i = 3
    for j in range(4):
        sheet.write(0 , i, u'绝缘子串%d-导线绝缘子串型号规格' % (j+1))
        i += 1
        sheet.write(0 , i, u'绝缘子串%d-导线绝缘子串串数' % (j+1))
        i += 1
        sheet.write(0 , i, u'绝缘子串%d-导线绝缘子串每串片数' % (j+1))
        i += 1

    #绝缘子串-跳线绝缘子串最多4
    for j in range(4):
        sheet.write(0 , i, u'绝缘子串%d-跳线绝缘子串型号规格' % (j+1))
        i += 1
        sheet.write(0 , i, u'绝缘子串%d-跳线绝缘子串串数' % (j+1))
        i += 1
        sheet.write(0 , i, u'绝缘子串%d-跳线绝缘子串每串片数' % (j+1))
        i += 1
    
    
    sheet.write(0 , i, u'防震锤-导线小号侧型号规格')
    i += 1
    sheet.write(0 , i, u'防震锤-导线小号侧个数')
    i += 1
    sheet.write(0 , i, u'防震锤-导线小号侧每线防震锤安装距离')
    i += 1
    
    sheet.write(0 , i, u'防震锤-导线大号侧型号规格')
    i += 1
    sheet.write(0 , i, u'防震锤-导线大号侧个数')
    i += 1
    sheet.write(0 , i, u'防震锤-导线大号侧每线防震锤安装距离')
    i += 1
    
    sheet.write(0 , i, u'防震锤-地线小号侧型号规格')
    i += 1
    sheet.write(0 , i, u'防震锤-地线小号侧个数')
    i += 1
    sheet.write(0 , i, u'防震锤-地线小号侧每线防震锤安装距离')
    i += 1
    
    sheet.write(0 , i, u'防震锤-地线大号侧型号规格')
    i += 1
    sheet.write(0 , i, u'防震锤-地线大号侧个数')
    i += 1
    sheet.write(0 , i, u'防震锤-地线大号侧每线防震锤安装距离')
    i += 1
    
    sheet.write(0 , i, u'地线金具串型号规格')
    i += 1
    sheet.write(0 , i, u'地线金具串数量')
    i += 1
    
    sheet.write(0 , i, u'OPGW金具串型号规格')
    i += 1
    sheet.write(0 , i, u'OPGW金具串数量')
    i += 1
    
    sheet.write(0 , i, u'护线条个数')
    i += 1
    
    sheet.write(0 , i, u'引下夹具个数')
    i += 1
    
    sheet.write(0 , i, u'余缆架个数')
    i += 1
    sheet.write(0 , i, u'接续盒个数')
    i += 1
    sheet.write(0 , i, u'不锈钢抱箍个数')
    i += 1
    sheet.write(0 , i, u'接地装置型号规格')
    i += 1
    sheet.write(0 , i, u'接地装置埋深')
    i += 1
    
    
    for tower in towers:
        m = re.search('(\d+)', tower['tower_name'])
        toweridx = ''
        if m:
            toweridx = m.group(0)
        sheet.write(towers.index(tower)  + 1 , 0, tower['id'])
        sheet.write(towers.index(tower)  + 1 , 1, tower['tower_name'])
        sheet.write(towers.index(tower)  + 1 , 2, toweridx)
        
    #线段信息    
    sheet = book.add_sheet(line['line_name'] + u'_线段信息')
    sheet.write(0, 0, u'前一个杆塔id')
    sheet.write(0, 1, u'前一个杆塔名称')
    sheet.write(0, 2, u'前一个杆塔杆塔序号')
    sheet.write(0, 3, u'后一个杆塔id')
    sheet.write(0, 4, u'后一个杆塔名称')
    sheet.write(0, 5, u'后一个杆塔杆塔序号')
    sheet.write(0, 6, u'分列值(默认值1,可取1,2,4)')
    sheet.write(0, 7, u'单线计数')
    sheet.write(0, 8, u'交叉跨越点数目')
    sheet.write(0, 9, u'使用档距(单位米)')
    sheet.write(0, 10, u'每项间隔棒')
    sheet.write(0, 11, u'接续管数量')
    sheet.write(0, 12, u'接续管类型')
    
        
    for tower in towers:
        m = re.search('(\d+)', tower['tower_name'])
        toweridx = ''
        idx = towers.index(tower)
        if m:
            toweridx = m.group(0)

        if idx+1 < len(towers):
            nexttower = towers[idx+1]
            sheet.write(idx + 1 , 0, tower['id'])    
            sheet.write(idx + 1 , 1, tower['tower_name'])    
            sheet.write(idx + 1 , 2,  toweridx)    
            m = re.search('(\d+)', nexttower['tower_name'])
            toweridx = ''
            if m:
                toweridx = m.group(0)
            sheet.write(idx + 1, 3, nexttower['id'])    
            sheet.write(idx + 1, 4, nexttower['tower_name'])    
            sheet.write(idx + 1, 5, toweridx)
            
        #if idx==0:
            #sheet.write(idx  + 1 , 0, str(uuid.UUID('0'*32)))    
            #sheet.write(idx  + 1 , 1, u'变电站')    
            #sheet.write(idx  + 1 , 2,  0)
            #sheet.write(idx  + 1 , 3,  tower['id'])
            #sheet.write(idx  + 1 , 4, tower['tower_name'])    
            #sheet.write(idx  + 1 , 5, toweridx)    
        
        #if idx+1 < len(towers):
            #nexttower = towers[idx+1]
            #sheet.write(idx + 1  + 1 , 0, tower['id'])    
            #sheet.write(idx + 1  + 1 , 1, tower['tower_name'])    
            #sheet.write(idx + 1   + 1 , 2,  toweridx)    
            #m = re.search('(\d+)', nexttower['tower_name'])
            #toweridx = ''
            #if m:
                #toweridx = m.group(0)
            #sheet.write(idx + 1   + 1 , 3, nexttower['id'])    
            #sheet.write(idx + 1   + 1 , 4, nexttower['tower_name'])    
            #sheet.write(idx + 1   + 1 , 5, toweridx)
        #else:
            #sheet.write(idx + 1   + 1 , 0, tower['id'])    
            #sheet.write(idx + 1   + 1 , 1, tower['tower_name'])    
            #sheet.write(idx + 1   + 1 , 2, toweridx)    
            #sheet.write(idx + 1   + 1 , 3, str(uuid.UUID('1'*32)))    
            #sheet.write(idx + 1   + 1 , 4, u'变电站')    
            #sheet.write(idx + 1   + 1 , 5, 0)    
        
    
    
    #耐张段信息    
    sheet = book.add_sheet(line['line_name'] + u'_耐张段信息')
    sheet.write(0, 0, u'起始杆塔名称')
    sheet.write(0, 1, u'起始杆塔序号')
    sheet.write(0, 2, u'结束杆塔名称')
    sheet.write(0, 3, u'结束杆塔序号')
    sheet.write(0, 4, u'耐张段长(单位米)')
    sheet.write(0, 5, u'代表档距(单位米)')
    sheet.write(0, 6, u'风速(单位米/秒)')
    sheet.write(0, 7, u'履冰(单位毫米)')
    sheet.write(0, 8, u'地线型号')
    sheet.write(0, 9, u'导线型号')
    sheet.write(0, 10, u'耐张系数K')
    
    #特殊区段信息    
    sheet = book.add_sheet(line['line_name'] + u'_特殊区段信息')
    sheet.write(0, 0, u'起始杆塔名称')
    sheet.write(0, 1, u'起始杆塔序号')
    sheet.write(0, 2, u'结束杆塔名称')
    sheet.write(0, 3, u'结束杆塔序号')
    sheet.write(0, 4, u'特殊区段类型')
    sheet.write(0, 5, u'特殊区段长度(单位米)')
    sheet.write(0, 6, u'特殊区段描述')
        
    #交叉跨越信息    
    sheet = book.add_sheet(line['line_name'] + u'_交叉跨越信息')
    sheet.write(0, 0, u'前一个杆塔id')
    sheet.write(0, 1, u'前一个杆塔名称')
    sheet.write(0, 2, u'前一个杆塔杆塔序号')
    sheet.write(0, 3, u'后一个杆塔id')
    sheet.write(0, 4, u'后一个杆塔名称')
    sheet.write(0, 5, u'后一个杆塔杆塔序号')
    sheet.write(0, 6, u'交叉跨越经度')
    sheet.write(0, 7, u'交叉跨越纬度')
    sheet.write(0, 8, u'交叉跨越高程')
    cp = [u'电力线',u'低压线', u'通讯线',u'广播线',u'房屋',u'公路',u'铁路',u'河流',u'其他']
    for i in cp:
        sheet.write(0, 9+cp.index(i)*2, u'交叉跨越类型-%s' % i)
        sheet.write(0, 10+cp.index(i)*2, u'交叉跨越-%s描述' % i)
    
        
    for tower in towers:
        m = re.search('(\d+)', tower['tower_name'])
        toweridx = ''
        idx = towers.index(tower)
        if m:
            toweridx = m.group(0)

        if idx+1 < len(towers):
            nexttower = towers[idx+1]
            sheet.write(idx + 1 , 0, tower['id'])    
            sheet.write(idx + 1 , 1, tower['tower_name'])    
            sheet.write(idx + 1 , 2,  toweridx)    
            m = re.search('(\d+)', nexttower['tower_name'])
            toweridx = ''
            if m:
                toweridx = m.group(0)
            sheet.write(idx + 1, 3, nexttower['id'])    
            sheet.write(idx + 1, 4, nexttower['tower_name'])    
            sheet.write(idx + 1, 5, toweridx)

            
        #if idx==0:
            #sheet.write(idx  + 1 , 0, str(uuid.UUID('0'*32)))    
            #sheet.write(idx  + 1 , 1, u'变电站')    
            #sheet.write(idx  + 1 , 2,  0)
            #sheet.write(idx  + 1 , 3,  tower['id'])
            #sheet.write(idx  + 1 , 4, tower['tower_name'])    
            #sheet.write(idx  + 1 , 5, toweridx)    
        
        #if idx+1 < len(towers):
            #nexttower = towers[idx+1]
            #sheet.write(idx + 1  + 1 , 0, tower['id'])    
            #sheet.write(idx + 1  + 1 , 1, tower['tower_name'])    
            #sheet.write(idx + 1   + 1 , 2,  toweridx)    
            #m = re.search('(\d+)', nexttower['tower_name'])
            #toweridx = ''
            #if m:
                #toweridx = m.group(0)
            #sheet.write(idx + 1   + 1 , 3, nexttower['id'])    
            #sheet.write(idx + 1   + 1 , 4, nexttower['tower_name'])    
            #sheet.write(idx + 1   + 1 , 5, toweridx)
        #else:
            #sheet.write(idx + 1   + 1 , 0, tower['id'])    
            #sheet.write(idx + 1   + 1 , 1, tower['tower_name'])    
            #sheet.write(idx + 1   + 1 , 2, toweridx)    
            #sheet.write(idx + 1   + 1 , 3, str(uuid.UUID('1'*32)))    
            #sheet.write(idx + 1   + 1 , 4, u'变电站')    
            #sheet.write(idx + 1   + 1 , 5, 0)    
        
    p = os.path.join(XLS_REPORT_DIR,  line['line_name'] + u'_待填.xls')
    book.save(p)
    

def import_from_excel():
    def dms2d(d, m, s): 
        ret = float(d) + float(m)/60.0 + float(s)/3600.0
        return ret
    ret = {}
    #ret['line'] = []
    #ret['towers'] = {}
    filepaths = {u'永甘甲线':ur'D:\gis\南网\昭通\云南_昭通_500_永甘甲线.xls',
                 u'永甘乙线': ur'D:\gis\南网\昭通\云南_昭通_500_永甘乙线.xls',
                 u'镇永甲线': ur'D:\gis\南网\昭通\云南_昭通_500_镇永甲线.xls',
                 u'甘大线': ur'D:\gis\南网\昭通\云南_昭通_220_甘大线.xls',
                 u'甘镇线': ur'D:\gis\南网\昭通\云南_昭通_220_甘镇线.xls',
                 }
    
    for key in filepaths.keys():
        lines = odbc_get_records('TABLE_LINE', "line_name='%s'" % key)
        #print('%s=%s' %(key,lines[0]['id']))
        line_id = lines[0]['id']
        book = xlrd.open_workbook(filepaths[key])
        sheet_line = book.sheet_by_name('Sheet1')
        ret[line_id] = []
        print(key)
        for i in range(sheet_line.nrows):
            try:
                ret[line_id].append( {'line_id':line_id, 
                                       'tower_name': key + str(int(sheet_line.cell_value(i+1,0))) + '#',
                                       'geo_x':dms2d(sheet_line.cell_value(i+1,1), sheet_line.cell_value(i+1,2), sheet_line.cell_value(i+1,3)  ),
                                       'geo_y':dms2d(sheet_line.cell_value(i+1,4), sheet_line.cell_value(i+1,5), sheet_line.cell_value(i+1,6)  ),
                                       } )
            except:
                pass
    
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    
    for key in ret.keys():
        cur.execute('''DELETE FROM TABLE_TOWER WHERE line_id='%s' ''' % key)
        #cur.execute('''DELETE FROM TABLE_TOWER_RELATION WHERE line_id='%s' ''' % key)
        cur.execute('''DELETE FROM TABLE_SEGMENT WHERE line_id='%s' ''' % key)
        
        towerid, tower_startid, tower_endid = None, None, None
        for tower in ret[key]:
            idx = ret[key].index(tower)
            tower_endid = towerid = str(uuid.uuid4()).upper()
            if idx  == len(ret[key]):
                tower_startid = None
            if tower_startid and tower_endid:
                #cur.execute('''INSERT INTO TABLE_TOWER_RELATION VALUES(?, ?, ?, ?)''',(str(uuid.uuid4()).upper(), key, tower_startid,  tower_endid))
                cur.execute('''INSERT INTO TABLE_SEGMENT VALUES(?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL)''',(str(uuid.uuid4()).upper(), key, tower_startid,  tower_endid, 0,0,0,0))
            cur.execute('''INSERT INTO TABLE_TOWER VALUES(?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?)''',(towerid, key, None, tower['tower_name'], str(uuid.UUID('0'*32)), tower['geo_x'],tower['geo_y'], 0, 0, None, 0, 0, 0, 0, 0))
            tower_startid = tower_endid
            
    cur.commit()
    cur.close()
    conn.close()
    return ret
    
    
def import_from_excel1():
    ret = {}
    filepath = ur'D:\gis\南网\昭通\昭通_220kv_永发I,II回线.xls'
    
    book = xlrd.open_workbook(filepath)
    
    for key in [u'永发I回线',u'永发II回线']:
        lines = odbc_get_records('TABLE_LINE', "line_name='%s'" % key)
        line_id = lines[0]['id']
        sheet_line = book.sheet_by_name(key)
        ret[line_id] = []
        #print(key)
        for i in range(sheet_line.nrows):
            try:
                if (i+1)%2>0:
                    ret[line_id].append( {'line_id':line_id, 
                                           'tower_name': key + unicode(int(sheet_line.cell_value(i+1,0))) + '#',
                                           'model_code': sheet_line.cell_value(i+1,1) ,
                                           'denomi_height': float(sheet_line.cell_value(i+1,2)),
                                           'horizontal_span': int(sheet_line.cell_value(i+1,3)),
                                           'vertical_span': int(sheet_line.cell_value(i+1,4)),
                                           } )
                    print(key + unicode(int(sheet_line.cell_value(i+1,0))) + '#')
            except:
                pass
            
        #print('%s=%d' % (key, len(ret[line_id])))
            
    
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    
    for key in ret.keys():
        cur.execute('''DELETE FROM TABLE_TOWER WHERE line_id='%s' ''' % key)
        #cur.execute('''DELETE FROM TABLE_TOWER_RELATION WHERE line_id='%s' ''' % key)
        cur.execute('''DELETE FROM TABLE_SEGMENT WHERE line_id='%s' ''' % key)
        
        towerid, tower_startid, tower_endid = None, None, None
        for tower in ret[key]:
            idx = ret[key].index(tower)
            tower_endid = towerid = str(uuid.uuid4()).upper()
            if idx  == len(ret[key]):
                tower_startid = None
            if tower_startid and tower_endid:
                #cur.execute('''INSERT INTO TABLE_TOWER_RELATION VALUES(?, ?, ?, ?)''',(str(uuid.uuid4()).upper(), key, tower_startid,  tower_endid))
                cur.execute('''INSERT INTO TABLE_SEGMENT VALUES(?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL)''',(str(uuid.uuid4()).upper(), key, tower_startid,  tower_endid, 0,0,0,0))
            cur.execute('''INSERT INTO TABLE_TOWER VALUES(?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?)''',(towerid, key, None, tower['tower_name'], str(uuid.UUID('0'*32)), None, None, None, 0, tower['model_code'], tower['denomi_height'], tower['horizontal_span'], tower['vertical_span'], 0, 0))
            tower_startid = tower_endid
            
    cur.commit()
    cur.close()
    conn.close()
    return ret
    
    
def excel_to_database(line_name):
    lines = odbc_get_records('TABLE_LINE',"line_name='%s'" % line_name)
    line_id = lines[0]['id']
    DIR_EXCLE = ur'G:\work\csharp\kmgdgis\doc'
    filepath = os.path.join(DIR_EXCLE ,  line_name + u'_已填.xls')
    book = xlrd.open_workbook(filepath)
    sqls = []
    #线路信息
    sheet_line = book.sheet_by_name(line_name + u'_线路信息')
    if sheet_line.nrows>1:
        length, manage_length = 0., 0.
        line_code = sheet_line.cell_value(1, 1)
        if isinstance(sheet_line.cell_value(1, 2), float):
            length = float(sheet_line.cell_value(1, 2))
        if isinstance(sheet_line.cell_value(1, 3), float):
            manage_length = float(sheet_line.cell_value(1, 3))
        start_point = sheet_line.cell_value(1, 4)
        end_point = sheet_line.cell_value(1, 5)
        status = sheet_line.cell_value(1, 6)
        maintenace  = sheet_line.cell_value(1, 7)
        management  = sheet_line.cell_value(1, 8)
        owner  = sheet_line.cell_value(1, 9)
        team  = sheet_line.cell_value(1, 10)
        responsible  = sheet_line.cell_value(1, 11)
        investor = sheet_line.cell_value(1, 12)
        designer = sheet_line.cell_value(1, 13)
        supervisor = sheet_line.cell_value(1, 14)
        constructor = sheet_line.cell_value(1, 15)
        operator = sheet_line.cell_value(1, 16)
        finish_date = sheet_line.cell_value(1, 17)
        production_date = sheet_line.cell_value(1, 18)
        decease_date = sheet_line.cell_value(1, 19)
        
        if isinstance(finish_date, str):
            finish_date = '1900-01-01'
        if isinstance(production_date, str):
            production_date = '1900-01-01'
        if isinstance(decease_date, str):
            decease_date = '1900-01-01'
        
        dtfmt = '%Y-%m-%d'
        
        if isinstance(finish_date, float):
            tu = xlrd.xldate_as_tuple(finish_date, book.datemode)
            dt = datetime.datetime(*tu)
            finish_date = dt.strftime(dtfmt)
        
        if isinstance(production_date, float):
            tu = xlrd.xldate_as_tuple(production_date, book.datemode)
            dt = datetime.datetime(*tu)
            production_date = dt.strftime(dtfmt)
        
        if isinstance(decease_date, float):
            tu = xlrd.xldate_as_tuple(decease_date, book.datemode)
            dt = datetime.datetime(*tu)
            decease_date = dt.strftime(dtfmt)
        
            
        sql = '''UPDATE TABLE_LINE SET
                       line_code='%s',
                       length=%f,
                       manage_length=%f,
                       start_point='%s',
                       end_point='%s',
                       status='%s',
                       maintenace='%s',
                       management='%s',
                       owner='%s',
                       team='%s',
                       responsible='%s',
                       investor='%s',
                       designer='%s',
                       supervisor='%s',
                       constructor='%s',
                       operator='%s',
                       finish_date=NULL,
                       production_date=NULL,
                       decease_date=NULL
                       WHERE line_name='%s' ''' % (
                        line_code,
                        length,
                        manage_length,
                        start_point,
                        end_point,
                        status,
                        maintenace,
                        management,
                        owner,
                        team,
                        responsible,
                        investor,
                        designer,
                        supervisor,
                        constructor,
                        operator,
                        #finish_date,
                        #production_date,
                        #decease_date,
                        line_name
                    )
        sqls.append(sql)


    
    
    #杆塔信息
    sheet_tower = book.sheet_by_name(line_name + u'_杆塔信息')
    for i in range(1, sheet_tower.nrows):
        tower_id = sheet_tower.cell_value(i, 0)
        tower_name = sheet_tower.cell_value(i, 1)
        if len(tower_id)>0:
            tower_code = sheet_tower.cell_value(i, 3)
            model_code = sheet_tower.cell_value(i, 4)
            denomi_height = 0.
            if isinstance(sheet_tower.cell_value(i, 5), float):
                denomi_height = sheet_tower.cell_value(i, 5)
            horizontal_span = 0
            if isinstance(sheet_tower.cell_value(i, 6), float):
                horizontal_span = int(sheet_tower.cell_value(i, 6))
            vertical_span = 0
            if isinstance(sheet_tower.cell_value(i, 7), float):
                vertical_span = int(sheet_tower.cell_value(i, 7))
            building_level = 0.
            if isinstance(sheet_tower.cell_value(i, 8), float):
                building_level = sheet_tower.cell_value(i, 8)
            line_rotate = 0.
            if isinstance(sheet_tower.cell_value(i, 9), float):
                line_rotate = sheet_tower.cell_value(i, 9)
    
            sql = ''' 
               UPDATE TABLE_TOWER SET 
               tower_code = '%s',
               model_code = '%s',
               denomi_height = %f,
               horizontal_span = %d,
               vertical_span = %d,
               building_level = %f,
               line_rotate = %f
               WHERE id='%s'
            ''' % (
                tower_code,
                model_code,
                denomi_height,
                horizontal_span,
                vertical_span,
                building_level,
                line_rotate,
                tower_id
                )
            sqls.append(sql)
            
            
    #杆塔附件信息
    sheet_tower_attach = book.sheet_by_name(line_name + u'_杆塔附件信息')
    for i in range(1, sheet_tower_attach.nrows):
        tower_id = sheet_tower_attach.cell_value(i, 0)
        if len(tower_id)>0:
            sql = '''DELETE FROM TABLE_TOWER_METALS WHERE tower_id='%s' ''' % tower_id
            sqls.append(sql)
            
            for j in range(3, sheet_tower_attach.ncols):
                if j in range(3,15,3):
                    if len(sheet_tower_attach.cell_value(i, j))>0:
                        if isinstance(sheet_tower_attach.cell_value(i, j+1), float) and isinstance(sheet_tower_attach.cell_value(i, j+2), float):
                            sql = '''INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d, %d, NULL)
                            ''' % (
                                str(uuid.uuid4()).upper(),
                                tower_id,
                                u'绝缘子串',
                                u'导线绝缘子串',
                                sheet_tower_attach.cell_value(i, j),
                                int(sheet_tower_attach.cell_value(i, j+1)),
                                int(sheet_tower_attach.cell_value(i, j+2))
                                )
                            sqls.append(sql)
    
                if j in range(15,27,3):
                    if len(sheet_tower_attach.cell_value(i, j))>0:
                        if isinstance(sheet_tower_attach.cell_value(i, j+1), float) and isinstance(sheet_tower_attach.cell_value(i, j+2), float):
                            sql = ''' 
                               INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d, %d, NULL)
                            ''' % (
                                str(uuid.uuid4()).upper(),
                                tower_id,
                                u'绝缘子串',
                                u'跳线绝缘子串',
                                sheet_tower_attach.cell_value(i, j),
                                int(sheet_tower_attach.cell_value(i, j+1)),
                                int(sheet_tower_attach.cell_value(i, j+2)),
                                )
                            sqls.append(sql)
                if j in range(27, 30, 3):
                    if len(sheet_tower_attach.cell_value(i, j))>0:
                        if isinstance(sheet_tower_attach.cell_value(i, j+1), float) and isinstance(sheet_tower_attach.cell_value(i, j+2), float):
                            sql = ''' 
                               INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d,  NULL, %f)
                            ''' % (
                                str(uuid.uuid4()).upper(),
                                tower_id,
                                u'防震锤',
                                u'导线小号侧',
                                sheet_tower_attach.cell_value(i, j),
                                int(sheet_tower_attach.cell_value(i, j+1)),
                                sheet_tower_attach.cell_value(i, j+2)
                                )
                            sqls.append(sql)
    
                if j in range(30, 33, 3):
                    if len(sheet_tower_attach.cell_value(i, j))>0:
                        if isinstance(sheet_tower_attach.cell_value(i, j+1), float) and isinstance(sheet_tower_attach.cell_value(i, j+2), float):
                            sql = ''' 
                               INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d,  NULL, %f)
                            ''' % (
                                str(uuid.uuid4()).upper(),
                                tower_id,
                                u'防震锤',
                                u'导线大号侧',
                                sheet_tower_attach.cell_value(i, j),
                                int(sheet_tower_attach.cell_value(i, j+1)),
                                sheet_tower_attach.cell_value(i, j+2)
                                )
                            sqls.append(sql)
                if j in range(33, 36, 3):
                    if len(sheet_tower_attach.cell_value(i, j))>0:
                        if isinstance(sheet_tower_attach.cell_value(i, j+1), float) and isinstance(sheet_tower_attach.cell_value(i, j+2), float):
                            sql = ''' 
                               INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d,  NULL, %f)
                            ''' % (
                                str(uuid.uuid4()).upper(),
                                tower_id,
                                u'防震锤',
                                u'地线小号侧',
                                sheet_tower_attach.cell_value(i, j),
                                int(sheet_tower_attach.cell_value(i, j+1)),
                                sheet_tower_attach.cell_value(i, j+2)
                                )
                            sqls.append(sql)
    
                if j in range(36, 39, 3):
                    if len(sheet_tower_attach.cell_value(i, j))>0:
                        if isinstance(sheet_tower_attach.cell_value(i, j+1), float) and isinstance(sheet_tower_attach.cell_value(i, j+2), float):
                            sql = ''' 
                               INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d,  NULL, %f)
                            ''' % (
                                str(uuid.uuid4()).upper(),
                                tower_id,
                                u'防震锤',
                                u'地线大号侧',
                                sheet_tower_attach.cell_value(i, j),
                                int(sheet_tower_attach.cell_value(i, j+1)),
                                sheet_tower_attach.cell_value(i, j+2)
                                )
                            sqls.append(sql)
                if j in range(39, 41, 2):
                    if len(sheet_tower_attach.cell_value(i, j))>0:
                        if isinstance(sheet_tower_attach.cell_value(i, j+1), float) :
                            sql = ''' 
                               INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d,  NULL, NULL)
                            ''' % (
                                str(uuid.uuid4()).upper(),
                                tower_id,
                                u'地线金具串',
                                u'',
                                sheet_tower_attach.cell_value(i, j),
                                int(sheet_tower_attach.cell_value(i, j+1))
                                )
                            sqls.append(sql)
                if j in range(41, 43, 2):
                    if len(sheet_tower_attach.cell_value(i, j))>0:
                        if isinstance(sheet_tower_attach.cell_value(i, j+1), float) :
                            sql = ''' 
                               INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d,  NULL, NULL)
                            ''' % (
                                str(uuid.uuid4()).upper(),
                                tower_id,
                                u'OPGW金具串',
                                u'',
                                sheet_tower_attach.cell_value(i, j),
                                int(sheet_tower_attach.cell_value(i, j+1))
                                )
                            sqls.append(sql)
                if j in range(43, 44, 1):
                    if isinstance(sheet_tower_attach.cell_value(i, j), float) :
                        sql = ''' 
                           INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d,  NULL, NULL)
                        ''' % (
                            str(uuid.uuid4()).upper(),
                            tower_id,
                            u'护线条',
                            u'',
                            u'',
                            int(sheet_tower_attach.cell_value(i, j))
                            )
                        sqls.append(sql)
                if j in range(44, 45, 1):
                    if isinstance(sheet_tower_attach.cell_value(i, j), float) :
                        sql = ''' 
                           INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d,  NULL, NULL)
                        ''' % (
                            str(uuid.uuid4()).upper(),
                            tower_id,
                            u'引下夹具',
                            u'',
                            u'',
                            int(sheet_tower_attach.cell_value(i, j))
                            )
                        sqls.append(sql)
                if j in range(45, 46, 1):
                    if isinstance(sheet_tower_attach.cell_value(i, j), float) :
                        sql = ''' 
                           INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d,  NULL, NULL)
                        ''' % (
                            str(uuid.uuid4()).upper(),
                            tower_id,
                            u'余缆架',
                            u'',
                            u'',
                            int(sheet_tower_attach.cell_value(i, j))
                            )
                        sqls.append(sql)
                if j in range(46, 47, 1):
                    if isinstance(sheet_tower_attach.cell_value(i, j), float) :
                        sql = ''' 
                           INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d,  NULL, NULL)
                        ''' % (
                            str(uuid.uuid4()).upper(),
                            tower_id,
                            u'接续盒',
                            u'',
                            u'',
                            int(sheet_tower_attach.cell_value(i, j))
                            )
                        sqls.append(sql)
                if j in range(47, 48, 1):
                    if isinstance(sheet_tower_attach.cell_value(i, j), float) :
                        sql = ''' 
                           INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', %d,  NULL, NULL)
                        ''' % (
                            str(uuid.uuid4()).upper(),
                            tower_id,
                            u'不锈钢抱箍',
                            u'',
                            u'',
                            int(sheet_tower_attach.cell_value(i, j))
                            )
                        sqls.append(sql)
                if j in range(48, 50, 2):
                    if len(sheet_tower_attach.cell_value(i, j))>0:
                        if isinstance(sheet_tower_attach.cell_value(i, j+1), float) :
                            sql = ''' 
                               INSERT INTO TABLE_TOWER_METALS VALUES( '%s', '%s', '%s', '%s', '%s', NULL, NULL, %f)
                            ''' % (
                                str(uuid.uuid4()).upper(),
                                tower_id,
                                u'接地装置',
                                u'',
                                sheet_tower_attach.cell_value(i, j),
                                sheet_tower_attach.cell_value(i, j+1)
                                )
                            sqls.append(sql)

    #线段信息
    sheet_segment = book.sheet_by_name(line_name + u'_线段信息')
    sql = '''DELETE FROM TABLE_SEGMENT WHERE line_id='%s'  '''  % line_id
    sqls.append(sql)
    
    for i in range(1, sheet_segment.nrows):
        small_tower = sheet_segment.cell_value(i, 0)
        big_tower = sheet_segment.cell_value(i, 3)
        if len(small_tower)>0 and len(big_tower)>0:
            splitting = sheet_segment.cell_value(i, 6)
            if isinstance(splitting, float):
                splitting = int(splitting)
            else:
                splitting = 1
                
            conductor_count = sheet_segment.cell_value(i, 7)
            if isinstance(conductor_count, float):
                conductor_count = int(conductor_count)
            else:
                conductor_count = 0
                
            crosspoint_count = sheet_segment.cell_value(i, 8)
            if isinstance(crosspoint_count, float):
                crosspoint_count = int(crosspoint_count)
            else:
                crosspoint_count = 0
                
            length = sheet_segment.cell_value(i, 9)
            if isinstance(length, float):
                pass
            else:
                length = 0.
                
            seperator_bar = sheet_segment.cell_value(i, 10)
            if isinstance(seperator_bar, float):
                seperator_bar = int(seperator_bar)
            else:
                seperator_bar = 0
                
            connector_count = sheet_segment.cell_value(i, 11)
            if isinstance(connector_count, float):
                connector_count = int(connector_count)
            else:
                connector_count = 0
                
            connector_type = sheet_segment.cell_value(i, 12)
            
                
            if small_tower=='start':
                small_tower = uuid.UUID('0'*32)
            if big_tower=='end':
                big_tower = uuid.UUID('1'*32)
                
            sql = '''INSERT INTO TABLE_SEGMENT 
                     VALUES( 
                     '%s',
                     '%s',
                     '%s',
                     '%s',
                     %d,
                     %d,
                     %d, 
                     %f,
                     %d,
                     %d,
                     '%s'
                     ) 
                     ''' % (
                             str(uuid.uuid4()).upper(),
                             line_id,
                             small_tower,
                             big_tower,
                             splitting,
                             conductor_count,
                             crosspoint_count,
                             length,
                             seperator_bar,
                             connector_count,
                             connector_type)
            sqls.append(sql)
    
    
    #耐张段信息
    sheet_strain = book.sheet_by_name(line_name + u'_耐张段信息')
    
    sql = '''DELETE FROM TABLE_STRAIN_SECTION WHERE line_id='%s'  '''  % line_id
    sqls.append(sql)
    
    for i in range(1, sheet_strain.nrows):
        start_tower_name = sheet_strain.cell_value(i, 0)
        end_tower_name = sheet_strain.cell_value(i, 2)
        if len(start_tower_name)>0 and len(end_tower_name)>0:
            tpairs = odbc_get_records('TABLE_TOWER', "tower_name in ('%s','%s')" % (start_tower_name, end_tower_name))
            if len(tpairs)<2:
                print('耐张段信息[%s,%s]不能在数据库中找到' % (start_tower_name, end_tower_name))
            else:
                start_tower, end_tower = tpairs[0]['id'], tpairs[1]['id']
                
                total_length = sheet_strain.cell_value(i, 4)
                if isinstance(total_length, float):
                    total_length = int(total_length)
                else:
                    total_length = 0
            
                typical_span = sheet_strain.cell_value(i, 5)
                if isinstance(typical_span, float):
                    typical_span = int(typical_span)
                else:
                    typical_span = 0
            
                wind_speed = sheet_strain.cell_value(i, 6)
                if isinstance(wind_speed, float):
                    pass
                else:
                    wind_speed = 0.
            
                ice_thickness = sheet_strain.cell_value(i, 7)
                if isinstance(ice_thickness, float):
                    ice_thickness = int(ice_thickness)
                else:
                    ice_thickness = 0
                    
                ground_type = sheet_strain.cell_value(i, 8)
                conductor_type = sheet_strain.cell_value(i, 9)
                
                k_value = sheet_strain.cell_value(i, 10)
                if isinstance(k_value, float):
                    pass
                else:
                    k_value = 0.
                
                sql = '''INSERT INTO TABLE_STRAIN_SECTION 
                         VALUES( 
                         '%s',
                         '%s',
                         '%s',
                         '%s',
                         %d,
                         %d,
                         %f, 
                         '%s',
                         '%s',
                         %d,
                         %f, 
                         ''
                         ) 
                         ''' % (
                                 str(uuid.uuid4()).upper(),
                                 line_id,
                                 start_tower,
                                 end_tower,
                                 total_length,
                                 typical_span,
                                 k_value,
                                 conductor_type,
                                 ground_type,
                                 ice_thickness,
                                 wind_speed
                             )
                sqls.append(sql)
    
    
    #特殊区段信息
    sheet_special = book.sheet_by_name(line_name + u'_特殊区段信息')
    
    sql = '''DELETE FROM TABLE_SPECIAL_SECTION WHERE line_id='%s'  '''  % line_id
    sqls.append(sql)
    
    for i in range(1, sheet_special.nrows):
        start_tower_name = sheet_special.cell_value(i, 0)
        end_tower_name = sheet_special.cell_value(i, 2)
        if len(start_tower_name)>0 and len(end_tower_name)>0:
            tpairs = odbc_get_records('TABLE_TOWER', "tower_name in ('%s','%s')" % (start_tower_name, end_tower_name))
            if len(tpairs)<2:
                print('特殊区段信息[%s,%s]不能在数据库中找到' % (start_tower_name, end_tower_name))
            else:
                start_tower, end_tower = tpairs[0]['id'], tpairs[1]['id']
                
                ss_type = sheet_special.cell_value(i, 4)
                
                length = sheet_special.cell_value(i, 5)
                if isinstance(length, float):
                    pass
                else:
                    length = 0.
            
                    
                detail = sheet_special.cell_value(i, 6)
                
                
                sql = '''INSERT INTO TABLE_SPECIAL_SECTION 
                         VALUES( 
                         '%s',
                         '%s',
                         '%s',
                         '%s',
                         '%s',
                         %f, 
                         '%s'
                         ) 
                         ''' % (
                                 str(uuid.uuid4()).upper(),
                                 line_id,
                                 start_tower,
                                 end_tower,
                                 ss_type,
                                 length,
                                 detail
                             )
                sqls.append(sql)
    
    ##交叉跨越信息
    ###sheet_cross_over = book.sheet_by_name(line_name + u'_交叉跨越信息')
    ###sql = '''DELETE FROM TABLE_CROSS_POINT WHERE line_id='%s'  '''  % line_id
    ###sqls.append(sql)
    
    #for i in range(1, sheet_special.nrows):
        #start_tower = sheet_cross_over.cell_value(i, 0)
        #end_tower = sheet_cross_over.cell_value(i, 3)
        #if len(start_tower)>0 and len(end_tower)>0:
            #seg = odbc_get_records('TABLE_SEGMENT', "small_tower='%s' AND big_tower='%s')" % (start_tower, end_tower))
            #if len(seg)<1:
                #print('交叉跨越信息[%s,%s]不能在数据库中找到' % (start_tower, end_tower))
            #else:
                #segid = seg[0]['id']
                #sql = '''DELETE FROM TABLE_CROSS_POINT WHERE segment_id='%s'  '''  % segid
                #sqls.append(sql)
                
                #for j in range(6, sheet_cross_over.ncols):
                    #if j in range(9,11,2):
                        #if isinstance(sheet_cross_over.cell_value(i, j), float):
                            #sql = '''INSERT INTO TABLE_CROSS_POINT  VALUES(  '%s', '%s', '%s', 0.0,0.0,0.0, '%s' ) ''' % (
                                             #str(uuid.uuid4()).upper(),
                                             #segid,
                                             #u'电力线',
                                             #sheet_cross_over.cell_value(i, j+1)
                                             #)
                            #sqls.append(sql)
    
    
    
    

    odbc_execute_sqls(sqls)


def insert_dragon():
    lines = odbc_get_records('TABLE_LINE', '1=1')
    sqls = []
    for line in lines:
        start_dragon = str(uuid.uuid4()).upper()
        end_dragon = str(uuid.uuid4()).upper()
        
        towers = odbc_get_sorted_tower_by_line(line['id'])
        
        tower_start, tower_end = towers[0], towers[len(towers)-1]
        sqls.append('''INSERT INTO TABLE_TOWER VALUES('%s', '%s', NULL, '%s', '%s',  NULL, NULL, NULL, NULL, NULL, NULL,NULL,NULL,NULL,NULL)''' % (start_dragon, line['id'], line['line_name'] + u'起始龙门架', str(uuid.UUID('0'*32))))
        sqls.append('''INSERT INTO TABLE_TOWER VALUES('%s', '%s', NULL, '%s', '%s',  NULL, NULL, NULL, NULL, NULL, NULL,NULL,NULL,NULL,NULL)''' % (end_dragon,   line['id'], line['line_name'] + u'结束龙门架', str(uuid.UUID('0'*32))))
        sqls.append('''INSERT INTO TABLE_SEGMENT VALUES('%s', '%s', '%s', '%s', 0, 0, 0, 0, NULL, NULL, NULL)''' % (str(uuid.uuid4()).upper(), line['id'], start_dragon,  tower_start['id']))
        sqls.append('''INSERT INTO TABLE_SEGMENT VALUES('%s', '%s', '%s', '%s', 0, 0, 0, 0, NULL, NULL, NULL)''' % (str(uuid.uuid4()).upper(), line['id'], tower_end['id'],end_dragon))
        sqls.append('''UPDATE TABLE_LINE SET start_tower='%s',end_tower='%s' WHERE id='%s' ''' % (start_dragon, end_dragon, line['id']))
            
    odbc_execute_sqls(sqls)


def import_from_excel2_lgt_lat():
    sqls = []
    for f in [ur'D:\work\python\ogc_server\doc\云南_昭通_220_永发Ⅰ回线.xls', ur'D:\work\python\ogc_server\doc\云南_昭通_220_永发Ⅱ回线.xls']:
        book = xlrd.open_workbook(f)
        sheet = book.sheet_by_name('Sheet1')
        for i in range(1, sheet.nrows):
            tower_name = sheet.cell_value(i, 0)
            if len(tower_name)>0:
                lgt = sheet.cell_value(i, 5)
                lat = sheet.cell_value(i, 9)
                #print('%s=[%f,%f]' % (tower_name, lgt, lat))
                sql = '''
                         UPDATE TABLE_TOWER SET geo_x=%f, geo_y=%f WHERE tower_name='%s' 
                ''' % (lgt, lat, tower_name)
                sqls.append(sql)
    odbc_execute_sqls(sqls)


def delete_dragon():
    lines = odbc_get_records('TABLE_LINE', '1=1')
    sqls = []
    for line in lines:
        towers = odbc_get_sorted_tower_by_line(line['id'])
        sqls.append('''UPDATE TABLE_LINE SET start_tower='%s',end_tower='%s' WHERE id='%s' ''' % (towers[0]['id'], towers[len(towers)-1]['id'], line['id']))
    
    odbc_execute_sqls(sqls)
    
def insert_lost_():
    line_id = '4436a644-7f61-426d-a6fe-f9b07d7a9142'
    lines = odbc_get_records('TABLE_LINE', "id='%s'" % line_id)
    line_name = lines[0]['line_name']
    idx = 349
    
    towers0 = odbc_get_sorted_tower_by_line(line_id)
    sqls = []
    towerid, tower_startid, tower_endid = None, None, None
    for i in range(23):
        idx += 1
        id = str(uuid.uuid4()).upper()
        if i==0:
            tower_startid = towers0[len(towers0)-1]['id']
        tower_endid = id
        #if idx  == 22:
            #tower_endid = None
            
        if tower_startid and tower_endid:
            sql = '''INSERT INTO TABLE_SEGMENT VALUES(
                     '%s', 
                     '%s', 
                     '%s', 
                     '%s', 
                     0, 
                     0, 
                     0, 
                     0, 
                     NULL, 
                     NULL, 
                     NULL)''' % (
                                  id, 
                                  line_id, 
                                  tower_startid,  
                                  tower_endid
                              )
            sqls.append(sql)
        sql = '''INSERT INTO TABLE_TOWER VALUES(
                '%s', 
                '%s', 
                NULL, 
                '%s', 
                '%s',  
                NULL, 
                NULL, 
                NULL, 
                NULL, 
                NULL,  
                NULL, 
                NULL, 
                NULL, 
                NULL, 
                NULL)''' % (id, line_id, line_name + str(idx) + '#', str(uuid.UUID('0'*32)))
        sqls.append(sql)
        tower_startid = tower_endid
    odbc_execute_sqls(sqls)

def sqlize_data(dataobj):
    ret = {}
    for k in dataobj.keys():
        if dataobj[k] is None:
            ret[k] = "NULL"
        elif isinstance(dataobj[k], str) or isinstance(dataobj[k], unicode):
            ret[k] = "'%s'" % dataobj[k]
        elif isinstance(dataobj[k], int) or isinstance(dataobj[k], float):
            ret[k] = "%s" % str(dataobj[k])
        else:
            ret[k] = "'%s'" % str(dataobj[k])
    return ret
    
def odbc_execute_sqls(sqls, area):
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect(ODBC_STRING[area])
        cur = conn.cursor()
        for sql in sqls:
            cur.execute(sql)
        cur.commit()

    except:
        print(sys.exc_info()[1])
        if cur:
            cur.rollback()
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    

    
def merge_dem():
    #import gdal_merge
    #sys.exit(gdal_merge.main(sys.argv))
    
    s = r'-o "H:\gis\YN_DEM1.tif" '
    l = []
    for root, dirs, files  in os.walk(r'H:\gis\demdata\zip', topdown=False):
        for name in files:
            if len(re.findall(r'ASTGTM2_\w{7}_dem', name))>0:
                p = os.path.join(root, name)
                l.append(p)
        #for name in dirs:
            #p = os.path.join(root, name)

    argv = ['', '-o', r"H:\gis\YN_DEM1.tif",]
    for i in l:
        print(i)
        argv.append(i)
    print(len(l))
        
    #print(argv)
    import gdal_merge
    gdal_merge.main(argv)

def merge_dem2():
    l = []
    #for root, dirs, files  in os.walk(ur'H:\gis', topdown=False):
    root = ur'H:\gis\demdata_srtm'
    for name in os.listdir(root):
        if len(re.findall(r'srtm_\d{2}_\d{2}', name))>0 and name[-4:] == '.tif':
            p = os.path.join(root, name)
            l.append(p)
    #for name in dirs:
        #p = os.path.join(root, name)

    argv = ['', '-o', r"H:\gis\YN_DEM_SRTM.tif",]
    for i in l:
        print(i)
        argv.append(i)
    print(len(l))
        
    #print(argv)
    import gdal_merge
    gdal_merge.main(argv)

def test_update_model_code(line_id):
    towers = odbc_get_records('TABLE_TOWER', "line_id='%s'" % line_id)
    s = set()
    sqls = []
    for tower in towers:
        if tower['model_code'] is None:
            tower['model_code'] = 'test2'
            sql = """ UPDATE TABLE_TOWER SET model_code='%s' WHERE id='%s'""" % ( 'test2', tower['id'])
            sqls.append(sql)
        s.add(tower['model_code'] )
    for mc in s:
        sql = """ INSERT INTO TABLE_CONTACT_POINT VALUES('%s', '%s', '%s', '反', NULL, NULL, 0,  -20, 140, -20)  """ % (str(uuid.uuid4()).upper(), line_id, mc)
        sqls.append(sql)
        sql = """ INSERT INTO TABLE_CONTACT_POINT VALUES('%s', '%s', '%s', '反', NULL, NULL, 1,  -10, 150, -20)  """ % (str(uuid.uuid4()).upper(), line_id, mc)
        sqls.append(sql)
        sql = """ INSERT INTO TABLE_CONTACT_POINT VALUES('%s', '%s', '%s', '反', NULL, NULL, 2,  10, 150, -20)  """ % (str(uuid.uuid4()).upper(), line_id, mc)
        sqls.append(sql)
        sql = """ INSERT INTO TABLE_CONTACT_POINT VALUES('%s', '%s', '%s', '反', NULL, NULL, 3,  20, 140, -20)  """ % (str(uuid.uuid4()).upper(), line_id, mc)
        sqls.append(sql)
        sql = """ INSERT INTO TABLE_CONTACT_POINT VALUES('%s', '%s', '%s', '正', NULL, NULL, 0,  -20, 140, 20)  """ % (str(uuid.uuid4()).upper(), line_id, mc)
        sqls.append(sql)
        sql = """ INSERT INTO TABLE_CONTACT_POINT VALUES('%s', '%s', '%s', '正', NULL, NULL, 1,  -10, 150, 20)  """ % (str(uuid.uuid4()).upper(), line_id, mc)
        sqls.append(sql)
        sql = """ INSERT INTO TABLE_CONTACT_POINT VALUES('%s', '%s', '%s', '正', NULL, NULL, 2,  10, 150, 20)  """ % (str(uuid.uuid4()).upper(), line_id, mc)
        sqls.append(sql)
        sql = """ INSERT INTO TABLE_CONTACT_POINT VALUES('%s', '%s', '%s', '正', NULL, NULL, 3,  20, 140, 20)  """ % (str(uuid.uuid4()).upper(), line_id, mc)
        sqls.append(sql)
        
    odbc_execute_sqls(sqls)
        
def test_insert_wire_segment(line_id):
    sqls = []
    towers = odbc_get_sorted_tower_by_line(line_id)
    
    
    start_tower, end_tower = None, None
    for tower in towers:
        end_tower = tower
        if start_tower and end_tower:
            obj0 = sqlize_data(start_tower)
            obj1 = sqlize_data(end_tower)
            for i in range(4):
                sql = """ INSERT INTO TABLE_WIRE_SEGMENT VALUES(
                            %s, 
                            %s,
                            %s, 
                            %d,
                            %d,
                            %s
                            )""" % (
                            "'%s'" % str(uuid.uuid4()).upper(),
                            obj0['id'],
                            obj1['id'],
                            i,
                            i,
                            "'D'"
                           )
                sqls.append(sql)
        start_tower = end_tower
        if end_tower == towers[len(towers)-1]:
            break
    odbc_execute_sqls(sqls)

def odbc_get_exist_record(table, value1, value2, area=''):
    ret = []
    if table == 'TABLE_WIRE_SEGMENT':
        ret = odbc_get_records(table, "start_tower_id=%s AND end_tower_id=%s" % (value1,value2), area)
    elif table == 'TABLE_CONTACT_POINT':
        ret = odbc_get_records(table, "model_code=%s" % value1, area)
    elif table == 'TABLE_TOWER_MODEL':
        ret = odbc_get_records(table, "model_code=%s" % value1, area)
    elif table == 'TABLE_LINE_MATERIAL_SPECIFICATION':
        ret = odbc_get_records(table, "line_model=%s" % value1, area)
    elif table in [ 'TABLE_SPECIAL_SECTION','TABLE_STRAIN_SECTION', 'TABLE_WEATHER_SECTION']:
        ret = odbc_get_records(table, "start_tower=%s and end_tower=%s" % (value1,value2), area)
    return ret
    
def odbc_save_data_to_table(table, op, data, line_id=None, start_tower_id=None, end_tower_id=None, area='', only_sql=False):
    tower_id = start_tower_id
    ret = {}
    sqls = []
    
    if table=='TABLE_ZERO_INSULATOR_ABNORMAL':
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_records(table, "id=%s" % obj['id'], area)
                if len(l)>0:
                    sql = '''
                         UPDATE %s SET 
                         work_id=%s,
                         z_insulators=%s,
                         remark=%s,
                         record_date=%s,
                         record_submitted=%s
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['work_id'],
                            obj['z_insulators'],
                            obj['remark'],
                            obj['record_date'],
                            obj['record_submitted'],
                            obj['id']
                            )
                    
                else:
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            obj['id'],
                            obj['work_id'],
                            obj['z_insulators'],
                            obj['remark'],
                            obj['record_date'],
                            obj['record_submitted'],
                            )
            elif op=='delete':
                if ss['id'] and len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s 
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_TEMPERATURE_ABNORMAL':
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_records(table, "id=%s" % obj['id'], area)
                if len(l)>0:
                    sql = '''
                         UPDATE %s SET 
                         work_id=%s,
                         abnormal_position=%s,
                         absolute_temperature=%s,
                         relative_temperature=%s,
                         remark=%s,
                         record_date=%s,
                         record_submitted=%s
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['work_id'],
                            obj['abnormal_position'],
                            obj['absolute_temperature'],
                            obj['relative_temperature'],
                            obj['remark'],
                            obj['record_date'],
                            obj['record_submitted'],
                            obj['id']
                            )
                    
                else:
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            obj['id'],
                            obj['work_id'],
                            obj['abnormal_position'],
                            obj['absolute_temperature'],
                            obj['relative_temperature'],
                            obj['remark'],
                            obj['record_date'],
                            obj['record_submitted'],
                            )
            elif op=='delete':
                if ss['id'] and len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s 
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_RESISTANCE_MEASURE':
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_records(table, "id=%s" % obj['id'], area)
                if len(l)>0:
                    sql = '''
                         UPDATE %s SET 
                         work_id=%s,
                         design_value=%s,
                         measure_value_A=%s,
                         measure_value_B=%s,
                         measure_value_C=%s,
                         measure_value_D=%s,
                         remark=%s,
                         record_date=%s,
                         record_submitted=%s
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['work_id'],
                            obj['design_value'],
                            obj['measure_value_A'],
                            obj['measure_value_B'],
                            obj['measure_value_C'],
                            obj['measure_value_D'],
                            obj['remark'],
                            obj['record_date'],
                            obj['record_submitted'],
                            obj['id']
                            )
                    
                else:
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            obj['id'],
                            obj['work_id'],
                            obj['design_value'],
                            obj['measure_value_A'],
                            obj['measure_value_B'],
                            obj['measure_value_C'],
                            obj['measure_value_D'],
                            obj['remark'],
                            obj['record_date'],
                            obj['record_submitted'],
                            )
            elif op=='delete':
                if ss['id'] and len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s 
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_DENSITY_MEASURE':
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_records(table, "id=%s" % obj['id'], area)
                if len(l)>0:
                    sql = '''
                         UPDATE %s SET 
                         work_id=%s,
                         salt_density=%s,
                         dust_density=%s,
                         dirty_level=%s,
                         remark=%s,
                         record_date=%s
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['work_id'],
                            obj['salt_density'],
                            obj['dust_density'],
                            obj['dirty_level'],
                            obj['remark'],
                            obj['record_date'],
                            obj['id']
                            )
                    
                else:
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            obj['id'],
                            obj['work_id'],
                            obj['salt_density'],
                            obj['dust_density'],
                            obj['dirty_level'],
                            obj['remark'],
                            obj['record_date'],
                            )
            elif op=='delete':
                if ss['id'] and len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s 
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_THUNDER_COUNTER':
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_records(table, "id=%s" % obj['id'], area)
                if len(l)>0:
                    sql = '''
                         UPDATE %s SET 
                         attach_id=%s,
                         counter=%s,
                         report_date=%s,
                         reporter=%s
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['attach_id'],
                            obj['counter'],
                            obj['report_date'],
                            obj['reporter'],
                            obj['id']
                            )
                    
                else:
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            obj['id'],
                            obj['attach_id'],
                            obj['counter'],
                            obj['report_date'],
                            obj['reporter'],
                            )
            elif op=='delete':
                if ss['id'] and len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s 
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_POTENTIAL_RISK_INFO':
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_records(table, "id=%s" % obj['id'], area)
                if len(l)>0:
                    sql = '''
                         UPDATE %s SET 
                         risk_type=%s,
                         risk_info=%s,
                         geometry_type=%s,
                         appear_date=%s,
                         record_person=%s,
                         contact_person=%s,
                         contact_number=%s,
                         center_x=%s,
                         center_y=%s,
                         height=%s
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['risk_type'],
                            obj['risk_info'],
                            obj['geometry_type'],
                            obj['appear_date'],
                            obj['record_person'],
                            obj['contact_person'],
                            obj['contact_number'],
                            obj['center_x'],
                            obj['center_y'],
                            obj['height'],
                            obj['id']
                            )
                    
                else:
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            obj['id'],
                            obj['risk_type'],
                            obj['risk_info'],
                            obj['geometry_type'],
                            obj['appear_date'],
                            obj['record_person'],
                            obj['contact_person'],
                            obj['contact_number'],
                            obj['center_x'],
                            obj['center_y'],
                            obj['height'],
                            )
            elif op=='delete':
                if ss['id'] and len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s 
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_PIC_SHOT':
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_records(table, "pic_file_name=%s AND folder_name=%s" % (obj['pic_file_name'], obj['folder_name']), area)
                if len(l)>0:
                    sql = '''
                         UPDATE %s SET 
                         pic_type=%s,
                         shot_person=%s,
                         shot_date=%s, 
                         remark=%s 
                         WHERE 
                         pic_file_name=%s 
                         AND folder_name=%s 
                    ''' % (
                            table,
                            obj['pic_type'],
                            obj['shot_person'],
                            obj['shot_date'],
                            obj['remark'],
                            obj['pic_file_name'],
                            obj['folder_name']
                            )
                    
                else:
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            obj['folder_name'],
                            obj['pic_file_name'],
                            obj['pic_type'],
                            obj['shot_person'],
                            obj['shot_date'],
                            obj['remark']
                            )
            elif op=='delete':
                if ss['pic_file_name'] and len(ss['pic_file_name'])>0 and ss['folder_name'] and len(ss['folder_name'])>0:
                    sql = '''
                         DELETE FROM %s 
                         WHERE 
                         pic_file_name=%s 
                         AND folder_name=%s
                    ''' % (
                            table,
                            obj['pic_file_name'],
                            obj['folder_name']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_WORK_ITEM':
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_records(table, "id=%s" % obj['id'], area)
                if len(l)>0:
                    sql = '''
                         UPDATE %s SET 
                         task_id=%s,
                         tower_id=%s,
                         work_status=%s,
                         worker_id=%s,
                         finish_date=%s,
                         remark=%s
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['task_id'],
                            obj['tower_id'],
                            obj['work_status'],
                            obj['worker_id'],
                            obj['finish_date'],
                            obj['remark'],
                            obj['id']
                            )
                    
                else:
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            "'%s'" % str(uuid.uuid4()).upper(),
                            obj['task_id'],
                            obj['tower_id'],
                            obj['work_status'],
                            obj['worker_id'],
                            obj['finish_date'],
                            obj['remark']
                            )
            elif op=='delete':
                if ss['id'] and len(ss['id'])>0 :
                    sql = '''
                         DELETE FROM %s 
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_OPERATING_TASK':
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_records(table, "id=%s " % obj['id'], area)
                if len(l)>0:
                    sql = '''
                         UPDATE %s SET 
                         task_name=%s,
                         task_type=%s,
                         task_status=%s,
                         line_id=%s,
                         team_id=%s,
                         measurement=%s,
                         remark=%s
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['task_name'],
                            obj['task_type'],
                            obj['task_status'],
                            obj['line_id'],
                            obj['team_id'],
                            obj['measurement'],
                            obj['remark'],
                            obj['id']
                            )
                    
                else:
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            "'%s'" % str(uuid.uuid4()).upper(),
                            obj['task_name'],
                            obj['task_type'],
                            obj['task_status'],
                            obj['line_id'],
                            obj['team_id'],
                            obj['measurement'],
                            obj['remark']
                            )
            elif op=='delete':
                if ss['id'] and len(ss['id'])>0 :
                    sql = '''
                         DELETE FROM %s 
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
        
        
        
    if table=='TABLE_WIRE_SEGMENT':
        sql = '''
             DELETE FROM %s 
             WHERE start_tower_id='%s' 
             AND end_tower_id='%s'
        ''' % (
                table,
                start_tower_id,
                end_tower_id
                )
        sqls.append(sql)
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                if len(ss['id'])==0 :
                    #l = odbc_get_records(table, "start_tower_id=%s AND end_tower_id=%s AND start_contact_point=%s AND end_contact_point=%s" % (obj['start_tower_id'], obj['end_tower_id'], obj['start_contact_id'], obj['end_contact_id']), area)
                    #if len(l)>0:
                        #sql = '''
                             #DELETE FROM %s 
                             #WHERE start_tower_id=%s 
                             #AND end_tower_id =%s
                             #AND start_contact_point =%s
                             #AND end_contact_point =%s
                        #''' % (
                                #table,
                                #obj['start_tower_id'],
                                #obj['end_tower_id'],
                                #obj['start_contact_id'],
                                #obj['end_contact_id']
                                #)
                        #sqls.append(sql)
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            "'%s'" % str(uuid.uuid4()).upper(),
                            obj['start_tower_id'],
                            obj['end_tower_id'],
                            obj['start_contact_id'],
                            obj['end_contact_id'],
                            obj['phase']
                            )
                else:
                    sql = '''
                         UPDATE %s SET 
                         phase=%s
                         WHERE 
                         id=%s 
                    ''' % (
                            table,
                            obj['phase'],
                            obj['id']
                            )
            elif op=='delete':
                if len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s WHERE id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_TOWER_MODEL' :
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_exist_record(table, obj['model_code'], None, area)
                if len(l)==0:
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            obj['model_code'],
                            obj['line_count'],
                            obj['height'],
                            obj['demoni_height'],
                            obj['material'],
                            obj['functional'],
                            obj['structure']
                            )
                else:
                    sql = '''
                         UPDATE %s SET 
                         model_code=%s, 
                         line_count=%s, 
                         height=%s, 
                         demoni_height=%s, 
                         material=%s, 
                         functional=%s, 
                         structure=%s 
                         WHERE 
                         model_code=%s
                    ''' % (
                            table,
                            obj['model_code'],
                            obj['line_count'],
                            obj['height'],
                            obj['demoni_height'],
                            obj['material'],
                            obj['functional'],
                            obj['structure'],
                            obj['model_code']
                            )
            elif op=='delete':
                if len(ss['model_code'])>0:
                    sql = '''
                         DELETE FROM %s WHERE model_code=%s 
                    ''' % (
                            table,
                            obj['model_code']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_CONTACT_POINT' :
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_records(table, "model_code=%s AND side=%s AND position=%s AND contact_index=%s" % (obj['model_code'], obj['side'], obj['position'], obj['contact_index']), area)
                if len(ss['id'])==0 :
                    if len(l)>0:
                        sql = '''
                             DELETE FROM %s WHERE model_code=%s AND side=%s AND position=%s AND contact_index=%s
                        ''' % (
                                table,
                                obj['model_code'],
                                obj['side'],
                                obj['position'],
                                obj['contact_index']
                                )
                        sqls.append(sql)
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            "'%s'" % str(uuid.uuid4()).upper(),
                            obj['model_code'],
                            obj['side'],
                            obj['position'],
                            obj['contact_index'],
                            obj['offset_x'],
                            obj['offset_y'],
                            obj['offset_z'],
                            obj['split_count'],
                            obj['split_x_offset'],
                            obj['split_z_offset']
                            )
                else:
                    sql = '''
                         UPDATE %s SET 
                         model_code=%s, 
                         side=%s, 
                         position=%s, 
                         contact_index=%s, 
                         offset_x=%s, 
                         offset_y=%s, 
                         offset_z=%s, 
                         split_count=%s, 
                         split_x_offset=%s, 
                         split_z_offset=%s  
                         WHERE 
                         id=%s
                    ''' % (
                            table,
                            obj['model_code'],
                            obj['side'],
                            obj['position'],
                            obj['contact_index'],
                            obj['offset_x'],
                            obj['offset_y'],
                            obj['offset_z'],
                            obj['split_count'],
                            obj['split_x_offset'],
                            obj['split_z_offset'],
                            obj['id']
                            )
            elif op=='delete':
                if len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s WHERE id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_LINE_MATERIAL_SPECIFICATION' :
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_exist_record(table, obj['line_model'], None, area)
                if len(ss['id'])==0 :
                    if len(l)>0:
                        sql = '''
                             DELETE FROM %s WHERE line_model=%s 
                        ''' % (
                                table,
                                obj['line_model']
                                )
                        sqls.append(sql)
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            "'%s'" % str(uuid.uuid4()).upper(),
                            obj['line_model'],
                            obj['aluminum_part'],
                            obj['steel_part'],
                            obj['sectional_area'],
                            obj['break_force'],
                            obj['calc_mass'],
                            obj['calc_diameter'],
                            obj['elastic_factor'],
                            obj['heat_stretch_factor'],
                            obj['manufacturer']
                            )
                else:
                    sql = '''
                         UPDATE %s SET 
                         line_model=%s, 
                         aluminum_part=%s, 
                         steel_part=%s, 
                         sectional_area=%s, 
                         break_force=%s, 
                         calc_mass=%s, 
                         calc_diameter=%s, 
                         elastic_factor=%s, 
                         heat_stretch_factor=%s, 
                         manufacturer=%s  
                         WHERE 
                         id=%s
                    ''' % (
                            table,
                            obj['line_model'],
                            obj['aluminum_part'],
                            obj['steel_part'],
                            obj['sectional_area'],
                            obj['break_force'],
                            obj['calc_mass'],
                            obj['calc_diameter'],
                            obj['elastic_factor'],
                            obj['heat_stretch_factor'],
                            obj['manufacturer'],
                            obj['id']
                            )
            elif op=='delete':
                if len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s WHERE id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_SPECIAL_SECTION' and line_id and len(line_id)>0:
        for ss in data:
            sql = ''
            obj = sqlize_data(ss)
            if op=='save':
                l = odbc_get_exist_record(table, obj['start_tower'], obj['end_tower'], area)
                if len(ss['id'])==0:
                    if len(l)>0:
                        sql = '''
                             DELETE FROM %s WHERE start_tower=%s AND end_tower=%s
                        ''' % (
                                table,
                                obj['start_tower'],
                                obj['end_tower']
                                )
                        sqls.append(sql)
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            "'%s'" % str(uuid.uuid4()).upper(),
                            obj['line_id'],
                            obj['start_tower'],
                            obj['end_tower'],
                            obj['ss_type'],
                            obj['length'],
                            obj['detail']
                            )
                else:
                    sql = '''
                         UPDATE %s SET 
                         line_id=%s, 
                         start_tower=%s, 
                         end_tower=%s, 
                         ss_type=%s, 
                         length=%s, 
                         detail=%s  
                         WHERE 
                         id=%s
                    ''' % (
                            table,
                            obj['line_id'],
                            obj['start_tower'],
                            obj['end_tower'],
                            obj['ss_type'],
                            obj['length'],
                            obj['detail'],
                            obj['id']
                            )
            elif op=='delete':
                if len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s WHERE id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_STRAIN_SECTION' and line_id and len(line_id)>0:
        #sql = ''' DELETE FROM %s WHERE line_id='%s' ''' % (table, line_id)
        #sqls.append(sql)
        for ss in data:
            sql = ''
            obj = sqlize_data(ss) 
            
            if op=='save':
                l = odbc_get_exist_record(table, obj['start_tower'], obj['end_tower'], area)
                if len(ss['id'])==0:
                    if len(l)>0:
                        sql = '''
                             DELETE FROM %s WHERE start_tower=%s AND end_tower=%s
                        ''' % (
                                table,
                                obj['start_tower'],
                                obj['end_tower']
                                )
                        sqls.append(sql)
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            "'%s'" % str(uuid.uuid4()).upper(),
                            obj['line_id'],
                            obj['start_tower'],
                            obj['end_tower'],
                            obj['total_length'],
                            obj['typical_span'],
                            obj['k_value'],
                            obj['conductor_type'],
                            obj['ground_type_left'],
                            obj['ground_type_right']
                            )
                else:
                    sql = '''
                         UPDATE %s SET 
                         line_id=%s, 
                         start_tower=%s, 
                         end_tower=%s, 
                         total_length=%s, 
                         typical_span=%s, 
                         k_value=%s, 
                         conductor_type=%s, 
                         ground_type_left=%s,
                         ground_type_right=%s
                         WHERE 
                         id=%s
                    ''' % (
                            table,
                            obj['line_id'],
                            obj['start_tower'],
                            obj['end_tower'],
                            obj['total_length'],
                            obj['typical_span'],
                            obj['k_value'],
                            obj['conductor_type'],
                            obj['ground_type_left'],
                            obj['ground_type_right'],
                            obj['id']
                            )
            elif op=='delete':
                if len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s WHERE id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
                
    if table=='TABLE_STRAIN_SECTION' and not line_id:
        if op=='save':
            for ss in data:
                sql = ''
                obj = sqlize_data(ss) 
                sql = '''
                     INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''' % (
                        table,
                        obj['id'],
                        obj['line_id'],
                        obj['start_tower'],
                        obj['end_tower'],
                        obj['total_length'],
                        obj['typical_span'],
                        obj['k_value'],
                        obj['conductor_type'],
                        obj['ground_type_left'],
                        obj['ground_type_right']
                        )
                sqls.append(sql)
                
                
                
    if table=='TABLE_WEATHER_SECTION' and line_id and len(line_id)>0:
        for ss in data:
            sql = ''
            obj = sqlize_data(ss) 
            
            if op=='save':
                l = odbc_get_exist_record(table, obj['start_tower'], obj['end_tower'], area)
                if len(ss['id'])==0:
                    if len(l)>0:
                        sql = '''
                             DELETE FROM %s WHERE start_tower=%s AND end_tower=%s
                        ''' % (
                                table,
                                obj['start_tower'],
                                obj['end_tower']
                                )
                        sqls.append(sql)
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            "'%s'" % str(uuid.uuid4()).upper(),
                            obj['line_id'],
                            obj['start_tower'],
                            obj['end_tower'],
                            obj['total_length'],
                            obj['ice_thickness'],
                            obj['wind_speed'],
                            obj['other_tech_spec']
                            )
                else:
                    sql = '''
                         UPDATE %s SET 
                         line_id=%s, 
                         start_tower=%s, 
                         end_tower=%s, 
                         total_length=%s, 
                         ice_thickness=%s, 
                         wind_speed=%s, 
                         other_tech_spec=%s 
                         WHERE 
                         id=%s
                    ''' % (
                            table,
                            obj['line_id'],
                            obj['start_tower'],
                            obj['end_tower'],
                            obj['total_length'],
                            obj['ice_thickness'],
                            obj['wind_speed'],
                            obj['other_tech_spec'],
                            obj['id']
                            )
            elif op=='delete':
                if len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s WHERE id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
            if len(sql)>0:
                sqls.append(sql)
    if table=='TABLE_LINE' and line_id and len(line_id)>0:
        if len(data)>0:
            obj = sqlize_data(data[0])
            sql = ''' UPDATE %s SET 
                           line_code=%s,
                           line_name=%s,
                           voltage=%s,
                           category=%s,
                           length=%s,
                           manage_length=%s,
                           start_point=%s,
                           end_point=%s,
                           start_tower=%s,
                           end_tower=%s,
                           status=%s,
                           maintenace=%s,
                           management=%s,
                           owner=%s,
                           team=%s,
                           responsible=%s,
                           investor=%s,
                           designer=%s,
                           supervisor=%s,
                           constructor=%s,
                           operator=%s,
                           finish_date=%s,
                           production_date=%s,
                           decease_date=%s
                    WHERE id='%s'
            ''' % (table, 
                   obj['line_code'],
                   obj['line_name'],
                   obj['voltage'],
                   obj['category'],
                   obj['length'],
                   obj['manage_length'],
                   obj['start_point'],
                   obj['end_point'],
                   obj['start_tower'],
                   obj['end_tower'],
                   obj['status'],
                   obj['maintenace'],
                   obj['management'],
                   obj['owner'],
                   obj['team'],
                   obj['responsible'],
                   obj['investor'],
                   obj['designer'],
                   obj['supervisor'],
                   obj['constructor'],
                   obj['operator'],
                   obj['finish_date'],
                   obj['production_date'],
                   obj['decease_date'],
                   line_id
                   )
            sqls.append(sql)
    if table=='TABLE_LINE' and not line_id:
        if len(data)>0:
            obj = sqlize_data(data[0])
            sql = ''' INSERT INTO %s VALUES( 
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s,
                           %s)
            ''' % (table, 
                   obj['id'],
                   obj['line_code'],
                   obj['line_name'],
                   obj['box_north'],
                   obj['box_south'],
                   obj['box_east'],
                   obj['box_west'],
                   obj['voltage'],
                   obj['category'],
                   obj['length'],
                   obj['manage_length'],
                   obj['start_point'],
                   obj['end_point'],
                   obj['start_tower'],
                   obj['end_tower'],
                   obj['status'],
                   obj['maintenace'],
                   obj['management'],
                   obj['owner'],
                   obj['team'],
                   obj['responsible'],
                   obj['investor'],
                   obj['designer'],
                   obj['supervisor'],
                   obj['constructor'],
                   obj['operator'],
                   obj['finish_date'],
                   obj['production_date'],
                   obj['decease_date']
                   )
            sqls.append(sql)
        
    if table=='TABLE_TOWER' and line_id and len(line_id)>0 and tower_id and len(tower_id)>0:
        if len(data)>0:
            obj = sqlize_data(data[0])
            sql = ''' UPDATE %s SET 
                           line_id=%s,
                           tower_code=%s,
                           tower_name=%s,
                           same_tower=%s,
                           line_position=%s,
                           geo_x=%s,
                           geo_y=%s,
                           geo_z=%s,
                           rotate=%s,
                           model_code=%s,
                           model_code_height=%s,
                           denomi_height=%s,
                           horizontal_span=%s,
                           vertical_span=%s,
                           grnd_resistance=%s,
                           building_level=%s,
                           line_rotate=%s
                    WHERE id='%s'
            ''' % (table, 
                   obj['line_id'],
                   obj['tower_code'],
                   obj['tower_name'],
                   obj['same_tower'],
                   obj['line_position'],
                   obj['geo_x'],
                   obj['geo_y'],
                   obj['geo_z'],
                   obj['rotate'],
                   obj['model_code'],
                   obj['model_code_height'],
                   obj['denomi_height'],
                   obj['horizontal_span'],
                   obj['vertical_span'],
                   obj['grnd_resistance'],
                   obj['building_level'],
                   obj['line_rotate'],
                   tower_id
                   )
            sqls.append(sql)
    if table=='TABLE_TOWER' and not line_id:
        if op == 'save':
            for i in data:
                obj = sqlize_data(i)
                sql = ''' INSERT INTO %s VALUES( 
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s,
                               %s)
                ''' % (table, 
                       obj['id'],
                       obj['line_id'],
                       obj['tower_code'],
                       obj['tower_name'],
                       obj['same_tower'],
                       obj['line_position'],
                       obj['geo_x'],
                       obj['geo_y'],
                       obj['geo_z'],
                       obj['rotate'],
                       obj['model_code'],
                       obj['model_code_height'],
                       obj['denomi_height'],
                       obj['horizontal_span'],
                       obj['vertical_span'],
                       obj['grnd_resistance'],
                       obj['building_level'],
                       obj['line_rotate']
                       )
                sqls.append(sql)
            
    if table=='TABLE_TOWER_METALS' and tower_id and len(tower_id)>0:
        sql = ''' DELETE FROM %s WHERE tower_id='%s' ''' % (table, tower_id)
        sqls.append(sql)
        for ss in data:
            obj = sqlize_data(ss)
            sql = '''
                 INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            ''' % (
                    table,
                    "'%s'" % str(uuid.uuid4()).upper(),
                    "'%s'" % tower_id,
                    obj['attach_type'],
                    obj['attach_subtype'],
                    obj['specification'],
                    obj['strand'],
                    obj['slice'],
                    obj['value1']
                    )
            sqls.append(sql)
            
    if table=='TABLE_TOWER_METALS' and not line_id:
        if op == 'save':
            for ss in data:
                obj = sqlize_data(ss)
                sql = '''
                     INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                ''' % (
                        table,
                        obj['id'],
                        obj['tower_id'],
                        obj['attach_type'],
                        obj['attach_subtype'],
                        obj['specification'],
                        obj['material'],
                        obj['strand'],
                        obj['slice'],
                        obj['value1']
                        )
                sqls.append(sql)
    
    if table=='TABLE_SEGMENT' and line_id and len(line_id)>0 and end_tower_id and len(end_tower_id)>0:
        if len(data)>0:
            obj = sqlize_data(data[0])
            sql = ''' UPDATE %s SET 
            splitting=%s,
            conductor_count=%s,
            crosspoint_count=%s,
            length=%s,
            seperator_bar=%s,
            connector_count=%s,
            connector_type=%s 
            WHERE line_id='%s' 
            AND big_tower='%s'
            ''' % (table, 
                   obj['splitting'],
                   obj['conductor_count'],
                   obj['crosspoint_count'],
                   obj['length'],
                   obj['seperator_bar'],
                   obj['connector_count'],
                   obj['connector_type'],
                   line_id,
                   end_tower_id
                   )
            sqls.append(sql)
            
    if table=='TABLE_SEGMENT' and line_id and len(line_id)>0 and start_tower_id and len(start_tower_id)>0:
        if len(data)>0:
            obj = sqlize_data(data[0])
            sql = ''' UPDATE %s SET 
            splitting=%s,
            conductor_count=%s,
            crosspoint_count=%s,
            length=%s,
            seperator_bar=%s,
            connector_count=%s,
            connector_type=%s 
            WHERE line_id='%s' 
            AND small_tower='%s'
            ''' % (table, 
                   obj['splitting'],
                   obj['conductor_count'],
                   obj['crosspoint_count'],
                   obj['length'],
                   obj['seperator_bar'],
                   obj['connector_count'],
                   obj['connector_type'],
                   line_id,
                   start_tower_id
                   )
            sqls.append(sql)
            
    if table=='TABLE_SEGMENT' and not line_id :
        if op == 'save':
            for i in data:
                obj = sqlize_data(i)
                sql = ''' INSERT INTO %s VALUES( 
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s)
                ''' % (table, 
                       obj['id'],
                       obj['line_id'],
                       obj['small_tower'],
                       obj['big_tower'],
                       obj['splitting'],
                       obj['conductor_count'],
                       obj['crosspoint_count'],
                       obj['length'],
                       obj['seperator_bar'],
                       obj['connector_count'],
                       obj['connector_type']
                       )
                sqls.append(sql)
            
    
    if table=='TABLE_CROSS_POINT' and tower_id and len(tower_id)>0:
        if op=='save':
            segs = odbc_get_records('TABLE_SEGMENT',"line_id='%s' AND small_tower='%s'" % (line_id, tower_id), area)
            if len(segs)>0:
                segment_id = segs[0]['id']
                sql = ''' DELETE FROM %s WHERE segment_id='%s' ''' % (table, segment_id)
                sqls.append(sql)
                for ss in data:
                    obj = sqlize_data(ss)
                    sql = '''
                         INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s)
                    ''' % (
                            table,
                            "'%s'" % str(uuid.uuid4()).upper(),
                            "'%s'" % segment_id,
                            obj['cp_type'],
                            obj['geo_x'],
                            obj['geo_y'],
                            obj['geo_z'],
                            obj['cp_desc'],
                            )
                    sqls.append(sql)
    
        elif op=='delete':
            for ss in data:
                obj = sqlize_data(ss)
                if len(ss['id'])>0:
                    sql = '''
                         DELETE FROM %s WHERE id=%s 
                    ''' % (
                            table,
                            obj['id']
                            )
                    sqls.append(sql)

    if only_sql:
        return sqls
    try:
        odbc_execute_sqls(sqls, area)
    except:
        ret['result'] = sys.exc_info()[1]
    
    return ret


def gen_geojson_tracks(area):
    ret = []
    l = odbc_get_records('TABLE_TRACKS', '1=1', area)
    for i in l:
        obj = {}
        obj['geometry'] = {}
        obj['geometry']['type'] = 'LineString'
        obj['geometry']['coordinates'] = json.loads(i['coords'])
        
        obj['type'] = 'Feature'
        obj['properties'] = {}
        obj['properties']['id'] = i['id']
        obj['properties']['NAME'] = i['name']
        obj['properties']['recorder'] = i['recorder']
        obj['properties']['record_date'] = i['record_date']
        obj['properties']['desc'] = i['description']
        ret.append({'type':'FeatureCollection', 'features':[obj,]})
    return ret
        
    
    
def mobile_action(mobileaction, area, data):
    ret = {}
    if mobileaction == 'save_potential_risk_point':
        if isinstance(data, list):
            for prp in data:
                l = odbc_get_records('VIEW_POTENTIAL_RISK', u"risk_info='%s'" % prp['properties']['risk_info'], area)
                if len(l)>0:
                    ret['result'] = u'服务器保存出错:同名隐患点已存在:[%s]' % prp['properties']['risk_info']
                    break
            if len(ret.keys()) == 0:
                sqls = []
                for prp in data:
                    sql = ''' ''' 
                    sqls.append(sql)
                    
                odbc_execute_sqls(sqls)
    elif mobileaction == 'download_tunnel_task':
        condition = '1=1'
        if isinstance(data, dict):
            for k in data.keys():
                if isinstance(data[k],str) or isinstance(data[k],unicode):
                    condition += " AND %s='%s'" % (k, data[k])
                if isinstance(data[k], list):
                    condliststr = ''
                    for j in data[k]:
                        if isinstance(j, str) or isinstance(data[k], unicode):
                            condliststr += u"'%s'" % j
                        elif isinstance(j, int):
                            condliststr += "%d" % j
                        elif isinstance(j, float):
                            condliststr += "%f" % j
                        else:
                            print('other list item type')
                            pass
                        if data[k].index(j) < len(data[k]) - 1:
                            condliststr += ","
                    condition += " AND %s IN (%s)" % (k, condliststr)
                
            l = db_util.odbc_get_records('TABLE_TC_WORK_PLAN_LIST', condition, area)
            ret['result']= l
    return ret
    
def save_tracks(tracks, area):
    #def checktrack(tlist, t):
        #ret = False
        #id1 = None
        #id = None
        #if len(t['features'])>0:
            #id1 = t['features'][0]['properties']['id']
        #for i in tlist:
            #if len(i['features'])>0:
                #id = i['features'][0]['properties']['id']
                #if id1 and id and id1==id:
                    #ret = True
                    #break
        #return ret
    ret = {}
    #dirpath = SERVERJSONROOT
    #if not os.path.exists(dirpath):
        #os.mkdir(dirpath)
    #dirpath = os.path.join(SERVERJSONROOT, area)
    #if not os.path.exists(dirpath):
        #os.mkdir(dirpath)
    #path = os.path.join(SERVERJSONROOT, area, 'tracks.json')
    
    #objs = gen_geojson_tracks(area)
    try:
        #if os.path.exists(path):
            #with open(path) as f: 
                #objs = json.loads(f.read())
        #for track in tracks:
            #if not checktrack(objs , track):
                #objs.append(track)
        #with open(path, 'w') as f:
            #f.write(json.dumps(objs))
        save_tracks_to_db(tracks, area)
    except:
        ret['result'] = sys.exc_info()[1]
    return ret
    
def save_tracks_to_db(objs, area):
    def check_in(aList, aId):
        ret = False
        for i in aList:
            if i['id'] == aId:
                ret = True
                break
        return ret
    sqls = []
    l = odbc_get_records('TABLE_TRACKS', '1=1', area)
    for obj in objs:
        sql = ''
        id = obj['features'][0]['properties']['id']
        name = obj['features'][0]['properties']['NAME']
        recorder = obj['features'][0]['properties']['recorder']
        record_date = obj['features'][0]['properties']['record_date']
        desc = obj['features'][0]['properties']['desc']
        coords = json.dumps(obj['features'][0]['geometry']['coordinates'])
        if not check_in(l, id):
            sql = '''
            INSERT INTO  TABLE_TRACKS VALUES(
            '%s',
            '%s',
            '%s',
            '%s',
            '%s',
            '%s')
            ''' % (
            id,
            name,
            recorder,
            record_date,
            desc,
            coords)
            sqls.append(sql)
    if len(sqls)>0:
        odbc_execute_sqls(sqls, area)
        
    
def pg_get_all_columns(table):
    ret= []
    cur = None
    dsn = gConfig['database']['dsn']
    try:
        conn = psycopg.connect(dsn)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return ret
    
    try:
        sql = ''' SELECT *
                  FROM information_schema.columns
                  WHERE  table_name   = '%s'
        ''' % table
        cur.execute(sql)
        result = cur.fetchall()
        for i in result:
            #find = False
            #for ex in exclude:
                #if ex in i[3]:
                    #find = True
                    #break
            #if find:
                #continue
            d = {}
            d['name'] = i[3]
            d['type'] = i[27]
            ret.append(d)
        #ret = result    
    except:
        print(sys.exc_info()[1])
        ret = []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return ret
    

def pg_get_records(table, condition='1=1'):
    
    ret = []
    conn = None
    cur = None
    dsn = gConfig['database']['dsn']
    try:
        conn = psycopg.connect(dsn)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return ret
 

    try:
        cols = pg_get_all_columns(table)
        sql = "SELECT "
        for col in cols:
            if cols.index(col) == len(cols)-1:
                if col['type']=='geometry':
                    sql += "ST_AsGeoJSON(%s)" % col['name']
                else:
                    sql += "%s" % col['name']
            else:
                if col['type']=='geometry':
                    sql += "ST_AsGeoJSON(%s)," % col['name']
                else:
                    sql += "%s," % col['name']
                
        sql += '''  FROM %s WHERE %s ''' % (table, condition)
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            d = {}
            for col in cols:
                if col['type']=='geometry':
                    d[col['name']] = json.loads(row[cols.index(col)])
                else:
                    obj = row[cols.index(col)]
                    v = obj
                    if isinstance(obj, decimal.Decimal):
                        v = float(obj)
                    elif isinstance(obj, datetime.datetime):
                        v = obj.strftime('%Y-%m-%d')
                    elif isinstance(obj, str) or isinstance(obj, unicode):
                        v = obj.strip()
                    d[col['name']] = v
            ret.append(d)
        
    except:
        print(sys.exc_info()[1])
        ret = []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return ret

def MeterToDecimalDegree(distance,  lat):
    a = 1./(3600.0*30.887)
    return distance * a * np.cos(np.deg2rad(lat))
    

def move_files():
    src_dir = r'F:\work\python\ogc_server\tilesCache\sat_tiles'
    dest_dir = r'D:\tilesCache\sat_tiles'
    for root, dirs, files  in os.walk(src_dir, topdown=False):
        for name in files:
            absp = os.path.join(root, name)
            p = absp.replace(src_dir + '\\', '')
            dest_absp = os.path.join(dest_dir, p)
            arr = p.split('\\')
            #d = os.path.dirname(p)
            del arr[-1]
            d = dest_dir
            for i in arr:
                d = os.path.join(d, i)
                if not os.path.exists(d):
                    os.mkdir(d)
                
            shutil.copy(absp, dest_absp)
            print(dest_absp)
    
    
def test_update_denomi_height_and_mode_code():
    towers = odbc_get_records('TABLE_TOWER', " model_code like '%-%'")
    sqls = []
    for tower in towers:
        arr = tower['model_code'].split('-')
        sql = ''' UPDATE TABLE_TOWER SET model_code='%s', denomi_height=%s  WHERE model_code='%s' ''' % (arr[0], arr[1], tower['model_code'])
        sqls.append(sql)
    
    odbc_execute_sqls(sqls)    
        
def insert_line_model():
    data = [
            #('LGJ-25/4',  6,  1, 29.59,  9290, 102.6, 6.96, 79000,0.0000191),
            #('LGJ-35/6',  6,  1, 40.67,  12630,141,   8.16, 79000,0.0000191),
            #('LGJ-50/8',  6,  1, 56.29,  16870,195.1, 9.6,  79000,0.0000191),
            #('LGJ-70/10', 6,  1, 79.39,  23390,275.2, 11.4, 79000,0.0000191),
            #('LGJ-95/15', 26, 7, 109.72, 35000,380.8, 13.61,76000,0.0000189),
            #('LGJ-95/20', 7,  7, 113.96, 37200,408.9, 13.87,76000,0.0000185),
            #('LGJ-120/20',26, 7, 134.49, 41000,466.8, 15.07,76000,0.0000189),
            #('LGJ-120/25',7,  7, 146.73, 47880,526.6, 15.74,76000,0.0000185),
            #('LGJ-150/20',24, 7, 164.5,  46630,549.4, 16.67,73000,0.0000196),
            #('LGJ-150/25',26, 7, 173.11, 54110,601,   17.1, 76000,0.0000189),
            #('LGJ-185/25',24, 7, 211.29, 59420,706.1, 18.9, 73000,0.0000196),
            #('LGJ-185/30',26, 7, 210.93, 64320,732.6, 18.88,76000,0.0000189),
            #('LGJ-240/30',24, 7, 275.96, 75620,922.2, 21.6, 73000,0.0000196),
            #('LGJ-240/40',24, 7, 277.75, 83370,964.3, 21.66,76000,0.0000189),
            #('LGJ-300/25',48, 7, 333.31, 83410,1058,  23.76,65000,0.0000205),
            #('LGJ-300/40',24, 7, 338.99, 92220,1133,  23.94,73000,0.0000196),
            ('LGJ-35/7',    0, 7, 37.15,  45472,318.2, 7.8,  181423, 0.0000115),
            ('LGJ-50/7',    0, 7, 49.46,  60564,423.7, 9,  181423, 0.0000115),
            ('LGJ-50/19',   0, 19,48.32,  59192,411.1, 9,  181423, 0.0000115),
            ('LGJ-70/19',   0, 19,72.19,  88396,615,   11, 181423, 0.0000115),
            ]
    sqls = []
    for i in data:
        sql = ''' INSERT INTO TABLE_LINE_MATERIAL_SPECIFICATION VALUES
        ('%s',
        '%s',
        %f,
        %f,
        %f,
        %f,
        %f,
        %f,
        %f,
        %f,
        NULL
        )''' % (
        str(uuid.uuid4()).upper(),
        i[0],
        i[1],
        i[2],
        i[3],
        i[4],
        i[5],
        i[6],
        i[7],
        i[8],
            )
        sqls.append(sql)
    odbc_execute_sqls(sqls)
    
def test_catenary():
    l = odbc_get_records('TABLE_LINE_MATERIAL_SPECIFICATION')
    for line in l:
        g = catenary.get_g(line, 10, 5)
        s = catenary.get_sigma(line)
        print('model=%s, g1=%f,g2=%f,g3=%f,g4=%f,g5=%f,g6=%f,g7=%f, sigma=%f' % (line['line_model'], g[0], g[1],g[2],g[3],g[4],g[5],g[6], s))
    

def get_towers_range_by_start_end(tower_list, start_tower_id, end_tower_id):
    ret = []
    is_in_range = False
    #tower_id_list = [t['id'] for t in tower_list]
    for tower in tower_list:
        if tower['id'] == start_tower_id:
            is_in_range = True
            if not tower in ret:
                ret.append(tower)
        if tower['id'] == end_tower_id:
            is_in_range = False
            if not tower in ret:
                ret.append(tower)
            break
        if is_in_range:
            if not tower in ret:
                ret.append(tower)
    return ret
        
            
    
    
    
def get_strain_info_by_segment(towers_sort, strain_list, prev_tower_id, next_tower_id,  filter_by='conductor'):
    ret = None
    findit = False
    
    for strain in strain_list:
        r = get_towers_range_by_start_end(towers_sort, strain['start_tower'], strain['end_tower'])
        range_ids = [t['id'] for t in r]
        #for t in r:
        if filter_by=='conductor' and strain['conductor_type'] is not None and len(strain['conductor_type'])>0:
            if prev_tower_id in range_ids and next_tower_id in range_ids:
                #findit = True
                ret = strain
                break
        if filter_by=='ground_left' and strain['ground_type_left'] is not None and len(strain['ground_type_left'])>0:
            if prev_tower_id in range_ids and next_tower_id in range_ids:
                #findit = True
                ret = strain
                break
        if filter_by=='ground_right' and strain['ground_type_right'] is not None and len(strain['ground_type_right'])>0:
            if prev_tower_id in range_ids and next_tower_id in range_ids:
                #findit = True
                ret = strain
                break
        
    return ret


def get_weather_info_by_segment(towers_sort, weather_list, prev_tower_id, next_tower_id):
    ret = None
    for w in weather_list:
        r = get_towers_range_by_start_end(towers_sort, w['start_tower'], w['end_tower'])
        range_ids = [t['id'] for t in r]
        if prev_tower_id in range_ids and next_tower_id in range_ids:
            ret = w
            break
    return ret


def get_ice_wind_by_segment(towers_sort, line_id, prev_tower_id, next_tower_id, area):
    ret = 0, 0
    wl = odbc_get_records('TABLE_WEATHER_SECTION', "line_id='%s'" % line_id, area)
    w = get_weather_info_by_segment(towers_sort, wl, prev_tower_id, next_tower_id)
    if w:
        ret = w['ice_thickness'], w['wind_speed']
    return ret



def get_conductor_T0_w_by_segment(towers_sort, line_id, prev_tower_id, next_tower_id, area):
    T0, w = 0, 0
    sl = odbc_get_records('TABLE_STRAIN_SECTION', "line_id='%s'" % line_id, area)
    s = get_strain_info_by_segment(towers_sort, sl,  prev_tower_id, next_tower_id)
    if s:
        ice, wind = get_ice_wind_by_segment(towers_sort, line_id, prev_tower_id, next_tower_id, area)
        model = s['conductor_type']
        lm = odbc_get_records('TABLE_LINE_MATERIAL_SPECIFICATION', "line_model='%s'" % model, area)
        if len(lm)>0:
            g = catenary.get_g(lm[0], wind, ice)
            w = g[6]
            T0 = catenary.get_sigma(lm[0])
    return T0, w
    
def get_ground_left_T0_w_by_segment(towers_sort, line_id, prev_tower_id, next_tower_id, area):
    T0, w = 0, 0
    sl = odbc_get_records('TABLE_STRAIN_SECTION', "line_id='%s'" % line_id, area)
    s = get_strain_info_by_segment(towers_sort, sl,  prev_tower_id, next_tower_id, 'ground_left')
    if s:
        ice, wind = get_ice_wind_by_segment(towers_sort, line_id, prev_tower_id, next_tower_id, area)
        model = s['ground_type_left']
        if ',' in model:
            model = model.split(',')[0]
        lm = odbc_get_records('TABLE_LINE_MATERIAL_SPECIFICATION', "line_model='%s'" % model, area)
        if len(lm)>0:
            g = catenary.get_g(lm[0], wind, ice)
            w = g[6]
            T0 = catenary.get_sigma(lm[0])
    return T0, w
    
    
def get_ground_right_T0_w_by_segment(towers_sort, line_id, prev_tower_id, next_tower_id, area):
    T0, w = 0, 0
    sl = odbc_get_records('TABLE_STRAIN_SECTION', "line_id='%s'" % line_id, area)
    s = get_strain_info_by_segment(towers_sort, sl,  prev_tower_id, next_tower_id, 'ground_right')
    if s:
        ice, wind = get_ice_wind_by_segment(towers_sort, line_id, prev_tower_id, next_tower_id, area)
        model = s['ground_type_right']
        if ',' in model:
            model = model.split(',')[0]
        lm = odbc_get_records('TABLE_LINE_MATERIAL_SPECIFICATION', "line_model='%s'" % model, area)
        if len(lm)>0:
            g = catenary.get_g(lm[0], wind, ice)
            w = g[6]
            T0 = catenary.get_sigma(lm[0])
    return T0, w
    
    
    
    

    
def distinct_weather():
    l = odbc_get_records('TABLE_WEATHER_SECTION')
    exist = []
    delete = []
    for i in l:
        pair = (i['start_tower'], i['end_tower'])
        if not pair in exist:
            exist.append(pair)
        else:
            delete.append(i['id'])
    ids = ""
    for i in delete:
        ids += "'%s'" % i
        if delete.index(i)<len(delete)-1:
            ids += ','
    sql = "DELETE FROM TABLE_WEATHER_SECTION WHERE id IN (%s)" % ids
    print(sql)
    odbc_execute_sqls([sql])
            
def test_strain(prev_tower_name, next_tower_name):
    l = odbc_get_records('TABLE_TOWER', "tower_name='%s'" % prev_tower_name)
    prev_id = l[0]['id']
    line_id = l[0]['line_id']
    l = odbc_get_records('TABLE_TOWER', "tower_name='%s'" % next_tower_name)
    next_id = l[0]['id']
    towers_sort = odbc_get_sorted_tower_by_line(line_id)
    sl = odbc_get_records('TABLE_STRAIN_SECTION', "line_id='%s'" % line_id)
    
    strain = get_strain_info_by_segment(towers_sort,sl,prev_id,next_id, 'conductor')
    if strain:
        print('conductor_type=%s' % strain['conductor_type'])
    
    strain = odbc_get_strain_info_by_segment(towers_sort,sl,prev_id,next_id, 'ground')
    if strain:
        print('ground_type=%s' % strain['ground_type'])
    

    
def test_T0_w(line_name):
    lines = odbc_get_records('TABLE_LINE')
    for line in lines:
        if line['line_name']==line_name:
            print(line['line_name'])
            line_id = line['id']
            towers_sort = odbc_get_sorted_tower_by_line(line_id)
            for i in range(len(towers_sort)):
                if i<len(towers_sort)-1:
                    t0, w = get_conductor_T0_w_by_segment(towers_sort, line_id, towers_sort[i]['id'], towers_sort[i+1]['id'])
                    print(u'%s-%s 导线:T0=%f,w=%f' % (towers_sort[i]['tower_name'], towers_sort[i+1]['tower_name'], t0, w))
                    t0, w = get_ground_T0_w_by_segment(towers_sort, line_id, towers_sort[i]['id'], towers_sort[i+1]['id'])
                    print(u'%s-%s 地线:T0=%f,w=%f' % (towers_sort[i]['tower_name'], towers_sort[i+1]['tower_name'], t0, w))
            break
    
    
def modify_model_code_by_denomi():
    towers = odbc_get_records('TABLE_TOWER')
    sqls = []
    for tower in towers:
        if tower['model_code'] is None:
            continue
        if '_' in tower['model_code']:
            continue
        else:
            if tower['model_code'] and len(tower['model_code'])>0:
                mc = '%s_' % tower['model_code']
                dh = tower['denomi_height']
                if dh:
                    sdh = '%.1f' % dh
                    if sdh[-2:] == '.0':
                        sdh = sdh[:-2]
                    else:
                        sdh = sdh.replace('.','_')
                    mc += sdh
                sql = '''UPDATE  TABLE_TOWER SET model_code='%s' WHERE id='%s' ''' % (mc, tower['id'])
                sqls.append(sql)
    for sql in sqls:
        print(sql)
    odbc_execute_sqls(sqls)
    
def test_insert_ZB422_39():
    sqls = []
    l = odbc_get_records('TABLE_CONTACT_POINT', "model_code='SZF242A_39'")
    for i in l:
        sql = ''' INSERT INTO TABLE_CONTACT_POINT VALUES(
        '%s', 
        '%s',
        '%s', 
        '%s',
        '%s',
        %d,
        %f,
        %f,
        %f
        )''' % (
        str(uuid.uuid4()).upper(),
        i['line_id'],
        'ZB422_39',
        i['side'],
        i['position'],
        i['contact_index'],
        i['offset_x'],
        i['offset_y'],
        i['offset_z']
             )
        sqls.append(sql)
    for sql in sqls:
        print(sql)
    odbc_execute_sqls(sqls)
    

def test_update_phase():
    sqls = []
    #l = odbc_get_records('TABLE_WIRE_SEGMENT')
    #for i in l:
        #if i['start_contact_index']==0 and i['end_contact_index']==0:
            #sql = '''UPDATE TABLE_WIRE_SEGMENT SET phase='A' WHERE id='%s' ''' % i['id']
        #elif i['start_contact_index']==1 and i['end_contact_index']==1:
            #sql = '''UPDATE TABLE_WIRE_SEGMENT SET phase='B' WHERE id='%s' ''' % i['id']
        #elif i['start_contact_index']==2 and i['end_contact_index']==2:
            #sql = '''UPDATE TABLE_WIRE_SEGMENT SET phase='C' WHERE id='%s' ''' % i['id']
        #elif i['start_contact_index']==3 and i['end_contact_index']==3:
            #sql = '''UPDATE TABLE_WIRE_SEGMENT SET phase='N' WHERE id='%s' ''' % i['id']
        #elif i['start_contact_index']==4 and i['end_contact_index']==4:
            #sql = '''UPDATE TABLE_WIRE_SEGMENT SET phase='K' WHERE id='%s' ''' % i['id']
        
    
    sql = '''UPDATE TABLE_WIRE_SEGMENT SET phase='A' WHERE start_contact_index=1 and end_contact_index=1 '''
    sqls.append(sql)
    sql = '''UPDATE TABLE_WIRE_SEGMENT SET phase='B' WHERE start_contact_index=2 and end_contact_index=3 '''
    sqls.append(sql)
    sql = '''UPDATE TABLE_WIRE_SEGMENT SET phase='C' WHERE start_contact_index=3 and end_contact_index=3 '''
    sqls.append(sql)
    sql = '''UPDATE TABLE_WIRE_SEGMENT SET phase='N' WHERE start_contact_index=4 and end_contact_index=4 '''
    sqls.append(sql)
    sql = '''UPDATE TABLE_WIRE_SEGMENT SET phase='K' WHERE start_contact_index=5 and end_contact_index=5 '''
    sqls.append(sql)
    odbc_execute_sqls(sqls)

def test_modify_tower_name():
    sqls = []
    towers = odbc_get_records('TABLE_TOWER')
    i = 0
    for tower in towers:
        tn = tower['tower_name']
        arr = re.split(r'\d+', tn)
        print(g)
        
        i += 1
        break
    

def altitude_by_lgtlat(demdir, lgt, lat):
    ret = -1
    l = []
    for i in os.listdir(demdir):
        if i[-4:] == '.tif' and 'ASTGTM2' in i:
            p = os.path.join(demdir, i)
            de = DemExtrctor(p)
            try:
                ret = de.lookup(lgt, lat)
                l.append(ret)
                print('ret=%f' % ret)
            except:
                pass
    minv = min(l)
    maxv = max(l)
    #l.remove(minv)
    #l.remove(maxv)
    if len(l)>0:
        ret = sum(l)/len(l)
    return ret
            
def test_compare_arcgis_demextract():
    ts = odbc_get_records('TABLE_TOWER')
    for t in ts:
        a1 = t['geo_z']
        a2 = altitude_by_lgtlat(t['geo_x'], t['geo_y'])
        print('arcgis=%f, demextract=%f' % (a1, a2))
    

def webgis_get_tower_data(line_id, area):
    ret = []
    ts = odbc_get_records('TABLE_TOWER', "line_id='%s'" % line_id, area)
    for t in ts:
        ret.append([t['geo_x'], t['geo_y'],  t['geo_z'], t['rotate'], t['model_code']])
    return ret
    
        
    




def test_merge_tif():
    d = r'I:\geotiff'
    l = []
    for root, dirs, files  in os.walk(d, topdown=False):
        for f in files:
            p = os.path.join(root, f)
            if p[-4:]=='.tif':
                print(p)
                l.append(p)
    argv = ['', '-o', os.path.join(d, 'zt.tif'),]
    for i in l:
        argv.append(i)
        
    print(argv)
    import gdal_merge
    gdal_merge.main(argv)
    
def test_copy_3ds_to_place():
    srcdir = ur'F:\work\csharp\kmgdnew\data\3ds\3DS模型\昭通模型\永发I,II回'
    destdir = r'F:\work\csharp\kmgdnew\data\3ds'
    l = []
    for root, dirs, files  in os.walk(srcdir, topdown=False):
        for f in files:
            p = os.path.join(root, f)
            if p[-4:]=='.3ds':
                l.append(p)
    for i in l:
        p = os.path.join(destdir, os.path.basename(i))
        if os.path.exists(p):
            os.remove(p)
        print('copy %s to %s' % (i, destdir))
        shutil.copy(i, destdir)
        

def get_temperary_model_code_mapping(stage=''):
    ret = {}
    filepath = ur'F:\work\csharp\kmgdnew\doc\220KV永发Ⅰ回线_暂时替换.xls'
    book = xlrd.open_workbook(filepath)
    sheet = book.sheet_by_name('old_new_mapping%s' % stage)
    for i in range(sheet.nrows):
        #print("%s=%s" % (sheet_tower.cell(i,0).value, sheet_tower.cell(i,1).value) )
        old = sheet.cell_value(i,0)
        new = sheet.cell_value(i,1)
        if len(old.strip())>0 and len(new.strip())>0 and not new.strip() == u'未录入':
            #print("%s=%s" % (old, new))
            ret[old] = new
    for k in ret.keys():    
        print("%s=%s" % (k, ret[k]))
    return ret
    
def test_replace_model_code_by_tempary(stage=''):
    sqls = []
    filepath = ur'F:\work\csharp\kmgdnew\doc\220KV永发Ⅰ回线_暂时替换.xls'
    p = os.path.join(os.path.dirname(filepath), 'model_code_backup%s.txt' % stage)
    with open(p, 'r') as f:
        for line in f:
            id, new, old = line.split('\t')
            print('id:%s, new:%s, old:%s' % (id, new, old.strip()))
            sql = '''UPDATE TABLE_TOWER SET model_code='%s' WHERE id='%s' ''' % (new, id)
            sqls.append(sql)
    odbc_execute_sqls(sqls)
    
    
    
def gen_model_code_back_up(stage=''):
    filepath = ur'F:\work\csharp\kmgdnew\doc\220KV永发Ⅰ回线_暂时替换.xls'
    towers = odbc_get_records('TABLE_TOWER')
    d = get_temperary_model_code_mapping(stage)
    s = ''
    cnt = 0
    for tower in towers:
        mc = tower['model_code']
        if d.has_key(mc):
            s += '%s\t%s\t%s\n' % (tower['id'], d[mc], mc)
            cnt += 1
    p = os.path.join(os.path.dirname(filepath), 'model_code_backup%s.txt' % stage)
    with open(p, 'w') as f:
        f.write(s)
    print(len(towers))
    print(cnt)
    print(s)
            
        
def test_update_old_model_code():
    filepath = ur'F:\work\csharp\kmgdnew\doc\old_tower_model_code.xls'
    book = xlrd.open_workbook(filepath)
    sheet = book.sheet_by_name('s1')
    sqls = []
    for i in range(sheet.nrows):
        id = sheet.cell_value(i,0).strip()
        mc = sheet.cell_value(i,1).strip()
        if len(id)>0 and len(mc)>0:
            sql = '''UPDATE TABLE_TOWER SET model_code='%s' WHERE id='%s' ''' % (mc, id)
            sqls.append(sql)
            print(sql)
    odbc_execute_sqls(sqls)
    

def test_update_line_position():
    lines = odbc_get_records('TABLE_LINE')
    yf1, yf2 = None, None
    sqls = []
    for line in lines:
        if line['line_name'] == u'永发I回线':
            yf1 = line['id']
        if line['line_name'] == u'永发II回线':
            yf2 = line['id']
    if yf1 :
        towers = odbc_get_sorted_tower_by_line(yf1)
        print('1-54')
        ts = towers[0:54]
        for t in ts:
            print(t['tower_name'])
            sql = '''update TABLE_TOWER set line_position='%s' where id='%s' ''' % (u'右侧', t['id'])
            sqls.append(sql)
        print('172-178')
        ts = towers[171:178]
        for t in ts:
            print(t['tower_name'])
            sql = '''update TABLE_TOWER set line_position='%s' where id='%s' ''' % (u'右侧', t['id'])
            sqls.append(sql)
    if yf2 :
        towers = odbc_get_sorted_tower_by_line(yf2)
        print('1-54')
        ts = towers[0:54]
        for t in ts:
            print(t['tower_name'])
            sql = '''update TABLE_TOWER set line_position='%s' where id='%s' ''' % (u'左侧', t['id'])
            sqls.append(sql)
        print('162-168')
        ts = towers[161:168]
        for t in ts:
            print(t['tower_name'])
            sql = '''update TABLE_TOWER set line_position='%s' where id='%s' ''' % (u'左侧', t['id'])
            sqls.append(sql)
    odbc_execute_sqls(sqls)    
        
    
def test_identify_strain_info():
    strains = odbc_get_records('TABLE_STRAIN_SECTION')
    l = []
    ids = []
    for s in strains:
        i = '%s_%s_%s' % (s['line_id'], s['start_tower'], s['end_tower'])
        if not i in l:
            l.append(i)
            ids.append(s['id'])
    cond = 'id NOT IN('
    for id in ids:
        cond += "'%s'" % id
        if ids.index(id)<len(ids)-1:
            cond += ","
    cond += ")"
    sql = ''' DELETE FROM TABLE_STRAIN_SECTION WHERE %s''' % cond
    print(sql)
    odbc_execute_sqls([sql,])
    
    
    
def test_threejs():
    d = 'static/threejs/examples'
    d = os.path.abspath(d)
    for i in os.listdir(d):
        if i[-5:]=='.html':
            print(os.path.basename(i))
    
def gen_js_file(user_id, table, cond, area):
    d = os.path.abspath('static/mobile_data')
    if not os.path.exists(d):
        os.mkdir(d)
    d = os.path.join(d, user_id)
    if not os.path.exists(d):
        os.mkdir(d)
    jsonfile = '%s.js' % table
     
    absp = os.path.join(d, jsonfile)
    l = odbc_get_records(table, cond, area)
    s = json.dumps(l, ensure_ascii=False)
    s = 'var %s = %s;\n' % (table, s)
    s = enc(s)
    with open(absp, 'w') as f:
        f.write(s)
    
    
def test_gen_json_file():
    user_id = 'admin'
    table = 'TABLE_OPERATING_TASK'
    cond = '1=1'
    area = 'zt'
    gen_js_file(user_id, table, cond, area)
    
def test_list_leafletjs():
    rt = r'H:\work\java\kmgdgis_mobile_android\assets\www\js\leaflet'
    for root, dirs, files  in os.walk(rt, topdown=False):
        for name in files:
            if name[-3:] == '.js':
                p = os.path.join(root, name)
                p1 = p.replace(rt, '').replace('\\', '/')[1:-3]
                if not p1 in ['copyright','Leaflet']:
                    print("'%s'," % p1)
                #s += '"%s" ' % p
        
    #print(s)  
    
def get_tiles_by_area(area):
    def get_round_tile(center):
        ret = []
        left = '%05d' % (int(center)-1)
        right = '%05d' % (int(center)+1)
        up = '%05d' % (int(center)-100+1)
        down = '%05d' % (int(center)+100-1)
        left_up = '%05d' % (int(up)-1)
        right_up = '%05d' % (int(up)+1)
        left_down = '%05d' % (int(down)-1)
        right_down = '%05d' % (int(down)+1)
        ret = [left, right, up, down, left_up, right_up, left_down, right_down]
        return ret
    
    ret = set()
    p = os.path.join(SERVERJSONROOT, 'yn_tiles_index.json')
    p = os.path.abspath(p)
    
    objlist = None
    with open(p) as f:
        objlist = json.loads(f.read())
    keylist = [i.keys()[0] for i in objlist]
    towers = []
    if area=='zt':
        towers = odbc_get_records('TABLE_TOWER', '1=1', area)
    elif area=='km':
        towers = kml_get_records(KUNMING_TOWER_KML)
        
    for tower in towers:
        for obj in objlist:
            key = obj.keys()[0]
            if tower['geo_x']<=obj[key]['ru'][0] and tower['geo_x']>=obj[key]['ld'][0] and tower['geo_y']<=obj[key]['ru'][1] and tower['geo_y']>=obj[key]['ld'][1]:
                
                ret.add(str(key))
                round_tiles = get_round_tile(key)
                for i in round_tiles:
                    if i in keylist:
                        ret.add(i)
                    if round_tiles.index(i) in [4,5,6,7]:
                        rts = get_round_tile(i)
                        for j in rts:
                            if j in keylist:
                                ret.add(j)
                break
    #print(ret)    
    print(len(ret))
    
    l = list(ret)
    objlist1 = []
    for obj in objlist:
        key = obj.keys()[0]
        if key in l:
            objlist1.append(obj)
 
    
    minxlist = [i[i.keys()[0]]['ld'][0] for i in objlist1]
    minylist = [i[i.keys()[0]]['ld'][1] for i in objlist1]
    maxxlist = [i[i.keys()[0]]['ru'][0] for i in objlist1]
    maxylist = [i[i.keys()[0]]['ru'][1] for i in objlist1]
    minx = min(minxlist)
    miny = min(minylist)
    maxx = max(maxxlist)
    maxy = max(maxylist)
    #print('geograhpical center=(%f,%f)' % ((minx + maxx)/2.0, (miny + maxy)/2.0))
    #m = ToWebMercator((minx + maxx)/2.0, (miny + maxy)/2.0)
    #print('mercator center=(%f,%f)' % (m[0], m[1]))
    #print('mercator center1=(%f,%f)' % (m[1], m[0]))
    #print('center=(%f,%f)' % ((minx + maxx)/2.0, (miny + maxy)/2.0))
    print('center1=(%f,%f)' % ((miny + maxy)/2.0, (minx + maxx)/2.0))
    
    root = os.path.abspath(SERVERJSONROOT)
    p = os.path.join(root, 'yn_tiles_list_%s.json' % area)
    with open(p, 'w') as f:
        f.write(json.dumps(l))
    p = os.path.join(root, 'yn_tiles_bounds_%s.json' % area)
    with open(p, 'w') as f:
        f.write(json.dumps({'min':(minx, miny), 'max':(maxx, maxy)}))
    
    sjz = ''
    for i in l:
        sjz += ur'J:\云南dat任务文件\%s.dat|' % i
    sjz = sjz[:-1]
    print(sjz)
    
def test_get_all_task_file_by_area(area):
    ret = set()
    p = os.path.join(SERVERJSONROOT, 'yn_tiles_index.json')
    p = os.path.abspath(p)
    objlist = None
    with open(p) as f:
        objlist = json.loads(f.read())
    keylist = [i.keys()[0] for i in objlist]
    towers = odbc_get_records('TABLE_TOWER', '1=1', area)
    for tower in towers:
        for obj in objlist:
            key = obj.keys()[0]
            if tower['geo_x']<=obj[key]['ru'][0] and tower['geo_x']>=obj[key]['ld'][0] and tower['geo_y']<=obj[key]['ru'][1] and tower['geo_y']>=obj[key]['ld'][1]:
                
                ret.add(str(key))
                left = '%05d' % (int(key)-1)
                right = '%05d' % (int(key)+1)
                up = '%05d' % (int(key)-100+1)
                down = '%05d' % (int(key)+100-1)
                left_up = '%05d' % (int(up)-1)
                right_up = '%05d' % (int(up)+1)
                left_down = '%05d' % (int(down)-1)
                right_down = '%05d' % (int(down)+1)
                if left in keylist:
                    ret.add(left)
                if right in keylist:
                    ret.add(right)
                if up in keylist:
                    ret.add(up)
                if down in keylist:
                    ret.add(down)
                if left_up in keylist:
                    ret.add(left_up)
                if right_up in keylist:
                    ret.add(right_up)
                if left_down in keylist:
                    ret.add(left_down)
                if right_down in keylist:
                    ret.add(right_down)
                break
    
    l = list(ret)
    sjz = ''
    for i in l:
        sjz += ur'J:\云南dat任务文件\%s.dat|' % i
    sjz = sjz[:-1]
    print(sjz)
    return ret
    
def test_get_center_mercator(mbtile_id):
    ret = None, None
    
    p = os.path.join(SERVERJSONROOT, 'yn_tiles_index.json')
    p = os.path.abspath(p)
    
    objlist = None
    with open(p) as f:
        objlist = json.loads(f.read())
    for i in objlist:
        key = i.keys()[0]
        if key==mbtile_id:
            obj = i[key]
            geox1 = obj['ld'][0]
            geox2 = obj['ru'][0]
            geoy1 = obj['ld'][1]
            geoy2 = obj['ru'][1]
            print('top=%f,left=%f,right=%f,down=%f' % (obj['lu'][1], obj['lu'][0], obj['rd'][0], obj['rd'][1]))
            ret = ToWebMercator((geox1+geox2)/2.0, (geoy1+geoy2)/2.0)
            print(( (geoy1+geoy2)/2.0, (geox1+geox2)/2.0) )
            break
    #print(ret)
    ret1 = ret[1], ret[0]
    print(ret1)


def list_by_tile_google(ldir, tile_id):
    ret = []
    for root, dirs, files  in os.walk(ldir, topdown=False):
        for d in dirs:
            if len(d)>5 and d[0:5] == tile_id:
                for root1, dirs1, files1  in os.walk(os.path.join(root, d), topdown=False):
                    for name in files1:
                        if name[-4:]=='.png':
                            objmap = {}
                            p = os.path.join(root1, name)
                            zoom = os.path.basename(os.path.dirname(os.path.dirname(p)))
                            objmap['zoom_level'] = int(zoom[1:])-1
                            arr = name[:-4].split('-')
                            objmap['tile_column'] = int(arr[1])-1
                            objmap['tile_row'] = int(arr[0])-1
                            objmap['tile_path'] = p
                            ret.append(objmap)
    return ret

def list_by_tile_esri(ldir, mbtile_id):
    ret = []
    #for root, dirs, files  in os.walk(ldir, topdown=False):
    for d in os.listdir(ldir):
        dpath = os.path.join(ldir, d)
        if os.path.isdir(dpath) and len(d)>5 and d[0:5] == mbtile_id:
            for root, dirs, files  in os.walk(dpath, topdown=False):
                for name in files:
                    if name[-4:]=='.png':
                        objmap = {}
                        p = os.path.join(root, name)
                        zoom = os.path.basename(os.path.dirname(os.path.dirname(p)))
                        objmap['zoom_level'] = int(zoom[1:])
                        objmap['tile_column'] = int(name[1:-4], 16)
                        row = os.path.basename(os.path.dirname(p))
                        objmap['tile_row'] = int(row[1:], 16)
                        objmap['tile_path'] = p
                        ret.append(objmap)
    return ret

def list_by_zoom_esri(area, ldir, minzoom, maxzoom, mbtile_id=None):
    ret = []
    mbtilelist = None
    

    for d in os.listdir(ldir):
        dpath = os.path.join(ldir, d)
        additional = True
        if mbtile_id:
            additional = (len(d)>5 and d[0:5] == mbtile_id)
        #if os.path.isdir(dpath) and len(d)>5 and d[0:5] in mbtilelist and additional:
        if os.path.isdir(dpath) and len(d)>5 and d[5:6]=='_'  and additional:
            dpath = os.path.join(dpath, '_alllayers')
            for d1 in os.listdir(dpath):
                zoom = d1
                if int(zoom[1:])>=minzoom and int(zoom[1:])<=maxzoom:
                #if True:
                    dpath1 = os.path.join(dpath, d1)
                    for d2 in os.listdir(dpath1):
                        dpath2 = os.path.join(dpath1, d2)
                        for d3 in os.listdir(dpath2):
                            dpath3 = os.path.join(dpath2, d3)
                            if os.path.isfile(dpath3) and d3[-4:]=='.png':
                                objmap = {}
                                p = dpath3
                                row = d2
                                column = d3
                                objmap['zoom_level'] = int(zoom[1:])
                                objmap['tile_column'] = int(column[1:-4], 16)
                                objmap['tile_row'] = int(row[1:], 16)
                                objmap['tile_path'] = p
                                ret.append(objmap)
    return ret

def write_n_data_to_db(index, pngdata, dxsize, dysize, bands, mb_db, cur, use_base64=True):
    pass
def write_one_data_to_db(index, pngdata, dxsize, dysize, bands, mb_db, use_base64=True):
    """
    Write raster 'data' (of the size 'dataxsize' x 'dataysize') read from
    'dataset' into the mbtiles document 'mb_db' with size 'tilesize' pixels.
    Later this should be replaced by new <TMS Tile Raster Driver> from GDAL.
    """
    gdal.FileFromMemBuffer(MEMORYPATH, '') 
    if bands == 3 and TILEFORMAT == 'png':
        tmp = TEMPDRIVER.Create(MEMORYPATH, TILESIZE, TILESIZE, bands=4)
        alpha = tmp.GetRasterBand(4)
        #from Numeric import zeros
        alphaarray = (np.zeros((dysize, dxsize)) + 255).astype('b')
        alpha.WriteArray( alphaarray, 0, TILESIZE-dysize )
    else:
        tmp = TEMPDRIVER.Create(MEMORYPATH, TILESIZE, TILESIZE, bands=bands)

    tmp.WriteRaster( 0, TILESIZE-dysize, dxsize, dysize, pngdata, band_list=range(1, bands+1))
    
    #ddd = tmp.getBytes()
    #print(len(ddd))
    
    tmpuid = str(uuid.uuid4())
    tmppath = os.path.abspath(TMPDIR)
    if not os.path.exists(tmppath):
        os.mkdir(tmppath)
    tmppath = os.path.join(tmppath, '%s.png' % tmpuid)
    dst = TILEDRIVER.CreateCopy(tmppath, tmp, strict=0)
    dst = None
    
    cur = mb_db.cursor()
    tile_id = str(uuid.uuid4())
    with open(tmppath, 'rb') as f:
        data = f.read()
    #data = gdal.Open(MEMORYPATH, gdal.GA_ReadOnly)
        print(len(data))
        if use_base64:
            base64Prefix = 'data:image/png;base64,'
            data = base64Prefix + base64.encodestring(data)
            query1 = """INSERT INTO images 
                (tile_id, tile_data) 
                VALUES ('%s', '%s')""" % (tile_id, data)
            cur.execute(query1)
        else:
            query1 = """INSERT INTO images 
                (tile_id, tile_data) 
                VALUES ('%s', ?)""" % tile_id
            cur.execute(query1, (sqlite3.Binary(data),))
    
    query2 = """INSERT INTO map 
        (zoom_level, tile_column, tile_row, tile_id) 
        VALUES (%d, %d, %d, '%s')""" % (index[0], index[1], index[2], tile_id)
    cur.execute(query2)
    
    mb_db.commit()
    cur.close()
    

def write_one_tile_data_from_file(path, zoom_level, tile_column, tile_row, mb_db, use_base64=True):
    cur = mb_db.cursor()
    tile_id = str(uuid.uuid4())
    with open(path, 'rb') as f:
        data = f.read()
        #print(len(data))
        if use_base64:
            base64Prefix = 'data:image/png;base64,'
            data = base64Prefix + base64.encodestring(data)
            query1 = """INSERT INTO images 
                (tile_id, tile_data) 
                VALUES ('%s', '%s')""" % (tile_id, data)
            cur.execute(query1)
        else:
            query1 = """INSERT INTO images 
                (tile_id, tile_data) 
                VALUES ('%s', ?)""" % tile_id
            cur.execute(query1, (sqlite3.Binary(data),))
    
    query2 = """INSERT INTO map 
        (zoom_level, tile_column, tile_row, tile_id) 
        VALUES (%d, %d, %d, '%s')""" % (zoom_level, tile_column, tile_row, tile_id)
    cur.execute(query2)
    
    mb_db.commit()
    cur.close()
    
def write_n_tile_data_from_file(path, zoom_level, tile_column, tile_row, mb_db, cur, use_base64=True, use_png8=False):
    tile_id = str(uuid.uuid4())
    #with open(path, 'rb') as f:
        #data = f.read()
        #if use_base64:
            #base64Prefix = 'data:image/png;base64,'
            #data = base64Prefix + base64.encodestring(data)
            #query1 = """INSERT INTO images 
                #(tile_id, tile_data) 
                #VALUES ('%s', '%s')""" % (tile_id, data)
            #cur.execute(query1)
        #else:
            #query1 = """INSERT INTO images 
                #(tile_id, tile_data) 
                #VALUES ('%s', ?)""" % tile_id
            #cur.execute(query1, (sqlite3.Binary(data),))
    
    #query2 = """INSERT INTO map 
        #(zoom_level, tile_column, tile_row, tile_id) 
        #VALUES (%d, %d, %d, '%s')""" % (zoom_level, tile_column, tile_row, tile_id)
    try:
        #cur.execute(query2)
        fileext = path[path.rindex('.')+1:]
        tmppath = None
        if use_png8:
            tmppath = path + '_rgb8.' + fileext 
            im = Image.open(path)
            im2 = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
            im2.save(tmppath)
            path = tmppath
            
        
        with open(path, 'rb') as f:
            data = f.read()
            #print(len(data))
            if use_base64:
                base64Prefix = 'data:image/%s;base64,' % fileext
                data = base64.encodestring(data)
                #query1 = """INSERT INTO images 
                    #(tile_id, tile_data) 
                    #VALUES ('%s', '%s')""" % (tile_id, data)
                query1 = """INSERT INTO tiles 
                    (zoom_level, tile_column, tile_row, tile_data) 
                    VALUES (%d, %d, %d, '%s')""" % (zoom_level, tile_column, tile_row, data)
                cur.execute(query1)
            else:
                #query1 = """INSERT INTO images 
                    #(tile_id, tile_data) 
                    #VALUES ('%s', ?)""" % tile_id
                query1 = """INSERT INTO tiles 
                    (zoom_level, tile_column, tile_row, tile_data) 
                    VALUES (%d, %d, %d, ?)""" % (zoom_level, tile_column, tile_row)
                cur.execute(query1, (sqlite3.Binary(data),))
        if tmppath:
            if os.path.exists(tmppath):
                os.remove(tmppath)
    except sqlite3.IntegrityError:
        print('Exist : select tile_data from tiles where zoom_level=%d and tile_column=%d and tile_row=%d' % (zoom_level, tile_column, tile_row))
    

    
def init_mbtiles_db(mbtile_id, use_base64=True):
    #if os.path.isfile(db_filename):
        #raise Exception('Output file already exists')
    
    db_filename = os.path.join(TILEROOT, '%s.mbtiles' % mbtile_id)
    if os.path.exists(db_filename):
        os.remove(db_filename)
    mb_db = sqlite3.connect(db_filename)
    
    #if use_base64:
        #mb_db.execute("""
          #CREATE TABLE images (
          #tile_data TEXT,
          #tile_id TEXT);
        #""")
    #else:
        #mb_db.execute("""
          #CREATE TABLE images (
          #tile_data BLOB,
          #tile_id TEXT);
        #""")
    
    #mb_db.execute("""
      #CREATE TABLE map (
      #zoom_level INTEGER, 
      #tile_column INTEGER, 
      #tile_row INTEGER, 
      #tile_id TEXT);
    #""")
    
    #mb_db.execute("""
      #CREATE UNIQUE INDEX tile_index on map 
        #(zoom_level, tile_column, tile_row);
    #""")
    
    #mb_db.execute("""
      #CREATE VIEW tiles AS SELECT
      #map.zoom_level AS zoom_level,
      #map.tile_column AS tile_column,
      #map.tile_row AS tile_row,
      #images.tile_data AS tile_data
      #FROM map JOIN images ON images.tile_id = map.tile_id;
    #""")
    
    
    
    if use_base64:
        mb_db.execute("""
        CREATE TABLE tiles (
        zoom_level INTEGER, 
        tile_column INTEGER, 
        tile_row INTEGER, 
        tile_data TEXT);
        """)
    else:
        mb_db.execute("""
          CREATE TABLE tiles (
          zoom_level INTEGER, 
          tile_column INTEGER, 
          tile_row INTEGER, 
          tile_data BLOB);
        """)
    
    
    mb_db.execute("""
      CREATE UNIQUE INDEX tile_index on tiles 
        (zoom_level, tile_column, tile_row);
    """)
    
    mb_db.execute("""
      CREATE TABLE "metadata" (
        "name" TEXT ,
        "value" TEXT );
    """)
    mb_db.execute("""
      CREATE UNIQUE INDEX "name" ON "metadata" 
        ("name");
    """)
    
    
    mb_db.execute('INSERT INTO metadata VALUES (?, ?)', ('name', mbtile_id))
    mb_db.execute('INSERT INTO metadata VALUES (?, ?)', ('type', 'baselayer'))
    mb_db.execute('INSERT INTO metadata VALUES (?, ?)', ('version', '1.0'))
    mb_db.execute('INSERT INTO metadata VALUES (?, ?)', ('description', mbtile_id))
    mb_db.execute('INSERT INTO metadata VALUES (?, ?)', ('format', 'png'))
    
    #mb_db.executemany("""
      #INSERT INTO metadata (name, value) values
      #(?, ?)""", metadata)
    mb_db.commit()
    return mb_db



def convert_projection(input_file):
    ret = input_file.replace('.tif', '_merc.tiff')
    osgeoroot = 'Python27/Lib/site-packages/osgeo'
    osgeoroot = os.path.abspath(osgeoroot)
    cmd = '"%s" -t_srs EPSG:900913 "%s" "%s"' % (os.path.join(osgeoroot, 'gdalwarp.exe'), input_file, ret)
    print(subprocess.check_output(cmd))
    return ret
    
    
    
def create_mbtiles_from_tiff(mbtile_id,  pipe=None, use_base64=True, user_dir=False):
    ttt = os.path.abspath(TMPDIR)
    if os.path.exists(ttt):
        shutil.rmtree(ttt)
        
    if user_dir:
        ttt = os.path.join(DIRTILEROOT, mbtile_id)
        if os.path.exists(ttt):
            shutil.rmtree(ttt)
        

    input_file = None
    for i in os.listdir(TILEROOT):
        if os.path.isfile(os.path.join(TILEROOT, i)) and '_%s_' % mbtile_id in i:
            input_file = os.path.join(TILEROOT, i)
            break
    if input_file is None:
        if pipe:
            pipe.send('%s:notfound' % mbtile_id)
        return
    input_file = convert_projection(input_file)


    isepsg4326 = False
    gdal.AllRegister()

    dataset = gdal.Open(input_file, GA_ReadOnly)
    bands = dataset.RasterCount
    xsize = dataset.RasterXSize
    ysize = dataset.RasterYSize

    geotransform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()

    north = geotransform[3]
    south = geotransform[3] + geotransform[5] * ysize
    east  = geotransform[0] + geotransform[1] * xsize
    west  = geotransform[0]


    if projection and projection.endswith('AUTHORITY["EPSG","4326"]]'):
        isepsg4326 = True

    log2 = lambda x: log10(x) / log10(2) # log2 (base 2 logarithm)
    sum = lambda seq, start=0: reduce(operator.add, seq, start)

    # Zoom levels of the pyramid.
    maxzoom = int(max(ceil(log2(xsize/float(TILESIZE))), ceil(log2(ysize/float(TILESIZE)))))
    minzoom = 0
    zoompixels = [geotransform[1] * 2.0**(maxzoom-zoom) for zoom in range(minzoom, maxzoom+1)]
    tilecount = sum([
        int(ceil(xsize / (2.0**(maxzoom-zoom)*TILESIZE))) * \
        int(ceil(ysize / (2.0**(maxzoom-zoom)*TILESIZE))) \
        for zoom in range(minzoom, maxzoom+1)
    ])

    
    print("Output: %s.mbtiles" % mbtile_id)
    print("Format of tiles: %s/%s" % (TILEDRIVER.ShortName ,  TILEDRIVER.LongName))
    print("Count of tiles: %d", tilecount)
    print("Zoom range: %d-%d" % (minzoom, maxzoom))
    print("Pixel resolution by zoomlevels: %s" % str(zoompixels))

    tileno = 0
    progress = 0

    #layer_type = "overlay" if options.overlay else "baselayer"

    mb_db = None
    if not user_dir:
        mb_db = init_mbtiles_db(mbtile_id, use_base64)

    for zoom in range(maxzoom, minzoom-1, -1):
        # Maximal size of read window in pixels.
        rmaxsize = 2.0**(maxzoom-zoom)*TILESIZE

        #x0 = int( ceil( west / rmaxsize))
        #y0 = int( ceil( south / rmaxsize))
        for ix in range(0,  int( ceil( xsize / rmaxsize))):
            # Read window xsize in pixels.
            if ix+1 == int( ceil( xsize / rmaxsize)) and xsize % rmaxsize != 0:
                rxsize = int(xsize % rmaxsize)
            else:
                rxsize = int(rmaxsize)
            
            # Read window left coordinate in pixels.
            rx = int(ix * rmaxsize)

            for iy in range(0,  int(ceil( ysize / rmaxsize)) ):
                # Read window ysize in pixels.
                if iy+1 == int(ceil( ysize / rmaxsize)) and ysize % rmaxsize != 0:
                    rysize = int(ysize % rmaxsize)
                else:
                    rysize = int(rmaxsize)

                # Read window top coordinate in pixels.
                ry = int(ysize - (iy * rmaxsize)) - rysize
                dxsize = int(rxsize/rmaxsize * TILESIZE)
                dysize = int(rysize/rmaxsize * TILESIZE)
                
                # Show the progress bar.
                percent = int(ceil((tileno) / float(tilecount-1) * 100))
                while progress <= percent:
                    if pipe:
                        pipe.send('%s:%d' % (mbtile_id, progress))
                    #if progress % 10 == 0:
                        #sys.stdout.write( "%d" % progress )
                        #sys.stdout.flush()
                    #else:
                        #sys.stdout.write( '.' )
                        #sys.stdout.flush()
                    progress += 1
               
                # Load raster from read window.
                data = dataset.ReadRaster(rx, ry, rxsize, rysize, dxsize, dysize)
                if user_dir:
                    write_data_to_dir(mbtile_id, (zoom, ix, iy), data, dxsize, dysize, bands)
                else:
                    if mb_db:
                        write_data_to_db((zoom, ix, iy), data, dxsize, dysize, bands, mb_db, use_base64)
                tileno += 1
    if mb_db:
        mb_db.close()



def write_data_to_dir(mbtile_id, index, pngdata, dxsize, dysize, bands):
    if bands == 3 and TILEFORMAT == 'png':
        tmp = TEMPDRIVER.Create('', TILESIZE, TILESIZE, bands=4)
        alpha = tmp.GetRasterBand(4)
        #from Numeric import zeros
        alphaarray = (np.zeros((dysize, dxsize)) + 255).astype('b')
        alpha.WriteArray( alphaarray, 0, TILESIZE-dysize )
    else:
        tmp = TEMPDRIVER.Create('', TILESIZE, TILESIZE, bands=bands)

    tmp.WriteRaster( 0, TILESIZE-dysize, dxsize, dysize, pngdata, band_list=range(1, bands+1))
    
    #ddd = tmp.getBytes()
    #print(len(ddd))
    
    zoom_level = index[0]
    tile_column = index[1]
    tile_row = index[2]
    if not os.path.exists(DIRTILEROOT):
        os.mkdir(DIRTILEROOT)
    p = os.path.join(DIRTILEROOT, mbtile_id)
    if not os.path.exists(p):
        os.mkdir(p)
    p = os.path.join(p, str(zoom_level))
    if not os.path.exists(p):
        os.mkdir(p)
    p = os.path.join(p, str(tile_column))
    if not os.path.exists(p):
        os.mkdir(p)
    p = os.path.join(p, '%d.png' % tile_row)
    TILEDRIVER.CreateCopy(p, tmp, strict=0)
    

    
def create_mbtiles_from_googletile(mbtile_id, pipe=None, use_base64=True):
    #ldir = None
    mb_db = init_mbtiles_db(mbtile_id, use_base64)
    l = list_by_tile_google(GOOGLETILEROOT, mbtile_id)
    curindex = 0
    cur = None
    for obj in l:
        if curindex % MAXCOMMITRECORDS == 0:
            cur = mb_db.cursor()
        write_n_tile_data_from_file(obj['tile_path'], obj['zoom_level'], obj['tile_column'], obj['tile_row'], mb_db, cur, use_base64)
        curindex += 1
        if curindex % MAXCOMMITRECORDS == 0:
            mb_db.commit()
            cur.close()
            cur = None
                        
    if cur:
        mb_db.commit()
        cur.close()
        cur = None
    mb_db.close()
    
def create_mbtiles_from_esritile(mbtile_id, pipe=None, use_base64=True):
    mb_db = init_mbtiles_db(mbtile_id, use_base64)
    l = list_by_tile_esri(ARCGISTILEROOT, mbtile_id)
    curindex = 0
    cur = None
    for obj in l:
        if curindex % MAXCOMMITRECORDS == 0:
            cur = mb_db.cursor()
        write_n_tile_data_from_file(obj['tile_path'], obj['zoom_level'], obj['tile_column'], obj['tile_row'], mb_db, cur, use_base64)
        curindex += 1
        if curindex % MAXCOMMITRECORDS == 0:
            mb_db.commit()
            cur.close()
            cur = None
                        
    if cur:
        mb_db.commit()
        cur.close()
        cur = None
    mb_db.close()
    
def create_mbtiles_from_esritile_and_zoom(area, minzoom, maxzoom, mbtile_id=None, pipe=None, use_base64=True, use_png8=False):
    mbname = '%s_sat_%d_%d' % (area, minzoom, maxzoom)
    if mbtile_id:
        mbname = '%s_sat_%s_%d_%d' % (area, mbtile_id,  minzoom, maxzoom)
    
    mb_db = init_mbtiles_db(mbname, use_base64)
    l = list_by_zoom_esri(area, ARCGISTILEROOT, minzoom, maxzoom, mbtile_id)
    curindex = 0
    cur = None
    for obj in l:
        if curindex % MAXCOMMITRECORDS == 0:
            cur = mb_db.cursor()
        write_n_tile_data_from_file(obj['tile_path'], obj['zoom_level'], obj['tile_column'], obj['tile_row'], mb_db, cur, use_base64, use_png8)
        curindex += 1
        if curindex % MAXCOMMITRECORDS == 0:
            mb_db.commit()
            cur.close()
            cur = None
                        
    if cur:
        mb_db.commit()
        cur.close()
        cur = None
    mb_db.close()
    

#copy tiles with structure zoom/row/column           
def copy_tiles_zoom_row_column(area, minzoom, maxzoom):
    tileroot = os.path.join(TILEROOT, '%s_sat_%d_%d' % (area, minzoom, maxzoom))
    if not os.path.exists(tileroot):
        os.mkdir(tileroot)
    l = list_by_zoom_esri(area, ARCGISTILEROOT,  minzoom, maxzoom)
    for i in l:
        zoom = '%d' % i['zoom_level']
        column = '%d' % i['tile_column']
        row = '%d' % i['tile_row']
        p = os.path.join(tileroot, zoom)
        if not os.path.exists(p):
            os.mkdir(p)
        p = os.path.join(p, row)
        if not os.path.exists(p):
            os.mkdir(p)
        oldname = os.path.join(p, os.path.basename(i['tile_path']))
        newname = os.path.join(p, '%s.png' % column)
        if not os.path.exists(newname):
            print('copying %s...' % newname)
            shutil.copy(i['tile_path'], p)
            os.rename(oldname, newname)

#copy tiles with structure zoom/column/row           
def copy_tiles_zoom_column_row(area, minzoom, maxzoom, mbtile_id=None, use_png8=False):
    tileroot = os.path.join(TILEROOT, '%s_sat_%d_%d' % (area, minzoom, maxzoom))
    #if os.path.exists(tileroot):
        #shutil.rmtree(tileroot)
    if not os.path.exists(tileroot):
        os.mkdir(tileroot)
    tilesrc = os.path.join(ARCGISTILEROOT, area)
    l = list_by_zoom_esri(area, tilesrc,  minzoom, maxzoom, mbtile_id)
    for i in l:
        zoom = '%d' % i['zoom_level']
        column = '%d' % i['tile_column']
        row = '%d' % i['tile_row']
        p = os.path.join(tileroot, zoom)
        if not os.path.exists(p):
            os.mkdir(p)
        p = os.path.join(p, column)
        if not os.path.exists(p):
            os.mkdir(p)
        oldname = os.path.join(p, os.path.basename(i['tile_path']))
        newname = os.path.join(p, '%s.png' % row)
        if os.path.exists(newname):
            os.remove(newname)
        if not os.path.exists(newname):
            if use_png8:
                print('copying %s use rgb8...' % newname)
                im = Image.open(i['tile_path'])
                im2 = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
                im2.save(newname)
            else:
                print('copying %s...' % newname)
                shutil.copy(i['tile_path'], p)
                os.rename(oldname, newname)
            
            
            
            
            
            
            

#copy tiles with same structure of esri tiles L0{zoom}/R0000{row}/C0000{column}
def copy_tiles_as_esri(area, minzoom, maxzoom):
    tileroot = os.path.join(TILEROOT, '%s_sat_%d_%d' % (area, minzoom, maxzoom))
    #if os.path.exists(tileroot):
        #shutil.rmtree(tileroot)
    if not os.path.exists(tileroot):
        os.mkdir(tileroot)
    l = list_by_zoom_esri(area, ARCGISTILEROOT,  minzoom, maxzoom)
    for i in l:
        p = i['tile_path']
        zoom = os.path.basename( os.path.dirname(os.path.dirname(p)))
        row = os.path.basename( os.path.dirname(p))
        
        p = os.path.join(tileroot, zoom)
        if not os.path.exists(p):
            os.mkdir(p)
        p = os.path.join(p, row)
        if not os.path.exists(p):
            os.mkdir(p)
        print('copying %s...' % i['tile_path'])
        shutil.copy(i['tile_path'], p)
 


def convert_shp_to_mongo(shp, piny):
    def tuple_to_list(obj):
        if isinstance(obj, tuple):
            l = []
            for i in obj:
                if isinstance(i, tuple):
                    l.append(tuple_to_list(i))
                else:
                    l.append(i)
            obj = l
        elif isinstance(obj, list):
            l = []
            for i in obj:
                l.append(tuple_to_list(i))
            obj = l
        elif isinstance(obj, dict):
            for k in obj.keys():
                obj[k] = tuple_to_list(obj[k])
        else:
            pass
        return obj
                
        
    POINTDEF = ['hotel', 'restaurant', 'mall',  'exitentrance', 'village', 'building', 'subcity', 'busstop', 'park',  'provincecapital', 'rollstop', 'parker', 'county', 'school', 'chemistsshop', 'hospital', 'bank', 'town', ]
    #LINESTRINGDEF = ['speedway', 'heighway', 'nationalroad',  'provinceroad', 'railway', ]#'countyroad','villageroad',
    #LINESTRINGDEF = ['countyroad',]#'villageroad',]
    ret = []
    shpname = os.path.basename(shp)
    shpname = shpname.replace('.shp','')
    key = None
    for k in GEOJSONSHAPEMAPPING.keys():
        if shpname == GEOJSONSHAPEMAPPING[k] and not k in ['subway',]:
            key = k
            break
    if key :
        if not key in LINESTRINGDEF:
            return ret
        print('%s%s' % (key, GEOJSONSHAPEMAPPING[key]))
        reader = shapefile.Reader(shp)
        fields = reader.fields[1:]
        field_names = [field[0] for field in fields]
        for sr in reader.shapeRecords():
            atr = {}
            for i in range(len(field_names)):
                #atr[enc(dec(field_names[i]))] = enc(dec(sr.record[i]))
                kk = dec1(field_names[i])
                if kk == u'KIND':
                    continue
                if kk == u'NAME':
                    kk = u'name'
                atr[kk] = dec1(sr.record[i])
            atr['type'] = key
            atr['description'] = ''
            atr['py'] = ''
            if atr.has_key(u'name') and len(atr[u'name'].strip())>0:
                try:
                    atr['py'] = piny.hanzi2pinyin_first_letter(atr[u'name'].strip().replace(u'银行',u'银哈').replace(u'工行',u'工哈').replace(u'农行',u'农哈').replace(u'建行',u'建哈').replace(u'中行',u'中哈').replace(u'交行',u'交哈').replace(u'招行',u'招哈').replace(u'支行',u'支哈').replace(u'分行',u'分哈'))
                except:
                    pass
            geom = tuple_to_list(sr.shape.__geo_interface__)
            #geom = chop(geom, bound)
            webgis_type = ''
            if geom:
                obj = dict(type="Feature",  geometry=geom, properties=atr)
                if obj['geometry']['type'] == 'Point':
                    if key in POINTDEF :
                        webgis_type = 'point_' + key
                if obj['geometry']['type'] == 'LineString':
                    if key in LINESTRINGDEF:
                        webgis_type = 'polyline_' + key
                if len(webgis_type)>0:
                    obj['properties']['webgis_type'] = webgis_type
                    if key in POINTDEF or key in LINESTRINGDEF:
                        obj = update_geometry2d(obj, True)
                    ret.append(obj) 
    return ret

    
def convert_shp_to_geojson(area, bound, shp, piny):
    def chop(g, b):
        ret = None
        if g['type']=='LineString':
            coord = []
            gcoordinates =  list(g['coordinates'])
            for i in gcoordinates:
                if i[0]>=b['min'][0] and i[1]>=b['min'][1] and i[0]<=b['max'][0] and i[1]<=b['max'][1]:
                    coord.append(i)
            g['coordinates'] = tuple(coord)
            if len(coord)>0:
                ret = g
        elif g['type']=='MultiLineString':
            #print(g['coordinates'])
            coord = []
            gcoordinates =  list(g['coordinates'])
            for i in gcoordinates:
                coord1 = []
                gcoordinates1 =  list(i)
                for j in gcoordinates1:
                    if j[0]>=b['min'][0] and j[1]>=b['min'][1] and j[0]<=b['max'][0] and j[1]<=b['max'][1]:
                        coord1.append(j)
                if len(coord1)>0:
                    coord.append(tuple(coord1))
            g['coordinates'] = tuple(coord)
            if len(coord)>0:
                ret = g
        elif g['type']=='Point':
            j = g['coordinates']
            if j[0]>=b['min'][0] and j[1]>=b['min'][1] and j[0]<=b['max'][0] and j[1]<=b['max'][1]:
                ret = g
        elif g['type']=='MultiPolygon':
            #print(g['coordinates'])
            coord = []
            gcoordinates =  g['coordinates']
            for i in gcoordinates:
                coord1 = []
                gcoordinates1 =  i
                for j in gcoordinates1:
                    coord2 = []
                    gcoordinates2 =  list(j)
                    for k in gcoordinates2:
                        if k[0]>=b['min'][0] and k[1]>=b['min'][1] and k[0]<=b['max'][0] and k[1]<=b['max'][1]:
                            coord2.append(k)
                    if len(coord2)>0:
                        coord1.append(tuple(coord2))
                if len(coord1)>0:
                    coord.append(coord1)
            g['coordinates'] = coord
            if len(coord)>0:
                ret = g
        elif g['type']=='Polygon':
            #print(g['coordinates'])
            coord = []
            gcoordinates =  list(g['coordinates'])
            for i in gcoordinates:
                coord1 = []
                gcoordinates1 =  list(i)
                for j in gcoordinates1:
                    if j[0]>=b['min'][0] and j[1]>=b['min'][1] and j[0]<=b['max'][0] and j[1]<=b['max'][1]:
                        coord1.append(j)
                if len(coord1)>0:
                    coord.append(tuple(coord1))
            g['coordinates'] = tuple(coord)
            if len(coord)>0:
                ret = g
        return ret
    # read the shapefile
    shpname = os.path.basename(shp)
    shpname = shpname.replace('.shp','')
    jsonfile = None
    for k in GEOJSONSHAPEMAPPING.keys():
        if shpname == GEOJSONSHAPEMAPPING[k] and not k in ['subway',]:
            jsonfile = '%s.json' % k
            break
    if jsonfile:
        fpath = os.path.abspath(SERVERJSONROOT)
        if not os.path.exists(fpath):
            os.mkdir(fpath)
        fpath = os.path.join(fpath, area, jsonfile)
        reader = shapefile.Reader(shp)
        fields = reader.fields[1:]
        field_names = [field[0] for field in fields]
        buf = []
        for sr in reader.shapeRecords():
            #atr = dict(zip(field_names, sr.record))
            atr = {}
            for i in range(len(field_names)):
                #atr[enc(dec(field_names[i]))] = enc(dec(sr.record[i]))
                atr[dec1(field_names[i])] = dec1(sr.record[i])
            atr['type'] = k
            atr['py'] = ''
            #if atr.has_key('NAME') and len(dec(atr['NAME'].strip()))>0:
            if atr.has_key(u'NAME') and len(atr[u'NAME'].strip())>0:
                try:
                    atr['py'] = piny.hanzi2pinyin_first_letter(atr[u'NAME'].strip().replace(u'银行',u'银哈').replace(u'工行',u'工哈').replace(u'农行',u'农哈').replace(u'建行',u'建哈').replace(u'中行',u'中哈').replace(u'交行',u'交哈').replace(u'招行',u'招哈').replace(u'支行',u'支哈').replace(u'分行',u'分哈'))
                except:
                    pass
            #print('%s=%s' % (dec(atr['NAME']), atr['py']))
            geom = sr.shape.__geo_interface__
            geom = chop(geom, bound)
            if geom:
                buf.append(dict(type="Feature",  geometry=geom, properties=atr)) 
    
        # write the GeoJSON file
        print(fpath)
        absroot = os.path.join(SERVERJSONROOT, area)
        if not os.path.exists(absroot):
            os.mkdir(absroot)
        
        
        with open(fpath, "w") as f:
            f.write(enc(json.dumps({"type": "FeatureCollection", "features": buf},ensure_ascii=False, indent=4)) + "\n")
        #try:
            #p = os.path.join(JSONROOT, os.path.basename(fpath))
            #if os.path.exists(p):
                #os.remove(p)
            #shutil.copy(fpath, JSONROOT)
        #except:
            #pass
            
def get_pinyin_data():
    global gPinYin
    if gPinYin is None:
        pydatapath = os.path.join(module_path(), 'pinyin_word.data');
        gPinYin =  PinYin(pydatapath)
        gPinYin.load_word()
    return gPinYin
        
             
def gen_geojson_by_shape(area = None):
    piny = get_pinyin_data()
    bounds = None
    if area:
        p = os.path.abspath(SERVERJSONROOT)
        p = os.path.join(p, 'yn_tiles_bounds_%s.json' % area)
        with open(p,) as f:
            bounds = json.loads(f.read())
    for i in os.listdir(SHAPEROOT):
        p = os.path.join(SHAPEROOT, i)
        if os.path.isfile(p) and i[-4:]=='.shp':
            #if i == u'村.shp':
            convert_shp_to_geojson(area, bounds,  p, piny)
            
def test_import_shape_to_mongo():
    global gClientMongo
    piny = get_pinyin_data()
    geojson = []
    for i in os.listdir(SHAPEROOT):
        p = os.path.join(SHAPEROOT, i)
        if os.path.isfile(p) and i[-4:]=='.shp':
            #if i in [u'省界.shp', u'市界.shp', u'县界.shp']:
            geojson.extend(convert_shp_to_mongo(p, piny))
            #if len(geojson)>0:
                #break
    #if True:return
    try:
        mongo_init_client()
        db = gClientMongo['webgis']['feature_yn']
        if not 'features' in db.collection_names(False):
            collection = db.create_collection(k)
        collection = db['features']   
        for i in geojson:
            collection.save(i)
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)

            

def gen_geojson_by_tunnel_devices(area, piny):
    ret = {}
    absroot = SERVERJSONROOT
    if not os.path.exists(absroot):
        os.mkdir(absroot)
    absroot = os.path.join(absroot, area)
    if not os.path.exists(absroot):
        os.mkdir(absroot)
    tuns = odbc_get_records('VIEW_DEVICE_TUNNEL', "1=1"  , area)
    paths = {}
    for tun in tuns:
        if not ret.has_key(tun['tunnel_id']):
            ret[tun['tunnel_id']] = {}
            ret[tun['tunnel_id']]['type'] = 'FeatureCollection'
            ret[tun['tunnel_id']]['features'] = []
        
        o = {}
        o['geometry'] = {}
        o['geometry']['type'] = 'Point'
        o['geometry']['coordinates'] = [tun['longitude'],  tun['latitude']]
        o['type'] = 'Feature'
        o['properties'] = {}
        o['properties']['device_name'] = tun['equip_name']
        o['properties']['NAME'] = tun['equip_name']
        o['properties']['py'] = ''
        try:
            o['properties']['py'] = piny.hanzi2pinyin_first_letter(tun['equip_name'].replace('#','').replace('II',u'二').replace('I',u'一'))
        except:
            pass
        for k in tun.keys():
            if isinstance(tun[k], unicode):
                #tun[k] = tun[k]
                pass
            o['properties'][k] = tun[k]
        ret[tun['tunnel_id']]['features'].append(o)
        
    for k in ret.keys():    
        s = json.dumps(ret[k], indent=4, ensure_ascii=False)
        path = os.path.join(absroot, 'geojson_tunneldevice_%s_%s.json' % (area, k) )
        with open(path, 'w') as f:
            f.write(enc(s) + '\n')
    return ret
        
    
    
    
def gen_geojson_by_tunnels(area, piny):
    ret = {}
    absroot = SERVERJSONROOT
    if not os.path.exists(absroot):
        os.mkdir(absroot)
    absroot = os.path.join(absroot, area)
    if not os.path.exists(absroot):
        os.mkdir(absroot)
        
        
    secs = odbc_get_records('TABLE_TUNNEL_SECTION', "1=1" , area)
    for sec in secs:
        tuns = odbc_get_records('TABLE_TUNNEL', "tunnel_id='%s'" % sec['tunnel_id'] , area)
        if len(tuns)>0:
            path = os.path.join(absroot, 'geojson_tunnel_%s_%s.json' % (area, sec['ts_id']) )
            recs = odbc_get_records('VIEW_TUNNEL_SECTION', "ts_id='%s'" %  sec['ts_id'], area)
            coords = []
            for rec in recs:
                coords.append([rec['point_seq'], rec['lng'], rec['lat'], ])
            coords1  = sorted(coords, key=lambda x: x[0], reverse=True)
            coords2  = [[i[1], i[2],] for i in coords1]
            tunnel_obj = {}
            tunnel_obj['type'] = 'FeatureCollection'
            tunnel_obj['features'] = []
            o = {}
            o['geometry'] = {}
            o['geometry']['type'] = 'LineString'
            o['geometry']['coordinates'] = coords2
            o['type'] = 'Feature'
            o['properties'] = {}
            
            
            o['properties']['tunnel_name'] = tuns[0]['tunnel_name'] + u' ' + sec['start_point'] + u'至' + sec['end_point']
            o['properties']['NAME'] = tuns[0]['tunnel_name'] + u' ' + sec['start_point'] + u'至' + sec['end_point']
            o['properties']['py'] = ''
            try:
                o['properties']['py'] = piny.hanzi2pinyin_first_letter(tuns[0]['tunnel_name'].replace('#','').replace('II',u'二').replace('I',u'一'))
            except:
                pass
            for k in sec.keys():
                if isinstance(sec[k], unicode):
                    #sec[k] = enc(sec[k])
                    pass
                o['properties'][k] = sec[k]
            tunnel_obj['features'].append(o)
            s = json.dumps(tunnel_obj, indent=4, ensure_ascii=False)
            with open(path, 'w') as f:
                f.write(enc(s) + '\n')
            ret[sec['ts_id']] = tunnel_obj
    return ret
                
def gen_geojson_by_potential_risk(area, piny):
    absroot = SERVERJSONROOT
    if not os.path.exists(absroot):
        os.mkdir(absroot)
    absroot = os.path.join(absroot, area)
    if not os.path.exists(absroot):
        os.mkdir(absroot)
    path = os.path.join(absroot, 'geojson_potential_risk_%s.json' % area )
    recs = odbc_get_records('VIEW_POTENTIAL_RISK', "1=1" , area)
    
    obj = {}
    obj['type'] = 'FeatureCollection'
    obj['features'] = []
    
    validlgtlat = None, None
    
    recdict = {}
    for rec in recs:
        if not recdict.has_key(rec['id']):
            recdict[rec['id']] = {}
        if not recdict[rec['id']].has_key('coordinates'):
            recdict[rec['id']]['coordinates'] = []
        recdict[rec['id']]['coordinates'].append([rec['xcoord'], rec['ycoord']])
        if not recdict[rec['id']].has_key('properties1'):
            recdict[rec['id']]['properties1'] = {}
            recdict[rec['id']]['properties1']['type'] = rec['risk_type']
            recdict[rec['id']]['properties1']['NAME'] = rec['risk_info']
            recdict[rec['id']]['properties1']['tip'] = u'隐患点描述:%s<br/>隐患点类型:%s<br/>发现时间:%s<br/>记录人:%s<br/>联系人:%s<br/>联系方式:%s<br/>' % (rec['risk_info'], rec['risk_type'], rec['appear_date'],rec['record_person'],rec['contact_person'],rec['contact_number'], )
            recdict[rec['id']]['properties1']['py'] = ''
            try:
                recdict[rec['id']]['properties1']['py'] = piny.hanzi2pinyin_first_letter(rec['risk_info'].replace('#','').replace('II',u'二').replace('I',u'一'))
                #print(o['properties']['py'])
            except:
                print(sys.exc_info()[1])
                
        if not recdict[rec['id']].has_key('properties'):
            recdict[rec['id']]['properties'] = {}
            recdict[rec['id']]['properties']['risk_type'] = rec['risk_type']
            recdict[rec['id']]['properties']['risk_info'] = rec['risk_info']
            recdict[rec['id']]['properties']['appear_date'] = rec['appear_date']
            recdict[rec['id']]['properties']['record_person'] = rec['record_person']
            recdict[rec['id']]['properties']['contact_person'] = rec['contact_person']
            recdict[rec['id']]['properties']['contact_number'] = rec['contact_number']
            recdict[rec['id']]['properties']['height'] = rec['height']
            
    for k in recdict:
        rec = recdict[k]
        o = {}
        o['geometry'] = {}
        if len(rec['coordinates']) == 1:
            o['geometry']['type'] = 'Point'
            o['geometry']['coordinates'] = list(rec['coordinates'][0])
        elif len(rec['coordinates']) >= 2 and not rec['coordinates'][0] == rec['coordinates'][-1]:
            o['geometry']['type'] = 'LineString'
            o['geometry']['coordinates'] = list(rec['coordinates'])
        elif len(rec['coordinates']) > 2 and rec['coordinates'][0] == rec['coordinates'][-1]:
            o['geometry']['type'] = 'Polygon'
            o['geometry']['coordinates'] = [rec['coordinates']]
        o['type'] = 'Feature'
        o['properties'] = rec['properties']
        #o['properties1'] = rec['properties1']
        obj['features'].append(o)
    
    with open(path, 'w') as f:
        #s = json.dumps(obj)
        f.write(enc(json.dumps(obj, ensure_ascii=False, indent=4)) + '\n')
    #try:
        #p = os.path.join(JSONROOT, os.path.basename(path))
        #if os.path.exists(p):
            #os.remove(p)
        #shutil.copy(path, JSONROOT)
    #except:
        #pass
    return obj
    
    
    
    
def gen_geojson_by_line_id(line_id, area, piny):
    bounds = None
    absroot = os.path.abspath(SERVERJSONROOT)
    if not os.path.exists(absroot):
        os.mkdir(absroot)
    absroot = os.path.join(absroot, area)
    if not os.path.exists(absroot):
        os.mkdir(absroot)
    
    linepath = os.path.join(absroot, 'geojson_line_%s_%s.json' % (area, line_id))
    towerspath = os.path.join(absroot, 'geojson_towers_%s_%s.json' % (area, line_id))
    lines = odbc_get_records('TABLE_LINE', "id='%s'" % line_id, area)
    if len(lines)<1:
        print('cannot found any line with id[%s]' % line_id)
        return
    line = lines[0]
    towers_sort = odbc_get_sorted_tower_by_line(line_id, area)
    if len(towers_sort)==0:
        return {}, {}
    line_obj = {}
    line_obj['type'] = 'FeatureCollection'
    line_obj['features'] = []
    o = {}
    o['geometry'] = {}
    o['geometry']['type'] = 'LineString'
    o['geometry']['coordinates'] = []
    o['type'] = 'Feature'
    o['properties'] = {}
    
    towers_obj = {}
    towers_obj['type'] = 'FeatureCollection'
    towers_obj['features'] = []
    
    
    
    
    for k in line.keys():
        if isinstance(line[k], unicode):
            #line[k] = line[k]
            pass
        if k=='line_name':
            o['properties']['NAME'] = line[k]
            o['properties']['py'] = ''
            try:
                o['properties']['py'] = piny.hanzi2pinyin_first_letter(line[k].replace('#','').replace('II',u'二').replace('I',u'一'))
            except:
                pass
        o['properties'][k] = line[k]
    validlgtlat = None, None
    for tower in towers_sort:
        x, y = tower['geo_x'], tower['geo_y']
        if x and y:
            validlgtlat = x, y
        else:
            if validlgtlat[0] and validlgtlat[1]:
                x, y = validlgtlat[0] , validlgtlat[1]
        if x is None or y is None:
            continue
        o['geometry']['coordinates'].append([x, y])
        tower_obj = {}
        tower_obj['geometry'] = {}
        tower_obj['geometry']['type'] = 'Point'
        tower_obj['geometry']['coordinates'] = [x, y]
        tower_obj['type'] = 'Feature'
        tower_obj['properties'] = {}
        for k in tower.keys():
            if isinstance(tower[k], unicode):
                #tower[k] = tower[k]
                pass
            if k=='tower_name':
                tower_obj['properties']['NAME'] = tower[k]
                tower_obj['properties']['py'] = ''
                try:
                    tower_obj['properties']['py'] = piny.hanzi2pinyin_first_letter(tower[k].replace('#','').replace('II',u'二').replace('I',u'一'))
                except:
                    pass
            tower_obj['properties'][k] = tower[k]
        towers_obj['features'].append(tower_obj)
                
    
    line_obj['features'].append(o)    
    with open(linepath, 'w') as f:
        f.write(enc(json.dumps(line_obj, ensure_ascii=False, indent=4) + '\n'))
    with open(towerspath, 'w') as f:
        f.write(enc(json.dumps(towers_obj, ensure_ascii=False, indent=4) + '\n'))
    #try:
        #p = os.path.join(JSONROOT, os.path.basename(linepath))
        #if os.path.exists(p):
            #os.remove(p)
        #p = os.path.join(JSONROOT, os.path.basename(towerspath))
        #if os.path.exists(p):
            #os.remove(p)
        #shutil.copy(linepath, JSONROOT)
        #shutil.copy(towerspath, JSONROOT)
    #except:
        #pass
    return line_obj, towers_obj
    
def gen_geojson_by_lines(area):
    piny = get_pinyin_data()
    ret = {}
    ret['line'] = {}
    ret['towers'] = {}
    ret['tunnels'] = {}
    ret['tunnel_devices'] = {}
    ret['potential_risk'] = {}
    lines = odbc_get_records('TABLE_LINE', '1=1',area)
    for line in lines:
        line_obj, towers_obj = gen_geojson_by_line_id(line['id'], area, piny)
        if len(line_obj.keys())==0 or len(line_obj.keys())==0:
            continue
        ret['line'][line['id']] = line_obj
        ret['towers'][line['id']] = towers_obj
    ret['potential_risk'] = gen_geojson_by_potential_risk(area, piny)
    if area == 'km':
        ret['tunnels'] = gen_geojson_by_tunnels(area, piny)
        ret['tunnel_devices'] = gen_geojson_by_tunnel_devices(area, piny)
    return ret
        
        

def test_insert_km_towers():
    line_names = [u'厂金II回', u'厂金I回', u'草海线', u'郭南线', u'郭金线', u'马海温线', u'七官II回', u'七官I回']
    line_towers_num = {u'厂金II回':78, u'厂金I回':78, u'草海线':97, u'郭南线':0, u'郭金线':0, u'马海温线':81, u'七官II回':56, u'七官I回':56}
    lines = odbc_get_records('TABLE_LINE', '1=1', 'km')
    sqls = []
    
    for line in lines:
        if line['line_name'] in line_names:
            for i in range(1, line_towers_num[line['line_name']]+1):
                sql = '''INSERT INTO TABLE_TOWER(
                id, 
                line_id, 
                tower_name, 
                same_tower, 
                line_position
                ) VALUES(
                '%s', 
                '%s', 
                '%s',
                '%s',
                '%s'
                )''' % (
                str(uuid.uuid4()),
                line['id'],
                '%s#%d' % (line['line_name'],i),
                ZEROID,
                u'单回'
                )
                sqls.append(sql)
    #print(sqls)
    try:
        odbc_execute_sqls(sqls, 'km')
    except:
        print(sys.exc_info()[1][1])
        
    
def test_insert_potential_risk():
    data = []
    for i in range(100):
        risk_type = ''
        if i % 5 == 0:
            risk_type = u'林木'
        if i % 5 == 1:
            risk_type = u'违章建筑'
        if i % 5 == 2:
            risk_type = u'施工区域'
        if i % 5 == 3:
            risk_type = u'交叉跨越'
        if i % 5 == 4:
            risk_type = u'污染源'
            
        data.append( {'risk_type':risk_type, 'risk_info':u'隐患点' + unicode(str(i)), 'geometry_type':1,'appear_date':'2013-10-08 17:39:51','record_person':u'记录人' + unicode(str(i)), 'contact_person':u'联系人' + unicode(str(i)),'contact_number':'12345678901', 'center_x':random.triangular(103.4, 104.0),'center_y':random.triangular(27.1, 27.6),'height':random.triangular(10, 100)})
    sqls = []
    for i in data:
        sql = '''
        INSERT INTO TABLE_POTENTIAL_RISK_INFO(
        id,
        risk_type,
        risk_info,
        geometry_type,
        appear_date,
        record_person,
        contact_person,
        contact_number,
        center_x,
        center_y,
        height
        )VALUES(
        '%s',
        '%s',
        '%s',
        %d,
        '%s',
        '%s',
        '%s',
        '%s',
        %f,
        %f,
        %f
        )
        ''' % (
        str(uuid.uuid4()),
        i['risk_type'],
        i['risk_info'],        
        i['geometry_type'],
        i['appear_date'],
        i['record_person'],
        i['contact_person'],
        i['contact_number'],
        i['center_x'],
        i['center_y'],
        i['height'],
        )
        sqls.append(sql)
    try:
        print(sqls)
        odbc_execute_sqls(sqls, 'zt')
    except:
        print(sys.exc_info()[1][1])
        
def test_insert_thunder_counter_attach():
    attach_data = []
    towers = odbc_get_sorted_tower_by_line('4a0d0df0-8685-489e-99c4-389db61044e7', 'zt')
    toweridx = 0
    for tower in towers:
        toweridx += 1
        if toweridx > 10:
            break
        j = random.randint(0, 5)
        for i in range(j+1):
            attach_name = ''
            if i % 5 == 0:
                attach_name = u'雷电计数器类型1'
            if i % 5 == 1:
                attach_name = u'雷电计数器类型2'
            if i % 5 == 2:
                attach_name = u'雷电计数器类型3'
            if i % 5 == 3:
                attach_name = u'雷电计数器类型4'
            if i % 5 == 4:
                attach_name = u'雷电计数器类型5'
            attaid = str(uuid.uuid4())
            attach_data.append( {'id': attaid, 
                                 'tower_id': tower['id'], 
                                 'attach_type':7, 
                                 'attach_name':attach_name, 
                                 'manufacturer':'test', 
                                 'series':'test', 
                                 'status':'', 
                                 'install_date':'2002-01-01 00:00:00', 
                                 'check_date':'2002-01-01 00:00:00', 
                                 'check_period_m':12, 
                                 'str_value1':'', 
                                 'str_value2':'', 
                                 'str_value3':'', 
                                 'int_value1':0, 
                                 'int_value2':0, 
                                 'int_value3':0, 
                                 'float_value1':0.0, 
                                 'float_value2':0.0, 
                                 'float_value3':0.0,
                                 'remark':'test'
                                 })
    sqls = []
    for i in attach_data:
        ss = sqlize_data(i)
        sql = '''
        INSERT INTO TABLE_TOWER_ATTACH(
        id,
        tower_id, 
        attach_type, 
        attach_name, 
        manufacturer, 
        series, 
        status, 
        install_date, 
        check_date, 
        check_period_m, 
        str_value1, 
        str_value2, 
        str_value3, 
        int_value1, 
        int_value2, 
        int_value3, 
        float_value1, 
        float_value2, 
        float_value3,
        remark
        )VALUES(
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
        )
        ''' % (
                ss['id'],
                ss['tower_id'], 
                ss['attach_type'], 
                ss['attach_name'], 
                ss['manufacturer'], 
                ss['series'], 
                ss['status'], 
                ss['install_date'], 
                ss['check_date'], 
                ss['check_period_m'], 
                ss['str_value1'], 
                ss['str_value2'], 
                ss['str_value3'], 
                ss['int_value1'], 
                ss['int_value2'], 
                ss['int_value3'], 
                ss['float_value1'], 
                ss['float_value2'], 
                ss['float_value3'],
                ss['remark']
        )
        sqls.append(sql)
    try:
        print(sqls)
        odbc_execute_sqls(sqls, 'zt')
    except:
        print(sys.exc_info()[1][1])

def test_png24_to_png8():
    testp = ur'I:\geotiff\01457_Esri瓦片\_alllayers\L16\R00006b27\C0000c9ca.png'
    testp1 = ur'I:\geotiff\01457_Esri瓦片\_alllayers\L16\R00006b27\C0000c9ca_rgb8.png'
    im = Image.open(testp)
    im2 = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
    im2.save(testp1)

def test_find_in_witch_tile(lgtlat):
    p = os.path.join(SERVERJSONROOT, 'yn_tiles_index.json')
    p = os.path.abspath(p)
    objlist = None
    with open(p) as f:
        objlist = json.loads(f.read())
    ret = None
    for i in objlist:
        key = i.keys()[0]
        obj = i[key]
        geox1 = obj['ld'][0]
        geox2 = obj['ru'][0]
        geoy1 = obj['ld'][1]
        geoy2 = obj['ru'][1]
        if geox1<=lgtlat[0] and geoy1<=lgtlat[1] and  lgtlat[0]<=geox2 and lgtlat[1]<=geoy2:
            ret = key
            break
    print('found (%f, %f) in %s' % (lgtlat[0], lgtlat[1], ret))
    return ret
    
def test_get_area_by_latlng(area):
    path = os.path.join(module_path(), 'static', 'geojson', 'yn_tiles_bounds_%s.json' % area)
    path = os.path.abspath(path)
    obj = {}
    with open(path) as f:
        obj = json.loads(f.read())
    if len(obj.keys())>0:
        d = catenary.distance([obj['max'][1],obj['max'][0] ], [obj['min'][1],obj['min'][0] ])
        print(d)
        
    
    
    
def test_tile_directory():
    s = test_get_all_task_file_by_area('zt')
    l = []
    for i in os.listdir(ARCGISTILEROOT):
        p = os.path.join(ARCGISTILEROOT, i)
        if os.path.isdir(p) and i[5:6]=='_':
            l.append(i[:5])
    print(l)
    ll = []
    for i in s:
        if not i in l:
            ll.append(i)
    print(ll)
            
    

def collation(lng, lat):
    lng1 = int(lng) + int(100*(lng-int(lng)))/60. + (100*(lng-int(lng))-int(100*(lng-int(lng))))*100/3600.
    lat1 = int(lat) + int(100*(lat-int(lat)))/60. + (100*(lat-int(lat))-int(100*(lat-int(lat))))*100/3600.
    return lng1, lat1

def get_key_by_text(text):
    ret = None
    if text in [u'碎步点',u'所有碎步及图根点坐标']:
        ret = 'step'
    if text in [u'交叉互联箱']:
        ret = 'crossbox'
    if text in [u'电缆直通头']:
        ret = 'joint'
    if text in [u'电源馈线箱']:
        ret = 'elec_resp'
    if text in [u'电子防盗井盖',u'电子井', u'井口']:
        ret = 'elec_cover'
    if text in [u'通风口']:
        ret = 'vent'
    if text in [u'石板井盖', u'井盖', u'石井盖',]:
        ret = 'stone_cover'
    if text in [u'配电箱', u'照明配电箱', u'总电源箱',u'隧道监控电源箱']:
        ret = 'elec_box'
    if text in [u'摄像机', u'摄像头',u'监控设备']:
        ret = 'camera'
    if text in [u'水泵',u'抽水机']:
        ret = 'pump'
    if text in [u'电话', u'应急通讯终端']:
        ret = 'telephone'
    if text in [u'防火分区',u'防火门']:
        ret = 'firewall'
    if text in [u'风机',]:
        ret = 'fan'
    if text in [u'照明灯开关',]:
        ret = 'switch'
    return ret
    
def collation_lnglat(filepath):
    ret = {}
    book = xlrd.open_workbook(filepath)
    for sheet in book.sheets():
        key = get_key_by_text(sheet.name)
        if key:
            if not ret.has_key(key):
                ret[key] = []
            for i in range(sheet.nrows):
                try:
                    lng, lat, altitude = float(sheet.cell_value(i,1)), float(sheet.cell_value(i,2)), float(sheet.cell_value(i,3))
                    lng1, lat1 =collation(lng, lat)
                    #print('%.10f,%.10f=>%.10f,%.10f' % (lng, lat, lng1, lat1))
                    o = {}
                    o['id'] = sheet.cell_value(i,0)
                    o['lng'] = lng1
                    o['lat'] = lat1
                    o['alt'] = altitude
                    ret[key].append( o )
                except:
                    continue
    return ret


def get_envlop_lnglat(pointlist):
    xlist = [i['lng'] for i in pointlist]
    ylist = [i['lat'] for i in pointlist]
    minx = min(xlist)
    miny = min(ylist)
    maxx = max(xlist)
    maxy = max(ylist)
    return {'minx':minx, 'miny':miny, 'maxx':maxx, 'maxy':maxy}
    
def gen_boundry_by_list(datadir, tunnelname, data = {}):
    path = os.path.abspath(os.path.join(datadir, u'tunnel_boundry_%s.json' % tunnelname))
    env = get_envlop_lnglat(data['step'])
    if os.path.exists(path):
        obj = None
        with open(path) as f:
            obj = json.loads(f.read())
        if obj:
            obj['lnglat']['minx'] = env['minx']
            obj['lnglat']['miny'] = env['miny']
            obj['lnglat']['maxx'] = env['maxx']
            obj['lnglat']['maxy'] = env['maxy']
            with open(path, 'w') as f:
                f.write(enc(json.dumps(obj, ensure_ascii=False, indent=4)) + '\n')
    
    
    
    
def gen_geojson_by_list(datadir, tunnelname, data = {}):
    for key in data.keys():
        if key == 'step':
            path = os.path.abspath(os.path.join(datadir, u'geojson_tunnel_%s.json' % tunnelname))
            obj = {}
            obj['type'] = 'FeatureCollection'
            obj['features'] = []
            o = {}
            o['type'] = 'Feature'
            o['properties'] = {'NAME':tunnelname}
            o['geometry'] = {}
            o['geometry']['type'] = 'LineString'
            o['geometry']['coordinates'] = []
            for point in data[key]:
                o['geometry']['coordinates'].append([point['lng'], point['lat']])
            obj['features'].append(o)
        else:
            path = os.path.abspath(os.path.join(datadir, u'geojson_%s_%s.json' % (key,tunnelname)))
            obj = {}
            obj['type'] = 'FeatureCollection'
            obj['features'] = []
            for point in data[key]:
                o = {}
                o['type'] = 'Feature'
                o['properties'] = {'NAME': point['id']}
                o['geometry'] = {}
                o['geometry']['type'] = 'Point'
                o['geometry']['coordinates'] = [point['lng'], point['lat']]
                obj['features'].append(o)
            
        with open(path, 'w') as f:
            f.write(enc(json.dumps(obj, ensure_ascii=False, indent=4)) + '\n')
                
def gen_tunnel_data_json():
    gen_tunnel_data_json_from_xls(u'羊甫隧道')

def check_points_distance_enough(p1, p2):
    ret = False
    d = math.sqrt(pow(p2[0] - p1[0],2) + pow(p2[1] - p1[1],2))
    d1 = p2[2] - p1[2]
    if d > 9 :#and abs(d1):
        ret = True
    return ret
    
    
def gen_tunnel_data_json_from_xls(tname):
    coords_ogre = []
    coords_geo = []
    coords = []
    minlng, minlat, maxlng, maxlat = -1, -1, -1, -1
    minx, miny, minz, maxx, maxy, maxz = -1, -1, -1, -1, -1, -1
    if tname == u'羊甫隧道':
        filepath = ur'F:\work\cpp\kmgdgis3D\data\docs\羊甫隧道线性整理.xls'
        book = xlrd.open_workbook(filepath)
        for sheet in book.sheets():
            key = get_key_by_text(sheet.name)
            if key == 'step':
                for i in range(sheet.nrows):
                    if i==0:
                        continue
                    x, y, z = 0, 0, 0
                    try:
                        x, y, z = float(sheet.cell_value(i,11)), float(sheet.cell_value(i,12)), float(sheet.cell_value(i,13))
                    except:
                        pass
                    if x and y and z:
                        #print('x=%f,y=%f,z=%f' % (lng, lat, altitude))
                        
                        coords_geo.append([x, y, z])
                        x, y = ToWebMercator(x, y)
                        coords.append([x, y, z])
        if len(coords_geo)>0:
            minlng = min([i[0] for i in coords_geo])
            minlat = min([i[1] for i in coords_geo])
            maxlng = max([i[0] for i in coords_geo])
            maxlat = max([i[1] for i in coords_geo])
        if len(coords)>0:
            minx = min([i[0] for i in coords])
            miny = min([i[1] for i in coords])
            minz = min([i[2] for i in coords])
            maxx = max([i[0] for i in coords])
            maxy = max([i[1] for i in coords])
            maxz = max([i[2] for i in coords])
            prev = None
            for i in coords:
                p2 = [i[0]-minx, i[1]-miny, i[2]-minz]
                if len(coords_ogre)>0:
                    prev = coords_ogre[-1]
                if prev is None or (prev and check_points_distance_enough(prev, p2)):
                    coords_ogre.append(p2)
    #for i in coords_ogre:
        #print('x=%f,y=%f,z=%f' % (i[0], i[1], i[2]))
    obj = {}
    obj['lnglat'] = {}
    if len(coords_geo)>0:
        obj['lnglat']['startx'] = coords_geo[0][0]
        obj['lnglat']['starty'] = coords_geo[0][1]
        obj['lnglat']['maxx'] = maxlng
        obj['lnglat']['minx'] = minlng
        obj['lnglat']['maxy'] = maxlat
        obj['lnglat']['miny'] = minlat
    obj['ogre'] = {}
    coords_ogre.reverse()
    if len(coords_geo)>0:
        obj['ogre']['startx'] = coords_ogre[0][0] + 0
        obj['ogre']['starty'] = coords_ogre[0][1] + 0
        obj['ogre']['startz'] = coords_ogre[0][2] - 0
        obj['ogre']['startx'] = 9.297
        obj['ogre']['starty'] = 25.4903
        obj['ogre']['startz'] = -2.582
        obj['ogre']['maxx'] = maxx - minx
        obj['ogre']['minx'] = 0
        obj['ogre']['maxy'] = maxy - miny
        obj['ogre']['miny'] = 0
        obj['ogre']['maxz'] = maxz - minz
        obj['ogre']['minz'] = 0
        obj['coords'] = coords_ogre
        
    for i in coords_ogre:
        idx = coords_ogre.index(i)
        prev = None
        if idx > 0:
            prev = coords_ogre[idx - 1]
        if prev:
            d = math.sqrt(pow(i[0] - prev[0],2) + pow(i[1] - prev[1],2))
            d1 = i[2] - prev[2]
            print('%d-%d, d=%f, d1=%f' % (idx - 1, idx, d, d1))
            
      
    jsonpath = ur'F:\work\cpp\kmgdgis3D\data\blend\%s.json' % tname
    with open(jsonpath, 'w+') as f:
        f.write(enc(json.dumps(obj, ensure_ascii=False, indent=4)) + '\n')

        
    

    
def test_gen_geojson_by_list(data_dir, filelist):
    for f in filelist:
        tname = os.path.basename(f).replace('.xls','').replace(u'线性整理','')
        ret = collation_lnglat(f)
        gen_geojson_by_list(data_dir, tname, ret)
        gen_boundry_by_list(data_dir, tname, ret)
 
def gen_mongo_geojson_by_line_id(alist, line_id, area, piny, mapping, refer_mapping):
    def get_referee_towers_by_refer_id(refer_mapping, refer_id):
        ret = []
        uids = []
        for k in refer_mapping.keys():
            if refer_mapping[k] == refer_id:
                uids.append(k)
                
        if len(uids)>0:
            ids = '('
            for i in uids:
                if uids.index(i) < len(uids) - 1:
                    ids += "'%s'," % i
                else:
                    ids += "'%s'" % i
            ids += ')'
            ret = odbc_get_records('TABLE_TOWER', "id IN %s" % ids, area)
        return ret
    
    def get_refer_tower_by_refer_id(mapping, refer_id):
        ret = None
        uid = None
        for k in mapping.keys():
            if mapping[k] == refer_id:
                uid = k
                break
        if uid:
            ret = odbc_get_records('TABLE_TOWER', "id='%s'" % uid, area)
            if len(ret)>0:
                ret = ret[0]
        return ret
    def checkexist(alist, id):
        ret = False
        for i in alist:
            if i['_id'] == ObjectId(id):
                return True
        return ret
    #ret = []
    towers_sort = odbc_get_sorted_tower_by_line(line_id, area)
    validlgtlat = None, None
    prev, tower, nextt = None, None, None
    existset = set()
    for i in range(len(towers_sort)):
        #if i == 0:
            #if len(towers_sort)==1:
                #prev, tower, nextt = None, towers_sort[i], None
            #else:    
                #prev, tower, nextt = None, towers_sort[i], towers_sort[i + 1]
        #elif i == len(towers_sort) - 1:
            #prev, tower, nextt = towers_sort[i - 1], towers_sort[i], None
        #else:    
            #prev, tower, nextt = towers_sort[i - 1], towers_sort[i], towers_sort[i + 1]
            
        tower = towers_sort[i]
        tower_name = tower['tower_name']
        if not mapping.has_key(tower['id']):
            continue
        id = mapping[tower['id']]
        idold = mapping[tower['id']]
        if refer_mapping.has_key(id):
            id = refer_mapping[id]
            tower = get_refer_tower_by_refer_id(mapping, id)
            if tower is None:
                continue
            
        if refer_mapping.has_key(idold):
            tower_name += ',' + tower['tower_name']
            
        x, y, z = tower['geo_x'], tower['geo_y'], extract_one_altitude(tower['geo_x'], tower['geo_y'])
        if z is None:
            z = 0.0
        if x and y:
            validlgtlat = x, y
        else:
            if validlgtlat[0] and validlgtlat[1]:
                x, y = validlgtlat[0] , validlgtlat[1]
        if x is None or y is None:
            continue
        tower_obj = {}
        tower_obj['geometry'] = {}
        tower_obj['geometry']['type'] = 'Point'
        tower_obj['geometry']['coordinates'] = [x, y, z]
        tower_obj['geometry2d'] = {}
        tower_obj['geometry2d']['type'] = 'Point'
        tower_obj['geometry2d']['coordinates'] = [x, y]
        tower_obj['type'] = 'Feature'
        tower_obj['properties'] = {}
        tower_obj['properties']['webgis_type'] = 'point_tower'
        for k in tower.keys():
            if isinstance(tower[k], unicode):
                #tower[k] = tower[k]
                pass
            if k=='line_id':
                continue
            elif k=='id':
                tower_obj['_id'] = ObjectId(id)
                
            elif k=='same_tower':
                continue
            elif k=='tower_name':
                tower_obj['properties']['name'] = tower_name
                tower_obj['properties']['py'] = ''
                try:
                    tower_obj['properties']['py'] = piny.hanzi2pinyin_first_letter(tower_name.replace('#','').replace(',','').replace('II',u'额').replace('I',u'一'))
                except:
                    pass
            elif k=='geo_x' or k=='geo_y' or k=='geo_z':
                continue
            elif k in ['model_code', 'model_code_height']:
                if not tower_obj['properties'].has_key('model'):
                    tower_obj['properties']['model'] = {}
                tower_obj['properties']['model'][k] = tower[k]
                if not tower_obj['properties']['model'].has_key('contact_points'):
                    tower_obj['properties']['model']['contact_points'] = []
                if k == 'model_code_height':
                    pts = odbc_get_records('TABLE_CONTACT_POINT', "model_code='%s'" % tower[k], area)
                    if len(pts)>0:
                        for pt in pts:
                            o = {}
                            o['side'] = 0
                            if pt['side'] == u'正':
                                o['side'] = 1
                            o['position'] = pt['position']
                            #o['contact_index'] = pt['contact_index']
                            #if o['side'] == 0:
                            if pt['position'] in [u'地左',u'地单']:
                                o['contact_index'] = 0
                            if pt['position'] == u'地右':
                                o['contact_index'] = 1
                            if pt['position'] in [ u'单回',u'左侧']:
                                if pt['contact_index']==1:
                                    o['contact_index'] = 2
                                if pt['contact_index']==2:
                                    o['contact_index'] = 3
                                if pt['contact_index']==3:
                                    o['contact_index'] = 4
                            if pt['position'] in [ u'右侧']:
                                if pt['contact_index']==1:
                                    o['contact_index'] = 5
                                if pt['contact_index']==2:
                                    o['contact_index'] = 6
                                if pt['contact_index']==3:
                                    o['contact_index'] = 7
                            
                            o['x'] = pt['offset_x']
                            o['y'] = pt['offset_z']
                            o['z'] = pt['offset_y']
                            o['split_count'] = pt['split_count']
                            tower_obj['properties']['model']['contact_points'].append(o)
            else:
                tower_obj['properties'][k] = tower[k]
                
        #if not tower_obj['properties'].has_key('prev_ids'):
            #tower_obj['properties']['prev_ids'] = []
        #if not tower_obj['properties'].has_key('next_ids'):
            #tower_obj['properties']['next_ids'] = []
        #if prev:
            #if mapping.has_key(prev['id']):
                #tower_obj['properties']['prev_ids'].append(mapping[prev['id']])
            
        #if nextt:
            #if mapping.has_key(nextt['id']):
                #tower_obj['properties']['next_ids'].append(mapping[nextt['id']])
            
        if not tower_obj['properties'].has_key('metals'):
            tower_obj['properties']['metals'] = []
        attachs = odbc_get_records('TABLE_TOWER_METALS', "tower_id='%s'" % tower['id'], area)
        if len(attachs)>0:
            for attach in attachs:
                o = {}
                o['assembly_graph'] = ''
                o['manufacturer'] = ''
                o['model'] = ''
                o['type'] = u'未知'
                if attach['attach_type'] == u'防振锤':
                    o['type'] = u'防振锤'
                    o['side'] = ''
                    if attach['attach_subtype']:
                        o['side'] = attach['attach_subtype']
                    o['count'] = attach['strand']
                    o['distance'] = attach['value1']
                elif attach['attach_type'] == u'绝缘子串':
                    o['type'] = u'绝缘子串'
                    o['insulator_type'] = ''
                    if attach['attach_subtype']:
                        o['insulator_type'] = attach['attach_subtype']
                    o['model'] = ''
                    if attach['specification']:
                        o['model'] = attach['specification']
                    o['material'] = ''
                    if attach['material']:
                        o['material'] = attach['material']
                    o['strand'] = attach['strand']
                    o['slice'] = attach['slice']
                elif attach['attach_type'] == u'接地装置':
                    o['type'] = u'接地装置'
                    o['model'] = ''
                    if attach['specification']:
                        o['model'] = attach['specification']
                    o['count'] = attach['strand']
                    o['depth'] = attach['value1']
                elif attach['attach_type'] == u'基础':
                    o['type'] = u'铁塔'
                    o['model'] = ''
                    o['platform_model'] = ''
                    o['anchor_model'] = ''
                    o['count'] = attach['strand']
                    o['depth'] = attach['value1']
                tower_obj['properties']['metals'].append(o)
        attachs = odbc_get_records('TABLE_TOWER_ATTACH', "tower_id='%s'" % tower['id'], area)
        if len(attachs)>0:
            for attach in attachs:
                o = {}
                o['assembly_graph'] = ''
                o['manufacturer'] = ''
                o['model'] = ''
                o['type'] = u'未知'
                if attach['manufacturer']:
                    o['manufacturer'] = attach['manufacturer']
                if attach['attach_name'] == u'接地装置':
                    o['type'] = u'接地装置'
                    if attach['series']:
                        o['model'] = attach['series']
                    o['count'] = attach['int_value1']
                    o['depth'] = attach['float_value1']
                elif u'计数器' in attach['attach_name'] :
                    o['type'] = u'雷电计数器'
                    if attach['series']:
                        o['model'] = attach['series']
                    o['counter'] = attach['int_value1']
                elif u'防鸟刺' in attach['attach_name'] :
                    o['type'] = u'防鸟刺'
                    if attach['series']:
                        o['model'] = attach['series']
                    o['count'] = attach['int_value1']
                elif u'在线监测装置' in attach['attach_name'] :
                    o['type'] = u'在线监测装置'
                    if attach['series']:
                        o['model'] = attach['series']
                    o['count'] = attach['int_value1']
                elif attach['attach_name'] == u'基础':
                    o['type'] = u'基础'
                    if attach['series']:
                        o['model'] = attach['series']
                    o['platform_model'] = u'铁塔'
                    o['anchor_model'] = ''
                    o['count'] = attach['int_value1']
                    o['depth'] = attach['float_value1']
                elif attach['attach_name'] == u'拉线':
                    o['type'] = u'拉线'
                    if attach['series']:
                        o['model'] = attach['series']
                    o['count'] = attach['int_value1']
                tower_obj['properties']['metals'].append(o)
            
        if not checkexist(alist, id):
            alist.append(tower_obj)
    return alist


def find_extent(data):
    ret = {'west':None, 'south':None, 'east':None, 'north':None}
    xl = []
    yl = []
    geomtype = None
    for i in data:
        if isinstance(i, dict) and  i.has_key('geometry') and i['geometry'].has_key('type'):
            geomtype = i['geometry']['type']
            if geomtype == 'Point':
                xl.append(i['geometry']['coordinates'][0])
                yl.append(i['geometry']['coordinates'][1])
    if len(xl)>0 and len(yl)>0:
        ret['west'] = min(xl)
        ret['south'] = min(yl)
        ret['east'] = max(xl)
        ret['north'] = max(yl)
    return ret

def remove_geometry2d(obj = {}):
    if obj.has_key('geometry2d'):
        del obj['geometry2d']
    return obj
    
    
    
def update_geometry2d(adict = {}, z_aware = False):
    def add_alt(coord, z_aware):
        if isinstance(coord, list) and len(coord)==2 and isinstance(coord[0], float):
            if z_aware:
                coord.append(extract_one_altitude(coord[0], coord[1]))
            else:
                coord.append(0)
        elif isinstance(coord, list) and len(coord)==3 and isinstance(coord[0], float) and coord[2]==0:
            if z_aware:
                coord[2] = extract_one_altitude(coord[0], coord[1])
            else:
                coord[2] = 0
        elif isinstance(coord, list) and isinstance(coord[0], list):
            l = []
            for i in coord:
                l.append(add_alt(i, z_aware))
            coord = l
        return coord
    def remove_alt(coord):
        if isinstance(coord, list) and isinstance(coord[0], float) and len(coord)==3:
            coord = coord[:2]
        elif isinstance(coord, list) and isinstance(coord[0], list):
            l = []
            for i in coord:
                l.append(remove_alt(i))
            coord = l
        return coord
    
    def add_pinyin(adict):
        name = None
        if adict.has_key('properties') and adict['properties'].has_key('name'):
            name = adict['properties']['name']
        if adict.has_key('properties') and adict['properties'].has_key('NAME'):
            name = adict['properties']['NAME']
            adict['properties']['name'] = name
            del adict['properties']['NAME']
        if name and len(name)>0 and adict.has_key('properties') and not adict['properties'].has_key('py'):
            try:
                piny = get_pinyin_data()
                adict['properties']['py'] = piny.hanzi2pinyin_first_letter(name.replace('#','').replace('II',u'二').replace('I',u'一'))
            except:
                pass
        return adict
        
        
    if adict.has_key('geometry'):
        coord = adict['geometry']['coordinates']
        adict['geometry']['coordinates'] = add_alt(coord, z_aware)
        if not adict.has_key('geometry2d'):
            adict['geometry2d'] = {}
            adict['geometry2d']['type'] = adict['geometry']['type']
        adict['geometry2d']['coordinates'] = remove_alt(coord)
            
        adict = add_pinyin(adict)
    return adict
    
    
    
def mongo_action(dbname, collection_name, action, data, conditions={}, clienttype='webgis'):
    global gClientMongo, gConfig, gFeatureslist
    ret = []
    try:
        piny = get_pinyin_data()
        mongo_init_client(clienttype)
        if dbname in gClientMongo[clienttype].database_names():      
            db = gClientMongo[clienttype][dbname]
            if action.lower() == 'login':
                if collection_name in db.collection_names(): 
                    if conditions.has_key('username') and conditions.has_key('password'):
                        ret = mongo_find(dbname, collection_name, conditions, )
                    else:
                        ret = []
                else:
                    ret = []
            elif action.lower() == 'remove':
                if collection_name in db.collection_names() :
                    if conditions.has_key('_id'):
                        if isinstance( conditions['_id'], list) or isinstance( conditions['_id'], tuple):
                            ids = []
                            for i in conditions['_id']:
                                if i:
                                    ids.append(str(i))
                            wr = mongo_remove(dbname, collection_name, {'_id':ids})
                            if wr:
                                ret.append(remove_mongo_id(wr))
                        elif isinstance(conditions['_id'], str) or isinstance(conditions['_id'], unicode):
                            def check_network_has_node(network_id):
                                result = False
                                network = mongo_find_one(dbname, 'network', {'_id':network_id}, )
                                if network:
                                    if len(network['properties']['nodes']) > 0:
                                        result = True
                                return result
                            
                            remove_check = ''
                            one = mongo_find_one(dbname, collection_name, {'_id':str(conditions['_id'])}, )
                            if collection_name == 'features':
                                if one and one.has_key('properties') and one['properties'].has_key('webgis_type') and one['properties']['webgis_type'] in ['point_dn','point_tower']:
                                    def check_has_edge(node_id):
                                        edgelist = mongo_find(dbname, 'edges', {'$or':[{'properties.start':node_id}, {'properties.end':node_id}]}, )
                                        if len(edgelist)>0:
                                            return True
                                        else:
                                            return False
                                    if  check_has_edge(str(conditions['_id'])):
                                        remove_check = u'edge_exist'
                            if check_network_has_node(str(conditions['_id'])):
                                remove_check = u'nodes_exist'
                            if len(remove_check) == 0:
                                wr = mongo_remove(dbname, collection_name, {'_id':str(conditions['_id'])}, )
                                    
                                if one and one.has_key('properties') and one['properties'].has_key('webgis_type') :
                                    def delete_node_from_network(node_id, collectionname):
                                        networklist = mongo_find(dbname, collectionname, {}, )
                                        for network in networklist:
                                            if node_id in network['properties']['nodes']:
                                                network['properties']['nodes'].remove(node_id)
                                                mongo_action(dbname, collectionname, 'update', {'properties.nodes': network['properties']['nodes']}, {'_id':network['_id']}, )
                                    def delete_segment_by_tower(node_id):
                                        seglist = mongo_find(dbname, 'segments', {'$or':[{'start_tower':node_id}, {'end_tower':node_id}]}, )
                                        ids = []
                                        for seg in seglist:
                                            ids.append(seg['_id'])
                                        wr1 = mongo_remove(dbname, 'segments', {'_id':ids}, )
                                        return wr1
                                    def delete_segment_by_edge(node_id0, node_id1):
                                        seglist = mongo_find(dbname, 'segments', {'$or':[{'start_tower':node_id0, 'end_tower':node_id1}, {'start_tower':node_id1, 'end_tower':node_id0}]}, )
                                        ids = []
                                        for seg in seglist:
                                            ids.append(seg['_id'])
                                        wr1 = mongo_remove(dbname, 'segments', {'_id':ids}, )
                                        return wr1
                                        
                                    if one['properties']['webgis_type'] == 'point_tower':
                                        delete_node_from_network(str(conditions['_id']), 'network')
                                        wr = delete_segment_by_tower(str(conditions['_id']))
                                    if one['properties']['webgis_type'] == 'point_dn':
                                        delete_node_from_network(str(conditions['_id']), 'network')
                                    if one['properties']['webgis_type'] == 'edge_tower':
                                        wr = delete_segment_by_edge(one['properties']['start'], one['properties']['end'])
                                    
                                        
                                if wr:
                                    ret.append(remove_mongo_id(wr))
                            else:
                                ret.append({'ok':0, 'err':remove_check})
                else:
                    s = 'collection [%s] does not exist.' % collection_name
                    raise Exception(s)
            elif action.lower() == 'update':
                if data is None:
                    raise Exception('data is none, nothing to save')
                if collection_name in db.collection_names(): 
                    z_aware = True
                    ids = [] 
                    ret = []
                    conditions = add_mongo_id(conditions)
                    result = db[collection_name].update(conditions, {'$set': add_mongo_id(data)}, multi=True, upsert=False)
                    ret = mongo_find(dbname, collection_name, conditions, )
                    #print(ret)
            elif action.lower() == 'save':
                if data is None:
                    raise Exception('data is none, nothing to save')
                if collection_name in db.collection_names(): 
                    data = add_mongo_id(data)
                    z_aware = True
                    ids = [] 
                    ret = []
                    if isinstance(data, list):
                        for i in data:
                            if i.has_key('properties') and  i['properties'].has_key('webgis_type'):
                                if i['properties']['webgis_type'] == 'polygon_buffer':
                                    z_aware = False
                                i = update_geometry2d(i, z_aware)
                            _id = db[collection_name].save(i)
                            ids.append(str(_id))
                    if isinstance(data, dict):
                        if data.has_key('properties') and data['properties'].has_key('webgis_type'):
                            if data['properties']['webgis_type'] == 'polygon_buffer':
                                z_aware = False
                            data = update_geometry2d(data, z_aware)
                        if check_edge_exist(dbname, collection_name, data) :
                            ret.append({'result':u'保存失败:该节点间关联已存在'});
                        elif check_edge_ring(dbname, collection_name, data):
                            ret.append({'result':u'保存失败:存在回路'});
                        else:
                            line_names = None
                            if data.has_key('properties') and data['properties'].has_key('webgis_type') and data['properties']['webgis_type'] == 'polyline_line':
                                data['properties']['py'] = piny.hanzi2pinyin_first_letter(data['properties']['name'].replace('#','').replace('II',u'额').replace('I',u'一'))
                            if data.has_key('properties') and data['properties'].has_key('webgis_type') and data['properties']['webgis_type'] == 'point_tower':
                                if data['properties'].has_key('line_names'):
                                    line_names = data['properties']['line_names']
                                    del data['properties']['line_names']
                                if data['properties'].has_key('model') and data['properties']['model'].has_key('model_code') and data['properties']['model'].has_key('model_code_height'):
                                    findmodel = mongo_find_one(dbname, 'models', {'model_code':data['properties']['model']['model_code'], 'model_code_height':data['properties']['model']['model_code_height']})
                                    # findmodel = False
                                    # for model in models:
                                    #     if model['model_code'] == data['properties']['model']['model_code'] and model['model_code_height'] == data['properties']['model']['model_code_height']:
                                    #         findmodel = True
                                    #         break
                                    if findmodel:
                                        modeldata = {}
                                        modeldata['model_code'] = data['properties']['model']['model_code']
                                        modeldata['model_code_height'] = data['properties']['model']['model_code_height']
                                        modeldata['contact_points'] = []
                                        mongo_action(dbname, 'models','save', modeldata, )
                            _id = db[collection_name].save(data)

                            if _id is not None and line_names is not None:
                                if isinstance(line_names, ObjectId):
                                    line_names = [line_names, ]
                                mongo_update_line_towers(dbname, _id, line_names, )
                            if _id:
                                ids.append(str(_id))
                    if len(ids) > 0:
                        ret = mongo_find(dbname, collection_name, {'_id':ids}, )
                else:
                    s = 'collection [%s] does not exist.' % collection_name
                    raise Exception(s)
            elif action.lower() == 'pinyin_search':
                arr = []
                tyarr = []
                limit = 100
                if collection_name in db.collection_names():
                    arr.append(collection_name)
                if '*' in collection_name:
                    arr = db.collection_names()
                if ';' in collection_name:
                    arr = collection_name.split(';')
                if not conditions.has_key('py'):
                    arr = []
                if conditions.has_key('type'):
                    tyarr = conditions['type']
                    #tyarr = map(lambda x:str(x), data['type'])
                if conditions.has_key('limit'):
                    limit = conditions['limit']
                for i in arr:
                    if len(tyarr)>0:
                        condd = {'$or':[{'properties.py':{'$regex':'^.*' + conditions['py'] + '.*$'}}, {'properties.name':{'$regex':'^.*' + conditions['py'] + '.*$'}}], 'properties.webgis_type':tyarr}
                        if i == 'network':
                            if gConfig['webgis'].has_key('anti_bird')\
                                and gConfig['webgis']['anti_bird'].has_key('line_filter') \
                                and len(gConfig['webgis']['anti_bird']['line_filter'])>0:
                                arr = gConfig['webgis']['anti_bird']['line_filter']
                                condd['properties.name'] = {'$in': arr}
                        # print(condd)
                        ret.extend(mongo_find(dbname, i, condd, limit, ))
                for i in gFeatureslist:
                    if i in tyarr: 
                        tyarr.remove(i)   
                    if unicode(i) in tyarr: 
                        tyarr.remove(unicode(i))   
                if len(tyarr)>0:
                    #ret.extend(mongo_find(gConfig['webgis']['geofeature']['mongodb']['database'], gConfig['webgis']['geofeature']['mongodb']['collection'], {'properties.py':{'$regex':'^.*' + conditions['py'] + '.*$'}, 'properties.webgis_type':tyarr}, limit=limit, clienttype='geofeature'))
                    ret.extend(mongo_find(gConfig['webgis']['geofeature']['mongodb']['database'], gConfig['webgis']['geofeature']['mongodb']['collection'], {'$or':[{'properties.py':{'$regex':'^.*' + conditions['py'] + '.*$'}}, {'properties.name':{'$regex':'^.*' + conditions['py'] + '.*$'}}], 'properties.webgis_type':tyarr}, limit=limit, clienttype='geofeature'))
                if 'heatmap_tile' in tyarr : 
                    ret.extend(get_heatmap_tile_service_list(conditions['py']))
                if 'heatmap_heatmap' in tyarr : 
                    pass
                if conditions.has_key('py') and conditions['py'] in [u'qnq', u'驱鸟器']:
                    ret.append({'action':'anti_bird_towers'})
                #print(ret)
            elif action.lower() == 'anti_bird_towers':
                ret = mongo_find(
                    gConfig['webgis']['mongodb']['database'],
                    'features',
                    #{"properties.webgis_type":"point_tower","properties.metals.type":u"多功能驱鸟装置"},
                    {
                        "properties.webgis_type":"point_tower",
                        "properties.metals":{
                            "$elemMatch":{
                                "type":u"多功能驱鸟装置",
                            }
                        }
                    },
                    0,
                    'webgis'
                )
            elif action.lower() == 'models_list':
                p = SERVERGLTFROOT
                if not os.path.exists(p):
                    p = os.path.join(gConfig['web']['webroot'], 'gltf')
                for i in os.listdir(p):
                    if i[-5:].lower() == '.gltf':
                        ret.append(i[:-5])
            #elif action.lower() == 'check_edge_exist':
                #if conditions.has_key('id0') and conditions.has_key('id1'):
                    #ret = mongo_find(dbname, 'edges', conditions = {'$or':[{"properties.start":conditions['id0'],"properties.end":conditions['id1']}, {"properties.start":conditions['id1'],"properties.end":conditions['id0']}]})
            elif action.lower() == 'buffer':
                if isinstance(data, dict):
                    geojsonobj = data
                    if data.has_key('geometry'):
                        geojsonobj = data['geometry']
                    if not conditions.has_key('distance'):
                        raise Exception('buffer distance should be specified')
                    res = 4
                    if conditions.has_key('res'):
                        res = conditions['res']
                    ret.append(calc_buffer(geojsonobj, conditions['distance'], res))
                else:
                    raise Exception('buffer calculation need geojson object')
            elif action.lower() == 'within':
                if isinstance(data, dict):
                    geojsonobj = data
                    if data.has_key('geometry'):
                        geojsonobj = data['geometry']
                    if not conditions.has_key('webgis_type'):
                        raise Exception('webgis_type should be specified in within calculation')
                    intersect = False
                    if conditions.has_key('intersect') and conditions['intersect']:
                        intersect = True
                    limit = 500
                    if conditions.has_key('limit'):
                        limit = conditions['limit']
                    ret.extend(mongo_geowithin(dbname,  geojsonobj, conditions['webgis_type'], intersect, limit))
                else:
                    raise Exception('within calculation need geojson object')
            elif action.lower() == 'getsysrole':
                ret = []
                if conditions.has_key('userid'):
                    rolelist = mongo_find(dbname, 'sysrole')
                    for role in rolelist:
                        if role['name'] == 'admin':
                            continue
                        if conditions['userid'] in role['users']:
                            for perm in role['permission']:
                                if not perm in ret:
                                    ret.append(perm)
            elif action.lower() == 'loadtoweredge':
                ret = []
                if conditions.has_key('lineid'):
                    linelist = mongo_find(dbname, 'network', {'_id':conditions['lineid']})
                    if len(linelist) > 0:
                        towers = linelist[0]['properties']['nodes']
                        # print('start:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        edges = mongo_find(dbname, 'edges', {'properties.webgis_type':'edge_tower',
                                                             '$or':[{'properties.start':{'$in':towers}},
                                                                    {'properties.end':{'$in':towers}},
                                                                    ]
                                                             })
                        ret.extend(edges)
                    # print('end:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            elif action.lower() == 'markdown_name_list':
                ret = []
                cond = {}
                if conditions.has_key('name'):
                    cond = {'name':{'$regex':'^.*' + conditions['name'] + '.*$'}}
                doclist = mongo_find(dbname, collection_name, cond, 0, 'markdown')
                for i in doclist:
                    del i['content']
                    ret.append(i)
            elif action.lower() == 'markdown_document_content':
                ret = []
                #if conditions.has_key('name'):
                doc = mongo_find_one(dbname, collection_name, conditions, 'markdown')
                if doc:
                    ret.append(doc)
            elif action.lower() == 'markdown_document_save':
                ret = []
                if data is None:
                    raise Exception('data is none, nothing to save')
                if collection_name in db.collection_names(): 
                    data = add_mongo_id(data)
                    if isinstance(data, dict):
                        _id = db[collection_name].save(data)
                        ret.append({'_id':str(_id)})
            elif action.lower() == 'markdown_document_remove':
                ret = []
                if conditions.has_key('_id'):
                    wr = mongo_remove(dbname, collection_name, {'_id':str(conditions['_id'])}, 'markdown')
                    ret.append(remove_mongo_id(wr))
            #else:
                #s = 'collection [%s] does not exist.' % collection_name
                #raise Exception(s)
        else:
            s = 'database [%s] does not exist.' % dbname
            raise Exception(s)
    except:
        traceback.print_exc()
        #err = sys.exc_info()[1].message
        #print(err)
        #ret = []
        raise
    return ret

def get_heatmap_tile_service_list(name):
    global gConfig
    ret = []
    h = gConfig['webgis']['heatmap']['arcgis']['protocal'] + '://' + gConfig['webgis']['heatmap']['arcgis']['host'] + ':' + gConfig['webgis']['heatmap']['arcgis']['port'] + '/'
    href = h +  gConfig['webgis']['heatmap']['arcgis']['catalog']
    connection_timeout, network_timeout = float(gConfig['webgis']['heatmap']['arcgis']['www_connection_timeout']), float(gConfig['webgis']['heatmap']['arcgis']['www_network_timeout'])
    url = URL(href)    
    http = HTTPClient.from_url(url, concurrency=1, connection_timeout=connection_timeout, network_timeout=network_timeout, )
    response = None
    try:
        g = gevent.spawn(http.get, url.request_uri)
        g.join()
        response = g.value
        if response and response.status_code == 200:
            d = pq(dec(response.read()))
            l = d('li > a')
            for a in l:
                if name in a.text:
                    obj = {}
                    obj['name'] = a.text
                    obj['type'] = 'heatmap_tile'
                    obj['url'] = h[:-1] + a.attrib['href']
                    ret.append(obj)
    except:
        pass
    return ret
    
    
    
    

def mongo_update_line_towers(dbname, id, line_names=[], ):
    lines = mongo_find(dbname, 'network', {'properties.webgis_type':'polyline_line'},)
    line_names_list = [str(i) for i in line_names]
    l = []
    for i in lines:
        modified = False
        if not i.has_key('properties'):
            i['properties'] = {}
        if not i['properties'].has_key('nodes'):
            i['properties']['nodes'] = []
        if i['_id'] in line_names_list and not str(id) in i['properties']['nodes']:
            i['properties']['nodes'].append(str(id))
            modified = True
        if not i['_id'] in line_names_list and id in i['properties']['nodes']:
            i['properties']['nodes'].remove(str(id))
            modified = True
        if modified:
            mongo_action(dbname, 'network','save', i, )
    
    
def check_edge_exist(db_name, collection_name, data):
    if collection_name == 'edges':
        ret = mongo_find(db_name, collection_name, conditions = {'$or':[{"properties.start":data['properties']['start'],"properties.end":data['properties']['end']}, {"properties.start":data['properties']['end'],"properties.end":data['properties']['start']}]})
        if len(ret)>0:
            return True
    return False
    
def check_edge_ring(db_name, collection_name, data):
    def get_next(node_id):
        ret = []
        if not isinstance(node_id, list):
            node_id = [add_mongo_id(node_id),]
        alist = mongo_find(db_name, collection_name, {'properties.start':{'$in':node_id}})
        ret = [add_mongo_id(i['properties']['end']) for i in alist]
        return ret

    iteration_step = 0
    if collection_name == 'edges':
        nl = get_next(data['properties']['end'])
        while len(nl)>0:
            if add_mongo_id(data['properties']['start']) in nl:
                print('found iteration:%d' % iteration_step)
                return True
            nl = get_next(nl)
            iteration_step += 1
        print('not found iteration:%d' % iteration_step)
    return False

def calc_buffer_ogr(geojsonobj, dist):
    obj = geojsonobj
    if obj.has_key('geometry'):
        obj = obj['geometry']
    geojson = enc(json.dumps(obj, ensure_ascii=False, indent=4))
    
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)
    target = osr.SpatialReference()
    target.ImportFromEPSG(3857) 
    transform = osr.CoordinateTransformation(source, target)    
    transform1 = osr.CoordinateTransformation(target, source)    
    pts = ogr.CreateGeometryFromJson(geojson)
    pts.Transform(transform)
    poly = pts.Buffer(dist)
    poly.Transform(transform1)
    #print("buffered by %d is \n%s" % ( dist, poly.ExportToJson()) )
    g = json.loads(poly.ExportToJson())
    return g

def calc_buffer(geojsonobj, dist, res=4):
    def transform(inp, outp, coordinates):
        if isinstance(coordinates, list) or isinstance(coordinates, tuple):
            if isinstance(coordinates[0], float):
                x2,y2 = pyproj.transform(inp, outp, coordinates[0], coordinates[1])
                return [x2, y2]
            elif isinstance(coordinates[0], list) or isinstance(coordinates[0], tuple):
                l = []
                for i in coordinates:
                    l.append(transform(inp, outp, i))
                return l
        return coordinates
        
    geometry = geojsonobj
    if geojsonobj.has_key('geometry'):
        geometry = geojsonobj['geometry']
        
    inProj = pyproj.Proj(init='epsg:4326')
    outProj = pyproj.Proj(init='epsg:3857')
    geometry['coordinates'] = transform(inProj,outProj,  geometry['coordinates'])        
    shp = shapely.geometry.asShape(geometry)
    b = shp.buffer(dist, res)
    #print(b)
    g1 = shapely.wkt.loads(b.wkt)
    g = geojson.Feature(geometry=g1, properties={})
    g['geometry']['coordinates'] = transform(outProj, inProj,  g['geometry']['coordinates'])
    return g['geometry']
    
def extract_one_altitude(lng, lat):
    global gConfig
    ret = None
    # exe_path = os.path.join(module_path(), 'gdal-bin', 'gdallocationinfo.exe')
    exe_path = gConfig['webgis']['terrain']['gdal-bin']['gdallocationinfo']
    dem_path = gConfig['webgis']['terrain']['dem_file']
    out = subprocess.check_output([exe_path, '-wgs84', "%s" % dem_path, "%f" % lng, "%f" % lat])
    t = 'Value:'
    if t in out:
        idx = out.index(t) + len(t)
        ret = float(out[idx:].strip())
    else:
        raise Exception('extract_altitude_from_dem:out of range!')
    return ret

def extract_many_altitudes(lnglatlist):
    ret = []
    for i in lnglatlist:
        if isinstance(i, dict) and i.has_key('lng') and i.has_key('lat'):
            ret.append({'lng':i['lng'], 'lat':i['lat'], 'alt':extract_one_altitude(i['lng'], i['lat'])})
    return ret
    

def mongo_remove(dbname, collection_name, conditions={}, clienttype='webgis'):
    global gClientMongo, gConfig
    ret = None
    try:
        mongo_init_client(clienttype)
        if dbname in gClientMongo[clienttype].database_names():      
            db = gClientMongo[clienttype][dbname]
            conditions = add_mongo_id(conditions)
            conds = build_mongo_conditions(conditions)
            if collection_name in db.collection_names():
                writeResult = db[collection_name].remove(conds)
                ret = writeResult
            else:
                s = 'mongo_remove:collection [%s] does not exist.' % collection_name
                raise Exception(s)
        else:
            s = 'mongo_remove:database [%s] does not exist.' % dbname
            raise Exception(s)
            
    except:
        traceback.print_exc()
        raise
    return ret
    
def mongo_geowithin(dbname, geojsonobj, webgis_type_list, intersect=False, limit=500):
    global gConfig, gFeatureslist
    ret = []
    #ret.extend( mongo_find(dbname, 'features', {'properties.webgis_type':webgis_type_list, 'geometry2d':{'$geoWithin':{'$geometry':geojsonobj['geometry']}}}))
    
    l_point, l_polyline, l_polygon = [], [], []
    for i in webgis_type_list:
        if i in gFeatureslist:
            if 'point_' in i:
                l_point.append(i)
            if 'polyline_' in i and intersect:
                l_polyline.append(i)
            if 'polygon_' in i and intersect:
                l_polygon.append(i)
    if len(l_point)>0:
        ret.extend( mongo_find(dbname, 'features', {'properties.webgis_type':l_point, 'geometry2d':{'$geoWithin':{'$geometry':geojsonobj}}}, limit))
    if len(l_polyline)>0:
        ret.extend( mongo_find(dbname, 'features', {'properties.webgis_type':l_polyline, 'geometry2d':{'$geoIntersects':{'$geometry':geojsonobj}}}, limit))
    if len(l_polygon)>0:
        ret.extend( mongo_find(dbname, 'features', {'properties.webgis_type':l_polygon, 'geometry2d':{'$geoIntersects':{'$geometry':geojsonobj}}}, limit))
    
    l_point, l_polyline, l_polygon = [], [], []
    for i in webgis_type_list:
        if not i in gFeatureslist:
            if 'point_' in i:
                l_point.append(i)
            if 'polyline_' in i and intersect:
                l_polyline.append(i)
            if 'polygon_' in i and intersect:
                l_polygon.append(i)
    if len(l_point)>0:
        ret.extend( mongo_find(gConfig['webgis']['geofeature']['mongodb']['database'], 'features', {'properties.webgis_type':l_point, 'geometry2d':{'$geoWithin':{'$geometry':geojsonobj}}}, limit, clienttype='geofeature'))
    if len(l_polyline)>0:
        ret.extend( mongo_find(gConfig['webgis']['geofeature']['mongodb']['database'], 'features', {'properties.webgis_type':l_polyline, 'geometry2d':{'$geoIntersects':{'$geometry':geojsonobj}}}, limit, clienttype='geofeature'))
    if len(l_polygon)>0:
        ret.extend( mongo_find(gConfig['webgis']['geofeature']['mongodb']['database'], 'features', {'properties.webgis_type':l_polygon, 'geometry2d':{'$geoIntersects':{'$geometry':geojsonobj}}}, limit, clienttype='geofeature'))
        
    return ret

def mongo_find(dbname, collection_name, conditions={}, limit=0, clienttype='webgis'):
    global gClientMongo, gConfig
    ret = []
    try:
        mongo_init_client(clienttype)
        if dbname in gClientMongo[clienttype].database_names():      
            db = gClientMongo[clienttype][dbname]
            conditions = add_mongo_id(conditions)
            conds = build_mongo_conditions(conditions)
            if collection_name in db.collection_names():
                if collection_name == 'network':
                    if gConfig['webgis'].has_key('anti_bird')\
                        and gConfig['webgis']['anti_bird'].has_key('line_filter') \
                        and len(gConfig['webgis']['anti_bird']['line_filter'])>0:
                        arr = gConfig['webgis']['anti_bird']['line_filter']
                        conds['properties.name'] = {'$in': arr}
                ret = list(db[collection_name].find(conds).limit(limit))
                # for i in cur:
                #     ret.append(remove_mongo_id(i))
                ret = remove_mongo_id(ret)
            elif collection_name == 'mongo_get_towers_by_line_name':
                conds['properties.webgis_type'] = 'polyline_line'
                lines = list(db['network'].find(conds))
                towerids = []
                for line in lines:
                    for t in line['properties']['nodes']:
                        #print(str(t))
                        towerids.append(t)
                towers = list(db['features'].find({'_id':{'$in':towerids}}).limit(limit))
                # for i in towers:
                #     ret.append(remove_mongo_id(i))
                ret = remove_mongo_id(towers)
            elif collection_name == 'get_line_geojson':
                line = remove_mongo_id(db['network'].find_one(conds))
                obj = get_line_geojson(dbname, line)
                if obj:
                    ret.append(obj)
            else:
                s = 'collection [%s] does not exist.' % collection_name
                raise Exception(s)
        else:
            s = 'database [%s] does not exist.' % dbname
            raise Exception(s)
    except:
        traceback.print_exc()
        #err = sys.exc_info()[1].message
        ret = []
    return ret



def mongo_find_one(dbname, collection_name, conditions, clienttype='webgis'):
    global gClientMongo
    ret = None
    try:
        mongo_init_client(clienttype)
        db = gClientMongo[clienttype][dbname]
        conditions = add_mongo_id(conditions)
        conds = build_mongo_conditions(conditions)
        ret = db[collection_name].find_one(conds)
        ret = remove_mongo_id(ret)
    except:
        traceback.print_exc()
        #err = sys.exc_info()[1].message
        #print(err)
        ret = None
    return ret

def test_find_by_string_id():
    #ret = mongo_find('kmgd', 'segments', {'_id':[ObjectId('535a1560ca49c804e457446a'), ObjectId('535a1560ca49c804e457446b')]})
    ret = mongo_find('kmgd', 'network', )
    print(map(lambda x:x['properties']['production_date'], ret))
    print(len(ret))
    
    

def build_mongo_conditions(obj):
    if isinstance(obj, list):
        obj = {'$in': obj}
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            if k in ['geometry2d','$geoWithin', '$geoIntersects', '$geometry', '$or', '$and', '$not', '$nor', '$nin', '$in', '$ne']:
                pass
            else:
                obj[k] = build_mongo_conditions(obj[k])
    return obj
    
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
        obj = remove_geometry2d(obj)
    elif isinstance(obj, list):
        for i in obj:
            obj[obj.index(i)] = remove_mongo_id(i)
    return obj




def test_mongo_import_segments(db_name, area):
    global gClientMongo
    lines = odbc_get_records('TABLE_LINE', '1=1', area)
    l = []
    mapping = get_tower_id_mapping(db_name)
    towers_refer_mapping = get_tower_refer_mapping(db_name)
    for line in lines:
        segs = gen_mongo_segments_by_line_id(line['id'], area,  mapping, towers_refer_mapping)
        l.extend(segs)
    
    try:
        mongo_init_client()
        db = gClientMongo['webgis'][db_name]
        if 'segments' in db.collection_names(False):
            db.drop_collection('segments')
        collection = db.create_collection('segments')
        for i in l:
            collection.save(i)
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)

def gen_mongo_segments_by_line_id(line_id, area, mapping, refer_mapping):
    def get_refer_toweruid_by_refer_id(mapping, id):
        ret = None
        for k in mapping.keys():
            if mapping[k] == id:
                ret = str(k)
                break
        return ret
    def gen_obj(mapping, startuid, enduid):
        obj = {}
        if startuid is None:
            return obj
        if enduid is None:
            return obj
        segs = odbc_get_records('VIEW_CONTACT_SEGMENT', "start_tower_id='%s' AND end_tower_id='%s'" % (startuid,  enduid), area)
        for seg in segs:
            #if mapping.has_key(seg['start_tower_id']) and mapping.has_key(seg['end_tower_id']):
            side0 = 1
            side1 = 0
            if not obj.has_key('start_tower'):
                obj['start_tower'] = ObjectId(mapping[seg['start_tower_id']])
            if not obj.has_key('end_tower'):
                obj['end_tower'] = ObjectId(mapping[seg['end_tower_id']])
            if not obj.has_key('start_model_code'):
                obj['start_model_code'] = seg['start_model_code']
            if not obj.has_key('end_model_code'):
                obj['end_model_code'] = seg['end_model_code']
            if not obj.has_key('start_side'):
                obj['start_side'] = side0
            if not obj.has_key('end_side'):
                obj['end_side'] = side1
            if not obj.has_key('splitting'):
                obj['splitting'] = seg['splitting']
            if not obj.has_key('conductor_count'):
                obj['conductor_count'] = seg['conductor_count']
            if not obj.has_key('crosspoint_count'):
                obj['crosspoint_count'] = seg['crosspoint_count']
            if not obj.has_key('seperator_bar'):
                obj['seperator_bar'] = seg['seperator_bar']
            if not obj.has_key('connector_count'):
                obj['connector_count'] = seg['connector_count']
            if not obj.has_key('connector_type'):
                obj['connector_type'] = seg['connector_type']
            if not obj.has_key('contact_points'):
                obj['contact_points'] = []
            if not obj.has_key('t0'):
                obj['t0'] = 0.9
            if not obj.has_key('w'):
                obj['w'] = 0.001
            o = {}
            o['phase'] = seg['phase']
            #o['start_side'] = seg['start_side']
            #o['end_side'] = seg['end_side']
            if seg['start_position'] in [u'地左',u'地单']:
                o['start'] = 0
            if seg['start_position'] == u'地右':
                o['start'] = 1
            if seg['start_position'] in [ u'单回',u'左侧']:
                if seg['start_contact_index']==1:
                    o['start'] = 2
                if seg['start_contact_index']==2:
                    o['start'] = 3
                if seg['start_contact_index']==3:
                    o['start'] = 4
            if seg['start_position'] in [ u'右侧']:
                if seg['start_contact_index']==1:
                    o['start'] = 5
                if seg['start_contact_index']==2:
                    o['start'] = 6
                if seg['start_contact_index']==3:
                    o['start'] = 7
            if seg['end_position'] in [u'地左',u'地单']:
                o['end'] = 0
            if seg['end_position'] == u'地右':
                o['end'] = 1
            if seg['end_position'] in [ u'单回',u'左侧']:
                if seg['end_contact_index']==1:
                    o['end'] = 2
                if seg['end_contact_index']==2:
                    o['end'] = 3
                if seg['end_contact_index']==3:
                    o['end'] = 4
            if seg['end_position'] in [ u'右侧']:
                if seg['end_contact_index']==1:
                    o['end'] = 5
                if seg['end_contact_index']==2:
                    o['end'] = 6
                if seg['end_contact_index']==3:
                    o['end'] = 7
            obj['contact_points'].append(o)
        return obj
    
    ret = []
    towers_sort = odbc_get_sorted_tower_by_line(line_id, area)
    validlgtlat = None, None
    prev, tower, nextt = None, None, None
    for i in range(len(towers_sort)):
        if i == 0:
            if len(towers_sort)==1:
                prev, tower, nextt = None, towers_sort[i], None
            else:    
                prev, tower, nextt = None, towers_sort[i], towers_sort[i + 1]
        elif i == len(towers_sort) - 1:
            prev, tower, nextt = towers_sort[i - 1], towers_sort[i], None
        else:    
            prev, tower, nextt = towers_sort[i - 1], towers_sort[i], towers_sort[i + 1]
        if tower and nextt:
            obj = {}
            startuid, enduid = tower['id'], nextt['id']
            if mapping.has_key(startuid) and mapping.has_key(enduid):
                obj = gen_obj(mapping, startuid, enduid)
                id0, id1 = mapping[startuid], mapping[enduid]
                startuidnew, enduidnew = startuid, enduid
                if refer_mapping.has_key(id0):
                    id0 = refer_mapping[id0]
                    startuidnew = get_refer_toweruid_by_refer_id(mapping, id0)
                if refer_mapping.has_key(id1):
                    id1 = refer_mapping[id1]
                    enduidnew = get_refer_toweruid_by_refer_id(mapping, id1)
                    
                if len(obj.keys())>0:
                    obj['start_tower'] = ObjectId(id0)
                    obj['end_tower'] = ObjectId(id1)
                    if startuidnew != startuid and enduidnew == enduid:
                        obj1 = gen_obj(mapping, startuidnew, enduid)
                        if len(obj1.keys())>0:
                            obj['contact_points'].extend(obj1['contact_points'])
                    if startuidnew == startuid and enduidnew != enduid:
                        obj1 = gen_obj(mapping, startuid, enduidnew)
                        if len(obj1.keys())>0:
                            obj['contact_points'].extend(obj1['contact_points'])
                    if startuidnew != startuid and enduidnew != enduid:
                        obj1 = gen_obj(mapping, startuidnew, enduidnew)
                        if len(obj1.keys())>0:
                            obj['contact_points'].extend(obj1['contact_points'])
                    l = []
                    for i in obj['contact_points']:
                        if not i in l:
                            l.append(i)
                    obj['contact_points'] = l
            if len(obj.keys())>0:
                ret.append(obj)
    return ret           
            

def get_same_tower_mapping(db_name, mapping, area):
    def get_line_id(_id, amap={}):
        ret = None
        if amap.has_key(_id):
            ret = amap[_id]
        return ret
    def get_tower_mongo_id(uid, amap={}):
        ret = None
        if amap.has_key(uid):
            ret = amap[uid]
        return ret
    towers_refer = odbc_get_records('TABLE_TOWER', "same_tower != '00000000-0000-0000-0000-000000000000'" , area)
    ret = []
    #print(mapping)
    for i in towers_refer:
        _id = get_tower_mongo_id(i['id'], mapping)
        refer = get_tower_mongo_id(i['same_tower'], mapping)
        ret.append({'id':ObjectId(_id), 'refer': ObjectId(refer)})
    return ret


def mongo_import_same_tower_mapping(db_name, area):
    global gClientMongo
    mapping = get_tower_id_mapping(db_name)
    same_tower_mapping = get_same_tower_mapping(db_name, mapping, area)
    try:
        mongo_init_client()
        db = gClientMongo['webgis'][db_name]
        if 'towers_refer' in db.collection_names(False):
            db.drop_collection('towers_refer')
        collection = db.create_collection('towers_refer')
        for i in same_tower_mapping:
            collection.save(i)
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
    
def get_tower_refer_mapping(db_name):
    mapping = {}
    refer_mapping = mongo_find(db_name, 'towers_refer')
    for i in refer_mapping:
        mapping[i['id']] = i['refer']
    return mapping
    

def test_mongo_import_towers(db_name, area):
    global gClientMongo
    piny = get_pinyin_data()
    lines = odbc_get_records('TABLE_LINE', '1=1', area)
    l = []
    mapping = get_tower_id_mapping(db_name)
    #print(mapping)
    ids = []
    for k in mapping.keys():
        ids.append(mapping[k])
    towers_refer_mapping = get_tower_refer_mapping(db_name)
    
    for line in lines:
        l = gen_mongo_geojson_by_line_id(l, line['id'], area, piny, mapping, towers_refer_mapping)
    #s= ''
    #for i in l:
        #s += '%s:%s\n' % (str(i['_id']), i['properties']['tower_name'])
    #with open(ur'd:\aaa.txt','w') as f:
        #f.write(enc(s))
    try:
        mongo_init_client()
        db = gClientMongo['webgis'][db_name]
        if not 'features' in db.collection_names(False):
            collection = db.create_collection('features')
        else:
            collection = db['features']
        mongo_remove(db_name, 'features', {'_id':ids})
        for i in l:
            collection.save(i)
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
    
def test_mongo_import_models(db_name, area):
    global gClientMongo
    l = []
    ll = []
    li = mongo_find(db_name, 'features')
    for i in li:
        m = i['properties']['model']
        if m and len(m.keys())>0:
            if not m['model_code_height'] in l:
                l.append(m['model_code_height'])
                ll.append(m)
    host, port = 'localhost', 27017
    try:
        mongo_init_client()
        db = gClientMongo['webgis'][db_name]
        if 'models' in db.collection_names(False):
            db.drop_collection('models')
        collection = db.create_collection('models')
        for i in ll:
            collection.save(i)
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)

def create_id_mapping(db_name, area):
    global gClientMongo
    try:
        mongo_init_client()
        db = gClientMongo['webgis'][db_name]
        if 'tower_ids_mapping' in db.collection_names(False):
            print('tower_ids_mapping exist in %s' % db_name)
        else:
            collection = db.create_collection('tower_ids_mapping')
            l = odbc_get_records('TABLE_TOWER', '1=1', area)
            for i in l:
                collection.save({'uuid':i['id'], 'id':ObjectId()})
            print('tower_ids_mapping created, total %d' % len(l))
            
        if 'line_ids_mapping' in db.collection_names(False):
            print('line_ids_mapping exist in %s' % db_name)
        else:
            collection = db.create_collection('line_ids_mapping')
            l = odbc_get_records('TABLE_LINE', '1=1', area)
            for i in l:
                collection.save({'uuid':i['id'], 'id':ObjectId()})
            print('line_ids_mapping created, total %d' % len(l))
            
        if 'model_ids_mapping' in db.collection_names(False):
            print('model_ids_mapping exist in %s' % db_name)
        else:
            collection = db.create_collection('model_ids_mapping')
            l = odbc_get_records('TABLE_TOWER_MODEL', '1=1', area)
            for i in l:
                collection.save({'model_code_height':i['model_code'], 'id':ObjectId()})
            print('model_ids_mapping created, total %d' % len(l))
        
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
    
    
    
    
    
def test_build_tower_odbc_mongo_id_mapping(db_name):
    global gClientMongo
    host, port = 'localhost', 27017
    try:
        mongo_init_client()
        db = gClientMongo['webgis'][db_name]
        if 'tower_ids_mapping' in db.collection_names(False):
            db.drop_collection('tower_ids_mapping')
        collection = db.create_collection('tower_ids_mapping')
        l = mongo_find(db_name, 'features')
        for i in l:
            collection.save({'uuid':i['properties']['id'], 'id':i['_id']})
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
     
def test_build_line_odbc_mongo_id_mapping(db_name):
    global gClientMongo
    host, port = 'localhost', 27017
    try:
        mongo_init_client()
        db = gClientMongo['webgis'][db_name]
        if 'line_ids_mapping' in db.collection_names(False):
            db.drop_collection('line_ids_mapping')
        collection = db.create_collection('line_ids_mapping')
        l = mongo_find(db_name, 'network')
        for i in l:
            collection.save({'uuid':i['id'], 'id':i['_id']})
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
        
def test_build_model_odbc_mongo_id_mapping(db_name):
    global gClientMongo
    host, port = 'localhost', 27017
    try:
        mongo_init_client()
        db = gClientMongo['webgis'][db_name]
        if 'model_ids_mapping' in db.collection_names(False):
            db.drop_collection('model_ids_mapping')
        collection = db.create_collection('model_ids_mapping')
        l = mongo_find(db_name, 'models')
        for i in l:
            if i['model_code_height'] and len(i['model_code_height'])>0:
                collection.save({'model_code_height':i['model_code_height'], 'id':i['_id']})
            
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
    
def get_tower_id_mapping(db_name):
    mapping = {}
    tower_ids_mapping = mongo_find(db_name, 'tower_ids_mapping')
    for i in tower_ids_mapping:
        mapping[i['uuid']] = i['id']
    return mapping
def get_line_id_mapping(db_name):
    mapping = {}
    line_ids_mapping = mongo_find(db_name, 'line_ids_mapping')
    for i in line_ids_mapping:
        mapping[i['uuid']] = i['id']
    return mapping
    
    
def test_mongo_import_line(db_name, area):
    global gClientMongo
    piny = get_pinyin_data()
    try:
        mongo_init_client()
        db = gClientMongo['webgis'][db_name]
        if 'network' in db.collection_names(False):
            db.drop_collection('network')
        collection = db.create_collection('network')
        #collection = db['network']
        #collection_edges = None
        #if not 'edges' in db.collection_names(False):
            #collection_edges = db.create_collection('edges')
        #else:
            #collection_edges = db['edges']
            #mongo_remove(db_name, 'edges', conditions={'properties.webgis_type':'edge_tower'})
        line_mapping = get_line_id_mapping(db_name)
        tower_mapping = get_tower_id_mapping(db_name)
        towers_refer_mapping = get_tower_refer_mapping(db_name)
        odbc_lines = odbc_get_records('TABLE_LINE', '1=1', area)
        for line in odbc_lines:
            #if not line['id'] == 'BAE4121F-6961-4B93-9819-AC2D00E92D9A':
                #continue
            lineobj = {}
            if line_mapping.has_key(line['id']):
                lineobj['_id'] = line_mapping[line['id']]
                lineobj['properties'] = {}
                towers_sort = odbc_get_sorted_tower_by_line(line['id'], area)
                del line['box_north']
                del line['box_south']
                del line['box_east']
                del line['box_west']
                del line['id']
                lineobj['properties']['nodes'] = []
                towers_pair_list = []
                for i in towers_sort:
                    if tower_mapping.has_key(i['id']):
                        id = tower_mapping[i['id']]
                        if towers_refer_mapping.has_key(id):
                            id = towers_refer_mapping[id]
                        if not id in lineobj['properties']['nodes']:
                            lineobj['properties']['nodes'].append(id)
                    
                    
                prev, tower, nextt = None, None, None
                for i in range(len(towers_sort)):
                    if i == 0:
                        if len(towers_sort)==1:
                            prev, tower, nextt = None, towers_sort[i], None
                        else:    
                            prev, tower, nextt = None, towers_sort[i], towers_sort[i + 1]
                    elif i == len(towers_sort) - 1:
                        prev, tower, nextt = towers_sort[i - 1], towers_sort[i], None
                        if tower_mapping.has_key(prev['id']) and tower_mapping.has_key(tower['id']):
                            id0, id1 = tower_mapping[prev['id']], tower_mapping[tower['id']]
                            if towers_refer_mapping.has_key(id0):
                                id0 = towers_refer_mapping[id0]
                            if towers_refer_mapping.has_key(id1):
                                id1 = towers_refer_mapping[id1]
                            towers_pair_list.append({"properties":{"start":id0, "end":id1, "webgis_type":"edge_tower"}})
                    else:    
                        prev, tower, nextt = towers_sort[i - 1], towers_sort[i], towers_sort[i + 1]
                        if tower_mapping.has_key(prev['id']) and tower_mapping.has_key(tower['id']):
                            id0, id1 = tower_mapping[prev['id']], tower_mapping[tower['id']]
                            if towers_refer_mapping.has_key(id0):
                                id0 = towers_refer_mapping[id0]
                            if towers_refer_mapping.has_key(id1):
                                id1 = towers_refer_mapping[id1]
                            towers_pair_list.append({"properties":{"start":id0, "end":id1, "webgis_type":"edge_tower"}})
                    
                    
                    
                    
                for k in line.keys():
                    if k=='line_name':
                        lineobj['properties']['name'] = line[k]
                    else:
                        lineobj['properties'][k] = line[k]
                lineobj['properties']['py'] = piny.hanzi2pinyin_first_letter(line['line_name'].replace('#','').replace('II',u'额').replace('I',u'一'))
                lineobj['properties']['webgis_type'] = 'polyline_line'
                collection.save(add_mongo_id(lineobj))
                #for edgeobj in towers_pair_list:
                    #collection_edges.save(add_mongo_id(edgeobj))
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
    
def test_mongo_import_code(db_name, area):
    global gClientMongo
    host, port = 'localhost', 27017
    try:
        mongo_init_client()
        db = gClientMongo['webgis'][db_name]
        cods = {
            'equipment_class':'TABLE_COD_EQU_CLASS',
            'equipment_container':'TABLE_COD_EQU_CONT',
            'fault_type':'TABLE_COD_FAULT_TYPE',
            'functional_type':'TABLE_COD_FUNC_TYPE',
            'object_class':'TABLE_COD_OBJ_CLASS',
            'voltage_level':'TABLE_COD_VOL_LEVEL',
        }
        if 'codes' in db.collection_names(False):
            db.drop_collection('codes')
        collection = db.create_collection('codes')
        obj = {}
        for k in cods.keys():
            obj[k] = {}
            odbc = odbc_get_records(cods[k], '1=1', area)
            for i in odbc:
                obj[k][i['code']] = i['name']
        collection.save(obj)
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
   
def test_pinyin_search():
    dbname = 'kmgd'
    collection_name = '*'
    action = 'pinyin_search'
    data = {'py':'qly'}
    conditions = {}
    ret = mongo_action(dbname, collection_name, action, data)
    print(len(ret))
    p1 = 0
    p2 = 0
    for i in ret:
        if i.has_key('geometry') and i['geometry']['type'] == 'Point':
            p1 += 1
        else:
            p2 += 1
    print('p1=%d, p2=%d' % (p1, p2))
    
            
            
def import_tower_xls_file(area, line_name,voltage, category, xls_file):
    
    #TABLE_LINE
    def extract_line(area, sheet, line_id, line_name, voltage, category):
        line = {}
        line['id'] = line_id
        line['line_code'] = ''
        line['line_name'] = line_name
        line['box_north'] = None
        line['box_south'] = None
        line['box_east'] = None
        line['box_west'] = None
        line['voltage'] = voltage
        line['category'] = category
        line['length'] = 0.0
        line['manage_length'] = 0.0
        line['start_point'] = None
        line['end_point'] = None
        line['start_tower'] = None
        line['end_tower'] = None
        line['status'] = u'运行中'
        line['maintenace'] = None
        line['management'] = None
        line['owner'] = None
        line['team'] = None
        line['responsible'] = None
        line['investor'] = None
        line['designer'] = None
        line['supervisor'] = None
        line['constructor'] = None
        line['operator'] = None
        line['finish_date'] = None
        line['production_date'] = None
        line['decease_date'] = None
        l = odbc_get_records('TABLE_LINE', u"line_name='%s'" % line_name, area)
        if len(l)>0:
            errmsg = u'已存在相同线路名[%s]' % line_name
            raise Exception(errmsg)
            
        return line
    
    
    #TABLE_TOWER
    def extract_tower(sheet, line_id):
        towers = []
        towers_id_name_mapping = {}
        for i in range(sheet.nrows):
            if i >= 7:
                tower_id = str(uuid.uuid4())
                tower = {'id':tower_id, 'line_id':line_id}
                for j in range(sheet.ncols):
                    try:
                        v = sheet.cell_value(i,j)
                        if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                            if '\n' in v:
                                arr = v.split('\n')
                                s = ''
                                for k in arr:
                                    s += k + ','
                                if len(s)>0:
                                    s = s[:-1]
                                v = s
                            #print('(%d,%d)=%s' % (i, j, v))
                            if j == 2:
                                tower['tower_name'] = line_name + v
                                towers_id_name_mapping[v] = tower['id']
                            elif j == 4:
                                arr = v.split(' - ')
                                tower['model_code'] = arr[0]
                                tower['denomi_height'] = int(arr[1])
                            #elif j == 7:
                                #tower['model_code'] = arr[0]
                            elif j in [7, 8, 9, 10, 42, 43]:
                                errmsg = u'解析单元格(%d,%d)出错,请检查, should be float' % (i+1, j+1)
                                raise Exception(errmsg)
                                
                        elif isinstance(v, int):
                            #print('(%d,%d)=%d' % (i, j, v))
                            pass
                        elif isinstance(v, float):
                            #print('(%d,%d)=%f' % (i, j, v))
                            if j == 7:
                                tower['horizontal_span'] = v
                            elif j == 8:
                                tower['vertical_span'] = v
                            elif j == 9:
                                tower['building_level'] = v
                            elif j == 10:
                                tower['line_rotate'] = v
                            elif j == 42:
                                tower['geo_x'] = v
                            elif j == 43:
                                tower['geo_y'] = v
                            elif j in [2, 4]:
                                errmsg = u'解析单元格(%d,%d)出错,请检查, should be string' % (i+1, j+1)
                                raise Exception(errmsg)
                                
                                
                                
                    except:
                        errmsg = u'解析单元格(%d,%d)出错,请检查' % (i+1, j+1)
                        raise Exception(errmsg)
                if tower.has_key('tower_name'):
                    #tower['id'],
                    #tower['line_id'],
                    tower['tower_code'] = ''
                    #tower['tower_name'],
                    tower['same_tower'] = '00000000-0000-0000-0000-000000000000'
                    tower['line_position'] = u'单回'
                    #tower['geo_x'],
                    #tower['geo_y'],
                    tower['geo_z'] = 0.0
                    tower['rotate'] = 0.0
                    #tower['model_code'],
                    tower['model_code_height'] = ''
                    #tower['denomi_height'],
                    #tower['horizontal_span'],
                    #tower['vertical_span'],
                    tower['grnd_resistance'] = None
                    #tower['building_level'],
                    #tower['line_rotate']
                    
                    towers.append(tower)
        
        return towers, towers_id_name_mapping
    
    #TABLE_STRAIN_SECTION
    def extract_strain(sheet, line_id, id_mapping):
        l = []
        lastrow = 0
        for i in range(sheet.nrows):
            if i >= 7:
                for j in range(sheet.ncols):
                    try:
                        if j == 1:
                            v = sheet.cell_value(i,j)
                            if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                                if '/' in v:
                                    arr = v.split('/')
                                    #print('(%d,%d)=%f, %f, %f' % (i, j, float(arr[0]), float(arr[1]), float(arr[2])))
                                    l.append({'row':i, 'total_length':float(arr[0].strip()), 'typical_span':float(arr[1].strip()), 'k_value':float(arr[2].strip())})
                            #else:
                                #errmsg = u'error occur when parsing tower in cell(%d,%d), should be string' % (i+1, j+1)
                                #raise Exception(errmsg)
                        if j == 2:
                            v = sheet.cell_value(i,j)
                            #if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                            lastrow = i
                            #else:
                                #errmsg = u'error occur when parsing tower in cell(%d,%d), should be string' % (i+1, j+1)
                                #raise Exception(errmsg)
                                
                    except:
                        errmsg = u'解析单元格(%d,%d)出错,请检查' % (i+1, j+1)
                        raise Exception(errmsg)
                                
        #print('lastrow = %d' % lastrow)
        strains = []
        for i in l:
            try:
                strain_id = str(uuid.uuid4())
                strain = {'id':strain_id, 'line_id':line_id}
                
                idx = l.index(i)
                v1 = sheet.cell_value(i['row']-1,2)
                if idx+1 < len(l):
                    v2 = sheet.cell_value(l[idx+1]['row']-1,2)
                else:
                    v2 = sheet.cell_value(lastrow,2)
                #print('start=%s, end=%s, total_length=%f, typical_span=%f, k_value=%f' % (v1, v2, i['total_length'], i['typical_span'], i['k_value']))
                strain['start_tower'] = id_mapping[v1]
                strain['end_tower'] = id_mapping[v2]
                strain['total_length'] = i['total_length']
                strain['typical_span'] = i['typical_span']
                strain['k_value'] = i['k_value']
                strain['conductor_type'] = ''
                strain['ground_type_left'] = ''
                strain['ground_type_right'] = ''
                strains.append(strain)
            except:
                errmsg = u'解析单元行[%d]出错,请检查' % i['row'] + 1
                raise Exception(errmsg)
                
        return strains
    
    #TABLE_SEGMENT
    def extract_segment(sheet, line_id, id_mapping):
        l = []
        m = {}
        lastrow = 0
        for i in range(sheet.nrows):
            if i >= 7:
                for j in range(sheet.ncols):
                    try:
                        if j == 6:
                            v = sheet.cell_value(i,j)
                            if isinstance(v, float) :
                                l.append({'row':i, 'length':v,})
                            elif (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                                errmsg = u'解析单元格(%d,%d)出错,请检查 should be float' % (i+1, j+1)
                                raise Exception(errmsg)
                            
                        if j == 2:
                            v = sheet.cell_value(i,j)
                            #if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                            lastrow = i
                            #else:
                                #errmsg = u'error occur when parsing tower in cell(%d,%d), should be string' % (i+1, j+1)
                                #raise Exception(errmsg)
                    except:
                        errmsg = u'解析单元格(%d,%d)出错,请检查' % (i+1, j+1)
                        raise Exception(errmsg)
                                
        segs = []
        for i in l:
            try:
                seg_id = str(uuid.uuid4())
                seg = {'id':seg_id, 'line_id':line_id}
                
                idx = l.index(i)
                v1 = sheet.cell_value(i['row']-1,2)
                if idx+1 < len(l):
                    v2 = sheet.cell_value(l[idx+1]['row']-1,2)
                else:
                    v2 = sheet.cell_value(lastrow,2)
                #print('small=%s, big=%s, length=%f' % (v1, v2, i['length']))
                m[v1+v2] = seg_id
                seg['small_tower'] = id_mapping[v1]
                seg['big_tower'] = id_mapping[v2]
                seg['splitting'] = 2
                seg['conductor_count'] = 0
                seg['crosspoint_count'] = 0
                seg['length'] = i['length']
                seg['seperator_bar'] = 0
                seg['connector_count'] = 0
                seg['connector_type'] = ''
                segs.append(seg)
            except:
                errmsg = u'解析单元格行[%d]出错,请检查' % i['row'] + 1
                raise Exception(errmsg)
        return segs, m
    
    
    #TABLE_CROSS_POINT
    def extract_crosspoint(sheet, line_id, id_mapping, seg_mapping):
        l = []
        lastrow = 0
        for i in range(sheet.nrows):
            if i >= 7:
                for j in range(sheet.ncols):
                    try:
                        if j >= 30 and j<=41:
                            v = sheet.cell_value(i,j)
                            if isinstance(v, float) :
                                cp_type = ''
                                if j == 30:
                                    cp_type = u'低压线'
                                if j == 31:
                                    cp_type = u'通讯线'
                                if j == 32:
                                    cp_type = u'电力线'
                                if j == 33:
                                    cp_type = u'铁路'
                                if j == 34:
                                    cp_type = u'公路'
                                if j == 35:
                                    cp_type = u'电车道'
                                if j == 36:
                                    cp_type = u'通航河流'
                                if j == 37:
                                    cp_type = u'不通航河流'
                                if j == 38:
                                    cp_type = u'管道'
                                if j == 39:
                                    cp_type = u'索道'
                                if j == 40:
                                    cp_type = u'房屋'
                                if j == 41:
                                    cp_type = u'林木'
                                if len(cp_type)>0:
                                    l.append({'row':i, 'col':j, 'cp_type':cp_type})
                        if j == 2:
                            v = sheet.cell_value(i,j)
                            if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                                lastrow = i
                    except:
                        errmsg = u'解析单元格(%d,%d)出错,请检查' % (i+1, j+1)
                        raise Exception(errmsg)
                                
        return []
    
    
    #TABLE_TOWER_METALS
    def extract_metals(sheet, line_id, id_mapping):
        l = []
        lastrow = 0
        for i in range(sheet.nrows):
            if i >= 7:
                metal_id = str(uuid.uuid4())
                metal = {'id':metal_id}
                for j in range(sheet.ncols):
                    try:
                        tower_name = sheet.cell_value(i,2)
                        if len(tower_name)>0:
                            metal['tower_id'] = id_mapping[str(tower_name)]
                            if j >= 19 and j<=24:
                                v = sheet.cell_value(i,j)
                                karr, varr = [], []
                                if j in [19, 21, 23]:
                                    if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                                        karr = v.strip().split('\n')
                                        vv = sheet.cell_value(i, j+1)
                                        if len(karr)==1 and (isinstance(vv, str) or isinstance(vv, unicode)) and len(vv)>0:
                                            metal['attach_type'] = u'绝缘子串'
                                            if j == 19:
                                                metal['attach_subtype'] = u'导线绝缘子'
                                            elif j == 21:
                                                metal['attach_subtype'] = u'跳线绝缘子'
                                            elif j == 23:
                                                metal['attach_subtype'] = u'地线绝缘子'
                                            metal['specification'] = karr[0]
                                            metal['material'] = u''
                                            metal['strand'] = int(vv.strip())
                                            metal['slice'] = 0
                                            metal['value1'] = 0
                                            print('%s %s %d' % (tower_name, karr[0], int(vv)))
                                            l.append(metal)
                                        elif len(karr)>1 and (isinstance(vv, str) or isinstance(vv, unicode)) and len(vv)>0:
                                            varr = vv.strip().split('\n')
                                            if len(karr) == len(varr):
                                                for k in karr:
                                                    metal['id'] = str(uuid.uuid4())
                                                    metal['attach_type'] = u'绝缘子串'
                                                    if j == 19:
                                                        metal['attach_subtype'] = u'导线绝缘子'
                                                    elif j == 21:
                                                        metal['attach_subtype'] = u'跳线绝缘子'
                                                    elif j == 23:
                                                        metal['attach_subtype'] = u'地线绝缘子'
                                                    metal['specification'] = k
                                                    metal['material'] = u''
                                                    metal['strand'] = int(varr[karr.index(k)])
                                                    metal['slice'] = 0
                                                    metal['value1'] = 0
                                                    print('%s %s %d' % (tower_name, k, int(varr[karr.index(k)])))
                                                    l.append(metal)
                                                
                    except:
                        errmsg = u'解析单元格(%d,%d)出错,请检查' % (i+1, j+1)
                        raise Exception(errmsg)
        return l
    
    
    line_id = str(uuid.uuid4())
    ret = {}
    ret['line_id'] = line_id
    ret['result'] = ''
    area = 'zt'
    sqls = []
    
    try:
        book = xlrd.open_workbook(xls_file)
        sheet = book.sheet_by_index(0)
        line = extract_line(area, sheet, line_id, line_name, voltage, category)
        towers, towers_id_name_mapping = extract_tower(sheet, line_id)
        strains = extract_strain(sheet, line_id, towers_id_name_mapping)
        segs, seg_mapping = extract_segment(sheet, line_id, towers_id_name_mapping)
        #metals = extract_metals(sheet, line_id, towers_id_name_mapping)
            
        sqls.extend(odbc_save_data_to_table('TABLE_LINE', 'save', [line,], None, None, None, area, True))
        sqls.extend(odbc_save_data_to_table('TABLE_TOWER', 'save', towers, None, None, None, area, True))
        sqls.extend(odbc_save_data_to_table('TABLE_STRAIN_SECTION', 'save', strains, None, None, None, area, True))
        sqls.extend(odbc_save_data_to_table('TABLE_SEGMENT', 'save', segs, None, None, None, area, True))
    except:
        ret['result'] = sys.exc_info()[1]
        raise
        
    print(len(sqls))
    for sql in sqls:
        print(sql)
    try:
        odbc_execute_sqls(sqls, area)
    except:
        ret['result'] = sys.exc_info()[1]
        raise
    return ret


def test_import_xlsdata():
    #XLS_FILE = ur'F:\work\csharp\kmgdnew10.2-2014-1-17\交流220kV永发II回线杆塔明细表.xls'
    #ret = import_tower_xls_file('zt',u'测试线路基于永发II回线', '13', u'架空线', XLS_FILE)
    #print('line_id=%s' % ret['line_id'])
    #print(ret['result'])
    test_delete_import_xlsdata('f1992b07-41b9-4fda-b802-15bdf4054f09')


def test_delete_import_xlsdata(line_id):
    sqls = []
    sqls.append('''delete from TABLE_LINE where id='%s' ''' % line_id)
    sqls.append('''delete from TABLE_TOWER where line_id='%s' ''' % line_id)
    sqls.append('''delete from TABLE_STRAIN_SECTION where line_id='%s' ''' % line_id)
    sqls.append('''delete from TABLE_SEGMENT where line_id='%s' ''' % line_id)
    try:
        odbc_execute_sqls(sqls, 'zt')
    except:
        print(sys.exc_info()[1])

 
def gridfs_save(qsdict, filename, data):
    global gClientMongo, gConfig
    
    if not qsdict.has_key('db'):
        raise Exception('db not specified in parameter')
    dbname = qsdict['db']
    
    clienttype = str(gConfig['wsgi']['application'])
    collection = 'fs'
    if qsdict.has_key('collection'):
        collection = str(qsdict['collection'])

    if not qsdict.has_key('mimetype'):
        raise Exception('mimetype not specified in parameter')
    mimetype = urllib.unquote_plus(qsdict['mimetype'])

     
    if qsdict.has_key('_id'):
        _id = qsdict['_id']
        try:
            _id = ObjectId(_id)
        except:
            _id = ObjectId()
        try:
            mongo_init_client(clienttype)
            db = gClientMongo[clienttype][dbname]
            fs = gridfs.GridFS(db, collection=collection)
            fs.put(data, _id=_id, mimetype=mimetype, filename=filename, )
        except:
            traceback.print_exc()
            raise
    else:
        if not qsdict.has_key('bindcollection'):
            raise Exception('bindcollection not specified in parameter')
        bindcollection = qsdict['bindcollection']
        
        
        if not qsdict.has_key('key'):
            raise Exception('key not specified in parameter')
        key = qsdict['key']
    
        if not qsdict.has_key('category'):
            raise Exception('category not specified in parameter')
        category = qsdict['category']
        
        
        
        description = u''
        if qsdict.has_key('description'):
            description = qsdict['description']
        
        
        #filename = dec(urllib.unquote_plus(qsdict['filename']))
        #size = int(qsdict['size'])
        try:
            mongo_init_client(clienttype)
            db = gClientMongo[clienttype][dbname]
            fs = gridfs.GridFS(db, collection=collection)
            fs.put(data, bindcollection=bindcollection, key=ObjectId(key), mimetype=mimetype, filename=filename, category=category, description=description)
        except:
            traceback.print_exc()
            raise
        
def gridfs_delete(qsdict, clienttype='webgis'):
    global gClientMongo, gConfig
    if not qsdict.has_key('db'):
        raise Exception('db not specified in parameter')
    dbname = qsdict['db']
    
    if qsdict.has_key('collection'):
        collection = qsdict['collection']
    else:
        collection = 'fs'
    _id, bindcollection, key, category = None, None, None, None
    if qsdict.has_key('_id'):
        _id = qsdict['_id']
    
    if  qsdict.has_key('bindcollection'):
        #raise Exception('bindcollection not specified in parameter')
        bindcollection = qsdict['bindcollection']
    
    if qsdict.has_key('key'):
        #raise Exception('key not specified in parameter')
        key = qsdict['key']
        
    if qsdict.has_key('category'):
        #raise Exception('category not specified in parameter')
        category = qsdict['category']
    try:
        mongo_init_client(clienttype)
        db = gClientMongo[clienttype][dbname]
        fs = gridfs.GridFS(db, collection=collection)
        if _id:
            r = fs.delete(ObjectId(_id))
            #print(r)
        else:
            if bindcollection and key:
                cond = {'bindcollection':bindcollection, 'key':ObjectId(key)}
                if category:
                    cond['category'] = category
                if fs.exists(cond):
                    l = []
                    for i in fs.find(cond):
                        l.append(i._id)
                    for i in l:
                        fs.delete(i)
    except:
        traceback.print_exc()
        raise



def mongo_init_client(clienttype='webgis', subtype=None, host=None, port=None, replicaset=None):
    global gClientMongo, gClientMongoTiles, gConfig
    try:
        app = gConfig['wsgi']['application']
        if clienttype in ['webgis', 'markdown', 'authorize_platform', 'pay_platform', 'combiz_platform', 'chat_platform']:
            if not gClientMongo.has_key(clienttype) :
                if host is None:
                    host = gConfig[clienttype]['mongodb']['host']
                if port is None:
                    port = int(gConfig[clienttype]['mongodb']['port'])
                if replicaset is None:
                    replicaset = gConfig[clienttype]['mongodb']['replicaset']
                if len(replicaset) == 0:
                    gClientMongo[clienttype] = MongoClient(host, port)
                else:
                    gClientMongo[clienttype] = MongoClient(host, port, replicaSet=str(replicaset),  read_preference = ReadPreference.PRIMARY)
        elif clienttype == 'geofeature':
            if not gClientMongo.has_key(clienttype) :
                if host is None:
                    host = gConfig['webgis']['geofeature']['mongodb']['host']
                if port is None:
                    port = int(gConfig['webgis']['geofeature']['mongodb']['port'])
                if replicaset is None:
                    replicaset = gConfig['webgis']['geofeature']['mongodb']['replicaset']
                if len(replicaset) == 0:
                    gClientMongo[clienttype] = MongoClient(host, port)
                else:
                    gClientMongo[clienttype] = MongoClient(host, port, replicaSet=str(replicaset),  read_preference = ReadPreference.PRIMARY)
        elif clienttype in [ 'anti_bird', 'state_examination']:
            if not gClientMongo.has_key(clienttype) :
                if host is None:
                    host = gConfig['webgis'][clienttype]['mongodb']['host']
                if port is None:
                    port = int(gConfig['webgis'][clienttype]['mongodb']['port'])
                if replicaset is None:
                    replicaset = gConfig['webgis'][clienttype]['mongodb']['replicaset']
                if len(replicaset) == 0:
                    gClientMongo[clienttype] = MongoClient(host, port)
                else:
                    gClientMongo[clienttype] = MongoClient(host, port, replicaSet=str(replicaset),  read_preference = ReadPreference.PRIMARY)
        elif  'webgis/' in  clienttype:
            arr = clienttype.split('/')
            tiletype = arr[1]
            if not gClientMongoTiles.has_key(tiletype):
                gClientMongoTiles[tiletype] = {}
            if not gClientMongoTiles[tiletype].has_key(subtype):
                gClientMongoTiles[tiletype][subtype] = None
            if gClientMongoTiles[tiletype][subtype] is None:
                if host is None:
                    host = gConfig['webgis'][tiletype][subtype]['mongodb']['host']
                if port is None:
                    port = int(gConfig['webgis'][tiletype][subtype]['mongodb']['port'])
                if replicaset is None:
                    replicaset = gConfig['webgis'][tiletype][subtype]['mongodb']['replicaset']
                if len(replicaset) == 0:
                    gClientMongoTiles[tiletype][subtype] = MongoClient(host, port)
                else:
                    gClientMongoTiles[tiletype][subtype] = MongoClient(host, port, replicaset=str(replicaset),  read_preference = ReadPreference.PRIMARY)
    except:
        raise


def gridfs_find(qsdict, clienttype='webgis'):
    global gClientMongo, gConfig
    def thumbnail(fp, size, use_base64=False):
        ret = None
        print(fp.mimetype)
        if 'image/' in fp.mimetype:
            im = Image.open(fp)
            im.thumbnail(size)
            buf= StringIO.StringIO()
            #print(im.format)
            im.save(buf, im.format)
            ret = buf.getvalue()
            if use_base64:
                ret = base64.b64encode(ret)
        else:
            p = None
            STATICRESOURCE_DIR = os.path.join(module_path(), 'static')
            if gConfig['web'].has_key('webroot') and len(gConfig['web']['webroot'])>0:
                if os.path.exists(gConfig['web']['webroot']):
                    STATICRESOURCE_DIR = gConfig['web']['webroot']
            #print(fp.mimetype)
            if gConfig['web']['thumbnail'].has_key( fp.mimetype):
                p = os.path.join(STATICRESOURCE_DIR, 'img', 'thumbnail', gConfig['web']['thumbnail'][fp.mimetype])
            else:
                p = os.path.join(STATICRESOURCE_DIR, 'img', 'thumbnail', 'other.png')
            im = Image.open(p)
            im.thumbnail(size)
            buf= StringIO.StringIO()
            im.save(buf, im.format)
            ret = buf.getvalue()
            if use_base64:
                ret = base64.b64encode(ret)
        return ret
        
    
    if not qsdict.has_key('db'):
        raise Exception('db not specified in parameter')
    dbname = qsdict['db']
    #if gConfig['wsgi']['application'] == 'markdown':
    
    
    download = False
    if qsdict.has_key('attachmentdownload'):
        download = True
    
    if qsdict.has_key('collection'):
        collection = qsdict['collection']
    else:
        collection = 'fs'
        
    width, height = 128, 128
    try:
        if qsdict.has_key('width'):
            width = int(qsdict['width'])
        if qsdict.has_key('height'):
            height = int(qsdict['height'])
    except:
        raise
    
    _id, bindcollection, key, category = None, None, None, None
    skip, limit = 0, 0
    if qsdict.has_key('_id'):
        _id = qsdict['_id']
    if qsdict.has_key('skip') and qsdict.has_key('limit'):
        skip = int(qsdict['skip'])
        limit = int(qsdict['limit'])
        
    if qsdict.has_key('bindcollection') and qsdict.has_key('key'):
        bindcollection = qsdict['bindcollection']
        key = qsdict['key']
        #if not qsdict.has_key('category'):
            #raise Exception('category not specified in parameter')
        #category = qsdict['category']
    
    
    mimetype, ret = None, None
    
    try:
        mongo_init_client(clienttype)
        db = gClientMongo[clienttype][dbname]
        fs = gridfs.GridFS(db, collection=collection)
        if qsdict.has_key('_id'):
            if fs.exists({'_id': ObjectId(_id)}):
                for i in fs.find({'_id':ObjectId(_id)}):
                    mimetype = str(i.mimetype)
                    if not download:
                        if 'image/' in mimetype:
                            ret = i.read()
                        else:
                            mimetype = 'image/png'
                            ret = thumbnail(i, (256, 256))
                    else:
                        ret = i.read()
                        return mimetype, ret, i.filename
                    break
            return mimetype, ret
        #elif qsdict.has_key('skip') and qsdict.has_key('limit'):
            #pass
        if qsdict.has_key('bindcollection') and qsdict.has_key('key'):
            ret = []
            if fs.exists({'bindcollection':bindcollection, 'key':ObjectId(key), }):
                for i in fs.find({'bindcollection':bindcollection, 'key':ObjectId(key), }, skip=skip, limit=limit):
                    size = (width , height)
                    t = thumbnail(i, size, True)
                    ret.append({'_id':str(i._id), 'filename':i.filename, 'description':i.description, 'mimetype':str(i.mimetype), 'data':t})
            return ret
        else:
            ret = []
            for i in fs.find(skip=skip, limit=limit):
                size = (width , height)
                t = thumbnail(i, size, True)
                ret.append({'_id':str(i._id), 'filename':i.filename, 'mimetype':str(i.mimetype), 'data':t})
            return ret
            
    except:
        traceback.print_exc()
        raise


def batch_tile_download(tiletype, subtype, westsouth, eastnorth, zoomrange):
    global gConfig, gIsSaveTileToDB
    def deg2num(lon_deg, lat_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (xtile, ytile)
    arr = tiletype.split('/')
    pathlist = []
    for zoom in zoomrange:
        startx, starty = deg2num(westsouth[0], westsouth[1], zoom)
        endx, endy = deg2num(eastnorth[0], eastnorth[1], zoom)
        if endx < startx:
            startx, endx = endx, startx
        if endy < starty:
            starty, endy = endy, starty
        for i in range(startx, endx+1):
            for j in range(starty, endy+1):
                path = '%d/%d/%d%s' % (zoom, i, j, gConfig['webgis'][arr[1]][subtype]['mimetype'])
                param = {}
                param['x'] = ['%d' % i]
                param['y'] = ['%d' % j]
                param['level'] = ['%d' % zoom]
                pathlist.append([path, param])
    return pathlist
    
def test_batch_tile_download():
    global gIsSaveTileToDB
    gIsSaveTileToDB = False
    tiletype='webgis/tiles'
    subtype = 'arcgis_sat'
    #tiletype='terrain'
    #subtype = 'quantized_mesh'
    westsouth = [102.49, 24.67]
    eastnorth = [102.94, 25.16]
    zoomrange = range(1, 18)
    pathlist = batch_tile_download(tiletype, subtype, westsouth, eastnorth, zoomrange)
    for i in pathlist:
        #print(i[0])
        if pathlist.index(i) % 5 == 1:
            gevent.sleep(2)
        else:
            gevent.spawn(gridfs_tile_find, tiletype, subtype, i[0], i[1])
            
def command_batch_tile_download(options):
    global gConfig, gIsSaveTileToDB
    gIsSaveTileToDB = options.save_to_db
    
    if options.tiletype is None \
       or options.subtype is None:
        print('please specify tiletype and subtype, now exit.')
        return
    
    if not gConfig.has_key('webgis'):
        print('Wrong webgis config file, now exit.')
        return
    tiletype = options.tiletype
    if '/' in tiletype:
        tiletype = tiletype.split('/')[1]
    if not gConfig['webgis'].has_key(tiletype):
        print('please use correct tiletype in config file, now exit.')
        return
        
    if not gConfig['webgis'][tiletype].has_key(options.subtype):
        print('please use correct subtype in config file section[webgis][%s], now exit.' % tiletype)
        return
    
    if options.num_cocurrent < 1 or options.num_cocurrent > 10:
        print('please specify a range[1, 10] of cocurrent number.')
        return
    
    if options.wait_sec < 1 :
        print('please specify a number > 0 of wait second.')
        return
    
    if options.west is None \
       or options.south is None \
       or options.east is None \
       or options.north is None:
        print('please specify extent by degree(WGS84) using --west --east --north --south. ')
        return
        
    
    westsouth = [options.west, options.south]
    eastnorth = [options.east, options.north]
    zoomrange = range(options.zoom_min, options.zoom_max+1)
    
    print('batch downloading extent: W%f,S%f,E%f,N%f' % (options.west, options.south, options.east, options.north))
    print('zoom range: [%d, %d]' % (options.zoom_min, options.zoom_max))
    s_save_to_db = 'False'
    if options.save_to_db:
        s_save_to_db = 'True'
    print('save to database: %s' % s_save_to_db)
    
    #if True:
        #return
    
    
    pathlist = batch_tile_download(options.tiletype, options.subtype, westsouth, eastnorth, zoomrange)
    totallen = len(pathlist)
    print('%d tile files need processing' % totallen)
    idx = 0
    for i in pathlist:
        #print(i[0])
        if pathlist.index(i) % options.num_cocurrent == 0:
            idx += options.num_cocurrent
            print('...%d%%...' % int(float(idx)/float(totallen) * 100.0))
            gevent.sleep(options.wait_sec)
        else:
            gevent.spawn(gridfs_tile_find, options.tiletype, options.subtype, i[0], i[1])
    

    
def gridfs_tile_find(tiletype, subtype, tilepath, params):
    global gClientMongoTiles, gConfig, gClientMetadata, gIsSaveTileToDB, gHttpClient
    arr = tiletype.split('/')
    dbname = gConfig['webgis'][arr[1]][subtype]['mongodb']['database']
    collection = gConfig['webgis'][arr[1]][subtype]['mongodb']['gridfs_collection']
    params1 = {}
    for k in params.keys():
        if isinstance(params[k], list) and len(params[k])>0:
            params1[k] = params[k][0]
        else:
            params1[k] = params[k]
    params = params1
    
    host, port, replicaset = gConfig['webgis'][arr[1]][subtype]['mongodb']['host'], int(gConfig['webgis'][arr[1]][subtype]['mongodb']['port']), gConfig['webgis'][arr[1]][subtype]['mongodb']['replicaset']
    mimetype, ret = None, None
    
    
    if not gClientMetadata.has_key(arr[1]):
        gClientMetadata[arr[1]] = {}
    if not gClientMetadata[arr[1]].has_key(subtype):
        gClientMetadata[arr[1]][subtype] = {}
    if len(gClientMetadata[arr[1]][subtype].keys()) == 0:
        size, content = get_missing_file(tiletype,  subtype)
        gClientMetadata[arr[1]][subtype]['missing_file_size'] = size
        gClientMetadata[arr[1]][subtype]['missing_file_content'] = content
    
    
    try:
        mongo_init_client(tiletype, subtype, host, port, replicaset)
        db = gClientMongoTiles[arr[1]][subtype][dbname]
        fs = gridfs.GridFS(db, collection=collection)
        #if fs.exists({'filename':tilepath}):
        for i in fs.find({'filename':tilepath}):
            mimetype, ret = str(i.mimetype), i.read()
            break
        #if ret is not None:
            #print('%s found in db' % tilepath)
        if ret is None:
            href = ''
            url_list = []
            connection_timeout, network_timeout = float(gConfig['webgis'][arr[1]]['www_connection_timeout']), float(gConfig['webgis'][arr[1]]['www_network_timeout'])
            if tiletype == 'webgis/terrain':
                s = gConfig['webgis'][arr[1]][subtype]['url_template']
                if s[-1] != '/':
                    s += '/'
                href = s + tilepath
                if tilepath == 'layer.json':
                    mimetype = 'application/json'
                    href += '?'
                    for k in params.keys():
                        href += k + '=' + params[k] + '&'
                    href += 'f=JSON'
                elif '.terrain' in tilepath:
                    mimetype = 'application/octet-stream'
                    href += '?'
                    for k in params.keys():
                        href += k + '=' + params[k] + '&'
                    href += 'f=TerrainTile'
                
            elif tiletype == 'webgis/tiles' and 'bing_' in subtype:
                x, y, level = int(params['x']), int(params['y']), int(params['level'])
                mimetype, ret = bing_tile(tiletype, subtype, tilepath, x, y, level)
            #elif tiletype == 'tiles' and 'arcgis_' in subtype:
                #x, y, level = int(params['x'][0]), int(params['y'][0]), int(params['level'][0])
                #mimetype, ret = arcgis_tile1(tiletype, subtype, tilepath, x, y, level)
            else:
                x, y, level = params['x'], params['y'], params['level']
                # if isinstance(x, list) and len(x)>0:
                #     x = x[0]
                # if isinstance(y, list) and len(y)>0:
                #     y = y[0]
                # if isinstance(level, list) and len(level)>0:
                #     level = level[0]
                s = gConfig['webgis'][arr[1]][subtype]['url_template']
                href = None
                mimetype = str(gConfig['mime_type'][gConfig['webgis'][arr[1]][subtype]['mimetype']])
                if isinstance(s, str) or isinstance(s, unicode):
                    s = s.replace(u'{x}', x).replace(u'{y}', y).replace(u'{level}', level)
                    href = str(s)
                    
                elif isinstance(s, list):
                    for i in s:
                        i = i.replace(u'{x}', x).replace(u'{y}', y).replace(u'{level}', level)
                        url_list.append(str(i))
            if not 'bing_' in subtype:
                def fetch_and_save_by_urlstr(urlstr):
                    global gClientMetadata
                    ret1 = None
                    response = None
                    try:
                        url = URL(urlstr)
                        #http = HTTPClient.from_url(url, concurrency=30, connection_timeout=connection_timeout, network_timeout=network_timeout, )
                        if not gHttpClient.has_key('tiles'):
                            gHttpClient['tiles'] = HTTPClient(url.host, port=url.port, connection_timeout=connection_timeout, network_timeout=network_timeout, concurrency=200)
                        headers = {}
                        if '.terrain' in tilepath:
                            headers['Accept'] = 'application/vnd.quantized-mesh,application/octet-stream;q=0.9'
                        response = gHttpClient['tiles'].get(url.request_uri, headers)
                        if response and response.status_code == 200:
                            if '.terrain' in tilepath:
                                with gzip.GzipFile(fileobj=StringIO.StringIO(response.read())) as f1:
                                    ret1 = f1.read()
                                if gIsSaveTileToDB:
                                    gevent.spawn(gridfs_tile_save, tiletype, subtype, tilepath, mimetype, ret1).join()
                            else:
                                ret1 = response.read()
                                if len(ret1) == gClientMetadata[arr[1]][subtype]['missing_file_size']:
                                    ret1 = gClientMetadata[arr[1]][subtype]['missing_file_content']
                                    #print('get blank tile size=%d' % len(ret1))
                                else:
                                    if gIsSaveTileToDB:
                                        gevent.spawn(gridfs_tile_save, tiletype, subtype, tilepath, mimetype, ret1).join()
                    except:
                        print('error')
                        ret1 = None
                    return ret1
                if href:
                    print('downloading tile from %s' % href)
                    ret = fetch_and_save_by_urlstr(href)
                elif len(url_list)>0:
                    for i in url_list:
                        print('downloading tile from %s' % i)
                        ret = fetch_and_save_by_urlstr(i)
                        if ret and len(ret) != gClientMetadata[arr[1]][subtype]['missing_file_size']:
                            break
    except:
        raise
    return mimetype, ret

#def arcgis_tile1(tiletype, subtype, tilepath, x, y, level):
    #global gConfig
    #mimetype = str(gConfig['mime_type'][gConfig[tiletype][subtype]['mimetype']])
    #ret = None
    #tileroot = gConfig[tiletype][subtype]['file_root']
    #lvl = 'L%02d' % level
    #row = 'R%08x' % int(hex(y), 16)
    #col = 'C%08x' % int(hex(x), 16)
    #p = os.path.join(tileroot, lvl, row, col+'.jpg')
    #print(p)
    #if os.path.exists(p):
        #with open(p, 'rb') as f:
            #f1 = gevent.fileobject.FileObjectThread(f, 'rb')
            #ret = f1.read()
    #else:
        #STATICRESOURCE_DIR = os.path.join(module_path(), 'static')
        #if gConfig['web'].has_key('webroot') and len(gConfig['web']['webroot'])>0:
            #if os.path.exists(gConfig['web']['webroot']):
                #STATICRESOURCE_DIR = gConfig['web']['webroot']
        #STATICRESOURCE_IMG_DIR = os.path.join(STATICRESOURCE_DIR, 'img')
        #picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['tiles'][image_type]['missing'])
        #with open(picpath, 'rb') as f:
            #f1 = gevent.fileobject.FileObjectThread(f, 'rb')
            #ret = f1.read()
        #mimetype = 'image/png'
    
    #return mimetype, ret
    
    
    
def bing_tile(tiletype, subtype, tilepath, x, y, level):
    global gClientMongoTiles, gConfig, gClientMetadata, gIsSaveTileToDB, gHttpClient
    
    def tileXYToQuadKey(x, y, level):
        quadkey = ''
        for i in range(level, -1, -1):
            bitmask = 1 << i
            digit = 0
            if (x & bitmask) != 0:
                digit |= 1
    
            if (y & bitmask) != 0:
                digit |= 2
            quadkey += str(digit)
        return quadkey
    
    def quadKeyToTileXY(quadkey):
        x = 0
        y = 0
        level = len(quadkey) - 1
        for i in range(level, -1, -1):
            bitmask = 1 << i
            digit = quadkey[level - i]
    
            if (digit & 1) != 0 :
                x |= bitmask
    
            if (digit & 2) != 0:
                y |= bitmask
        return {
            'x' : x,
            'y' : y,
            'level' : level
        }
    arr = tiletype.split('/')
    connection_timeout, network_timeout = float(gConfig['webgis'][arr[1]]['www_connection_timeout']), float(gConfig['webgis'][arr[1]]['www_network_timeout'])
    #tilepath = '%s/%s/%s%s' % (level, x, y, gConfig[tiletype][subtype]['mimetype'])
    mimetype = str(gConfig['mime_type'][gConfig['webgis'][arr[1]][subtype]['mimetype']])
    ret = None
    if not gClientMetadata.has_key(tiletype):
        gClientMetadata[tiletype] = {}
    if not gClientMetadata[tiletype].has_key(subtype):
        gClientMetadata[tiletype][subtype] = {}
    if len(gClientMetadata[tiletype][subtype].keys()) == 0:
        size, content = get_missing_file(tiletype,  subtype)
        gClientMetadata[tiletype][subtype]['missing_file_size'] = size
        gClientMetadata[tiletype][subtype]['missing_file_content'] = content
        url_metadata_template = gConfig['webgis'][arr[1]][subtype]['url_template']
        href = url_metadata_template.replace('{key}', gConfig['webgis'][arr[1]][subtype]['key'])
        url = URL(href) 
        #http = HTTPClient.from_url(url, concurrency=30, connection_timeout=connection_timeout, network_timeout=network_timeout, )
        if not gHttpClient.has_key('tiles'):
            gHttpClient['tiles'] = HTTPClient(url.host, port=url.port, connection_timeout=connection_timeout, network_timeout=network_timeout, concurrency=1000)
        response = gHttpClient['tiles'].get(url.request_uri)
        if response and response.status_code == 200:
            obj = json.load(response)
            if obj.has_key('resourceSets') and len(obj['resourceSets'])>0 and obj['resourceSets'][0].has_key('resources') and len(obj['resourceSets'][0]['resources'])>0:
                gClientMetadata[tiletype][subtype] = obj['resourceSets'][0]['resources'][0]
            #print(gClientMetadata[tiletype][subtype])
    quadkey = tileXYToQuadKey(x, y, level)
    href = gClientMetadata[tiletype][subtype]['imageUrl']
    href = href.replace('{quadkey}', quadkey).replace('{culture}', '')
    subdomains = gClientMetadata[tiletype][subtype]['imageUrlSubdomains']
    subdomainIndex = (x + y + level) % len(subdomains)
    href = href.replace('{subdomain}', subdomains[subdomainIndex]);
    print('downloading from %s' % href)
    url = URL(href)    
    #http = HTTPClient.from_url(url, concurrency=30, connection_timeout=connection_timeout, network_timeout=network_timeout, )
    if not gHttpClient.has_key('tiles'):
        gHttpClient['tiles'] = HTTPClient(url.host, port=url.port, connection_timeout=connection_timeout, network_timeout=network_timeout, concurrency=200)
    
    response = gHttpClient['tiles'].get(url.request_uri)
    if response and response.status_code == 200:
        ret = response.read()
        if len(ret) == gClientMetadata[tiletype][subtype]['missing_file_size']:
            ret = gClientMetadata[tiletype][subtype]['missing_file_content']
        else:
            if gIsSaveTileToDB:
                gevent.spawn(gridfs_tile_save, tiletype, subtype, tilepath, mimetype, ret).join()
    else:
        ret = None
    return mimetype, ret
    
    

def gridfs_tile_save(tiletype, subtype, tilepath, mimetype, data):
    global gClientMongoTiles, gConfig
    arr = tiletype.split('/')
    dbname = gConfig['webgis'][arr[1]][subtype]['mongodb']['database']
    collection = gConfig['webgis'][arr[1]][subtype]['mongodb']['gridfs_collection']
    host, port, replicaset = gConfig['webgis'][arr[1]][subtype]['mongodb']['host'], int(gConfig['webgis'][arr[1]][subtype]['mongodb']['port']), gConfig['webgis'][arr[1]][subtype]['mongodb']['replicaset']
    try:
        mongo_init_client(tiletype, subtype, host, port, replicaset)
        db = gClientMongoTiles[arr[1]][subtype][dbname]
        fs = gridfs.GridFS(db, collection=collection)
        fs.put(data, mimetype=mimetype, filename=tilepath)
    except:
        traceback.print_exc()
        raise


def gridfs_tile_delete(tiletype, subtype, tilepath=None):
    global gClientMongoTiles, gConfig
    arr = tiletype.split('/')
    
    dbname = gConfig['webgis'][arr[1]][subtype]['mongodb']['database']
    collection = gConfig['webgis'][arr[1]][subtype]['mongodb']['gridfs_collection']
    host, port, replicaset = gConfig['webgis'][arr[1]][subtype]['mongodb']['host'], int(gConfig['webgis'][arr[1]][subtype]['mongodb']['port']), gConfig['webgis'][arr[1]][subtype]['mongodb']['replicaset']
    try:
        mongo_init_client(tiletype, subtype, host, port, replicaset)
        db = gClientMongoTiles[arr[1]][subtype][dbname]
        fs = gridfs.GridFS(db, collection=collection)
        if tilepath:
            if fs.exists({'filename':tilepath}):
                l = []
                for i in fs.find({'filename':tilepath}):
                    l.append(i._id)
                for i in l:
                    fs.delete(i)
        else:
            l = []
            for i in fs.find():
                l.append(i._id)
            for i in l:
                fs.delete(i)
            
    except:
        traceback.print_exc()
        raise

    
def test_clear_gridfs(dbname, clienttype='webgis'):
    global gClientMongo, gConfig
    try:
        mongo_init_client(clienttype)
                
        db = gClientMongo[clienttype][dbname]
        fs = gridfs.GridFS(db)
        l = fs.list()
        idlist = []
        for i in fs.find():
            idlist.append(i._id)
            print(i.filename)
            #print(i.bindcollection)
            #print(i.key)
        for i in idlist:
            fs.delete(i)
    except:
        traceback.print_exc()
    
def test_resize_image(dbname, clienttype='webgis'):
    global gClientMongo, gConfig 
    
    size = (100, 100)
    try:
        mongo_init_client(clienttype)
        db = gClientMongo[clienttype][dbname]
        fs = gridfs.GridFS(db)
        for i in fs.find():
            mimetype = i.mimetype
            print(mimetype)
            #ret = i.read()
            im = Image.open(i)
            im.thumbnail(size)
            buf= StringIO.StringIO()
            print(im.format)
            im.save(buf, im.format)
            print(base64.b64encode(buf.getvalue()))
            break
            
        
    except:
        traceback.print_exc()
        raise
    
def test_httpclient():
    href = 'http://cesiumjs.org/stk-terrain/tilesets/world/tiles/0/1/0.terrain?v=3924.0.0&f=TerrainTile'
    url = URL(href)    
    http = HTTPClient.from_url(url, connection_timeout=3.0, network_timeout=3.0, )
    response = http.get(url.request_uri)
    #g = gevent.spawn(http.get, url.request_uri)
    #g.start()
    #while not g.ready():
        #if g.exception:
            #break
        #gevent.sleep(0.1)
    #response = g.value
    if response.status_code == 200:
        with open(os.path.join(ur'd:', 'test_httpclient_0_1_0.terrain'), 'wb') as f:
            with gzip.GzipFile(fileobj=StringIO.StringIO(response.read())) as f1:
                f.write(f1.read())
    
def test_httpclient1():
    
    #href = 'http://cesiumjs.org/stk-terrain/tilesets/world/tiles/0/1/0.terrain'
    #request = urllib2.Request(href, urllib.urlencode({'v':'3924.0.0','f':'TerrainTile'}))
    href = 'http://cesiumjs.org/stk-terrain/tilesets/world/tiles/0/1/0.terrain?v=3924.0.0&f=TerrainTile'
    request = urllib2.Request(href)
    request.add_header('User-Agent', 'Mozilla/5.0')
    request.add_header('Accept-Encoding', 'gzip')
    request.add_header('Accept', 'application/json,application/octet-stream,*/*')
    response = urllib2.urlopen(request)
    with open(os.path.join(ur'd:', 'test_httpclient1_0_1_0.terrain'), 'wb') as f:
        with gzip.GzipFile(fileobj=StringIO.StringIO(response.read())) as f1:
            f.write(f1.read())

def get_line_geojson(db_name, line):
    ret = None
    if line.has_key('properties') and line['properties'].has_key('webgis_type') and line['properties']['webgis_type'] == 'polyline_line':
        tids = line['properties']['nodes']
        towers_order_list = get_orderlist_by_edges(db_name, 'edge_tower', 'point_tower', tids)
        towers = [i['_id'] for i in towers_order_list]
        #print(len(towers_order_list))
        obj = {}
        obj['_id'] = line['_id']
        obj['geometry'] = {'type':'LineString', 'coordinates':[]}
        obj['type'] = 'Feature'
        obj['properties'] = line['properties']
        for i in towers_order_list:
            lng, lat, alt = i['geometry']['coordinates'][0], i['geometry']['coordinates'][1], i['geometry']['coordinates'][2]
            obj['geometry']['coordinates'].append([lng, lat, alt])
        obj['properties']['nodes'] = towers
        ret = obj
    return ret
            
def get_orderlist_by_edges(db_name, edge_webgis_type, node_webgis_type, node_id_list=[]):
    def get_prev(id, nodeidlist):
        ret = None
        edgelist = mongo_find(db_name, 'edges', {'properties.webgis_type':edge_webgis_type, 'properties.end':add_mongo_id(id), 'properties.start':{'$in':add_mongo_id(nodeidlist)}})
        ret = [i['properties']['start'] for i in edgelist]
        if len(ret)>0:
            ret = add_mongo_id(ret[0])
        return ret
    def get_next(id,  nodeidlist):
        ret = None
        edgelist = mongo_find(db_name, 'edges', {'properties.webgis_type':edge_webgis_type, 'properties.start':add_mongo_id(id), 'properties.end':{'$in':add_mongo_id(nodeidlist)}})
        ret = [i['properties']['end'] for i in edgelist]
        if len(ret)>0:
            ret = add_mongo_id(ret[0])
        return ret
    
    def get_start(id, nodeidlist):
        start = get_prev(id, nodeidlist)
        startold = None
        while start:
            startold = start
            start = get_prev(start, nodeidlist)
        return startold
    
    def get_end(id, nodeidlist):
        end = get_next(id, nodeidlist)
        endold = None
        while end:
            endold = end
            end = get_next(end, nodeidlist)
        return endold
    
    def get_path(endid, nodeidlist):
        ret = []
        while endid:
            ret.append(endid)
            endid = get_prev(endid, nodeidlist)
        ret.reverse()
        return ret
    
    def get_node(id):
        ret = None
        # for i in alist:
        #     if i['_id'] == id or i[u'_id'] == id:
        #         ret = i
        #         break
        ret = mongo_find_one(db_name, 'features', {'_id':add_mongo_id(id)})
        return ret
                
    def get_by_function_type(alist, typ):
        ret = []
        for i in alist:
            if i['properties']['function_type'] == typ:
                ret.append(i)
        return ret
                
    # edges = mongo_find(db_name, 'edges', {'properties.webgis_type':edge_webgis_type})
    cond = {'properties.webgis_type':node_webgis_type, }
    if len(node_id_list)>0:
        cond['_id'] = node_id_list
    nodes = mongo_find(db_name, 'features', cond)
    
    ret = []
    nodeidlist = [str(i) for i in node_id_list]
    if len(nodes)>0:
        node0 = nodes[0]
        end = get_end(node0['_id'], nodeidlist)
        if end is None:
            end = node0['_id']
        path = get_path(end,  nodeidlist)
        for i in path:
            node = get_node(i)
            if node:
                ret.append(node)
    return ret


            
def test_generate_ODT(db_name):
    def get_prev(id, alist):
        ret = None
        for i in alist:
            if i['properties']['end'] == id:
                ret = i['properties']['start']
                break
        return ret
    def get_next(id, alist):
        ret = None
        for i in alist:
            if i['properties']['start'] == id:
                ret = i['properties']['end']
                break
        return ret
    
    def get_start(id, alist):
        start = get_prev(id, alist)
        startold = None
        while start:
            startold = start
            start = get_prev(start, alist)
        return startold
    
    def get_end(id, alist):
        end = get_next(id, alist)
        endold = None
        while end:
            endold = end
            end = get_next(end, alist)
        return endold
    
    def get_path(endid, alist):
        ret = []
        while endid:
            ret.append(endid)
            endid = get_prev(endid, alist)
        ret.reverse()
        return ret
    
    def get_node(id, alist):
        ret = None
        for i in alist:
            if i['_id'] == id:
                ret = i
                break
        return ret
                
    def get_by_type(alist, typ):
        ret = []
        for i in alist:
            if i['properties']['function_type'] == typ:
                ret.append(i)
        return ret
                
    def slim_matrix(mapping):
        l = []
        rowexist = []
        for k in mapping.keys():
            ll = []
            for kk in mapping[k].keys():
                ll.append(mapping[k][kk])
            lll = [i[1] for i in l]
            namel = [i[0] for i in l]
            if ll in lll:
                idx = lll.index(ll)
                rowexist.append(namel[idx], k)
            else:
                l.append((k,ll))
        #while 
                
    def print_odt(odt):
        colnames = [u'样本']
        for i in odt[odt.keys()[0]].keys():
            colnames.append(i)
        colnames.append(u'故障元件')
        print(colnames)
        idx = 1
        for k in odt.keys():
            row = [idx]
            for kk in odt[k].keys():
                row.append(odt[k][kk])
            row.append(k)
            print(row)
            idx += 1
            
    
    edges = mongo_find(db_name, 'edges', {'properties.webgis_type':'edge_dn'})
    nodes = mongo_find(db_name, 'features', {'properties.webgis_type':'point_dn'})
    odt = OrderedDict()
    if len(edges)>0:
        edge = edges[0]
        start = get_start(edge['properties']['start'], edges)
        if start is None:
            start = edge['properties']['start']
        #node = get_node(start, nodes)
        #if node:
            #print(node['properties']['name'])
        #for i in get_by_type(nodes, 'T'):
            #id = i['_id']
            #path = get_path(id,  edges)
            #names = map(lambda x:get_node(x, nodes)['properties']['name'],  path)
            #print(names)
        cols = get_by_type(nodes, 'T')
        #switch
        rows = get_by_type(nodes, 'PAE')
        #transform
        rows.extend(get_by_type(nodes, 'PAB'))
        
        for i in rows:
            odt[i['properties']['name']] = OrderedDict()
            for j in cols:
                odt[i['properties']['name']][j['properties']['name']] = 0
                prev = get_prev(j['_id'], edges)
                while prev:
                    if prev == i['_id']:
                        odt[i['properties']['name']][j['properties']['name']] = 1
                        break
                    else:
                        prev = get_prev(prev, edges)
        print_odt(odt)
        
def test_bing_map():
    tiletype = 'tiles'
    subtype = 'bing_sat'
    tilepath = '11/3221/1755.jpeg'
    params = {'level':['11',], 'x':['3221',], 'y':['1755',]}
    gridfs_tile_find(tiletype, subtype, tilepath, params)


def test_edge_exist():
    db_name, area = 'kmgd', 'km'
    id0 = '53f2ff35ca49c822ece7663b'
    #id0 = '53f3021cca49c822ece7663d'
    id0 = '53f302a8ca49c822ece76640'
    id1 = '53f3027aca49c822ece7663f'
    ret = mongo_action(db_name, '-', 'check_edge_exist',[], conditions={'id0':id0, 'id1':id1})
    print(ret)
    
def test_edge_ring():
    db_name, area = 'kmgd', 'km'
    # exist = check_edge_exist(db_name, 'edges', {'properties':{'start':'53f301e4ca49c822ece7663c','end':'53f2ff35ca49c822ece7663b'}})
    # print(exist)
    # ring = check_edge_ring(db_name, 'edges', {'properties':{'start':'533e88cbca49c8156025a633','end':'533e88cbca49c8156025a61a'}})
    # ring = check_edge_ring(db_name, 'edges', {'properties':{'start':'533e88cbca49c8156025a6f8','end':'533e88cbca49c8156025a668'}})
    ring = check_edge_ring(db_name, 'edges', {'properties':{'start':'533e88cbca49c8156025a642','end':'533e88cbca49c8156025a61c'}})
    # '55883415ca49c80a7cbf78a7'

    print(ring)

def get_missing_file(tiletype, subtype):
    global gConfig
    arr = tiletype.split('/')
    staticresource_dir = os.path.join(module_path(), 'static')
    if gConfig['web'].has_key('webroot') and len(gConfig['web']['webroot'])>0:
        if os.path.exists(gConfig['web']['webroot']):
            staticresource_dir = gConfig['web']['webroot']
    staticresource_img_dir = os.path.join(staticresource_dir, 'img')
    miss_file_path = os.path.join(staticresource_img_dir,   gConfig['webgis'][arr[1]][subtype]['missing'])
    miss_file_size = 0
    miss_file_content = None
    if os.path.exists(miss_file_path):
        with open(miss_file_path, 'rb') as f:
            miss_file_content = f.read()
            if len(miss_file_content) >0:
                miss_file_size = len(miss_file_content)
    return miss_file_size, miss_file_content
    

def remove_blank_tiles(tiletype, subtype, dbname, collection):
    global  gClientMongoTiles
    arr = tiletype.split('/')
    miss_file_size, content = get_missing_file(tiletype, subtype)
    print('miss_file_size = %d' % miss_file_size)
    mongo_init_client(tiletype, subtype)
    db = gClientMongoTiles[arr[1]][subtype][dbname]
    fs = gridfs.GridFS(db, collection=collection)
    for i in fs.find():
        #if i.filename[:3] in ['17/','18/', '19/', '20/']:
        #if i.filename[:3] in ['19/', '20/']:
        if i.filename[:3] in ['9/' ,'10/', '11/', '12/', '13/', '14/', '15/', '16/', '17/', '18/', '19/', '20/']:
            s = i.read()
            #print(len(s))
            #if len(s) < 1034:
            if len(s) == miss_file_size:
                print(i.filename)
                fs.delete(i._id)
                #with open(ur'd:\tmp\%s' % i.filename.replace('/', '_'), 'wb') as f:
                    #f.write(s)
            #break
    
    
def test_remove_blank_tile():
    global gClientMongoTiles
    tiletype, subtype, dbname, collection = 'webgis/tiles', 'arcgis_sat', 'tiles_arcgis_sat', 'arcgis_sat'
    tiletype, subtype, dbname, collection = 'webgis/tiles', 'bing_sat', 'tiles_bing_sat', 'bing_sat'
    tiletype, subtype, dbname, collection = 'webgis/tiles', 'amap_map', 'tiles_amap_map', 'amap_map'
    remove_blank_tiles(tiletype, subtype, dbname, collection)

def test_import_userinfo():
    userinfo = odbc_get_records('TABLE_USER_INFO', '1=1', 'zt')
    uilist = []
    for ui in userinfo:
        uilist.append({'username':ui['user_id'], 'displayname':ui['user_name'], 'password':ui['user_passwd']})
    mongo_action('ztgd', 'userinfo', 'save', uilist)
    
def test_import_sysrole(db_name):
    global  gConfig, gClientMongo
    l = []
    l.append({'name':'admin', 'displayname':u'管理员','users':[], 'permission':['all']})
    l.append({'name':'maintainresp', 
              'displayname':u'检修专责',
              'users':[], 
              'permission':['line_save', 'edge_save', 'tower_save', 'tower_delete', 'feature_save', 'feature_delete', 'buffer_analyze'],
              })
    l.append({'name':'runresp', 
              'displayname':u'运行专责',
              'users':[], 
              'permission':[ 'buffer_analyze'],
              })
    l.append({'name':'runresp', 
              'displayname':u'班组成员',
              'users':[], 
              'permission':[ 'buffer_analyze'],
              })
    gClientMongo['webgis'] = MongoClient('localhost', 27017)
    db = gClientMongo['webgis'][gConfig['webgis']['mongodb']['database']]
    if 'sysrole' in db.collection_names(False):
        db.drop_collection('sysrole')
    if not 'sysrole' in db.collection_names(False):
        db.create_collection('sysrole')
        mongo_action(db_name, 'sysrole', 'save', l)

def test_antibird_tower_modify():
    cond = {
                "properties.webgis_type":"point_tower",
                "properties.metals":{
                    "$elemMatch":{
                        "type":u"多功能驱鸟装置",
                    }
                }
            }
    gClientMongo['webgis'] = MongoClient('192.168.1.8', 27017)
    db = gClientMongo['webgis'][gConfig['webgis']['mongodb']['database']]
    collection = db['features']
    l = list(collection.find(cond))
    # for i in l:
    #     idx = l.index(i)
    #     for j in i['properties']['metals']:
    #         idx1 = i['properties']['metals'].index(j)
    #         if j['type'] == u'超声波驱鸟装置':
    #             j['type'] = u'多功能驱鸟装置'
    #             i['properties']['metals'][idx1] = j
    #     l[idx] = i
    # for i in l:
    #     collection.save(i)
    print(json.dumps(remove_mongo_id(l),  ensure_ascii=False, indent=4))

def test_birdfamily():
    l = os.listdir(ur'F:\work\html\webgis\img\birds')
    ll = []
    for i in l:
        o = {}
        o['img'] = 'img/birds/%s' % i
        o['full'] = 'img/birds/%s' % i
        o['thumb'] = 'img/birds/%s' % i
        o['caption'] = i.replace('.jpg', '')
        o['mimetype'] = 'image/jpeg'
        ll.append(o)
    ret = json.dumps(ll, ensure_ascii=False, indent=4, encoding='utf-8')
    print ('aaa')

def test_linename_add_huixian():
    gClientMongo['webgis'] = MongoClient('192.168.1.8', 27017)
    db = gClientMongo['webgis'][gConfig['webgis']['mongodb']['database']]
    collection = db['network']
    l = list(collection.find({"properties.name":{"$regex":"^.*回$"}}))
    for i in l:
        i['properties']['name'] += u'线'
        print(i['properties']['name'])
        # collection.save(i)

def test_qinshiluxian():
    q1 = '551a30a1ca49c81a6882a1f0'
    # q1t = '551a30a1ca49c81a6882a1f1'
    # n1 = u'青石路线#20'
    # n1t = u'青石路线T接#20.1'
    gClientMongo['webgis'] = MongoClient('192.168.1.8', 27017)
    db = gClientMongo['webgis'][gConfig['webgis']['mongodb']['database']]
    # collection1 = db['network']
    collection2 = db['features']
    # collection.remove({"_id":ObjectId(q1t)})
    # o = collection1.find_one({'_id':ObjectId(q1)})
    l = list(collection2.find({"properties.name":{"$in":["花青II回#43","七花I回#28"]}}))
    # o1t = collection.find_one({'_id':ObjectId(q1t)})
    # for i in l:
    #     idx = l.index(i)
    #     for j in i['properties']['metals']:
    #         idx1 = i['properties']['metals'].index(j)
    #         if j['type'] == u'驱鸟装置':
    #             j['type'] = u'多功能驱鸟装置'
    #             i['properties']['metals'][idx1] = j
    #     l[idx] = i
    # for i in l:
    #     collection2.save(i)
    print(json.dumps( remove_mongo_id(l), ensure_ascii=False, indent=4))
    # o1['properties']['nodes'].extend(o1t['properties']['nodes'])
    # for i in l:
    #     if u'T接' in i['properties']['name']:
    #         print(i['properties']['name'])
    #         i['properties']['name'] = i['properties']['name'].replace(u'T接', '')
    #         collection2.save(i)
    # # collection.save(o1)
    # # o1 = collection.find_one({'_id':ObjectId(q1)})
    # print(len(o1['properties']['nodes']))
    # collection = db['features']
    # o1 = collection.find_one({"properties.name":n1})
    # o1t = collection.find_one({"properties.name":n1t})
    # id1 = o1['_id']
    # id1t = o1t['_id']
    # print(id1)
    # print(id1t)
    # collection = db['edges']
    # o = collection.find_one({"properties.start":id1, "properties.end":id1t})
    # print(o)
    # # o = {"properties":{"start":id1,"end":id1t, "webgis_type":"edge_tower"}}
    # # collection.save(o)
    # # o = collection.find_one({"properties.start":id1, "properties.end":id1t})
    # # print(o)

def test_auth():
    global gClientMongo
    mongo_init_client('authorize_platform')
    db = gClientMongo['authorize_platform']['authorize']
    collection = db['user_account']
    wr = collection.update({'username':'bbbb'}, {'$set':{'password':'222222'}},  multi=True, upsert=False)
    print(wr)
    

def test_check_exist_line_towers():
    l = mongo_find('kmgd', 'network', {'properties.webgis_type':'polyline_line'})
    for i in l:
        print('%s: towers: %d' % (i['properties']['name'], len(i['properties']['nodes'])))
    
    
def test_kml_import():
    def get_exist_anti_bird1(filepath):
        ret = []
        with open(filepath) as f:
            ret = json.loads(f.read())
        return ret
    def get_exist_anti_bird():
        l = mongo_find(
            'kmgd',
            'features',
            {
                "properties.webgis_type":"point_tower",
                "properties.metals":{
                    "$elemMatch":{
                        "type":u"多功能驱鸟装置"
                    }
                }
            },
            0,
            'webgis'
            )
        ret = []
        for i in l:
            o = {}
            o['_id'] = i['_id']
            o['name'] = i['properties']['name']
            if u'草海线' in o['name'] or u'七罗' in o['name'] :
                continue
            o['metals'] = []
            for j in i['properties']['metals']:
                obj = {}
                for k in j.keys():
                    if not 'button_' in k and not 'assembly_graph' in k:
                        obj[k] = j[k]
                obj["manufacturer"] = u'昶丰科技有限公司'
                o['metals'].append(obj)
            ret.append(o)
        return ret
    def fill_anti_bird(towers, alist):
        m = {}
        for i in alist:
            if m.has_key(i['name']):
                raise Exception('exist')
            m[i['name']] = i['metals']
        for tower in towers:
            idx = towers.index(tower)
            if m.has_key( tower['properties']['name']):
                tower['properties']['metals'] = m[tower['properties']['name']]
                towers[idx] = tower
        return towers
        
    
    filepath = ur'D:\kml\sdxl.kml'
    filepath1 = ur'D:\kml\lines.json'
    filepath2 = ur'D:\kml\towers.json'
    filepath3 = ur'D:\kml\edges.json'
    filepath4 = ur'D:\kml\exist_anti_bird.json'
    lines, towers, edges = kml_to_geojson(filepath)
    exist_anti_bird = get_exist_anti_bird1(filepath4)
    towers = fill_anti_bird(towers, exist_anti_bird)
    print(len(lines))
    print(len(towers))
    print(len(edges))
    print(len(exist_anti_bird))
    with open(filepath1, 'w') as f:
        f.write(enc(json.dumps(lines,  ensure_ascii=False, indent=4)))
    with open(filepath2, 'w') as f:
        f.write(enc(json.dumps(towers,  ensure_ascii=False, indent=4)))
    with open(filepath3, 'w') as f:
        f.write(enc(json.dumps(edges,  ensure_ascii=False, indent=4)))
    #with open(filepath4, 'w') as f:
        #f.write(enc(json.dumps(exist_anti_bird,  ensure_ascii=False, indent=4)))

def test_delete_anti_bird():
    filepath = ur'D:\kml\exist_anti_bird.json'
    ids = []
    l = []
    with open(filepath ) as f:
        l = json.loads(f.read())
    for i in l:
        ids.append(i['_id'])
    print(ids)
    mongo_remove('kmgd', 'features', {'_id':ids})

def test_import_lines():
    filepath = ur'D:\kml\lines.json'
    l = []
    with open(filepath) as f:
        l = json.loads(f.read())
    mongo_init_client('webgis')
    db = gClientMongo['webgis']['kmgd']
    collection = db['network']
    print('network before:%d' % collection.count())
    for i in l:
        collection.save(add_mongo_id(i))
    print('network after:%d' % collection.count())
    
def test_import_towers():
    filepath = ur'D:\kml\towers.json'
    l = []
    with open(filepath) as f:
        l = json.loads(f.read())
    mongo_init_client('webgis')
    db = gClientMongo['webgis']['kmgd']
    collection = db['features']
    print('features before:%d' % collection.count())
    for i in l:
        collection.save(add_mongo_id(i))
    print('features after:%d' % collection.count())
    
def test_import_edges():
    filepath = ur'D:\kml\edges.json'
    l = []
    with open(filepath) as f:
        l = json.loads(f.read())
    mongo_init_client('webgis')
    db = gClientMongo['webgis']['kmgd']
    collection = db['edges']
    print('edges before:%d' % collection.count())
    for i in l:
        collection.save(add_mongo_id(i))
    print('edges after:%d' % collection.count())
    
def test_import_all():
    test_import_lines()
    test_import_towers()
    test_import_edges()
        
def test_print_line_names():
    filepath = ur'D:\kml\lines.json'
    l = []
    with open(filepath) as f:
        l = json.loads(f.read())
    for i in l:
        print(i['properties']['name'])
    
    
    
    
if __name__=="__main__":
    opts = init_global()
    #test_insert_thunder_counter_attach()
    #test_insert_potential_risk()
    #admin_create_lines_layers('zt')
    #admin_create_towers_layers('zt')
    #create_segments_by_area('zt')
    ##print( time.strftime("%Y-%m-%d %H:%M:%S.%F", time.localtime()))
    ##print(datetime.datetime.fromtimestamp(time.time()))
    #test_merge_tif()
    #kmtiles = get_tiles_by_area('km')
    
    #test_gen_geojson_by_lines('zt')
    #create_mbtiles_from_esritile_and_zoom('zt', 12, 16, None, None, True, True)
    #test_insert_tower_segment()
    #test_png24_to_png8()
    #test_find_in_witch_tile(( 103.64172, 27.23023))
    #copy_tiles_zoom_column_row('km', 1, 13, None, True)
    #test_get_all_task_file_by_area('zt')
    #test_tile_directory()
    #d = gen_geojson_by_lines('zt')
    #gen_geojson_by_shape('zt')
    
    #test_get_area_by_latlng('km')
    #gen_geojson_by_lines('km')
    #gen_geojson_by_shape('km')
    #odbc_update_towers_rotate(False, 'km')
    #filelist = [ur'F:\work\cpp\kmgdgis3D\data\docs\郭家凹隧道.xls']
    filelist = [
        #ur'F:\work\cpp\kmgdgis3D\data\docs\郭家凹隧道.xls',
        #ur'F:\work\cpp\kmgdgis3D\data\docs\郭家凹隧道线性整理.xls',
        #ur'F:\work\cpp\kmgdgis3D\data\docs\海埂隧道.xls',
        #ur'F:\work\cpp\kmgdgis3D\data\docs\昆洛隧道.xls',
        ur'F:\work\cpp\kmgdgis3D\data\docs\羊甫隧道.xls',
    ]
    data_dir = u'F:\work\cpp\kmgdgis3D\data\www\geojson'
    #test_gen_geojson_by_list(data_dir, filelist)
    
    #gen_geojson_by_lines('km')
    
    db_name, area = 'kmgd', 'km'
    # db_name, area = 'ztgd', 'zt'
    #alt = altitude_by_lgtlat(ur'H:\gis\demdata', 102.70294, 25.05077)
    #print('alt=%f' % alt)
    #create_id_mapping(db_name, area)
    #mongo_import_same_tower_mapping(db_name, area)
    #test_mongo_import_code(db_name, area)
    #test_mongo_import_line(db_name, area)
    #test_mongo_import_towers(db_name, area)
    #print(len(get_tower_refer_mapping(db_name).keys()))
    #test_mongo_import_segments(db_name, area)
    #test_mongo_import_models(db_name, area)
    #test_build_tower_odbc_mongo_id_mapping()
    #test_build_line_odbc_mongo_id_mapping()
    #test_build_model_odbc_mongo_id_mapping()
    #ret = mongo_find('kmgd', 'mongo_get_towers_by_line_name', {'line_name':u'七罗I回'})
    #print(ret)
    #print('count=%d' % len(ret))
    #for i in ret:
        #print(i)
    #print('find one')
    #ret = mongo_find_one('kmgd', 'towers', {'properties.line_id':'AF77864E-B8D5-479F-896B-C5F5DFE3450F'})
    #print(ret)
    #test_find_by_string_id()
    #test_pinyin_search()
    #test_import_geojson_feature_by_shape()
    #test_import_xlsdata()
    #test_clear_gridfs(db_name)
    #test_resize_image(db_name)
    #test_httpclient()
    #l = mongo_find(db_name, 'features', {'_id':'53a8f01cca49c818b8aeaf30'})
    #print(l[0]['properties']['tower_name'])
    
    #test_import_shape_to_mongo()
    #merge_dem2()
    #test_generate_ODT(db_name)
    #test_bing_map()
    # test_edge_ring()
    #test_remove_blank_tile()
    #print(get_heatmap_tile_service_list('yn'))
    #test_import_userinfo()
    #test_import_sysrole(db_name)
    #test_auth()
    #test_kml_import()
    #test_delete_anti_bird()
    #test_check_exist_line_towers()
    # test_import_all()
    #test_print_line_names()
    # test_antibird_tower_modify()
    # test_qinshiluxian()
    # test_birdfamily()
    # test_linename_add_huixian()
    
    