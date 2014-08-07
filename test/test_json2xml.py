# -*- coding: utf-8 -*-
import os, sys
import json
from lxml import etree

ENCODING = 'utf-8'

JSON_FILE = ur'D:\2014项目\jiakongztpj.json'
XML_FILE = JSON_FILE.replace('.json', '.xml')
XML_FILE_STANDARD = ur'D:\2014项目\状态评价\输电线路状态评价标准.xml'
XML_FILE_CA_REQUEST = ur'D:\2014项目\状态评价\输电线路状态评价数据请求.xml'
XML_FILE_CA_RESPONSE = ur'D:\2014项目\状态评价\输电线路状态评价数据响应.xml'



def format_value(value):
    if isinstance(value, int) or isinstance(value, float):
        return str(value)
    else:
        return value
    
def json2xml():
    o = None
    with open(JSON_FILE) as f:
        s = f.read()
        #print(s)
        o = json.loads(s)
    if o:
        root = etree.Element("root")
        for i in o:
            item = etree.SubElement(root, "item")
            for k in ['category', 'parent','index', 'name', 'weight', 'levels']:
                if k == 'levels':
                    levels = etree.SubElement(item, "levels")
                    for kk in ['I','II','III','IV']:
                        if i[k].has_key(kk):
                            level = etree.SubElement(levels, kk)
                            for kkk in i[k][kk].keys():
                                according = etree.SubElement(level, kkk).text = format_value(i[k][kk][kkk])
                            
                else:
                    obj = etree.SubElement(item, k).text = format_value(i[k])
        ret = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding=ENCODING)
        
        with open(XML_FILE_STANDARD, 'w') as f:
            f.write(ret)

#data = [{'index':18,'level':u'II', 'description':u'#97 A相绝缘子自爆一片（导线起第16片）'}]            
def condition_assessment_req_xml(data):
    
    def get_data_by_index(index, data):
        ret = None
        for i in data:
            if i['index'] == index:
                ret = i
                break
        return ret
    
    root = etree.Element("root")
    records = etree.SubElement(root, 'records')
    record = etree.SubElement(records, 'record')
    category = etree.SubElement(record, "category").text = u'110kV～500kV架空输电线路'
    etree.SubElement(record, "name").text = u'七罗I回线'
    etree.SubElement(record, "check_year").text = u'2013'
    total_lost_score = etree.SubElement(record, "total_lost_score")
    etree.SubElement(record, "collaborate_factor").text = u'1.0'
    
    items = etree.SubElement(record, "items")
    
    score = 0
    o = None
    with open(JSON_FILE) as f:
        s = f.read()
        #print(s)
        o = json.loads(s)
    if o:
        for i in o:
            item = etree.SubElement(items, "item")
            index = i['index']
            #level_fault = None
            #if 
            for k in ['index', 'parent', 'name', 'weight', 'levels',]:
                if k == 'levels':
                    levels = etree.SubElement(item, "levels")
                    for kk in ['I','II','III','IV']:
                        if i[k].has_key(kk):
                            level = etree.SubElement(levels, kk)
                            according = etree.SubElement(level, 'according').text = format_value(i[k][kk]['according'])
                            base_score = etree.SubElement(level, 'base_score').text = format_value(i[k][kk]['base_score'])
                            lost_score = etree.SubElement(level, "lost_score")
                            description = etree.SubElement(level, "description")
                            d = get_data_by_index(index, data)
                            if d and d['level'] == kk:
                                sco = i['weight'] * i[k][kk]['base_score']
                                score += sco
                                lost_score.text = format_value(sco)
                                description.text = d['description']
                            else:
                                lost_score.text = format_value(0)
                                description.text = u''
                                
                            
                else:
                    etree.SubElement(item, k).text = format_value(i[k])
    total_lost_score.text = format_value(score)
    ret = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding=ENCODING)
    print(ret)
    with open(XML_FILE_CA_REQUEST, 'w') as f:
        f.write(ret)
    
