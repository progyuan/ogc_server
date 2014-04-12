# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import codecs
import os, sys, time, datetime
import traceback
from lxml import etree
import pypyodbc
import uuid
import math
import shutil
import subprocess
import xlrd
import xlwt
import numpy as np
from collections import OrderedDict
import catenary
import decimal
import json
import urllib
import urllib2
import StringIO
import re
import configobj
import psycopg2 as psycopg
from psycopg2 import errorcodes
import gdal, osr
import shapefile
import sqlite3
import base64
import random
from PIL import Image
from module_locator import module_path
from pymongo import MongoClient
from bson.objectid import ObjectId

#try:
    #import arcpy
    #from arcpy import env
    #from arcpy.sa import ExtractValuesToPoints
    #import arcpy.da as da
#except ImportError:
    #print('import arcpy error:%s' % sys.exc_info()[1])
#except RuntimeError:
    #print('import arcpy error:%s' % sys.exc_info()[1])


ENCODING = 'utf-8'
ENCODING1 = 'gb18030'

CONFIGFILE = os.path.join(module_path(), 'ogc-config.ini')

#if not os.path.exists(CONFIGFILE):
    #CONFIGFILE = 'config.ini'
    
gConfig = configobj.ConfigObj(CONFIGFILE, encoding='UTF8')
gClientMongo = None
ODBC_STRING = {}
#print(gConfig.keys())
for k in gConfig['odbc'].keys():
    if not k in ['odbc_driver']:
        if len(gConfig['odbc'][k]['db_instance'])>0:
            ODBC_STRING[k] = "DRIVER={SQL Server Native Client 10.0};server=%s\\%s;Database=%s;TrustedConnection=no;Uid=%s;Pwd=%s;" % (gConfig['odbc'][k]['db_server'], gConfig['odbc'][k]['db_instance'], gConfig['odbc'][k]['db_name'], gConfig['odbc'][k]['db_username'], gConfig['odbc'][k]['db_password'])
        else:
            ODBC_STRING[k] = "DRIVER={SQL Server Native Client 10.0};server=%s;Database=%s;TrustedConnection=no;Uid=%s;Pwd=%s;" % (gConfig['odbc'][k]['db_server'],  gConfig['odbc'][k]['db_name'], gConfig['odbc'][k]['db_username'], gConfig['odbc'][k]['db_password'])




DEM_NAME = 'YN_DEM'
#DEM_NAME = 'YN_DEM_SRTM30_zt'

gDemExtractor = None
gTowerDict = {}

AREA_DATA = {'zt':[u'永甘甲线',u'永发II回线', u'镇永甲线', u'永发I回线',u'甘大线',u'永甘乙线',u'甘镇线'],
             'km':[u'厂口曲靖I回', u'和平厂口I回', u'草和乙线', u'厂口七甸I回',u'七罗II回', u'厂口曲靖II回',u'草和甲线',u'草宝乙线',u'和平厂口II回', u'草宝甲线', u'七罗I回',u'大宝I回',u'宝七I回',u'宝七II回']
             }


GP_STATUS = ['New',
             'Submitted',
             'Waiting',
             'Executing',
             'Succeeded',
             'Failed',
             'Timed Out',
             'Canceling',
             'Canceled',
             'Deleting',
             'Deleted',]



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

CODE_XLS_FILE=dec1(r'G:\work\csharp\kmgdgis\doc\电网设备信息分类与编码.xls')
XLS_FILE=dec(r'G:\work\csharp\kmgdgis\doc\线路杆塔代码.xls')
KUNMING_TOWER_KML = ur'D:\gis\昆明\sdxl - 副本.kml'



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


def init_python_lib_path():
    currdir = os.path.dirname(__file__)
    for d in ARCGIS_PYTHON_SITE_PACKAGES_DIR:
        for i in ['server10.1.pth', 'Desktop10.1.pth', 'Engine10.1.pth']:
            p = os.path.join(d, i)
            if os.path.exists(p):
                with open(p, 'a+') as f:
                    l = f.readlines()
                    ll = [ii.strip().lower() for ii in l]
                    if currdir in ll:
                        print('"%s" already exist in [%s]' % (currdir, p))
                    else:
                        f.write('\n' + currdir + '\n')
                        print('add "%s" to [%s]' % (currdir, p))
                        
                        
                
        
    
    
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
    
def read_kml(filepath):
    lines = []
    tree = etree.parse(filepath)
    if tree:
        root = tree.getroot()
        for child in root:
            for child1 in child:
                for child2 in child1:
                    line = {}
                    tag = child2.tag.replace('{http://www.opengis.net/kml/2.2}','')
                    if tag in ['Folder']:
                        linename = None
                        for item in child2:
                            tagname = item.tag.replace('{http://www.opengis.net/kml/2.2}','')
                            if tagname == 'name':
                                #print('%s' % item.text)
                                linename = item.text
                                line['name'] = linename
                            if tagname == 'Region':
                                line['box'] = {'north':float(item[0][0].text),'south':float(item[0][1].text),'east':float(item[0][2].text),'west':float(item[0][3].text)}
                            if tagname == 'Placemark':
                                if not line.has_key('towers'):
                                    line['towers'] = []
                                tower = {}
                                tower['name'] = item[0].text
                                tower['coordinates'] = {}
                                arr = item[2][2].text.split(',')
                                tower['coordinates']['lgt'] = float(arr[0])
                                tower['coordinates']['lat'] = float(arr[1])
                                line['towers'].append(tower)
                        lines.append(line)
        #print(lines)
        #for line in lines:
            ##for k in line.keys():
            #print('%s=%s' % (line['name'],str(line['towers'])))
    return lines

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
 
#def odbc_get_line_seg_count():
    #segs = odbc_get_records('TABLE_LINE_SEG', '1=1')
    #print(len(segs))
    #segs = odbc_get_records('VIEW_ATTACH_LINE_SEG', '1=1')
    #print(len(segs))
    
    
#def odbc_insert_line_seg():
    #lines = odbc_get_records('TABLE_LINE', '1=1')
    #conn = None
    #cur = None
    #try:
        #conn = pypyodbc.connect(ODBC_STRING)
        #cur = conn.cursor()
    #except:
        #print(sys.exc_info()[1])
        #return 
    ##print(len(lines))
    #for line in lines:
        #attas = get_records('VIEW_ATTACH_LINE_SEG', "line_id='%s'" % line['id'])
        #print('attachpoint rec=%d' % len(attas))
        #for atta in attas:
            #id = str(uuid.uuid4()).upper()
            #cur.execute('''INSERT INTO TABLE_LINE_SEG VALUES(?, ?, ?, ?, ?, ?)''',(id, line['id'], atta['start_point_id'],atta['end_point_id'], 0.9, '' ))


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

def sde_get_sorted_tower_by_line(rdb_conn_path, database, line_id):
    towers = get_data_from_rdbms(rdb_conn_path, database, 'TABLE_TOWER', "line_id='%s'" % line_id)
    if len(towers.keys())>1:
        towers_relation = get_data_from_rdbms(rdb_conn_path, database, 'VIEW_TOWER_RELATIONS', "line_id='%s'" % line_id)
        towers = resort_towers_by_dict(towers, towers_relation)
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


def test():
    v1 = Vector(1, 0, 0)
    v2 = Vector(1, -1, 0)
    a = np.cross(v1.get_array(), v2.get_array())
    print(a[2])
    d = np.rad2deg(v1.angle(v2))
    print(d)
    


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

    
    
def odbc_update_tower_rotate_by_line_id(line_id, is_update_feature=False, area=''):
    #kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    towers = odbc_get_sorted_tower_by_line(line_id, area)
    if is_update_feature:
        env.workspace = kmgdgeo
        fc = arcpy.ListFeatureClasses('*towers_%s' % line_id.replace('-',''))
        if fc and len(fc)>0:
            tfc = fc[0]
            arcpy.Delete_management(tfc)
            print('delete exist towers : towers_%s' % line_id.replace('-',''))
    
    linespoints = ''
    for tower in towers:
        idx = towers.index(tower)
        lgt, lat = tower['geo_x'], tower['geo_y']
        if lgt is None or lat is None or lgt==0. or lat==0.:
            lgt,lat = 0.,0.
        if idx == len(towers)-1:
            linespoints += '(%.8f,%.8f)' % (lgt, lat)
        else:
            linespoints += '(%.8f,%.8f);' % (lgt, lat)
    s = subprocess.check_output([SERVER_UTIL , '-o', 'angle', '-m', 'linepoints', '-e', '0.0', '-l', linespoints])
    angs = s.split('\r\n')
    sqls = []
    for tower in towers:
        ang = 0.
        try:
            ang = float(angs[towers.index(tower)])
        except:
            ang = 0.
        print('%s=%f' % (tower['tower_name'], ang))
        #if not (tower['geo_x'] is None or tower['geo_y'] is None or tower['geo_x']==0.0 or tower['geo_y']==0.0):
        sql = """ UPDATE  TABLE_TOWER SET 
        rotate=%f 
        WHERE 
        id='%s'""" % ( 
        ang,
        tower['id']
        ) 
        sqls.append(sql)
    odbc_execute_sqls(sqls, area)    
    
    if is_update_feature:
        dem_raster = 'sde.DBO.%s' % DEM_NAME
        create_towers_layer(kmgd, kmgdgeo, 'kmgd', line_id, dem_raster)
    
    
def odbc_update_towers_rotate(is_update_feature=False, area=''):
    lines = odbc_get_records('TABLE_LINE', '1=1', area)
    for line in lines:
        odbc_update_tower_rotate_by_line_id(line['id'], is_update_feature, area)
        
        
    
    
#def update_rotate4():
    #def GetAzimuthPolyline((lgt1, lat1),(lgt2, lat2)):
        #if lat2 - lat1 == 0:
            #return 90.
        #radian = math.atan((lgt2 - lgt1)/(lat2 - lat1))
        #degrees = radian * 180 / np.pi
        ##degrees = (degrees + 360) % 360
        #return -degrees    
    
    #lines = get_records('TABLE_LINE', '1=1')
    #d_towers_relation = {}
    #d_towers = {}
    #for line in lines:
        #towers = get_records('TABLE_TOWER', "line_id='%s'" % line['id'])
        #towers_relation = get_records('VIEW_TOWER_RELATIONS', "line_id='%s'" % line['id'])
        #d_towers[line['id']] = towers
        #d_towers_relation[line['id']] = towers_relation
        
    ##conn = None
    ##cur = None
    ##try:
        ##conn = pypyodbc.connect(ODBC_STRING)
        ##cur = conn.cursor()
    ##except:
        ##print(sys.exc_info()[1])
        ##return
    #linespoints = ''
    #for line in lines:
        #towers = resort_towers(d_towers[line['id']], d_towers_relation[line['id']])
        #linespoints += line['id'] + '@'
        #linespoints = ''
        #print(line['line_name'] + "(" + str(len(towers)) + ')')
        #for tower in towers:
            #idx = towers.index(tower)
            #lgt, lat = tower['geo_x'], tower['geo_y']
            #if idx == len(towers)-1:
                #linespoints += '(%.6f,%.6f)' % (lgt, lat)
            #else:
                #linespoints += '(%.6f,%.6f);' % (lgt, lat)
        #s = subprocess.check_output(SERVER_UTIL + ' -o angle -m linepoints -g ' +  CONFIG_PATH + ' -l ' +  linespoints)
        #angs = s.split(',')
        #print('%s:%d' % (line['id'], len(angs)))
    
        #for tower in towers:
            #ang = float(angs[towers.index(tower)])
            #idx = towers.index(tower)
            #ang_ = 0
            #if idx==0:
                #lgt1, lat1 = towers[idx]['geo_x'], towers[idx]['geo_y']
                #lgt2, lat2 = towers[idx+1]['geo_x'], towers[idx+1]['geo_y']
                #ang_ = GetAzimuthPolyline((lgt1, lat1), (lgt2, lat2))
                
            #elif idx>0 and idx<len(towers)-1:
                #lgt1, lat1 = towers[idx-1]['geo_x'], towers[idx-1]['geo_y']
                #lgt2, lat2 = towers[idx]['geo_x'], towers[idx]['geo_y']
                #lgt3, lat3 = towers[idx+1]['geo_x'], towers[idx+1]['geo_y']
                ##print('lgt1=%f, lat1=%f, lgt2=%f, lat2=%f, lgt3=%f, lat3=%f' % (lgt1, lat1, lgt2, lat2, lgt3, lat3))
                ##rotate = get_ab2((lgt1, lat1), (lgt2, lat2), (lgt3, lat3))
                #ang1 = GetAzimuthPolyline((lgt1, lat1), (lgt2, lat2))
                #ang2 = GetAzimuthPolyline((lgt2, lat2), (lgt3, lat3))
                #ang_ = (ang1+ang2)/2.0
                ##towerAngle = 0
                #sita1 = ang1
                #sita2 = ang2
                #print('sita1=%f, sita2=%f' % (sita1, sita2))
                #if  sita1*sita2<0:
                    #ang_ += 90.
                ##if sita > 90:
                    ##towerAngle = (ang_ - 90) % 360
                
                ##else:
                    ##towerAngle = (ang_ + 90) % 360
                
                ##towerAngleProject = (180 - towerAngle + 360) % 360
                ##ang_ = towerAngleProject
            #elif idx==len(towers)-1:
                #lgt1, lat1 = towers[idx-1]['geo_x'], towers[idx-1]['geo_y']
                #lgt2, lat2 = towers[idx]['geo_x'], towers[idx]['geo_y']
                #ang_ = GetAzimuthPolyline((lgt1, lat1), (lgt2, lat2))
            ##if ang_<90.:
                ##ang_ = 90. - ang_
            ##else:
                ##ang_ = ang_ - 90.
            ##ang_ = 90-ang_
            
            #if abs(ang-ang_)>0.00001:
                #print('%s=%f,%f' % (tower['tower_name'], ang, ang_))
        
    ##cur.commit()
    ##cur.close()
    ##conn.close()
   
    
