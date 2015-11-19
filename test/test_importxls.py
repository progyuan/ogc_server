# -*- coding: utf-8 -*-
import os, sys
import json
import xlrd
import codecs
from collections import  OrderedDict
from db_util import init_global, get_pinyin_data, update_geometry2d


XLS_FILE = ur'G:\work\matlab\dn\bayes_rset\data_bus.xls'
XLS_FILE = ur'G:\work\matlab\dn\bayes_rset\data_lnbr.xls'
XLS_FILE = ur'G:\work\matlab\dn\bayes_rset\data_conlnbr.xls'
XLS_FILE = ur'D:\2014项目\配电网故障定位\yx.xls'

def test():
    ret = []
    book = xlrd.open_workbook(XLS_FILE)
    startrowidx = 1
    for sheet in book.sheets():
        sheetdata = []
        header = []
        for i in range(0, 8):
            header.append(sheet.cell_value(0, i).strip())
        for row in range(startrowidx, sheet.nrows):
            v = OrderedDict()
            for col in range(0, 8):
                if col == 0:
                    v[header[col]] = int(sheet.cell_value(row, col))
                else:
                    v[header[col]] = sheet.cell_value(row, col)
            sheetdata.append(v)
        ret.append(sheetdata)
    s = json.dumps(ret, ensure_ascii=True, indent=4)
    # with codecs.open(XLS_FILE.replace('.xls', '.json'), 'w', 'utf-8-sig') as f:
    with open(XLS_FILE.replace('.xls', '.json'), 'w') as f:
        f.write(s)
    # print(s)

def test1():
    ret = []
    book = xlrd.open_workbook(XLS_FILE)
    startrowidx = 1
    sheet = book.sheets()[0]#book.get_sheet(0)

    header = []
    for i in range(0, 10):
        header.append(sheet.cell_value(0, i).strip())
    for row in range(startrowidx, sheet.nrows):
        v = OrderedDict()
        for col in range(0, 10):
            if col == 0:
                v[header[col]] = int(sheet.cell_value(row, col))
            else:
                v[header[col]] = sheet.cell_value(row, col)
        ret.append(v)
    s = json.dumps(ret, ensure_ascii=True, indent=4)
    # with codecs.open(XLS_FILE.replace('.xls', '.json'), 'w', 'utf-8-sig') as f:
    with open(XLS_FILE.replace('.xls', '.json'), 'w') as f:
        f.write(s)
    # print(s)




