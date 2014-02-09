# -*- coding: utf-8 -*-
import os
import sys
import json
import shutil
import subprocess
import uuid
import gdal
import numpy as np
import base64
from math import ceil, log10
import sqlite3
import operator
from osr import SpatialReference
from gdalconst import GA_ReadOnly
import shapefile



ARCGISTILEROOT = r'I:\geotiff'
GOOGLETILEROOT = r'I:\geotiff'
DIRTILEROOT = r'I:\geotiff\tiles'
TILEROOT = r'I:\geotiff'
BLANKTILEID = '00000000-0000-0000-0000-000000000000'

MAXCOMMITRECORDS = 100
TILESIZE = 256
TILEFORMAT = 'png'

TMPDIR = 'static/tmp'
SHAPEROOT= u'I:\云南省矢量数据'
JSONROOT= 'static/json'

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

TEMPDRIVER = gdal.GetDriverByName('MEM')
TILEDRIVER = gdal.GetDriverByName(TILEFORMAT)
MEMORYPATH = '/vsimem/tiffinmem'

 
            
            
if __name__=="__main__":
    #create_mbtiles_from_arcgistile('yn', 8, 12,  None, False)
    #create_mbtiles_from_googletile('00765', None, False)
    #create_mbtiles_from_esritile('00765', None, True)
    #create_mbtiles_from_esritile_and_zoom('zt',12, 15)
    #test_copy_tiles1('zt',12, 16)
    test_gen_geojson('zt')
    
    