#def get_angle_from_two_points((x1,y1), (x2, y2)):
    #p1 = arcpy.Point(x1,y1)
    #p2 = arcpy.Point(x2,y2)
    #arr = arcpy.Array()
    #arr.add(p1)
    #arr.add(p2)
    ##fl = []
    ##fl.append(arr)
    #line =  arcpy.Polyline(arr, arcpy.SpatialReference(text='WGS 1984 World Mercator'))
    ##fl.append(line)
    ##polyline = arcpy.CreateFeatureclass_management(out_path='in_memory',out_name='testline',geometry_type='POLYLINE',has_z='DISABLED',spatial_reference= arcpy.SpatialReference(text='WGS 1984 World Mercator'))
    #polyline = arcpy.CreateFeatureclass_management(out_path='temp.gdb',out_name='tmp_testline',geometry_type='POLYLINE',has_z='DISABLED',spatial_reference= arcpy.SpatialReference(text='WGS 1984 World Mercator'))
    ##polyline1 = arcpy.Project_management(in_dataset='testline', out_dataset='testline1', out_coor_system=arcpy.SpatialReference(text='WGS 1984 World Mercator'))
    #arcpy.AddField_management(polyline, 'rotate', 'DOUBLE')
    #with arcpy.da.InsertCursor('tmp_testline',("SHAPE@", 'rotate')) as cursor:
        #cursor.insertRow((line, 0))
    ##arcpy.CopyFeatures_management(in_features=fl, out_feature_class='testline')
    ##arcpy.PointsToLine_management(Input_Features=fl, Output_Feature_Class=polyline, Line_Field='SHAPE@')
    #arcpy.CalculateGridConvergenceAngle_cartography(in_features=polyline, angle_field='rotate',  rotation_method='GEOGRAPHIC',)# coordinate_sys_field='UTM')
    ##for i in arcpy.ListFields(polyline):
        ##print(i.name)
    #ret = 0
    #with arcpy.da.SearchCursor(polyline, ("OID@", "SHAPE@", 'rotate')) as cursor:
        #for row in cursor:
            ##print("{0}, {1}".format(row[0],   row[2]))
            #ret = row[2]
    #return ret


    
def create_line_polyline_shape(towersdictlist,  out_path, out_name, area):
    ret = False
    #tmp = '_' + out_name
    #tmp1 = '_1_' + out_name
    arcpy.CheckOutExtension("Spatial")
    if len(towersdictlist)>0:
        env.workspace = out_path
        if arcpy.Exists(out_name):
            arcpy.Delete_management(out_name)
            
        input_feature = []    
        for towersdict in  towersdictlist:
            line_name = towersdict['line_name']
            print(line_name)
            voltage = towersdict['voltage']
            towers = towersdict['towers']
            tower0 = towers[0]
            tmp = '_%s_%s' % ( out_name , tower0['line_id'].replace('-',''))
            tmp1 = '_1_%s_%s' % ( out_name , tower0['line_id'].replace('-',''))
            ptobj = None
            ptobj = arcpy.CreateFeatureclass_management(out_path=out_path, out_name=tmp, geometry_type='POINT',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='DISABLED')
            arcpy.AddMessage(arcpy.GetMessages())
            
            cur = arcpy.InsertCursor(tmp)
            p = arcpy.Point()
            id = 1
            for tower in towers:
                if tower['geo_x'] is None or tower['geo_y'] is None:
                    continue
                p.X, p.Y = tower['geo_x'], tower['geo_y']
                    
                id += 1
                feat = cur.newRow()
                feat.shape = p
                cur.insertRow(feat)
            del cur
        
            lobj = arcpy.PointsToLine_management(Input_Features=tmp, Output_Feature_Class=tmp1)
            arcpy.AddMessage(arcpy.GetMessages())
            arcpy.AddField_management(lobj, 'line_name', 'TEXT')
            arcpy.AddField_management(lobj, 'line_id', 'TEXT')
            arcpy.AddField_management(lobj, 'voltage', 'TEXT')
            cur = arcpy.UpdateCursor(tmp1)
            row = cur.next()
            if row:
                row.line_name = line_name
                row.line_id = tower0['line_id']
                row.voltage = voltage
                cur.updateRow(row)
                row = cur.next()
            del cur
            input_feature.append(tmp1)
            
        arcpy.Merge_management(inputs=input_feature, output=out_name)
        arcpy.AddMessage(arcpy.GetMessages())
        for towersdict in  towersdictlist:
            tower0 = towers[0]
            tmp = '_%s_%s' % ( out_name , tower0['line_id'].replace('-',''))
            tmp1 = '_1_%s_%s' % ( out_name , tower0['line_id'].replace('-',''))
            if arcpy.Exists(tmp):
                arcpy.Delete_management(tmp)
            if arcpy.Exists(tmp1):
                arcpy.Delete_management(tmp1)

    return ret            
    

    
def create_tower_point_shape(towersdictlist,  out_path, out_name, out_3D_name, dem_raster, area):
    ret = False
    tmp = '_%s_' % out_name 
    tmp3d = '_%s_3d' %  out_3D_name 
    #center_feature_name = '_center_%s' % out_name
    tower_info_list = odbc_get_records('TABLE_TOWER_MODEL', '1=1', area)
    arcpy.CheckOutExtension("Spatial")
    if len(towersdictlist)>0:
        env.workspace = out_path
        if arcpy.Exists(out_name):
            arcpy.Delete_management(out_name)
        if arcpy.Exists(out_3D_name):
            arcpy.Delete_management(out_3D_name)
        if arcpy.Exists(tmp):
            arcpy.Delete_management(tmp)
        if arcpy.Exists(tmp3d):
            arcpy.Delete_management(tmp3d)
        
        ptobj_3d = arcpy.CreateFeatureclass_management(out_path=out_path, out_name=out_3D_name, geometry_type='POINT',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='ENABLED', has_m='DISABLED')
        arcpy.AddMessage(arcpy.GetMessages())
        
        ptobj = arcpy.CreateFeatureclass_management(out_path=out_path, out_name=out_name, geometry_type='POINT',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='DISABLED', has_m='DISABLED')
        arcpy.AddMessage(arcpy.GetMessages())
        
        #ptobj_center = arcpy.CreateFeatureclass_management(out_path=out_path, out_name=tmp1, geometry_type='POINT',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='DISABLED', has_m='DISABLED')
        
        arcpy.AddField_management(ptobj, 'tower_id', 'TEXT')
        arcpy.AddField_management(ptobj, 'tower_name', 'TEXT')
        arcpy.AddField_management(ptobj, 'model_code', 'TEXT')
        arcpy.AddField_management(ptobj, 'rotate', 'DOUBLE')
        arcpy.AddField_management(ptobj, 'line_id', 'TEXT')
        
        
        arcpy.AddField_management(ptobj_3d, 'tower_id', 'TEXT')
        arcpy.AddField_management(ptobj_3d, 'tower_name', 'TEXT')
        arcpy.AddField_management(ptobj_3d, 'model_code', 'TEXT')
        arcpy.AddField_management(ptobj_3d, 'rotate', 'DOUBLE')
        arcpy.AddField_management(ptobj_3d, 'line_id', 'TEXT')
        
        

        for towersdict in towersdictlist:
            line_name = towersdict['line_name']
            towers = towersdict['towers']
            
            
            cur = arcpy.InsertCursor(out_name)
            p = arcpy.Point()
            id = 1
            for tower in towers:
                if tower['geo_x'] is None or tower['geo_y'] is None:
                    continue
                if not tower['same_tower'] == ZEROID:
                    continue
                p.X, p.Y = tower['geo_x'], tower['geo_y']
                
                id += 1
                feat = cur.newRow()
                feat.shape = p
                feat.tower_id = tower['id']
                if tower.has_key('tower_name'):
                    feat.tower_name = tower['tower_name']
                if tower.has_key('model_code_height'):
                    #if tower['model_code'] is None or len(tower['model_code'])==0:
                        #feat.model_code = 'test2'
                    #else:
                        ##denomi_height = '0_0'
                        ##if tower['denomi_height']:
                            ##denomi_height = '%.1f' % tower['denomi_height']
                            ##if denomi_height[-2:]=='.0':
                                ##denomi_height = denomi_height[:-2]
                            ##else:
                                ##arr = denomi_height.split('.')
                                ##denomi_height = arr[0] + '_' + arr[1]
                        ##feat.model_code = tower['model_code']+'_'+denomi_height
                    feat.model_code = tower['model_code_height']
                if tower.has_key('rotate'):
                    feat.rotate = tower['rotate']
                if tower.has_key('line_id'):
                    feat.line_id = tower['line_id']
                cur.insertRow(feat)
            del cur
            
            
            cur = arcpy.InsertCursor(out_3D_name)
            p_3d = arcpy.Point()
            id = 1
            for tower in towers:
                if tower['geo_x'] is None or tower['geo_y'] is None:
                    continue
                if not tower['same_tower'] == ZEROID:
                    continue
                p_3d.X, p_3d.Y, p_3d.Z = tower['geo_x'], tower['geo_y'], tower['geo_z']
                
                id += 1
                feat = cur.newRow()
                feat.shape = p_3d
                feat.tower_id = tower['id']
                if tower.has_key('tower_name'):
                    feat.tower_name = tower['tower_name']
                if tower.has_key('model_code_height'):
                    #feat.model_code = get_suitable_model_code(tower_info_list, tower['model_code_height'], tower['line_position'], area)
                    feat.model_code = tower['model_code_height']
                if tower.has_key('rotate'):
                    feat.rotate = tower['rotate']
                if tower.has_key('line_id'):
                    feat.line_id = tower['line_id']
                cur.insertRow(feat)
            del cur
            
            
            ##arcpy.AddField_management(ptobj_center, 'center_id', 'TEXT')
            ##arcpy.AddField_management(ptobj_center, 'start_id', 'TEXT')
            ##arcpy.AddField_management(ptobj_center, 'end_id', 'TEXT')
            ##cur_cent = arcpy.InsertCursor(tmp1)
            ##keys = towers.keys()
            ##for i in range(len(keys)):
                ##if i<len(keys)-1:
                    ##start_tower, end_tower = towers[keys[i]], towers[keys[i+1]]
                    ##if start_tower['geo_x'] is None or start_tower['geo_y'] is None or end_tower['geo_x'] is None or end_tower['geo_y'] is None :
                        ##continue
                    
                    ##p.X, p.Y = (start_tower['geo_x'] + end_tower['geo_x'])/2.0, (start_tower['geo_y'] + end_tower['geo_y'])/2.0
                    ##feat = cur_cent.newRow()
                    ##feat.shape = p
                    ##feat.center_id = str(uuid.uuid4()).upper()
                    ##feat.start_id = start_tower['id']
                    ##feat.end_id = end_tower['id']
                    ##cur_cent.insertRow(feat)
            ##del cur_cent
            
            ##ExtractValuesToPoints(in_point_features=tmp, in_raster=dem_raster, out_point_features=out_name,)
            ##arcpy.AddMessage(arcpy.GetMessages())
            
        #20131123   
        #ExtractValuesToPoints(in_point_features=tmp3d, in_raster=dem_raster, out_point_features=out_3D_name,)
        #arcpy.AddMessage(arcpy.GetMessages())
        
        #sqls = []
        #cur_update = arcpy.UpdateCursor(out_3D_name)
        
        #for row in cur_update:
            #tower_id = row.getValue('tower_id')
            #p = row.getValue('Shape').firstPoint
            #p.Z = row.RASTERVALU
            #row.setValue('Shape', p)
            #cur_update.updateRow(row)
            #sql = """ UPDATE  TABLE_TOWER SET geo_z=%f WHERE id='%s'""" % (float(row.getValue('RASTERVALU')), tower_id)
            #sqls.append(sql)
        #del cur_update
        
        #odbc_execute_sqls(sqls, area)
        
        if arcpy.Exists(tmp):
            arcpy.Delete_management(tmp)
        if arcpy.Exists(tmp3d):
            arcpy.Delete_management(tmp3d)

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

    
def create_tower_multipatch_shape(towers,  out_path, out_name, dem_raster):
    ret = False
    tmp = '_'+out_name
    arcpy.CheckOutExtension("Spatial")
    if len(towers.keys())>0:
        env.workspace = out_path
        if arcpy.Exists(out_name):
            arcpy.Delete_management(out_name)
        if arcpy.Exists(tmp):
            arcpy.Delete_management(tmp)
        ptobj = arcpy.CreateFeatureclass_management(out_path=out_path, out_name=tmp, geometry_type='POINT',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='ENABLED')
        #print(arcpy.GetMessages())
        
        arcpy.AddField_management(ptobj, 'tower_id', 'TEXT')
        arcpy.AddField_management(ptobj, 'tower_name', 'TEXT')
        arcpy.AddField_management(ptobj, 'tower_code', 'TEXT')
        arcpy.AddField_management(ptobj, 'model_code', 'TEXT')
        arcpy.AddField_management(ptobj, 'height', 'DOUBLE')
        arcpy.AddField_management(ptobj, 'rotate', 'DOUBLE')
        arcpy.AddField_management(ptobj, 'line_name', 'TEXT')
        arcpy.AddField_management(ptobj, 'line_code', 'TEXT')
        arcpy.AddField_management(ptobj, 'line_id', 'TEXT')
        cur = arcpy.InsertCursor(tmp)
        p = arcpy.Point()
        id = 1
        for key in towers.keys():
            p.X, p.Y, p.Z = towers[key]['geo_x'], towers[key]['geo_y'], towers[key]['geo_z']
            id += 1
            feat = cur.newRow()
            feat.shape = p
            feat.tower_id = key
            if towers[key].has_key('tower_name'):
                feat.tower_name = towers[key]['tower_name']
            if towers[key].has_key('tower_code'):
                feat.tower_code = towers[key]['tower_code']
            if towers[key].has_key('model_code'):
                feat.model_code = towers[key]['model_code']
            if towers[key].has_key('height'):
                feat.height = towers[key]['height']
            if towers[key].has_key('rotate'):
                feat.rotate = towers[key]['rotate']
            if towers[key].has_key('line_name'):
                feat.line_name = towers[key]['line_name']
            if towers[key].has_key('line_code'):
                feat.line_code = towers[key]['line_code']
            if towers[key].has_key('line_id'):
                feat.line_id = towers[key]['line_id']
            cur.insertRow(feat)
        del cur
        
        
        ExtractValuesToPoints(in_point_features=tmp, in_raster=dem_raster, out_point_features=out_name,)
        print(arcpy.GetMessages())
        cur = arcpy.UpdateCursor(out_name)
        for row in cur:
            #row.Shape.firstPoint.Z = row.Shape.firstPoint.Z + row.RASTERVALU
            p = row.getValue('Shape').firstPoint
            p.Z = p.Z + row.RASTERVALU
            row.setValue('Shape', p)
            cur.updateRow(row)
        del cur
        
        if arcpy.Exists(tmp):
            arcpy.Delete_management(tmp)

    return ret            

def create_lines_layers(area):
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn(area)
    #lines = get_data_from_rdbms(rdb_conn_path, database, 'TABLE_LINE', ' 1=1')
    lines = odbc_get_records( 'TABLE_LINE', '1=1', area)
    #dem_raster = 'sde.DBO.%s' % DEM_NAME
    dem_raster = DEM_NAME
    l = []
    for line in lines:
        if line['line_name'] in AREA_DATA[area]:
            #create_lines_layer(area, kmgdgeo, line['line_name'],  line['id'])
            towers = odbc_get_sorted_tower_by_line(line['id'], area)
            d = {}
            d['line_name'] = line['line_name']
            d['voltage'] = line['voltage']
            d['towers'] = towers
            l.append(d)
    create_line_polyline_shape(l, kmgdgeo, 'line_%s' % area, area)

        
    