def condition_assessment_resp_xml():
    records = etree.Element("records")
    record = etree.SubElement(records, "record")
    etree.SubElement(record, "category").text = u'110kV～500kV架空输电线路'
    etree.SubElement(record, "name").text = u'七罗I回线'
    etree.SubElement(record, "estimate_year").text = u'2014'
    
    etree.SubElement(record, "I").text = u'0.05'
    
    
    
    etree.SubElement(record, "probability_I").text = u'0.05'
    etree.SubElement(record, "probability_II").text = u'0.0'
    etree.SubElement(record, "probability_III").text = u'0.2'
    etree.SubElement(record, "probability_IV").text = u'0.5'
    
    units = etree.SubElement(record, "units")
    
    unit = etree.SubElement(units, "unit")
    etree.SubElement(unit, "name").text = u'基础'
    etree.SubElement(unit, "probability_I").text = u'0.05'
    etree.SubElement(unit, "probability_II").text = u'0.0'
    etree.SubElement(unit, "probability_III").text = u'0.2'
    etree.SubElement(unit, "probability_IV").text = u'0.5'
    
    unit = etree.SubElement(units, "unit")
    etree.SubElement(unit, "name").text = u'杆塔'
    etree.SubElement(unit, "probability_I").text = u'0.05'
    etree.SubElement(unit, "probability_II").text = u'0.0'
    etree.SubElement(unit, "probability_III").text = u'0.2'
    etree.SubElement(unit, "probability_IV").text = u'0.5'
    
    unit = etree.SubElement(units, "unit")
    etree.SubElement(unit, "name").text = u'导地线'
    etree.SubElement(unit, "probability_I").text = u'0.05'
    etree.SubElement(unit, "probability_II").text = u'0.0'
    etree.SubElement(unit, "probability_III").text = u'0.2'
    etree.SubElement(unit, "probability_IV").text = u'0.5'
    
    unit = etree.SubElement(units, "unit")
    etree.SubElement(unit, "name").text = u'绝缘子'
    etree.SubElement(unit, "probability_I").text = u'0.05'
    etree.SubElement(unit, "probability_II").text = u'0.0'
    etree.SubElement(unit, "probability_III").text = u'0.2'
    etree.SubElement(unit, "probability_IV").text = u'0.5'
    
    unit = etree.SubElement(units, "unit")
    etree.SubElement(unit, "name").text = u'金具'
    etree.SubElement(unit, "probability_I").text = u'0.05'
    etree.SubElement(unit, "probability_II").text = u'0.0'
    etree.SubElement(unit, "probability_III").text = u'0.2'
    etree.SubElement(unit, "probability_IV").text = u'0.5'
    
    unit = etree.SubElement(units, "unit")
    etree.SubElement(unit, "name").text = u'接地装置'
    etree.SubElement(unit, "probability_I").text = u'0.05'
    etree.SubElement(unit, "probability_II").text = u'0.0'
    etree.SubElement(unit, "probability_III").text = u'0.2'
    etree.SubElement(unit, "probability_IV").text = u'0.5'
    
    unit = etree.SubElement(units, "unit")
    etree.SubElement(unit, "name").text = u'附属设施'
    etree.SubElement(unit, "probability_I").text = u'0.05'
    etree.SubElement(unit, "probability_II").text = u'0.0'
    etree.SubElement(unit, "probability_III").text = u'0.2'
    etree.SubElement(unit, "probability_IV").text = u'0.5'
    
    unit = etree.SubElement(units, "unit")
    etree.SubElement(unit, "name").text = u'通道环境'
    etree.SubElement(unit, "probability_I").text = u'0.05'
    etree.SubElement(unit, "probability_II").text = u'0.0'
    etree.SubElement(unit, "probability_III").text = u'0.2'
    etree.SubElement(unit, "probability_IV").text = u'0.5'
    
    ret = etree.tostring(records, pretty_print=True, xml_declaration=True, encoding=ENCODING)
    print(ret)
    with open(XML_FILE_CA_RESPONSE, 'w') as f:
        f.write(ret)
    
if __name__ == "__main__":
    #json2xml()
    data = [{'index':18, 'level':'II', 'description':u'#97 A相绝缘子自爆一片（导线起第16片）'},
            {'index':33, 'level':'III', 'description':u'1、#4国土资源学校建设施工，其中#3-#4之间20米左右新建房屋时常有大型施工机械进入线路保护区，可能造成对线路距离不足引起跳闸。2、#4-#5通道内有桉树300棵左右，与导线垂直距离7.5米—8米；#59-#61通道内有桉树1000棵左右，与导线垂直距离8米左右。'}
            ]
    condition_assessment_req_xml(data)
    #condition_assessment_resp_xml()
    
    