def test2():
    book = xlrd.open_workbook(XLS_FILE)
    startrowidx = 1
    for sheet in book.sheets():
        if sheet.name == u'负荷开关':
            for row in range(startrowidx, sheet.nrows):
                o = {}
                lng = sheet.cell_value(row, 8)
                lat = sheet.cell_value(row, 9)
                if isinstance(lng, str) or isinstance(lng, unicode) or isinstance(lat, str) or isinstance(lat, unicode):
                    pass
                elif isinstance(lng, float) and  isinstance(lat, float):
                    o['type'] = 'Feature'
                    o['properties'] = {}
                    # o['properties']['device_id'] = sheet.cell_value(row, 0)
                    o['properties']['webgis_type'] = 'point_dn'
                    o['properties']['function_pos_code'] = sheet.cell_value(row, 1)
                    o['properties']['function_pos_name'] = sheet.cell_value(row, 2)
                    o['properties']['function_pos_type'] = 'PAD'
                    o['properties']['owner'] = sheet.cell_value(row, 4)
                    # o['properties']['line_no'] = str(int(sheet.cell_value(row, 5)))
                    o['properties']['device_no'] = sheet.cell_value(row, 10)
                    # o['properties']['tower'] = None
                    if isinstance(sheet.cell_value(row, 12), float):
                        o['properties']['voltage_rated'] = sheet.cell_value(row, 12)
                    if isinstance(sheet.cell_value(row, 13), float):
                        o['properties']['current_rated'] = sheet.cell_value(row, 13)
                    o['geometry'] = {'type':'Point','coordinates':[lng, lat]}
                    o = update_geometry2d(o, True)
                    print(o['properties']['device_no'])


        if sheet.name == u'断路器':
            for row in range(startrowidx, sheet.nrows):
                o = {}
                lng = sheet.cell_value(row, 8)
                lat = sheet.cell_value(row, 9)
                if isinstance(lng, str) or isinstance(lng, unicode) or isinstance(lat, str) or isinstance(lat, unicode):
                    pass
                elif isinstance(lng, float) and  isinstance(lat, float):
                    o['type'] = 'Feature'
                    o['properties'] = {}
                    # o['properties']['device_id'] = sheet.cell_value(row, 0)
                    o['properties']['webgis_type'] = 'point_dn'
                    o['properties']['function_pos_code'] = sheet.cell_value(row, 1)
                    o['properties']['function_pos_name'] = sheet.cell_value(row, 2)
                    o['properties']['function_pos_type'] = 'PAC'
                    o['properties']['owner'] = sheet.cell_value(row, 4)
                    # o['properties']['line_no'] = str(int(sheet.cell_value(row, 5)))
                    o['properties']['device_no'] = sheet.cell_value(row, 10)
                    # o['properties']['tower'] = None
                    if isinstance(sheet.cell_value(row, 12), float):
                        o['properties']['voltage_rated'] = sheet.cell_value(row, 12)
                    if isinstance(sheet.cell_value(row, 13), float):
                        o['properties']['current_rated'] = sheet.cell_value(row, 13)
                    o['geometry'] = {'type':'Point','coordinates':[lng, lat]}
                    o = update_geometry2d(o, True)
                    print(o['properties']['device_no'])

        if sheet.name == u'隔离开关':
            for row in range(startrowidx, sheet.nrows):
                o = {}
                lng = sheet.cell_value(row, 8)
                lat = sheet.cell_value(row, 9)
                if isinstance(lng, str) or isinstance(lng, unicode) or isinstance(lat, str) or isinstance(lat, unicode):
                    pass
                elif isinstance(lng, float) and  isinstance(lat, float):
                    o['type'] = 'Feature'
                    o['properties'] = {}
                    # o['properties']['device_id'] = sheet.cell_value(row, 0)
                    o['properties']['webgis_type'] = 'point_dn'
                    o['properties']['function_pos_code'] = sheet.cell_value(row, 1)
                    o['properties']['function_pos_name'] = sheet.cell_value(row, 2)
                    o['properties']['function_pos_type'] = 'PAE'
                    o['properties']['owner'] = sheet.cell_value(row, 4)
                    # o['properties']['line_no'] = str(int(sheet.cell_value(row, 5)))
                    o['properties']['device_no'] = sheet.cell_value(row, 10)
                    # o['properties']['tower'] = None
                    if isinstance(sheet.cell_value(row, 12), float):
                        o['properties']['voltage_rated'] = sheet.cell_value(row, 12)
                    if isinstance(sheet.cell_value(row, 13), float):
                        o['properties']['current_rated'] = sheet.cell_value(row, 13)
                    o['geometry'] = {'type':'Point','coordinates':[lng, lat]}
                    o = update_geometry2d(o, True)
                    print(o['properties']['device_no'])

def test3():
    XLS_FILE = ur'D:\2014项目\配电网故障定位\玉溪局台账数据导出1\玉溪杆塔.xls'

def test4():
    XLS_FILE = ur'D:\2014项目\配电网故障定位\玉溪局台账数据导出1\线路台账.xls'
    book = xlrd.open_workbook(XLS_FILE)
    startrowidx = 1
    toplines = set()
    for sheet in book.sheets():
        for row in range(startrowidx, sheet.nrows):
            # o = {'properties':{'webgis_type':'polyline_dn'}}
            # o['properties']['func_pos_code'] = sheet.cell_value(row, 1)
            # o['properties']['name'] = sheet.cell_value(row, 2)
            # o['properties']['owner'] = sheet.cell_value(row, 3)
            # update_geometry2d(o, False)
            if len(sheet.cell_value(row, 6)):
                toplines.add(sheet.cell_value(row, 6))
        # print(toplines)
        for row in range(startrowidx, sheet.nrows):
            funcpos = sheet.cell_value(row, 1)
            if funcpos in toplines:
                o = {'properties':{'webgis_type':'polyline_dn'}}
                o['properties']['func_pos_code'] = funcpos
                o['properties']['name'] = sheet.cell_value(row, 2)
                o['properties']['owner'] = sheet.cell_value(row, 3)
                o = update_geometry2d(o, False)
                print(o)





if __name__ == "__main__":
    init_global()
    test4()
    
    