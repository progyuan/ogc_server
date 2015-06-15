# -*- coding: utf-8 -*-

import os, sys, codecs
import StringIO
import xlrd, xlwt
from lxml import etree


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

ROOTDIR = ur'D:\2014项目\状态评价\xml'
INPUTFILE = 'input_data.xml'
TEMPLATE = 'template.xml'
XLS_FILES = [ur'D:\2014项目\贝叶斯\贝叶斯隐形故障系统状态评价数据(2010-2015)\2011年 全局输电线路设备状态评价统201108271.xls', ]

def build_exist_dict():
    p = os.path.join(ROOTDIR, INPUTFILE)
    tree = etree.parse(p)
    rn = tree.getroot()
    m = {}
    for i in rn:
        if i.attrib.has_key('check_year'):
            #print('%s %s' % (i.attrib['check_year'], i.attrib['name']))
            if not m.has_key(i.attrib['line_name']):
                m[i.attrib['line_name']] = []
            m[i.attrib['line_name']].append(i.attrib['check_year'])
    return m
    #print(m)
    #for k in m.keys():
        #pp = os.path.join(ROOTDIR, 'input_data_%s.xml' % k)
        #records = etree.Element("records")
        ##records.append('\n')
        #for i in m[k]:
            #records.append(i)
        #ret = etree.tostring(records, pretty_print=True, xml_declaration=True, encoding='utf-8')
        #with open(pp, 'w') as f:
            #f.write(ret)
def print_dict(d):
    for k in d.keys():
        print(u'%s:%s' % (k, str(d[k])))

def check_name_year_exist(d, name, year):
    ret = False
    for k in d.keys():
        if k == name:
            if year in d[k]:
                ret = True
                break
    return ret

def append_node(rn0, d0, data):
    p = os.path.join(ROOTDIR, TEMPLATE)
    for d in data:
        if not check_name_year_exist(d0, d['line_name'], d['check_year']):
        #if check_name_year_exist(d0, d['line_name'], d['check_year']):
            tree = etree.parse(p)
            rn = tree.getroot()
            rn.attrib['line_name'] = d['line_name']
            rn.attrib['check_year'] = d['check_year']
            rn.attrib['line_state'] = d['line_state']
            list_unit_index = filter(None, d['unit_index'].split('\n')) 
            list_unit_state = filter(None, d['unit_state'].split('\n')) 
            list_item_index = filter(None, d['item_index'].split('\n'))
            list_zip = zip(list_unit_index, list_unit_state, list_item_index)
            for unit in rn[0]:
                #idx = rn[0].index(unit)
                for i in list_zip:
                    unit_index = i[0]
                    if isinstance(unit_index, float):
                        unit_index = int(unit_index)
                    if str(unit.attrib['unit_index']) == str(unit_index):
                        unit.attrib['unit_state'] = i[1]
                        for item in unit[0]:
                            #idx1 = unit[0].index(item)
                            if isinstance(i[2], float):
                                i[2] = int(i[2])
                            if str(item.attrib['item_index']) == str(i[2]):
                                item.attrib['item_state'] = i[1]
                                #unit[0][idx1] = item
                #rn[0][idx] = unit
            #s = etree.tostring(rn, pretty_print=True, xml_declaration=True, encoding='utf-8')
            #print(s)
            rn0.append(rn)
        
                        

def get_all_root():
    p = os.path.join(ROOTDIR, INPUTFILE)
    tree = etree.parse(p)
    rn = tree.getroot()
    return rn
    

def test_data_create():
    ret = []
    d = {}
    d['check_year'] = u'2011'
    d['line_name'] = u'双狮线'
    d['line_state'] = u'IV'
    d['unit_index'] = u'1\n2\n4\n6\n'
    d['unit_state'] = u'IV\nIV\nIII\nIII'
    d['item_index'] = u'3\n7\n17\n25\n'
    ret.append(d)
    return ret

def data_create():
    ret = []
    for i in XLS_FILES:
        book = xlrd.open_workbook(i)
        idx = XLS_FILES.index(i)
        sheet = None
        if idx == 0:
            sheet = book.sheet_by_name(u'检修建议')
            for row in range(1, sheet.nrows):
                d = {}
                d['line_name'] = sheet.cell(row, 9).value
                if len(d['line_name']) > 0:
                    d['check_year'] = dec(str(int(sheet.cell(row, 8).value)))
                    d['line_state'] = sheet.cell(row, 10).value
                    d['unit_index'] = sheet.cell(row, 11).value
                    if isinstance(d['unit_index'], float):
                        d['unit_index'] = str(int(d['unit_index'])) + '\n'
                    d['unit_state'] = sheet.cell(row, 12).value
                    d['item_index'] = sheet.cell(row, 13).value
                    if isinstance(d['item_index'], float):
                        d['item_index'] = str(int(d['item_index'])) + '\n'
                    ret.append(d)
        
    return ret

    
def test():
    rn = None
    rn = get_all_root()
    d0 = build_exist_dict()
    #d = test_data_create()
    d = data_create()
    append_node(rn, d0, d)
    pp = os.path.join(ROOTDIR, 'test_input_data.xml')
    ret = etree.tostring(rn, pretty_print=True, xml_declaration=True, encoding='utf-8')
    with open(pp, 'w') as f:
        f.write(ret)
    
    

if __name__ == "__main__":
    #print(get_params_from_xml(XML))
    #root = etree.XML(XML)
    #print(etree.tostring(root, pretty_print=True))
    #merge_xml1()
    #d = build_dict()
    #print_dict(d)
    test()
    #print(data_create())
    