# -*- coding: utf-8 -*-
import os,sys, codecs
import subprocess
from py3o.template import Template


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


LIBREOFFICE_EXECUTEABLE = ur'E:\Program Files (x86)\LibreOffice\program\soffice.exe'
TEMPLATE_ROOT = ur'F:\work\html\temp_web\form_templates\document'
EXPORT_ROOT = ur'F:\work\html\temp_web\form_templates\document\export'

TEMPLATE = os.path.join(TEMPLATE_ROOT, u'《企业(字号)名称预先核准申请表》_template.odt')
OUTPUT = os.path.join(TEMPLATE_ROOT, u'《企业(字号)名称预先核准申请表》_output.odt')
EXPORT_OUTPUT = u'《企业(字号)名称预先核准申请表》'
EXPORT_INPUT = os.path.join(TEMPLATE_ROOT, u'《企业(字号)名称预先核准申请表》.doc')


class Item(object):
    pass




def render(data):
    t = Template(TEMPLATE, OUTPUT)
    t.render(data)
    
def test_export(ext):
    format = 'pdf'
    if ext == 'pdf':
        #format = 'pdf:writer pdf Export'
        format = 'pdf'
        #format = 'pdf:writer web pdf Export'
    elif ext == 'doc':
        format = 'doc:MS Word 97'
    elif ext == 'docx':
        format = 'docx:MS Word 2007 XML'
    elif ext == 'html':
        format = 'html:XHTML Writer File'
    cmd = [
        enc1(LIBREOFFICE_EXECUTEABLE),
           '--headless',
           '--convert-to',
           format,
           '--outdir',
           enc1(EXPORT_ROOT),
           enc1(EXPORT_INPUT)
    ]
    
    if not os.path.exists(EXPORT_ROOT):
        os.mkdir(EXPORT_ROOT)
    p1 = os.path.join(EXPORT_ROOT, '%s.%s' % (EXPORT_OUTPUT, ext))
    if os.path.exists(p1):
        os.remove(p1)
    subprocess.check_output(cmd)
    
def test_render():
    document = Item()
    document.company_name = u'aaa'
    document.company_registration_apply_type1 = u'\u2610'
    document.company_registration_apply_type2 = u'\u2611'
    #items1 = []
    #for i in range(10):
        #item = Item()
        #item.name = u'%s - %d' %( u'发达省份试点', i)
        #item.id_no = u'%s - %d%d%d' %( u'发达省份试点身份证', i, i, i)
        #items1.append(item)
    #items2 = []
    #for i in range(10):
        #item = Item()
        #item.old_content = u'%s - %d' %( u'阿斯发大幅度', i)
        #item.new_content = u'%s - %d%d%d' %( u'阿斯发大幅度new', i, i, i)
        #items2.append(item)
    
    #data = {'items1':items1, 'items2':items2, 'document':document}
    data = {'document':document}
    render(data)
    

if __name__=="__main__":
    test_export('html')
    