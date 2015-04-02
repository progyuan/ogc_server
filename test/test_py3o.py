# -*- coding: utf-8 -*-
import os,sys
from py3o.template import Template

TEMPLATE_ROOT = ur'F:\work\html\temp_web\odt'

TEMPLATE = os.path.join(TEMPLATE_ROOT, u'《企业(字号)名称预先核准申请表》_template.odt')
OUTPUT = os.path.join(TEMPLATE_ROOT, u'《企业(字号)名称预先核准申请表》_output.odt')


class Item(object):
    pass




def render(data):
    t = Template(TEMPLATE, OUTPUT)
    t.render(data)
    

if __name__=="__main__":
    document = Item()
    document.name = u'反对萨芬的萨浮点数'
    document.name1 = u'反对萨芬的萨浮点数1'
    document.name2 = u'反对萨芬的萨浮点数2'
    document.name3 = u'反对萨芬的萨浮点数3'
    items1 = []
    for i in range(10):
        item = Item()
        item.name = u'%s - %d' %( u'发达省份试点', i)
        item.id_no = u'%s - %d%d%d' %( u'发达省份试点身份证', i, i, i)
        items1.append(item)
    items2 = []
    for i in range(10):
        item = Item()
        item.old_content = u'%s - %d' %( u'阿斯发大幅度', i)
        item.new_content = u'%s - %d%d%d' %( u'阿斯发大幅度new', i, i, i)
        items2.append(item)
    
    data = {'items1':items1, 'items2':items2, 'document':document}
    render(data)
    
    