def create_towers_layers(area):
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn(area)
    #lines = get_data_from_rdbms(rdb_conn_path, database, 'TABLE_LINE', ' 1=1')
    lines = odbc_get_records('TABLE_LINE', '1=1', area)
    #dem_raster = 'sde.DBO.%s' % DEM_NAME
    env.workspace = kmgdgeo
    dem_raster = DEM_NAME
    #for line in lines:
        #print(line['line_name'])
        #create_towers_layer(kmgdgeo, line['id'], dem_raster)
    l = []    
    for line in lines:
        if line['line_name'] in AREA_DATA[area]:
            #create_lines_layer(area, kmgdgeo, line['line_name'],  line['id'])
            towers = odbc_get_sorted_tower_by_line(line['id'], area)
            d = {}
            d['line_name'] = line['line_name']
            d['towers'] = towers
            l.append(d)
    create_tower_point_shape(l, kmgdgeo, 'towers_%s' % area, 'towers3D_%s' % area,  dem_raster, area)
        
        
        
    
def create_towers_layer(geo_conn_path,  line_id, dem_raster):
    #towers = sde_get_sorted_tower_by_line(rdb_conn_path,  database,  line_id)
    towers = odbc_get_sorted_tower_by_line(line_id)
    #create_tower_point_shape(towers, geo_conn_path, 'towers_' + line_id.replace('-',''), 'towers3D_' + line_id.replace('-',''),  dem_raster, )
    create_tower_point_shape(towers, geo_conn_path, 'towers_%s' % area, 'towers3D_%s' % area,  dem_raster, )
    
def create_lines_layer(area, geo_conn_path,  line_name, line_id):
    towers = odbc_get_sorted_tower_by_line(line_id, area)   
    #create_line_polyline_shape(area, line_name, towers, geo_conn_path, 'line_' + line_id.replace('-',''))
    create_line_polyline_shape(line_name, towers, geo_conn_path, 'line_%s' % area)

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
                
                
                
        
        
def clear_towers(geo_conn_path, area=None):
    env.workspace = geo_conn_path
    if area:
        towers = arcpy.ListFeatureClasses('*towers_%s' % area)
    else:
        towers = arcpy.ListFeatureClasses('*towers_*')
    for i in towers:
        arcpy.Delete_management(i)
    if area:
        towers3d = arcpy.ListFeatureClasses('*towers3D_%s' % area)
    else:
        towers3d = arcpy.ListFeatureClasses('*towers3D_*' )
    for i in towers3d:
        arcpy.Delete_management(i)
        
def clear_lines(geo_conn_path, area=None):
    env.workspace = geo_conn_path
    if area:
        lines = arcpy.ListFeatureClasses('*line_%s' % area)
    else:
        lines = arcpy.ListFeatureClasses('*line_*' )
    for i in lines:
        arcpy.Delete_management(i)
    #print(lines)
    
def clear_segments(geo_conn_path, area=None):
    env.workspace = geo_conn_path
    if area:
        lines = arcpy.ListFeatureClasses('*segment_%s' % area)
    else:
        lines = arcpy.ListFeatureClasses('*segment_*' )
    for i in lines:
        arcpy.Delete_management(i)
    
def test_update_rotate_null():
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    env.workspace = kmgdgeo
    lines = arcpy.ListFeatureClasses('*towers_*')
    for line in lines:
        cur = arcpy.UpdateCursor(line)
        for row in cur:
            #print(row.rotate)
            if row.rotate is None:
                print(row.tower_name)
                row.rotate = 0.0
                cur.updateRow(row)
        del cur
    
    
def admin_create_towers_layers(area):
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn(area)
    #geo_conn_path = r'G:\work\csharp\kmgdgis\data\local_workspace\local.gdb'
    clear_towers(kmgdgeo, area)
    create_towers_layers(area)
    #odbc_update_towers_rotate()


def admin_create_lines_layers(area):
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn(area)
    clear_lines(kmgdgeo, area)
    create_lines_layers(area)

def calc_one_attach_point(point, adder_x=0, adder_y=0, adder_z=0, degree_offset = 90):
    pt = point.copy()
    #point['offset_y'] *= -1
    adder_x = abs(adder_x) 
    
    if point['offset_x']>0:
        point['offset_x'] += adder_x
    else:
        point['offset_x'] -= adder_x
    point['offset_y'] += adder_y
    point['offset_z'] += adder_z
    a = 1./(3600.0*30.887)
    one_meter_of_lat_deg = a * np.cos(np.deg2rad(point['geo_y']))
    
    #pt['geo_x'] = point['geo_x'] + point['offset_x'] * (1./(3600*30.887)) * np.cos(np.deg2rad(point['rotate'] + degree_offset)) + point['offset_y'] * (1./(3600*30.887)) * np.sin(np.deg2rad(point['rotate'] + degree_offset))
    #pt['geo_y'] = point['geo_y'] + point['offset_x'] * (1./(3600*30.887)) * np.sin(np.deg2rad(point['rotate'] + degree_offset)) / np.cos(np.deg2rad(point['geo_y'])) - point['offset_y'] * (1./(3600*30.887)) * np.cos(np.deg2rad(point['rotate'] + degree_offset)) / np.cos(np.deg2rad(point['geo_y']))
    #pt['geo_z'] = point['geo_z'] + point['offset_z']
    point['offset_x'] *= -1
    pt['geo_x'] = point['geo_x'] + point['offset_x'] * one_meter_of_lat_deg * np.cos(np.deg2rad(point['rotate'] + degree_offset)) + point['offset_y'] * one_meter_of_lat_deg * np.sin(np.deg2rad(point['rotate'] + degree_offset))
    pt['geo_y'] = point['geo_y'] + point['offset_x'] * a * np.sin(np.deg2rad(point['rotate'] + degree_offset))  - point['offset_y'] * a * np.cos(np.deg2rad(point['rotate'] + degree_offset)) 
    pt['geo_z'] = point['geo_z'] + point['offset_z']
    
    
    
    
    return pt

def calc_point_pair_segment(row,  interp_num=15, is_use_catenary=True):
    ret = []
    start , end = {}, {}
    start['geo_x'] = float(row['start_geo_x'])
    start['geo_y'] = float(row['start_geo_y'])
    start['geo_z'] = float(row['start_geo_z'])
    start['offset_x'] = row['start_offset_x']
    start['offset_y'] = row['start_offset_y']
    start['offset_z'] = row['start_offset_z']
    
    end['geo_x'] = float(row['end_geo_x'])
    end['geo_y'] = float(row['end_geo_y'])
    end['geo_z'] = float(row['end_geo_z'])
    end['offset_x'] = row['end_offset_x']
    end['offset_y'] = row['end_offset_y']
    end['offset_z'] = row['end_offset_z']
    r1 = float(row['start_rotate'])
    r2 = float(row['end_rotate'])
    start['rotate'] = r1
    end['rotate'] = r2
    start , end = calc_one_attach_point(start), calc_one_attach_point(end)
    dx = (end['geo_x']-start['geo_x'])/(interp_num+1)
    dy = (end['geo_y']-start['geo_y'])/(interp_num+1)
    dz = (end['geo_z']-start['geo_z'])/(interp_num+1)
    l, h, cdx = 0.,  0.,  0.
    if is_use_catenary:
        l = catenary.distance((start['geo_y'],start['geo_x']), (end['geo_y'],end['geo_x']) )
        h = end['geo_z'] - start['geo_z']
        cdx = l/(interp_num+1)
        
            
    
    for i in range(interp_num+1):
        if is_use_catenary:
            #20131125
            if l <= 100:
                row['tensor_T0'],  row['w'] = 0.5, 0.001
            elif l>100 and l <= 200:
                row['tensor_T0'],  row['w'] = 0.6, 0.001
            elif l > 200 and l<=300:
                row['tensor_T0'],  row['w'] = 0.7, 0.001
            elif l > 300 and l<=400:
                row['tensor_T0'],  row['w'] = 1.1, 0.001
            elif l > 400 and l<=500:
                row['tensor_T0'],  row['w'] = 1.2, 0.001
            elif l > 500:
                row['tensor_T0'],  row['w'] = 1.4, 0.001
            #print('l=%f, tensor_T0=%f, w=%f' % (l, row['tensor_T0'],  row['w']))
            x = i * cdx
            y = catenary.f( l,  h,  start['geo_z'],  x,  row['tensor_T0'],  row['w'] )
            X, Y, Z = start['geo_x']+i*dx,   start['geo_y']+i*dy,  y
            #print('y=%f' % y)
        else:
            X, Y, Z = start['geo_x']+i*dx,   start['geo_y']+i*dy,  start['geo_z']+i*dz
        ret.append((X, Y, Z))
    X, Y, Z = end['geo_x'],   end['geo_y'],  end['geo_z']
    ret.append((X, Y, Z))
    
    return ret

    
    
def create_segments(line_name=None, max_tower=0):
    print('Generate segments...')
    kmgd, kmgdgeo, kmgdgeotmp  = create_sde_conn()
    database = DATABASE_RDBMS
    if line_name:
        lines = odbc_get_records('TABLE_LINE' ,"line_name='%s'" % line_name)
    else:   
        lines = odbc_get_records('TABLE_LINE' )
    for line in lines:
        print(line['line_name'])
        create_segment_by_line(kmgd, kmgdgeo,  database, line['id'], max_tower)


def get_single_side_contact(tower_id, side, contact_index, position, area):
    #env.workspace = rdb_conn_path
    whereclause = " tower_id='%s' and side='%s' and contact_index='%s' and position='%s'" % (tower_id, side, contact_index, position)
    #tbname = r'%s.dbo.%s' % (database, 'VIEW_SINGLE_SIDE_CONTACT')
    rows = odbc_get_records('VIEW_SINGLE_SIDE_CONTACT',whereclause, area)
    return rows
    #rows = arcpy.SearchCursor(tbname, whereclause)
    #contacts = []
    #for row in rows:
        #contact = {}
        #contact['tower_id'] = row.getValue('tower_id')
        #contact['geo_x'] = row.getValue('geo_x')
        #contact['geo_y'] = row.getValue('geo_y')
        #contact['geo_z'] = row.getValue('geo_z')
        #contact['offset_x'] = row.getValue('offset_x')
        #contact['offset_y'] = row.getValue('offset_y')
        #contact['offset_z'] = row.getValue('offset_z')
        #contact['rotate'] = row.getValue('rotate')
        #contact['contact_index'] = row.getValue('contact_index')
        #contact['side'] = row.getValue('side')
        #contacts.append(contact)
    #del rows
    #return contacts
    
    
    
def create_segments_by_line_id(area, line_id, min_tower=0, max_tower=0):
    model_code_list = []
    towers_sort = odbc_get_sorted_tower_by_line(line_id, area)
    tower_info_list = odbc_get_records('TABLE_TOWER_MODEL', '1=1', area)
    
    for i in range(len(towers_sort)):
        #if i>20:
            #break
        if i<len(towers_sort)-1:
            if i<min_tower:
                continue
            if max_tower>0:
                if i+1>max_tower:
                    break
            start_tower_id, end_tower_id = towers_sort[i]['id'], towers_sort[i+1]['id']
            #start_model_code = get_suitable_model_code(tower_info_list, towers_sort[i]['model_code'], towers_sort[i]['line_position'], area)
            #end_model_code = get_suitable_model_code(tower_info_list, towers_sort[i+1]['model_code'], towers_sort[i+1]['line_position'], area)
            start_model_code = towers_sort[i]['model_code_height']
            end_model_code   = towers_sort[i+1]['model_code_height']
            
                
                
            
            l_1, l_2 = [], []
            start_position,end_position = towers_sort[i]['line_position'], towers_sort[i+1]['line_position']
            l_1 = odbc_get_records('TABLE_CONTACT_POINT', " model_code='%s' AND side='%s' " % (start_model_code, u'反' ), area)
            l_2 = odbc_get_records('TABLE_CONTACT_POINT', " model_code='%s' AND side='%s' " % (end_model_code, u'正' ), area)
                
            if len(l_1)==0:
                print(u"前一杆塔 model_code='%s' and side='%s' and position='%s' 未找到挂线点" % (start_model_code, u'反', start_position))
                continue
            if len(l_2)==0:
                print(u"后一杆塔  model_code='%s' and side='%s' and position='%s' 未找到挂线点" % (end_model_code, u'正', end_position))
                continue
            
            contact_id_list = []
            for i1 in l_1:
                for i2 in l_2:
                    #if i1['side']== u'正' and i2['side']==u'反' and i1['position']==i2['position'] and i1['contact_index']==i2['contact_index']:
                    if i1['side']== u'反' and i2['side']==u'正':
                        phase = 'D'
                        if i1['contact_index'] == 0 and i2['contact_index'] == 0 and i1['position'] in [ u'地左', ]:
                            phase = 'N'
                        if i1['contact_index'] == 0 and i2['contact_index'] == 0 and i1['position'] in [u'地右',u'地单']:
                            phase = 'K'
                        if i1['contact_index'] == 0 and i2['contact_index'] == 0 and i1['position'] in [u'通左',u'通右',u'通单']:
                            phase = 'O'
                        if i1['contact_index'] == 1 and i2['contact_index'] == 1:
                            phase = 'A'
                        if i1['contact_index'] == 2 and i2['contact_index'] == 2:
                            phase = 'B'
                        if i1['contact_index'] == 3 and i2['contact_index'] == 3:
                            phase = 'C'
                        if  i1['contact_index'] ==  i2['contact_index'] and i1['position']==i2['position']:
                            contact_id_list.append((i1['id'], i2['id'], phase))
                    
            print(u'[%s]-[%s]segs=%d' % (gTowerDict[start_tower_id]['tower_name'], gTowerDict[end_tower_id]['tower_name'], len(contact_id_list)))
            update_segment_by_start_end(area, towers_sort, line_id, start_tower_id, end_tower_id, contact_id_list)
    
    
def test_create_segments_by_line_id(line_name, area):
    #line_name = u'永发I回线'
    #line_name = u'永甘乙线'
    #max_tower = 37
    #min_tower = 35
    max_tower = 54
    min_tower = 53
    if line_name:
        lines = odbc_get_records('TABLE_LINE' ,"line_name='%s'" % line_name, area)
    else:   
        lines = odbc_get_records('TABLE_LINE','1=1', area )
    for line in lines:
        print(line['line_name'])
        create_segments_by_line_id(area, line['id'], min_tower, max_tower)
    
def create_segments_by_area(area):
    global gTowerDict
    if len(gTowerDict.keys())==0:
        ts = odbc_get_records('TABLE_TOWER', '1=1', area)
        for t in ts:
            gTowerDict[t['id']] = t
    
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn(area)
    clear_segments(kmgdgeo)
    max_tower = 0
    min_tower = 0
    #if line_name:
        #lines = odbc_get_records('TABLE_LINE' ,"line_name='%s'" % line_name)
    #else:   
    lines = odbc_get_records('TABLE_LINE', '1=1', area)
    for line in lines:
        if line['line_name'] in AREA_DATA[area]:
            if line['line_name'] in [u'永发II回线',u'永发I回线']:
            #if line['line_name'] in [u'永发II回线']:
                print(line['line_name'])
                create_segments_by_line_id(area, line['id'], min_tower, max_tower)
    
    
    
    
    
    
def update_segment_by_start_end(area, towers_sort, line_id, start_tower_id, end_tower_id, contact_id_list):
    global gTowerDict
    if len(gTowerDict.keys())==0:
        ts = odbc_get_records('TABLE_TOWER', '1=1', area)
        for t in ts:
            gTowerDict[t['id']] = t
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn(area)
    ret = 'ok'
    whereclause = "start_tower_id='%s' AND end_tower_id='%s'" % (start_tower_id, end_tower_id)
    #20131123
    ##sql = """DELETE FROM  TABLE_WIRE_SEGMENT WHERE %s""" % whereclause
    ##odbc_execute_sqls([sql], area)
    
    env.workspace = kmgdgeo
    out_name = 'segment_' + area
    
    
    try:
        if not arcpy.Exists(out_name):
            segobj = arcpy.CreateFeatureclass_management(out_path=kmgdgeo, out_name=out_name , geometry_type='POLYLINE',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='ENABLED')
            arcpy.AddField_management(segobj, 'segid', 'TEXT')
            arcpy.AddField_management(segobj, 'start_tower_id', 'TEXT')
            arcpy.AddField_management(segobj, 'end_tower_id', 'TEXT')
            arcpy.AddField_management(segobj, 'start_contact_id', 'TEXT')
            arcpy.AddField_management(segobj, 'end_contact_id', 'TEXT')
            arcpy.AddField_management(segobj, 'phase', 'TEXT')
            arcpy.AddField_management(segobj, 'line_id', 'TEXT')
    
        cur = arcpy.UpdateCursor(out_name, whereclause)
        for row in cur:
            cur.deleteRow(row)
        del cur
    except:
        print(sys.exc_info()[1])
        
        
    wiresegs = []
    for t in contact_id_list:
        start_contact_id = t[0]
        end_contact_id = t[1]
        phase = 'D'
        if len(t)>2:
            phase = t[2]
        seg = {}
        seg['start_tower_id'] = start_tower_id
        seg['end_tower_id'] = end_tower_id
        seg['start_contact_id'] = start_contact_id
        seg['end_contact_id'] = end_contact_id
        seg['phase'] = phase
        wiresegs.append(seg)
        
            
    if len(wiresegs)>0:
        #20131123
        #odbc_update_segment_by_start_end(wiresegs, area)
        env.workspace = kmgdgeo
        cur = arcpy.InsertCursor(out_name)
        
        polylines = create_polyline_by_endpoint( towers_sort, line_id, start_tower_id, end_tower_id, area)
        for polyline in polylines:
            feat = cur.newRow()
            pointlist = polyline['pointlist']
            arr = arcpy.Array()
            for pt in pointlist:
                p = arcpy.Point(X=pt[0], Y=pt[1], Z=pt[2])
                arr.add(p)
            line =  arcpy.Polyline(arr, arcpy.SpatialReference(text='WGS 1984'),)
            try:
                feat.shape = line
            except:
                print(sys.exc_info()[1])
            feat.segid = polyline['segid']
            feat.start_tower_id = polyline['start_tower_id']
            feat.end_tower_id = polyline['end_tower_id']
            feat.phase = polyline['phase']
            feat.start_contact_id = polyline['start_contact_id']
            feat.end_contact_id = polyline['end_contact_id']
            feat.line_id = line_id
            cur.insertRow(feat)
        del cur
    else:
        ret = 'no segment added'
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
    
    
    
    
    
def create_segment_by_line(rdb_conn_path, geo_conn_path,  database, line_id, max_tower=0):
    towers = odbc_get_sorted_tower_by_line(line_id)
    
    out_name = 'segment_' + line_id.replace('-','').upper()
    env.workspace = geo_conn_path
    if arcpy.Exists(out_name):
        arcpy.Delete_management(out_name)
    segobj = arcpy.CreateFeatureclass_management(out_path=geo_conn_path, out_name=out_name , geometry_type='POLYLINE',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='ENABLED')
    arcpy.AddField_management(segobj, 'segid', 'TEXT')
    arcpy.AddField_management(segobj, 'start_tower_id', 'TEXT')
    arcpy.AddField_management(segobj, 'end_tower_id', 'TEXT')
    arcpy.AddField_management(segobj, 'start_contact_index', 'SHORT')
    arcpy.AddField_management(segobj, 'end_contact_index', 'SHORT')
    arcpy.AddField_management(segobj, 'phase', 'TEXT')
    cur = arcpy.InsertCursor(out_name)
    
    
    
    
    start_tower, end_tower = None, None
    for tower in towers:
        if max_tower>0:
            if towers.index(tower)==max_tower:
                break
        end_tower = tower
        if start_tower and end_tower:
            print(u'起始[%s]-终止[%s]' % (start_tower['tower_name'], end_tower['tower_name']))
            polylines = create_polyline_by_endpoint(rdb_conn_path, geo_conn_path,  database,  None, towers, line_id, start_tower['id'], end_tower['id'] )
            for polyline in polylines:
                feat = cur.newRow()
                pointlist = polyline['pointlist']
                arr = arcpy.Array()
                for pt in pointlist:
                    p = arcpy.Point(X=pt[0], Y=pt[1], Z=pt[2])
                    arr.add(p)
                line =  arcpy.Polyline(arr, arcpy.SpatialReference(text='WGS 1984'),)
                feat.shape = line
                feat.segid = polyline['segid']
                feat.start_tower_id = polyline['start_tower_id']
                feat.end_tower_id = polyline['end_tower_id']
                feat.start_contact_index = polyline['start_contact_index']
                feat.end_contact_index = polyline['end_contact_index']
                feat.phase = polyline['phase']
                cur.insertRow(feat)
            
        start_tower = end_tower
        if end_tower == towers[len(towers)-1]:
            break
    
    del cur
    
    
        
def create_polyline_by_endpoint( towers_sort, line_id, start_tower_id, end_tower_id,  area):
    def is_same_sign(a1, a2):
        ret = False
        if a1>0 and a2>0:
            ret = True
        elif a1<0 and a2<0:
            ret = True
        elif a1 == a2:
            ret = True
        return ret
        
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn(area)
    env.workspace = kmgdgeo
    #center_altitude = get_center_altitude()
    ret = []
    
    T0, w = get_conductor_T0_w_by_segment(towers_sort, line_id, start_tower_id, end_tower_id, area)
    if T0==0 and w==0:
        T0, w = get_ground_left_T0_w_by_segment(towers_sort, line_id, start_tower_id, end_tower_id, area)
    if T0==0 and w==0:
        T0, w = get_ground_right_T0_w_by_segment(towers_sort, line_id, start_tower_id, end_tower_id, area)
    #if T0==0 and w==0:
        #T0, w = 1.1, 0.001
    if T0 < 1.0:
        T0, w = 0.9, 0.001
        
        
    print('tensor_T0=%f, w=%f' % (T0, w))
    #if segs:
        #wiresegs = segs
    #else:
        ##wiresegs = get_data_from_rdbms(rdb_conn_path, database,'VIEW_CONTACT_POINT', "start_tower_id='%s' AND end_tower_id='%s' AND start_side='%s' AND end_side='%s'" % (start_tower_id, end_tower_id, u'正', u'反')) 
    #wiresegs = odbc_get_records('VIEW_CONTACT_POINT', "start_tower_id='%s' AND end_tower_id='%s' AND start_side='%s' AND end_side='%s' AND start_contact_id='%s' AND end_contact_id='%s'" % (start_tower_id, end_tower_id, u'正', u'反', start_contact_id, end_contact_id), area)
    cond = "start_tower_id='%s' AND end_tower_id='%s' AND start_side='%s' AND end_side='%s'" % (start_tower_id, end_tower_id, u'反', u'正')
    #print('select from VIEW_CONTACT_POINT where %s' % cond)
    wiresegs = odbc_get_records('VIEW_CONTACT_POINT', cond, area)
        
    for seg in wiresegs:
        #if is_same_sign(seg['start_offset_x'], seg['end_offset_x']):
        d = {}
        d['segid'] = seg['id']
        d['start_tower_id'] = seg['start_tower_id']
        d['end_tower_id'] = seg['end_tower_id']
        d['start_contact_id'] = seg['start_contact_id']
        d['end_contact_id'] = seg['end_contact_id']
        d['phase'] = seg['phase']
        seg['tensor_T0'] = T0
        seg['w'] = w
        pts = calc_point_pair_segment(seg)
        #isok = check_geo_z(center_altitude, pts, seg)
        #while not isok:
            #print('If tensor_T0=%f, w=%f, lowest point is less than %f and may be underground.' % (seg['tensor_T0'], seg['w'], center_altitude))
            #seg['tensor_T0'] *= 1.1
            #seg['w'] *= 1.1
            #print('Take tensor_T0=%f and recalculating...' % seg['tensor_T0'])
            #pts = calc_point_pair_segment(seg)
            #isok = check_geo_z(center_altitude, pts, seg)
        
        d['pointlist'] = pts
        ret.append(d)
    return ret        


        
    
    

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

def create_sde_conn(area):
    global gConfig
    d = os.path.dirname(SDE_DIR)
    if not os.path.exists(d):
        os.mkdir(d)
    if not os.path.exists(SDE_DIR):
        os.mkdir(SDE_DIR)
    kmgd = None #os.path.join(SDE_DIR, SDE_FILE_KMGD)
    kmgdgeo = os.path.join(SDE_DIR, gConfig['odbc'][area]['sde_file'])
    kmgdgeotmp = None #os.path.join(SDE_DIR, SDE_FILE_KMGDGEO_TMP)
    #if not os.path.exists(kmgd):
        #if len(DATABASE_INSTANCE)>0:
            #arcpy.CreateDatabaseConnection_management(out_folder_path=SDE_DIR, out_name=SDE_FILE_KMGD, database_platform='SQL_SERVER', instance='%s\\%s' % (DATABASE_SERVER, DATABASE_INSTANCE),account_authentication='DATABASE_AUTH',username=DATABASE_USERNAME, password=DATABASE_PASSWORD,  database=DATABASE_RDBMS)
        #else:
            #arcpy.CreateDatabaseConnection_management(out_folder_path=SDE_DIR, out_name=SDE_FILE_KMGD, database_platform='SQL_SERVER', instance='%s' % DATABASE_SERVER,account_authentication='DATABASE_AUTH',username=DATABASE_USERNAME, password=DATABASE_PASSWORD,  database=DATABASE_RDBMS)
    #if not os.path.exists(kmgdgeo):
        ##arcpy.CreateDatabaseConnection_management(out_folder_path=SDE_DIR, out_name=SDE_FILE_KMGDGEO, database_platform='SQL_SERVER', instance=r'XIEJUN-DESKTOP\SQLEXPRESS',account_authentication='DATABASE_AUTH',username='sa', password='sa', database='sde')
        #arcpy.CreateArcSDEConnectionFile_management(out_folder_path=SDE_DIR, out_name=SDE_FILE_KMGDGEO, server=DATABASE_SERVER, service=DATABASE_GEO_PORT,  account_authentication='DATABASE_AUTH',username=DATABASE_USERNAME, password=DATABASE_PASSWORD, save_username_password='SAVE_USERNAME', database=DATABASE_GEO)
    #if not os.path.exists(kmgdgeotmp):
        #arcpy.CreateArcSDEConnectionFile_management(out_folder_path=SDE_DIR, out_name=SDE_FILE_KMGDGEO_TMP, server=DATABASE_SERVER, service=DATABASE_GEO_TMP_PORT,  account_authentication='DATABASE_AUTH',username=DATABASE_USERNAME, password=DATABASE_PASSWORD, save_username_password='SAVE_USERNAME', database=DATABASE_GEO_TMP)
        ##arcpy.CreateDatabaseUser_management
    
    if not os.path.exists(kmgdgeo):
        if len(gConfig['odbc'][area]['db_instance'])>0:
            #arcpy.CreateArcSDEConnectionFile_management(out_folder_path=SDE_DIR, out_name=gConfig['odbc'][area]['sde_file'], server='%s\\%s' % (gConfig['odbc'][area]['db_server'], gConfig['odbc'][area]['db_instance']), service=gConfig['odbc'][area]['sde_port'],  account_authentication='DATABASE_AUTH',username=gConfig['odbc'][area]['db_username'], password=gConfig['odbc'][area]['db_password'], save_username_password='SAVE_USERNAME', database=gConfig['odbc'][area]['sde_name'])
            arcpy.CreateDatabaseConnection_management(out_folder_path=SDE_DIR, out_name=gConfig['odbc'][area]['sde_file'], database_platform='SQL_SERVER',  instance='%s\\%s' % (gConfig['odbc'][area]['db_server'], gConfig['odbc'][area]['db_instance']),   account_authentication='DATABASE_AUTH',username=gConfig['odbc'][area]['db_username'], password=gConfig['odbc'][area]['db_password'],  database=gConfig['odbc'][area]['sde_name'])
        else:
            #arcpy.CreateArcSDEConnectionFile_management(out_folder_path=SDE_DIR, out_name=gConfig['odbc'][area]['sde_file'], server=gConfig['odbc'][area]['db_server'], service=gConfig['odbc'][area]['sde_port'],  account_authentication='DATABASE_AUTH',username=gConfig['odbc'][area]['db_username'], password=gConfig['odbc'][area]['db_password'], save_username_password='SAVE_USERNAME', database=gConfig['odbc'][area]['sde_name'])
            arcpy.CreateDatabaseConnection_management(out_folder_path=SDE_DIR, out_name=gConfig['odbc'][area]['sde_file'], database_platform='SQL_SERVER',  instance='%s' % gConfig['odbc'][area]['db_server'],   account_authentication='DATABASE_AUTH',username=gConfig['odbc'][area]['db_username'], password=gConfig['odbc'][area]['db_password'],  database=gConfig['odbc'][area]['sde_name'])
    return kmgd, kmgdgeo, kmgdgeotmp


def get_data_from_rdbms(rdb_conn_path, database, table, where_clause, flds=None):
    ret = {}
    root = ''
    tbname = '%s.dbo.%s' % (database, table)
    env.workspace = rdb_conn_path
    if arcpy.Exists(tbname):
        fc = tbname
        rows = arcpy.SearchCursor(fc, where_clause=where_clause)
        fields = arcpy.ListFields(fc, '', '')
        if flds:
            for row in rows:
                #print(dir(row))
                d = {}
                id = None
                for fld in fields:
                    if fld.name in flds:
                        if isinstance(row.getValue(fld.name), str) or isinstance(row.getValue(fld.name), unicode):
                            relist = re.findall(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', row.getValue(fld.name))
                            if len(relist)>0:
                                d[fld.name] = row.getValue(fld.name).upper().replace('{','').replace('}','')
                                if fld.name in ['id']:
                                    id = d[fld.name]
                            else:
                                d[fld.name] = row.getValue(fld.name)
                        else:
                            d[fld.name] = row.getValue(fld.name)
                if id:
                    ret[id] = d
        else:
            for row in rows:
                #print(dir(row))
                d = {}
                id = None
                for fld in fields:
                    v = row.getValue(fld.name)
                    if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0 and v[0]=='{' and v[-1]=='}':
                        v = v.upper().replace('{','').replace('}','')
                        if fld.name in ['id']:
                            id = v
                    d[fld.name] = v
                if id:
                    ret[id] = d
                else:
                    id = str(uuid.uuid4()).upper()
                    ret[id] = d
            
            
    else:
        arcpy.AddMessage('no table [%s] exist' % tbname)
        arcpy.AddMessage(arcpy.ListTables())
        
    return ret


def copy_sde_to_sdetmp():
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    env.workspace = kmgdgeo
    fs = []
    l = arcpy.ListFeatureClasses()
    for i in l:
        if 'towers_' in i or 'line_' in i or 'segment_' in i:
            fs.append(i.replace('sde.DBO.', ''))
    env.workspace = kmgdgeotmp
    for i in fs:
        #n = i.replace('sde.DBO.', '')
        #name = 'sde_tmp.DBO.' + n
        if arcpy.Exists(i):
            print('delete exist %s ...' % i)
            arcpy.Delete_management(i)
        print('copying %s ...' % i)
        arcpy.CopyFeatures_management(os.path.join(kmgdgeo, i), os.path.join(kmgdgeotmp, i))
        print(arcpy.GetMessages())


def copy_sde_to_sde(src, dest):
    srcsde = os.path.join(SDE_DIR, src)
    destsde = os.path.join(SDE_DIR, dest)
    env.workspace = srcsde
    fs = []
    l = arcpy.ListFeatureClasses()
    for i in l:
        if 'towers_' in i or 'line_' in i or 'segment_' in i or 'towers3D_' in i or 'segment3D_' in i:
            fs.append(i.replace('sde.DBO.', ''))
    env.workspace = destsde
    for i in fs:
        #n = i.replace('sde.DBO.', '')
        #name = 'sde_tmp.DBO.' + n
        if arcpy.Exists(i):
            print('delete exist %s ...' % i)
            arcpy.Delete_management(i)
        print('copying %s ...' % i)
        arcpy.CopyFeatures_management(os.path.join(srcsde, i), os.path.join(destsde, i))
        arcpy.AddMessage(arcpy.GetMessages())
    
    
    
    

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

def copy_features(src_ws,  dest_ws,  obj):
    tmp = '_tmp_%s' % str(uuid.uuid4()).upper().replace('-','')
    env.workspace = src_ws
    fs = []
    if obj['type']=='line':
        for line in obj['lines']:
            fc = 'line_%s' % line['id'].replace('-','')
            if arcpy.Exists(fc.lower()) or arcpy.Exists(fc) or arcpy.Exists(fc.upper()):
                cur = arcpy.SearchCursor(fc)
                for row in cur:
                    p = row.getValue('Shape')
                    if not p in fs:
                        fs.append(p)
                del cur
            
        if len(fs)>0:
            env.workspace = dest_ws
            lineobj = arcpy.CreateFeatureclass_management(out_path=dest_ws, out_name=tmp, geometry_type='POLYLINE',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='DISABLED')
            #cur = arcpy.InsertCursor(tmp)
            cur = arcpy.da.InsertCursor(tmp, ("SHAPE@"))
            for polyline in fs:
                #row = cur.newRow()
                #lineobj.shape = polyline
                #cur.insertRow(row)
                cur.insertRow((polyline,))
            del cur
            
    elif obj['type']=='tower':
        env.workspace = src_ws
        for tower in obj['towers']:
            fc = 'towers_%s' % tower['line_id'].replace('-','')
            if arcpy.Exists(fc.lower()) or arcpy.Exists(fc) or arcpy.Exists(fc.upper()):
                where_clause = "tower_id='%s'" % tower['id']
                cur = arcpy.SearchCursor(fc, where_clause)
                for row in cur:
                    p = row.getValue('Shape')
                    if not p in fs:
                        fs.append(p)
                del cur
        
        if len(fs)>0:
            env.workspace = dest_ws
            ptobj = arcpy.CreateFeatureclass_management(out_path=dest_ws, out_name=tmp, geometry_type='POINT',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='ENABLED')
            #cur = arcpy.InsertCursor(tmp)
            cur = arcpy.da.InsertCursor(tmp, ("SHAPE@"))
            for pt in fs:
                #row = cur.newRow()
                #lineobj.shape = polyline
                #cur.insertRow(row)
                cur.insertRow((pt,))
            del cur
    return tmp                
                


def test_GP():
    ret = None
    p = r"C:\Users\Jeffrey\AppData\Roaming\ESRI\Desktop10.1\ArcToolbox\My Toolboxes\kmgdgis.pyt"
    #if os.path.exists(p):
        #print('ok')
    #arcpy.ImportToolbox(r"C:\Users\Jeffrey\AppData\Roaming\ESRI\Desktop10.1\ArcToolbox\My Toolboxes\kmgdgis.pyt", "kmgdgis")
    arcpy.ImportToolbox(r"C:\Users\Jeffrey\AppData\Roaming\ESRI\Desktop10.1\ArcToolbox\My Toolboxes\kmgdgis.pyt", "kmgdgis")
    try:
        #ret = arcpy.Dispatch_kmgdgis('query_lines_layers', 'client', 'admin', 'admin', '')
        ret = arcpy.Dispatch_kmgdgis('query_towers_layers', 'client', 'admin', 'admin', '')
        #ret = arcpy.Dispatch_kmgdgis('update_line', 'client', 'admin', 'admin', test_json_line())
        #ret = arcpy.Dispatch_kmgdgis('update_tower', 'client', 'admin', 'admin', test_json_tower())
        #ret = arcpy.Dispatch_kmgdgis('update_segment', 'client', 'admin', 'admin', test_json_seg())
        #ret = arcpy.Dispatch_kmgdgis('analyse_buffer', 'client', 'admin', 'admin', test_json_buff())
    except:
        print(sys.exc_info()[1])
        #print(arcpy.GetMessages() )   
    if ret:
        #print(dir(ret))
        print('status=%s' % GP_STATUS[ret.status] )
        for i in range(ret.inputCount):
            print(ret.getInput(i))
    for i in range(ret.outputCount):
        ##print('%s=%s' % (p.name , p.value))
        ##print('Output%d=%s' % (i, type(ret[i])))
        print('Output%d=%s' % (i, ret.getOutput(i)))

def test_json_line():
    line = {'id':None,'line_code':'0501S15026847LAB847', 'line_name':'testline','box_north':0,'box_south':0,'box_east':0,'box_west':0,}
    obj = {'lines':[line,], 'is_delete':False}
    s = json.dumps(obj)
    #print(s)
    return s
    
def test_delete_tower():
    #delete
      #FROM [kmgd].[dbo].[TABLE_TOWER_ATTACH_POINT]
      #where tower_id not in (select id from TABLE_TOWER)
    #GO    
    ids = []
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    table = 'TABLE_TOWER'
    sdeConn = arcpy.ArcSDESQLExecute(kmgd)
    sql = """select convert(nvarchar(50), id) from  %s where line_id='%s'""" % (table, '2d38f0e2-3218-4562-80d1-2d38f9fa6d15')
    sdeReturn = sdeConn.execute(sql)
    if sdeReturn and not isinstance(sdeReturn, bool) and len(sdeReturn)>0:
        if isinstance(sdeReturn, unicode) or isinstance(sdeReturn, str):
            ids.append(sdeReturn)
        elif isinstance(sdeReturn, list):
            for i in sdeReturn:
                ids.append(i[0])
    del sdeConn
    
    arcpy.ImportToolbox(r"C:\Users\XIEJUN\AppData\Roaming\ESRI\Desktop10.1\ArcToolbox\My Toolboxes\kmgdgis.pyt", "kmgdgis")
    for id in ids:
        tower = {'id':id, 'line_id':'2D38F0E2-3218-4562-80D1-2D38F9FA6D15','tower_code':None, 'tower_name':None,'geo_x':102.4907,'geo_y':25.2245,'geo_z':0,'height':0, 'rotate':0, 'model_code':''}
        obj = {}
        obj['tower'] = tower
        obj['prev_tower_id'] = None
        obj['next_tower_id'] = None
        obj['is_delete'] = True
        obj['is_recalc_line'] = True
        obj['is_recalc_segment'] = True
        s = json.dumps(obj)
        ret = None
        try:
            ret = arcpy.Dispatch_kmgdgis('update_tower', 'client', 'admin', 'admin', s)
        except:
            print(sys.exc_info()[1])
        if ret:
            print('status=%s' % GP_STATUS[ret.status] )
        
    
    
def test_json_seg():
    obj = {}
    obj['line_id'] = 'FDB76D30-639E-40B9-B3F9-82975644EFAD'
    obj['start_point_index'] = 0
    obj['end_point_index'] = 0
    obj['prev_tower_id'] = '46A2EF51-67B1-48D5-9CBB-77ABE807984B'
    obj['next_tower_id'] = 'A3CD0892-3B20-4BD3-AA08-C99B06D2CE4D'
    obj['prev_tower_id'] = 'A3CD0892-3B20-4BD3-AA08-C99B06D2CE4D'
    obj['next_tower_id'] = '2823ACD4-E885-4CF2-A002-863B286E41B2'
    obj['tensor'] = 1.0
    obj['w'] = 0.001
    obj['is_delete'] = False
    s = json.dumps(obj)
    #print(s)
    return s
    
def merge_kunming_towers():
    lines = ['926bcabe-f750-400a-b002-25986be66c6b',
             '207a1bf8-cfc6-4b22-b6c0-2f99f1398a65',
             '60b49830-d957-463b-bb1a-68a579fcfafb',
             'dfcbd4d4-5a05-4ea6-8220-7205c48bb240',
             '446e8088-acb5-4d33-b49a-78555c897a56',
             '771ebb8c-d6a1-43f3-a066-89524478ab62',
             '8e3c440d-208c-419b-9e64-897d2a4c0a54',
             '9ac72590-4a3e-4a40-a052-918d0ab45059',
             'f4ebb144-67b1-4ea7-9965-a19e19f848d2',
             '295b2f26-4863-4f87-8de1-b1998a85aff9',
             'af77864e-b8d5-479f-896b-c5f5dfe3450f',
             'ca2b1c8c-b5a0-4686-9162-ea6feae3c091',
             'cfb25596-40a1-4a0c-84a8-eea9b8b50fd5',
             'b6926c06-354d-466d-9d22-fa970c503a94']
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    env.workspace = kmgdgeo
    inputs = []
    for line in lines:
        inputs.append('towers_%s' % line.replace('-',''))
    output = 'km_merged_tower'
    arcpy.Merge_management(inputs=inputs, output=output)
    arcpy.AddMessage(arcpy.GetMessages())
    

def make_km_tower_kml():
    lines = ['926bcabe-f750-400a-b002-25986be66c6b',
             '207a1bf8-cfc6-4b22-b6c0-2f99f1398a65',
             '60b49830-d957-463b-bb1a-68a579fcfafb',
             'dfcbd4d4-5a05-4ea6-8220-7205c48bb240',
             '446e8088-acb5-4d33-b49a-78555c897a56',
             '771ebb8c-d6a1-43f3-a066-89524478ab62',
             '8e3c440d-208c-419b-9e64-897d2a4c0a54',
             '9ac72590-4a3e-4a40-a052-918d0ab45059',
             'f4ebb144-67b1-4ea7-9965-a19e19f848d2',
             '295b2f26-4863-4f87-8de1-b1998a85aff9',
             'af77864e-b8d5-479f-896b-c5f5dfe3450f',
             'ca2b1c8c-b5a0-4686-9162-ea6feae3c091',
             'cfb25596-40a1-4a0c-84a8-eea9b8b50fd5',
             'b6926c06-354d-466d-9d22-fa970c503a94']
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn('km')
    env.workspace = kmgdgeo
    
    inputs = []
    for line in lines:
        inputs.append('towers_%s' % line.replace('-',''))
    output = 'km_merged_tower_layer'
    #if arcpy.Exists(output):
        #arcpy.Delete_management(output)
    #arcpy.MakeFeatureLayer_management(in_features='km_merged_tower', out_layer=output, workspace=kmgdgeo)
    arcpy.SaveToLayerFile_management()
    arcpy.AddMessage(arcpy.GetMessages())
    
    
    
    
def test_json_tower():
    id = None #str(uuid.uuid4())
    #id = 'F605BFE5-2217-4469-A562-5F134F308045' # 2D38F0E2-3218-4562-80D1-2D38F9FA6D15
    isdelete = False
    #isdelete = True
    if isdelete:
        kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn('km')
        table = 'TABLE_TOWER'
        sdeConn = arcpy.ArcSDESQLExecute(kmgd)
        sql = """select convert(nvarchar(50), id) from  %s where line_id='%s'""" % (table, 'F605BFE5-2217-4469-A562-5F134F308045')
        sdeReturn = sdeConn.execute(sql)
        if sdeReturn and len(sdeReturn)>0:
            id = sdeReturn
        del sdeConn
        
    #tower = {'id':id, 'line_id':'F605BFE5-2217-4469-A562-5F134F308045','tower_code':'0501S15026847LAD001', 'tower_name':'bbb0','geo_x':102.4907,'geo_y':25.2245,'geo_z':0,'height':0, 'rotate':0, 'model_code':'test2'}
    #tower = {'id':id, 'line_id':'F605BFE5-2217-4469-A562-5F134F308045','tower_code':'0501S15026847LAD002', 'tower_name':'bbb1','geo_x':102.4827,'geo_y':25.2305,'geo_z':0,'height':0, 'rotate':0, 'model_code':'test2'}
    tower = {'id':id, 'line_id':'F605BFE5-2217-4469-A562-5F134F308045','tower_code':'0501S15026847LAD003', 'tower_name':'bbb2','geo_x':102.4807,'geo_y':25.2325,'geo_z':0,'height':0, 'rotate':0, 'model_code':'test2'}
    obj = {}
    obj['tower'] = tower
    obj['prev_tower_id'] = None
    #obj['prev_tower_id'] = '46A2EF51-67B1-48D5-9CBB-77ABE807984B'
    #obj['prev_tower_id'] = 'A3CD0892-3B20-4BD3-AA08-C99B06D2CE4D'
    
    obj['next_tower_id'] = None
    #obj['is_delete'] = True
    obj['is_delete'] = False
    obj['is_recalc_line'] = True
    
    if isdelete:
        obj['is_delete'] = True
    #attachs = []
    #attach = {'id':None, 'model_code':tower['model_code'], 'point_index':0, 'offset_x':-65, 'offset_y':145}
    #attachs.append(attach)
    #attach = {'id':None, 'model_code':tower['model_code'], 'point_index':1, 'offset_x':-65, 'offset_y':125}
    #attachs.append(attach)
    #attach = {'id':None, 'model_code':tower['model_code'], 'point_index':2, 'offset_x':-65, 'offset_y':105}
    #attachs.append(attach)
    #attach = {'id':None, 'model_code':tower['model_code'], 'point_index':3, 'offset_x':-65, 'offset_y':85}
    #attachs.append(attach)
    #attach = {'id':None, 'model_code':tower['model_code'], 'point_index':4, 'offset_x':65, 'offset_y':145}
    #attachs.append(attach)
    #attach = {'id':None, 'model_code':tower['model_code'], 'point_index':5, 'offset_x':65, 'offset_y':125}
    #attachs.append(attach)
    #attach = {'id':None, 'model_code':tower['model_code'], 'point_index':6, 'offset_x':65, 'offset_y':105}
    #attachs.append(attach)
    #attach = {'id':None, 'model_code':tower['model_code'], 'point_index':7, 'offset_x':65, 'offset_y':85}
    #attachs.append(attach)
    #obj['attachs'] = attachs
    s = json.dumps(obj)
    #print(s)
    return s
    
def test_sql():
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    table = 'towers_0168908B83414C7C9B1D81049780639D'
    sdeConn = arcpy.ArcSDESQLExecute(kmgdgeotmp)
    sql = """select SHAPE, tower_name from  %s""" % table
    sdeReturn = sdeConn.execute(sql)
    print(sdeReturn)
    del sdeConn
    

def test_toolbox():
    #arcpy.ImportToolbox(r"e:\program files (x86)\arcgis\desktop10.1\ArcToolbox\Toolboxes\3D Analyst Tools.tbx", "3d")
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    arcpy.CheckOutExtension('3D')
    env.workspace = kmgdgeotmp
    in_features = 'line_2d38f0e23218456280d12d38f9fa6d15'
    out_feature_class = 'tmp__buff3d_line_2d38f0e23218456280d12d38f9fa6d15'
    if arcpy.Exists(out_feature_class):
        arcpy.Delete_management(out_feature_class)
    buffer_distance_or_field = '150 Meters'
    buffer_joint_type = 'STRAIGHT' 
    buffer_joint_type = 'ROUND'
    buffer_quality = 20
    arcpy.Buffer3D_3d(in_features=in_features, out_feature_class=out_feature_class,buffer_distance_or_field=buffer_distance_or_field, buffer_joint_type=buffer_joint_type, buffer_quality=buffer_quality)
    arcpy.AddMessage(arcpy.GetMessages())



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

def deploy_GP():
    def gentoken(url, username, password, expiration=60):
        query_dict = {'username':   username,
                      'password':   password,
                      'expiration': str(expiration),
                      'client':     'requestip'}
        query_string = urllib.urlencode(query_dict)
        return json.loads(urllib.urlopen(url + "?f=json", query_string).read())['token']
    
    def deleteservice(server, servicename, username, password, token=None, port=6080):
        if token is None:
            token_url = "http://{}:{}/arcgis/admin/generateToken".format(server, port)
            token = gentoken(token_url, username, password)
        delete_service_url = "http://{}:{}/arcgis/admin/services/{}.GPServer/delete?token={}".format(server, port, servicename, token)
        return urllib2.urlopen(delete_service_url, ' ').read() # The ' ' forces POST
    
    arcpy.ImportToolbox(r"C:\Users\XIEJUN\AppData\Roaming\ESRI\Desktop10.1\ArcToolbox\My Toolboxes\kmgdgis.pyt", "kmgdgis")
    try:
        ret = arcpy.Dispatch_kmgdgis('', 'client', 'admin', 'admin', '')
    except:
        print(sys.exc_info()[1])
        #print(arcpy.GetMessages() )   
    if ret:
        #print(dir(ret))
        print('status=%s' % GP_STATUS[ret.status] )
        #for i in range(ret.inputCount):
            #print(ret.getInput(i))
        d = os.path.dirname(SERVICE_DEFINITION_DRAFT)
        if not os.path.exists(d):
            os.mkdir(d)
        #if not os.path.exists(SERVER_CONNECTION_FILE):
        arcpy.mapping.CreateGISServerConnectionFile(
            connection_type='PUBLISH_GIS_SERVICES',
            out_folder_path=os.path.dirname(SERVER_CONNECTION_FILE),
            out_name=os.path.basename(SERVER_CONNECTION_FILE),
            server_url=SERVER_URL,
            server_type='ARCGIS_SERVER',
            use_arcgis_desktop_staging_folder=True,
            staging_folder_path=d,
            username=SERVER_USERNAME,
            password=SERVER_PASSWORD,
            save_username_password=True,
            )
            
            
        #if not os.path.exists(SERVICE_DEFINITION_DRAFT):
        arcpy.CreateGPSDDraft(
            result=ret,
            out_sddraft = SERVICE_DEFINITION_DRAFT, 
            service_name = 'Dispatch', 
            server_type="ARCGIS_SERVER",
            connection_file_path=SERVER_CONNECTION_FILE,
            copy_data_to_server=False, 
            folder_name='kmgdgis', 
            summary='Dispatch', 
            tags='Dispatch',
            executionType='Asynchronous',
            resultMapServer=False,
            showMessages='None',
            maximumRecords=100000,
            minInstances=1,
            maxInstances=20,
            maxUsageTime=600,
            maxWaitTime=60,
            maxIdleTime=1800
        )  
        
        tree = etree.parse(SERVICE_DEFINITION_DRAFT)
        root = tree.getroot()
        r = root.xpath('//Description')
        #print(r)
        for i in r:
            i.text = 'DispatchDispatchDispatch'
        #r = root.xpath('//Name')
        ##print(r)
        #for i in r:
            #i.text = 'Dispatch'
        print(etree.tostring(root, pretty_print=True))
        s = etree.tostring(root)
        with open(SERVICE_DEFINITION_DRAFT, 'w') as f:
            f.write(s)
        
        
        #analyzeMessages = arcpy.mapping.AnalyzeForSD(SERVICE_DEFINITION_DRAFT)
        #if analyzeMessages['errors'] == {}:
            #ret = arcpy.StageService_server(SERVICE_DEFINITION_DRAFT, SERVICE_DEFINITION)
            #print("ret=" + str(ret))
            ##upStatus = arcpy.UploadServiceDefinition_server(SERVICE_DEFINITION, SERVER_CONNECTION_FILE)
            ##print("Completed upload=" + str(upStatus))
        #else: 
            ## if the sddraft analysis contained errors, display them
            #print(analyzeMessages['errors'])
        
        
        env.workspace = d
        f1 = os.path.basename(SERVICE_DEFINITION_DRAFT)
        f2 = os.path.basename( SERVICE_DEFINITION)
        #ret = arcpy.StageService_server(SERVICE_DEFINITION_DRAFT, SERVICE_DEFINITION)
        ret = arcpy.StageService_server(f1, f2)
        print("ret=" + str(ret))
            
        #ret = deleteservice(SERVER_NAME, 'kmgdgis/Dispatch',SERVER_USERNAME, SERVER_PASSWORD, None, SERVER_PORT)
        #upStatus = arcpy.UploadServiceDefinition_server(SERVICE_DEFINITION, SERVER_CONNECTION_FILE, in_folder_type=)
        #print("upStatus=" + str(upStatus))
            
def test_xml():
    r1 = etree.parse(r'D:\arcgisserver\sd\kmgdgis.xml')
    r2 = etree.parse(r'D:\arcgisserver\sd\kmgdgis1.xml')
    print(etree.tostring(r2.getroot(), pretty_print=True))


def insert_action_log(conn, user, action):
    #kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    table = 'TABLE_ACTION_LOG'
    st =  datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    #st =  time.time()
    sql = """ insert into %s values('%s',  '%s',  '%s') """ % (table,  user, action, st)
    #print(sql)
    sdeConn = arcpy.ArcSDESQLExecute(conn)
    ret = sdeConn.execute(sql)
    del sdeConn
    return st


def get_latest_action_log(conn):
    #kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    table = 'TABLE_ACTION_LOG'
    sql = """ select top 1 time_stamp from  %s order by id desc """ % table
    #print(sql)
    sdeConn = arcpy.ArcSDESQLExecute(conn)
    ret = sdeConn.execute(sql)
    del sdeConn
    return ret
    
def test_group():
    ext = ['53629C78-78DD-4761-90FC-027504B7F5E3', '798DEB82-055A-4261-A229-C22ECA3D1FC4','F4A47635-2376-4D58-872D-6F0DB8B924F0' ]
    #ext = ['BB35BD60-01A1-44ED-9B4D-527834A711BF', '529EFBD8-69E3-4DE3-9C99-DA6735263D7B', '146C24F4-C84B-4AD0-AC8B-ED12AC810231']
    ext = ['6513923A-BDE9-4845-8E47-C88FEB18ADB8','0E641E3C-037B-46FE-A2A8-22D119EB1645', '3CFC8F44-24A2-4E75-B470-DE0A37C0351E']
    ext = []
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    towers = get_data_from_rdbms(kmgd, 'kmgd', 'VIEW_TOWER_LINE', "line_id='%s'" % '0168908b-8341-4c7c-9b1d-81049780639d')
    print(len(towers.keys()))
    towers_relation = get_data_from_rdbms(kmgd, 'kmgd', 'VIEW_TOWER_RELATIONS', "line_id='%s'" % '0168908b-8341-4c7c-9b1d-81049780639d')
    towers = resort_towers_to_groups(towers, towers_relation, ext)
    print('group count=%d' % len(towers))
    for g in towers:
        print('group(%d)=%d' % ( towers.index(g), len(g.keys())))
        for k in g.keys():
            if k in ext:
                print('idx(%d)=%d' % ( towers.index(g), g.keys().index(k)))
        print(g)

#def test_update_model_code():
    ##kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    #kmgdgeotmp = r'G:\work\csharp\kmgdgis\data\local_workspace\local.gdb'
    #env.workspace = kmgdgeotmp
    #lines = odbc_get_records('TABLE_LINE', "1=1" )
    #cur = None
    #for line in lines:
        ##if line['id'].lower() in ['7ba9b56f-d940-4ad0-b0bb-0abd677f78d6','d1b2bf5c-fd3f-4e2b-917d-28def43d3b1f', '44aeb7fb-71e9-4559-97c3-52301e007b42', '46da1ec5-9717-473f-a918-5eceffc21308','48e1c59f-6778-46f5-b930-79cb9272a1b1','c94c0b57-9930-4fe5-8b38-7b181f7dab72','0168908b-8341-4c7c-9b1d-81049780639d']:
        ##if line['id'].lower() in ['7ba9b56f-d940-4ad0-b0bb-0abd677f78d6','d1b2bf5c-fd3f-4e2b-917d-28def43d3b1f', '44aeb7fb-71e9-4559-97c3-52301e007b42','0168908b-8341-4c7c-9b1d-81049780639d']:
        ##if line['id'].lower() in ['46da1ec5-9717-473f-a918-5eceffc21308','48e1c59f-6778-46f5-b930-79cb9272a1b1','c94c0b57-9930-4fe5-8b38-7b181f7dab72']:
        #if True:
            #out_name = 'towers_%s' % line['id'].replace('-', '').upper()
            #i = 0
            #cur = arcpy.UpdateCursor(out_name)
            #for row in cur:
                ##if row.model_code == '500kv1':
                #row.model_code='test2'
                #i += 1
                #cur.updateRow(row)
            #print('%s updated %d' % (out_name, i))
            #del cur 
            
def test_list():
    ws = r'G:\work\csharp\kmgdgis\data\local_workspace\local.gdb'
    env.workspace = ws
    lines = arcpy.ListFeatureClasses('line_*')
    for i in lines:
        if not i in ['line_all','towers_all']:
            print('wildCard + "%s",' % i[i.index('_')+1:])


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
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    

    
def merge_dem():
    #import gdal_merge
    #sys.exit(gdal_merge.main(sys.argv))
    
    s = r'-o "D:\gis\YN_DEM.tif" '
    
    for root, dirs, files  in os.walk(r'D:\gis\demdata\zip', topdown=False):
        for name in files:
            if len(re.findall(r'ASTGTM2_\w{7}_dem', name))>0:
                p = os.path.join(root, name)
                print(p)
                s += '"%s" ' % p
        #for name in dirs:
            #p = os.path.join(root, name)
    print(s)  


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
    
def odbc_save_data_to_table(table, op, data, line_id=None, start_tower_id=None, end_tower_id=None, area=''):
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
        
    if table=='TABLE_TOWER' and line_id and len(line_id)>0 and tower_id and len(tower_id)>0:
        if len(data)>0:
            obj = sqlize_data(data[0])
            sql = ''' UPDATE %s SET 
                           tower_code=%s,
                           tower_name=%s,
                           same_tower=%s,
                           line_position=%s,
                           geo_x=%s,
                           geo_y=%s,
                           geo_z=%s,
                           rotate=%s,
                           model_code=%s,
                           denomi_height=%s,
                           horizontal_span=%s,
                           vertical_span=%s,
                           grnd_resistance=%s,
                           building_level=%s,
                           line_rotate=%s
                    WHERE id='%s'
            ''' % (table, 
                   obj['tower_code'],
                   obj['tower_name'],
                   obj['same_tower'],
                   obj['line_position'],
                   obj['geo_x'],
                   obj['geo_y'],
                   obj['geo_z'],
                   obj['rotate'],
                   obj['model_code'],
                   obj['denomi_height'],
                   obj['horizontal_span'],
                   obj['vertical_span'],
                   obj['grnd_resistance'],
                   obj['building_level'],
                   obj['line_rotate'],
                   tower_id
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
    
    
    
def analyse_buffer3d(workspace, featureclass, obj):
    if obj['type']=='line':
        if obj['buffer_distance']>500:
            ret = 'err', '缓冲区距离必须小于500米'
            return ret
    
    #tmp = copy_features(workspace, workspacetmp, obj)
    arcpy.CheckOutExtension('3D')
    env.workspace = workspace
    uid = str(uuid.uuid4()).upper().replace('-','')
    in_features = 'sde.DBO.' + featureclass
    out_feature_class = 'buffer3d_%s' % uid
    buffer_quality = 20
    buffer_joint_type = 'STRAIGHT'
    m = MeterToDecimalDegree(obj['buffer_distance'], 25)
    print('MeterToDecimalDegree = %f' % m)
    buffer_distance_or_field = str(m)
    if obj['type']=='line':
        buffer_quality = 6
    ret = '', ''
    try:    
        arcpy.Buffer3D_3d(in_features=in_features, out_feature_class=out_feature_class, buffer_distance_or_field=buffer_distance_or_field,buffer_joint_type=buffer_joint_type, buffer_quality=buffer_quality)
        arcpy.AddMessage(arcpy.GetMessages())
        err = arcpy.GetMessage(2)
        ret =  'ok', out_feature_class
        #if 'warning'.upper() in err:
            #ret = 'err', err
    except:
        ret = 'err', sys.exc_info()[1]
    #if arcpy.Exists(tmp):
        #arcpy.Delete_management(tmp)
    return ret

def analyse_buffer2d(workspace, featureclass, cfg={}):
    env.workspace = workspace
    uid = str(uuid.uuid4()).upper().replace('-','')
    in_features = 'sde.DBO.' + featureclass
    out_feature_class = '_tmp_buffer2d_%s' % uid
    #buffer_quality = 20
    #buffer_joint_type = 'STRAIGHT'
    #m = MeterToDecimalDegree(obj['buffer_distance'], 25)
    #print('MeterToDecimalDegree = %f' % m)
    buffer_distance_or_field = '100 Meter'
    if cfg.has_key('buffer_distance_or_field'):
        buffer_distance_or_field = '%f Meter' % cfg['buffer_distance_or_field']
    line_side = 'FULL'
    if cfg.has_key('line_side'):
        line_side = cfg['line_side']
    line_end_type = 'FLAT'    
    if cfg.has_key('line_end_type'):
        line_end_type = cfg['line_end_type']
        
        
    ret = '', ''
    try:    
        arcpy.Buffer_analysis(in_features=in_features, 
                              out_feature_class=out_feature_class, 
                              buffer_distance_or_field=buffer_distance_or_field,
                              line_side=line_side, 
                              line_end_type=line_end_type)
        arcpy.AddMessage(arcpy.GetMessages())
        err = arcpy.GetMessage(2)
        ret =  'ok', out_feature_class
        
    except:
        ret = 'err', sys.exc_info()[1]
    #if arcpy.Exists(tmp):
        #arcpy.Delete_management(tmp)
    return ret


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
    
def update_model_code(model_code, line_id, where_clause=None):
    out_name = 'towers_' + line_id.replace('-','')
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    env.workspace = kmgdgeo
    if arcpy.Exists(out_name):
        if where_clause:
            cur = arcpy.UpdateCursor(out_name, where_clause=where_clause)
        else:
            cur = arcpy.UpdateCursor(out_name)
        for row in cur:
            row.setValue('model_code', model_code)
            cur.updateRow(row)
        del cur
    else:
        print('%s not exist' % out_name)
    
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
    #global gDemExtractor
    #d = r'H:\gis\demdata'
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
    
        
    

def test_buff2d():
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    cfg = {}
    cfg['buffer_distance_or_field'] = 100
    analyse_buffer2d(kmgdgeo, 'line_BAE4121F69614B939819AC2D00E92D9A', cfg)
    cfg['buffer_distance_or_field'] = 200
    analyse_buffer2d(kmgdgeo, 'towers_BAE4121F69614B939819AC2D00E92D9A', cfg)

def feature_to_json():
    fc = r"c:\temp\myData.shp"
    featurSet = arcpy.FeatureSet()
    featureSet.load(fc)
    desc = arcpy.Describe(featureSet)
    print desc.pjson # so we can read it
    #### desc.json also works. ####
    del desc
    del fc
    del featureSet

def test_3dd_stamp():
    print(get_latest_stamp('%Y-%m-%d %H:%M:%S'))
    print(get_latest_3dd_stamp('%Y-%m-%d %H:%M:%S'))


def test_merge_tif():
    d = r'I:\geotiff'
    l = []
    for root, dirs, files  in os.walk(d, topdown=False):
        for f in files:
            p = os.path.join(root, f)
            if p[-4:]=='.tif':
                print(p)
                l.append(p)
    s = ''
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
    
def test_create_potential_hazard_feature():
    kmgd, kmgdgeo, kmgdgeotmp = create_sde_conn()
    env.workspace = kmgdgeo
    out_path = kmgdgeo
    out_name = 'point_potential_hazard'
    if arcpy.Exists(out_name):
        arcpy.Delete_management(out_name)
    
    obj = arcpy.CreateFeatureclass_management(out_path=out_path, out_name=out_name, geometry_type='POINT',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='DISABLED', has_m='DISABLED')
    arcpy.AddMessage(arcpy.GetMessages())
    arcpy.AddField_management(obj, 'id', 'TEXT')
    arcpy.AddField_management(obj, 'type', 'TEXT')
    arcpy.AddField_management(obj, 'description', 'TEXT')
    
    out_name = 'polyline_potential_hazard'
    if arcpy.Exists(out_name):
        arcpy.Delete_management(out_name)
    print('create polyline...')
    obj = arcpy.CreateFeatureclass_management(out_path=out_path, out_name=out_name, geometry_type='POLYLINE',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='DISABLED', has_m='DISABLED')
    arcpy.AddMessage(arcpy.GetMessages())
    arcpy.AddField_management(obj, 'id', 'TEXT')
    arcpy.AddField_management(obj, 'type', 'TEXT')
    arcpy.AddField_management(obj, 'description', 'TEXT')
    
    out_name = 'polygon_potential_hazard'
    if arcpy.Exists(out_name):
        arcpy.Delete_management(out_name)
    print('create polyline...')
    obj = arcpy.CreateFeatureclass_management(out_path=out_path, out_name=out_name, geometry_type='POLYGON',spatial_reference= arcpy.SpatialReference(text='WGS 1984'), has_z='DISABLED', has_m='DISABLED')
    arcpy.AddMessage(arcpy.GetMessages())
    arcpy.AddField_management(obj, 'id', 'TEXT')
    arcpy.AddField_management(obj, 'type', 'TEXT')
    arcpy.AddField_management(obj, 'description', 'TEXT')
    
    
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
                atr[enc(dec1(field_names[i]))] = enc(dec1(sr.record[i]))
            atr['type'] = k
            atr['py'] = ''
            if atr.has_key('NAME') and len(dec(atr['NAME'].strip()))>0:
                try:
                    atr['py'] = enc(piny.hanzi2pinyin_first_letter(dec(atr['NAME'].strip())))
                except:
                    pass
            #print('%s=%s' % (dec(atr['NAME']), atr['py']))
            geom = sr.shape.__geo_interface__
            #if not geom['type'] in ['LineString', 'MultiLineString', 'Point','MultiPolygon','Polygon']:
                #print(geom)
            geom = chop(geom, bound)
            if geom:
                buf.append(dict(type="Feature",  geometry=geom, properties=atr)) 
    
        # write the GeoJSON file
        print(fpath)
        absroot = os.path.join(SERVERJSONROOT, area)
        if not os.path.exists(absroot):
            os.mkdir(absroot)
        
        
        with open(fpath, "w") as f:
            f.write(json.dumps({"type": "FeatureCollection", "features": buf},ensure_ascii=False, indent=4) + "\n")
            #f.write(json.dumps({"type": "FeatureCollection", "features": buf},ensure_ascii=True))
        #try:
            #p = os.path.join(JSONROOT, os.path.basename(fpath))
            #if os.path.exists(p):
                #os.remove(p)
            #shutil.copy(fpath, JSONROOT)
        #except:
            #pass
            
            
             
def gen_geojson_by_shape(area):
    from pinyin import PinYin
    pydatapath = os.path.join(module_path(), 'pinyin_word.data');
    piny =  PinYin(pydatapath)
    piny.load_word()
    bounds = None
    p = os.path.abspath(SERVERJSONROOT)
    p = os.path.join(p, 'yn_tiles_bounds_%s.json' % area)
    with open(p,) as f:
        bounds = json.loads(f.read())
    for i in os.listdir(SHAPEROOT):
        p = os.path.join(SHAPEROOT, i)
        if os.path.isfile(p) and i[-4:]=='.shp':
            #if i == u'村.shp':
            convert_shp_to_geojson(area, bounds,  p, piny)

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
        o['properties']['device_name'] = enc(tun['equip_name'])
        o['properties']['py'] = ''
        try:
            o['properties']['py'] = enc(piny.hanzi2pinyin_first_letter(tun['equip_name'].replace('#','').replace('I',u'一').replace('II',u'二')))
        except:
            pass
        for k in tun.keys():
            if isinstance(tun[k], unicode):
                tun[k] = enc(tun[k])
            o['properties'][k] = tun[k]
        ret[tun['tunnel_id']]['features'].append(o)
        
    for k in ret.keys():    
        s = json.dumps(ret[k], indent=4, ensure_ascii=True)
        path = os.path.join(absroot, 'geojson_tunneldevice_%s_%s.json' % (area, k) )
        with open(path, 'w') as f:
            f.write(s + '\n')
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
            
            
            o['properties']['tunnel_name'] = enc(tuns[0]['tunnel_name'] + u' ' + sec['start_point'] + u'至' + sec['end_point'])
            o['properties']['py'] = ''
            try:
                o['properties']['py'] = enc(piny.hanzi2pinyin_first_letter(tuns[0]['tunnel_name'].replace('#','').replace('I',u'一').replace('II',u'二')))
            except:
                pass
            for k in sec.keys():
                if isinstance(sec[k], unicode):
                    sec[k] = enc(sec[k])
                o['properties'][k] = sec[k]
            tunnel_obj['features'].append(o)
            s = json.dumps(tunnel_obj, indent=4, ensure_ascii=True)
            with open(path, 'w') as f:
                f.write(s + '\n')
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
    recs = odbc_get_records('TABLE_POTENTIAL_RISK_INFO', "1=1" , area)
    
    obj = {}
    obj['type'] = 'FeatureCollection'
    obj['features'] = []
    
    validlgtlat = None, None
    for rec in recs:
        x, y = rec['center_x'], rec['center_y']
        if x is None or y is None or x==0 or y==0:
            continue
        o = {}
        o['geometry'] = {}
        o['geometry']['type'] = 'Point'
        o['geometry']['coordinates'] = [x, y]
        o['type'] = 'Feature'
        o['properties'] = {}
        o['properties']['type'] = enc(rec['risk_type'])
        o['properties']['NAME'] = enc(rec['risk_info'])
        o['properties']['tip'] = enc(u'隐患点描述:%s<br/>隐患点类型:%s<br/>发现时间:%s<br/>记录人:%s<br/>联系人:%s<br/>联系方式:%s<br/>' % (rec['risk_info'], rec['risk_type'], rec['appear_date'],rec['record_person'],rec['contact_person'],rec['contact_number'], ))
        o['properties']['py'] = ''
        try:
            o['properties']['py'] = enc(piny.hanzi2pinyin_first_letter(rec['risk_info'].replace('#','').replace('I',u'一').replace('II',u'二')))
            #print(o['properties']['py'])
        except:
            print(sys.exc_info()[1])
        obj['features'].append(o)
    
    with open(path, 'w') as f:
        #s = json.dumps(obj)
        f.write(json.dumps(obj, ensure_ascii=True, indent=4) + '\n')
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
            line[k] = enc(line[k])
        if k=='line_name':
            o['properties']['NAME'] = line[k]
            o['properties']['py'] = ''
            try:
                o['properties']['py'] = enc(piny.hanzi2pinyin_first_letter(dec(line[k]).replace('#','').replace('I',u'一').replace('II',u'二')))
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
                tower[k] = enc(tower[k])
            if k=='tower_name':
                tower_obj['properties']['NAME'] = tower[k]
                tower_obj['properties']['py'] = ''
                try:
                    tower_obj['properties']['py'] = enc(piny.hanzi2pinyin_first_letter(dec(tower[k]).replace('#','').replace('I',u'一').replace('II',u'二')))
                except:
                    pass
            tower_obj['properties'][k] = tower[k]
        towers_obj['features'].append(tower_obj)
                
    
    line_obj['features'].append(o)    
    with open(linepath, 'w') as f:
        f.write(json.dumps(line_obj, ensure_ascii=False, indent=4) + '\n')
    with open(towerspath, 'w') as f:
        f.write(json.dumps(towers_obj, ensure_ascii=False, indent=4) + '\n')
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
    from pinyin import PinYin
    pydatapath = os.path.join(module_path(), 'pinyin_word.data');
    piny =  PinYin(pydatapath)
    piny.load_word()
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
            
def mongodb_get_server_tree(host, port):
    ret = [{"id":u"root","text":u"服务器列表","isexpand":True, "children":[]}]
    server = {"id":u"%s_%s" % (host, port), "type":"server", "text":u"%s:%s" % (host, port), "isexpand":True, "err":"", "children":[]}
    try:
        gClientMongo = MongoClient(host, int(port))
        for dbname in gClientMongo.database_names():
            if dbname != 'admin' and dbname != 'local':
                db = {}
                db["id"] = u"%s_%s_%s" % (host, port, dbname)
                db["text"] = u"%s" % dbname
                db["isexpand"] = True
                db["type"] = "database"
                db["children"] = []
                dbo = gClientMongo[dbname]
                for collectionname in dbo.collection_names():
                    if collectionname != "system.indexes":
                        collection = {}
                        collection["id"] = u"%s_%s_%s_%s" % (host, port, dbname, collectionname)
                        collection["text"] = u"%s" % collectionname
                        collection["isexpand"] = True
                        collection["type"] = "collection"
                        collection["children"] = []
                        db["children"].append(collection)
                server["children"].append(db)
    except:
        traceback.print_exc()
        server['err'] = sys.exc_info()[1].message
        print("err=%s" % server['err'])
        server["children"].append({"id":u"%s_%s_err" % (host, port), "text":u"Error:%s" % server['err']})
    finally:
        ret[0]["children"].append(server)
    return ret
    

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
                f.write(json.dumps(obj, ensure_ascii=True, indent=4) + '\n')
    
    
    
    
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
            f.write(json.dumps(obj, ensure_ascii=True, indent=4) + '\n')
                
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
        f.write(json.dumps(obj, ensure_ascii=True, indent=4) + '\n')

        
    

    
def test_gen_geojson_by_list(data_dir, filelist):
    for f in filelist:
        tname = os.path.basename(f).replace('.xls','').replace(u'线性整理','')
        ret = collation_lnglat(f)
        gen_geojson_by_list(data_dir, tname, ret)
        gen_boundry_by_list(data_dir, tname, ret)
 
def gen_mongo_geojson_by_line_id(line_id, area, piny, mapping):
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
            
            
            
        x, y = tower['geo_x'], tower['geo_y']
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
        tower_obj['geometry']['coordinates'] = [x, y]
        tower_obj['type'] = 'Feature'
        tower_obj['properties'] = {}
        for k in tower.keys():
            if isinstance(tower[k], unicode):
                tower[k] = enc(tower[k])
            if k=='line_id':
                #if not tower_obj['properties'].has_key('line_id'):
                    #tower_obj['properties']['line_id'] = []
                #tower_obj['properties']['line_id'].append(tower[k])
                continue
            elif k=='id':
                if mapping.has_key(tower[k]):
                    tower_obj['_id'] = ObjectId(mapping[tower[k]])
                #continue
            elif k=='same_tower':
                #if not tower[k] == '00000000-0000-0000-0000-000000000000':
                    #st = odbc_get_records('TABLE_TOWER', "id='%s'" % tower[k], 'km')
                    #if len(st)>0:
                        #lindid = st[0]['line_id']
                        #if not tower_obj['properties'].has_key('line_id'):
                            #tower_obj['properties']['line_id'] = []
                        #tower_obj['properties']['line_id'].append(lindid)
                continue
            elif k=='tower_name':
                tower_obj['properties'][k] = tower[k]
                tower_obj['properties']['py'] = ''
                try:
                    tower_obj['properties']['py'] = enc(piny.hanzi2pinyin_first_letter(dec(tower[k]).replace('#','').replace('I',u'一').replace('II',u'二')))
                except:
                    pass
            elif k=='geo_x' or k=='geo_y':
                continue
            elif k in ['model_code', 'model_code_height']:
                if not tower_obj['properties'].has_key('model'):
                    tower_obj['properties']['model'] = {}
                tower_obj['properties']['model'][k] = tower[k]
                if not tower_obj['properties']['model'].has_key('contact_points'):
                    tower_obj['properties']['model']['contact_points'] = []
                if k == 'model_code_height':
                    pts = odbc_get_records('TABLE_CONTACT_POINT', "model_code='%s'" % tower[k], 'km')
                    if len(pts)>0:
                        for pt in pts:
                            o = {}
                            o['side'] = 0
                            if pt['side'] == u'正':
                                o['side'] = 1
                            o['position'] = enc(pt['position'])
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
                
        if not tower_obj['properties'].has_key('prev_ids'):
            tower_obj['properties']['prev_ids'] = []
        if not tower_obj['properties'].has_key('next_ids'):
            tower_obj['properties']['next_ids'] = []
        if prev:
            if mapping.has_key(prev['id']):
                tower_obj['properties']['prev_ids'].append(mapping[prev['id']])
        #else:
            #tower_obj['properties']['prev_ids'] = []
            
        if nextt:
            if mapping.has_key(nextt['id']):
                tower_obj['properties']['next_ids'].append(mapping[nextt['id']])
        #else:
            #tower_obj['properties']['next_ids'] = []
            
        if not tower_obj['properties'].has_key('metals'):
            tower_obj['properties']['metals'] = []
        attachs = odbc_get_records('TABLE_TOWER_METALS', "tower_id='%s'" % tower['id'], 'km')
        if len(attachs)>0:
            for attach in attachs:
                o = {}
                o['assembly_graph'] = ''
                o['manufacturer'] = ''
                o['model'] = ''
                o['type'] = enc(u'未知')
                #if attach['manufacturer']:
                    #o['manufacturer'] = enc(attach['manufacturer'])
                if attach['attach_type'] == u'防振锤':
                    o['type'] = enc(u'防振锤')
                    o['side'] = ''
                    if attach['attach_subtype']:
                        o['side'] = enc(attach['attach_subtype'])
                    o['count'] = attach['strand']
                    o['distance'] = attach['value1']
                elif attach['attach_type'] == u'绝缘子串':
                    o['type'] = enc(u'绝缘子串')
                    o['insulator_type'] = ''
                    if attach['attach_subtype']:
                        o['insulator_type'] = enc(attach['attach_subtype'])
                    o['model'] = ''
                    if attach['specification']:
                        o['model'] = enc(attach['specification'])
                    o['material'] = ''
                    if attach['material']:
                        o['material'] = enc(attach['material'])
                    o['strand'] = attach['strand']
                    o['slice'] = attach['slice']
                elif attach['attach_type'] == u'接地装置':
                    o['type'] = enc(u'接地装置')
                    o['model'] = ''
                    if attach['specification']:
                        o['model'] = enc(attach['specification'])
                    o['count'] = attach['strand']
                    o['depth'] = attach['value1']
                elif attach['attach_type'] == u'基础':
                    o['type'] = enc(u'铁塔')
                    o['model'] = ''
                    o['platform_model'] = ''
                    o['anchor_model'] = ''
                    o['count'] = attach['strand']
                    o['depth'] = attach['value1']
                tower_obj['properties']['metals'].append(o)
        #if not tower_obj['properties'].has_key('attachments'):
            #tower_obj['properties']['attachments'] = []
        attachs = odbc_get_records('TABLE_TOWER_ATTACH', "tower_id='%s'" % tower['id'], 'km')
        if len(attachs)>0:
            for attach in attachs:
                o = {}
                o['assembly_graph'] = ''
                o['manufacturer'] = ''
                o['model'] = ''
                o['type'] = enc(u'未知')
                if attach['manufacturer']:
                    o['manufacturer'] = enc(attach['manufacturer'])
                if attach['attach_name'] == u'接地装置':
                    o['type'] = enc(u'接地装置')
                    if attach['series']:
                        o['model'] = enc(attach['series'])
                    o['count'] = attach['int_value1']
                    o['depth'] = attach['float_value1']
                elif u'计数器' in attach['attach_name'] :
                    o['type'] = enc(u'雷电计数器')
                    if attach['series']:
                        o['model'] = enc(attach['series'])
                    o['counter'] = attach['int_value1']
                elif u'防鸟刺' in attach['attach_name'] :
                    o['type'] = enc(u'防鸟刺')
                    if attach['series']:
                        o['model'] = enc(attach['series'])
                    o['count'] = attach['int_value1']
                elif u'在线监测装置' in attach['attach_name'] :
                    o['type'] = enc(u'在线监测装置')
                    if attach['series']:
                        o['model'] = enc(attach['series'])
                    o['count'] = attach['int_value1']
                elif attach['attach_name'] == u'基础':
                    o['type'] = enc(u'基础')
                    if attach['series']:
                        o['model'] = enc(attach['series'])
                    o['platform_model'] = enc(u'铁塔')
                    o['anchor_model'] = ''
                    o['count'] = attach['int_value1']
                    o['depth'] = attach['float_value1']
                elif attach['attach_name'] == u'拉线':
                    o['type'] = enc(u'拉线')
                    if attach['series']:
                        o['model'] = enc(attach['series'])
                    o['count'] = attach['int_value1']
                tower_obj['properties']['metals'].append(o)
            
        ret.append(tower_obj)
    return ret

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

def mongo_find(dbname, collection_name, *args, **kwargs):
    global gClientMongo
    host, port = gConfig['mongodb']['host'], int(gConfig['mongodb']['port'])
    ret = []
    try:
        if gClientMongo is not None and not gClientMongo.alive():
            gClientMongo.close()
            gClientMongo = None
        if gClientMongo is None:
            gClientMongo = MongoClient(host, port)
        if dbname in gClientMongo.database_names():      
            db = gClientMongo[dbname]
            if collection_name in db.collection_names():
                cur = db[collection_name].find(*args, **kwargs)
                for i in cur:
                    ret.append(remove_mongo_id(i))
                    #ret.append(i)
            elif collection_name == 'mongo_get_towers_by_line_name':
                lines = db['lines'].find(*args, **kwargs)
                towerids = []
                for line in lines:
                    for t in line['towers']:
                        #print(str(t))
                        towerids.append(t)
                towers = db['towers'].find({'_id':{'$in':towerids}})
                for i in towers:
                    ret.append(remove_mongo_id(i))
                    #ret.append(i)
            else:
                print('collection [%s] does not exist.' % collection_name)
        else:
            print('database [%s] does not exist.' % dbname)
    except:
        traceback.print_exc()
        #err = sys.exc_info()[1].message
        #print(err)
        ret = []
    return ret

def mongo_find_one(dbname, collection_name, *args, **kwargs):
    global gClientMongo
    host, port = gConfig['mongodb']['host'], int(gConfig['mongodb']['port'])
    ret = None
    try:
        if gClientMongo is not None and not gClientMongo.alive():
            gClientMongo.close()
            gClientMongo = None
        if gClientMongo is None:
            gClientMongo = MongoClient(host, port)
                
        db = gClientMongo[dbname]
        ret = db[collection_name].find_one(*args, **kwargs)
        ret = remove_mongo_id(ret)
    except:
        traceback.print_exc()
        #err = sys.exc_info()[1].message
        #print(err)
        ret = None
    return ret
    
def remove_mongo_id(obj):
    if isinstance(obj, ObjectId):
        obj = str(obj)
        return obj
    elif isinstance(obj, dict):
        #if obj.has_key(u'_id'):
            ##del obj[u'_id']
            #obj[u'_id'] = str(obj[u'_id'])
        for k in obj.keys():
            obj[k] = remove_mongo_id(obj[k])
    elif isinstance(obj, list):
        for i in obj:
            obj[obj.index(i)] = remove_mongo_id(i)
    return obj


def test_mongo_import_segments():
    global gClientMongo
    area = 'km'
    lines = odbc_get_records('TABLE_LINE', '1=1', area)
    l = []
    mapping = get_tower_id_mapping()
    for line in lines:
        segs = gen_mongo_segments_by_line_id(line['id'], area,  mapping)
        l.extend(segs)
    host, port = 'localhost', 27017
    try:
        if gClientMongo is None:
            gClientMongo = MongoClient(host, port)
        db = gClientMongo['kmgd']
        if 'segments' in db.collection_names(False):
            db.drop_collection('segments')
        collection = db.create_collection('segments')
        for i in l:
            collection.save(i)
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)

def gen_mongo_segments_by_line_id(line_id, area, mapping): 
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
            segs = odbc_get_records('VIEW_CONTACT_SEGMENT', "start_tower_id='%s' AND end_tower_id='%s'" % (tower['id'],  nextt['id']), 'km')
            obj = {}
            for seg in segs:
                if mapping.has_key(seg['start_tower_id']) and mapping.has_key(seg['end_tower_id']):
                    side0 = 0
                    #if seg['start_side'] == u'正':
                        #side0 = 1
                    side1 = 1
                    #if seg['end_side'] == u'正':
                        #side1 = 1
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
            if len(obj.keys())>0:
                ret.append(obj)
    return ret           
            
    
def test_mongo_import_towers():
    global gClientMongo
    area = 'km'
    from pinyin import PinYin
    pydatapath = os.path.join(module_path(), 'pinyin_word.data');
    piny =  PinYin(pydatapath)
    piny.load_word()
    lines = odbc_get_records('TABLE_LINE', '1=1', area)
    l = []
    mapping = get_tower_id_mapping()
    for line in lines:
        towers = gen_mongo_geojson_by_line_id(line['id'], area, piny, mapping)
        l.extend(towers)

    host, port = 'localhost', 27017
    try:
        if gClientMongo is None:
            gClientMongo = MongoClient(host, port)
        db = gClientMongo['kmgd']
        if 'towers' in db.collection_names(False):
            db.drop_collection('towers')
        collection = db.create_collection('towers')
        for i in l:
            collection.save(i)
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
    
    
def test_build_tower_odbc_mongo_id_mapping():
    global gClientMongo
    host, port = 'localhost', 27017
    try:
        if gClientMongo is None:
            gClientMongo = MongoClient(host, port)
        db = gClientMongo['kmgd']
        if 'tower_ids_mapping' in db.collection_names(False):
            db.drop_collection('tower_ids_mapping')
        collection = db.create_collection('tower_ids_mapping')
        l = mongo_find('kmgd', 'towers')
        for i in l:
            collection.save({'uuid':i['properties']['id'], 'id':i['_id']})
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
     
def test_build_line_odbc_mongo_id_mapping():
    global gClientMongo
    host, port = 'localhost', 27017
    try:
        if gClientMongo is None:
            gClientMongo = MongoClient(host, port)
        db = gClientMongo['kmgd']
        if 'line_ids_mapping' in db.collection_names(False):
            db.drop_collection('line_ids_mapping')
        collection = db.create_collection('line_ids_mapping')
        l = mongo_find('kmgd', 'lines')
        for i in l:
            collection.save({'uuid':i['id'], 'id':i['_id']})
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
    
def get_tower_id_mapping():
    mapping = {}
    #tower_ids_mapping = db['tower_ids_mapping']
    tower_ids_mapping = mongo_find('kmgd', 'tower_ids_mapping')
    for i in tower_ids_mapping:
        mapping[i['uuid']] = i['id']
    return mapping
    
    
def test_mongo_import_line():
    global gClientMongo
    host, port = 'localhost', 27017
    area = 'km'
    try:
        if gClientMongo is None:
            gClientMongo = MongoClient(host, port)
        db = gClientMongo['kmgd']
        
        if 'lines' in db.collection_names(False):
            db.drop_collection('lines')
        collection_lines = db.create_collection('lines')
        mapping = get_tower_id_mapping()
        #collection_lines = db['lines']
        odbc_lines = odbc_get_records('TABLE_LINE', '1=1', area)
        for line in odbc_lines:
            towers_sort = odbc_get_sorted_tower_by_line(line['id'], area)
            del line['box_north']
            del line['box_south']
            del line['box_east']
            del line['box_west']
            line['towers'] = []
            for i in towers_sort:
                if mapping.has_key(i['id']):
                    line['towers'].append(mapping[i['id']])
            del line['id']
            collection_lines.save(line)
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
    
def test_mongo_import_code():
    global gClientMongo
    host, port = 'localhost', 27017
    try:
        if gClientMongo is None:
            gClientMongo = MongoClient(host, port)
        db = gClientMongo['kmgd']
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
            odbc = odbc_get_records(cods[k], '1=1', 'km')
            for i in odbc:
                obj[k][i['code']] = i['name']
        collection.save(obj)
    except:
        traceback.print_exc()
        err = sys.exc_info()[1].message
        print(err)
   
    
if __name__=="__main__":
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
    
    
    #alt = altitude_by_lgtlat(ur'H:\gis\demdata', 102.70294, 25.05077)
    #print('alt=%f' % alt)
    #test_mongo_import_line()
    #test_mongo_import_code()
    #test_build_tower_odbc_mongo_id_mapping()
    #test_build_line_odbc_mongo_id_mapping()
    #test_mongo_import_towers()
    test_mongo_import_segments()
    #ret = mongo_find('kmgd', 'mongo_get_towers_by_line_name', {'line_name':u'七罗I回'})
    #print(ret)
    #print('count=%d' % len(ret))
    #for i in ret:
        #print(i)
    #print('find one')
    #ret = mongo_find_one('kmgd', 'towers', {'properties.line_id':'AF77864E-B8D5-479F-896B-C5F5DFE3450F'})
    #print(ret)
    
    