# -*- coding: utf-8 -*-
import os, sys
import json
import xlrd, xlwt
import re
import codecs


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



DIR_ROOT = ur'D:\TDDOWNLOAD\附件3：安规学习资料'
EXPORT_PATH = os.path.join(DIR_ROOT, u'result.xls')
EXPORT_PATH = os.path.join(DIR_ROOT, u'result.json')

def get_txt_files():
    ret = []
    for root, dirs, files  in os.walk(DIR_ROOT, topdown=False):
        for name in files:
            ext = name[-4:]
            if ext == '.txt':
                p = os.path.join(root, name)
                ret.append( p)
    return ret
    

def parse_txt(path):
    ret = []
    with open(path) as f:
        lines = f.readlines()
        o = {}
        for line in lines:
            s = dec(line.strip())
            if len(s) == 0:
                continue
            if "<center>'''" in s:
                continue
            if len(re.findall(r'^\d+\.', s))>0:
                l = re.findall(r'^\d+\.', s)
                #o['title'] = s.replace(l[0], '')
            if len(re.findall(ur'^[ABCD]．', s))>0:
                if not o.has_key('choice'):
                    o['choice'] = ''
                o['choice'] += ' ' + s
            if u'答案：' in s:
                o['answer'] = s
            if o.has_key('title') and o.has_key('answer'):
                ret.append(o)
                o = {}
    return ret
                
                
def export_to_xls(alist):
    book = xlwt.Workbook()
    sheet = book.add_sheet('Sheet1')
    sheet.write(0, 0, u'题目')
    sheet.write(0, 1, u'选择')
    sheet.write(0, 2, u'答案')
    for i in alist:
        row = alist.index(i) + 1
        sheet.write(row, 0, i['title'])
        sheet.write(row, 2, i['answer'])
        if i.has_key('choice'):
            sheet.write(row, 1, i['choice'])
    book.save(EXPORT_PATH)
    
def export_to_json(alist):
    ret = []
    for i in alist:
        o = {}
        o['question'] = i['title']
        ans = i['answer'].replace(u'答案：', '').strip()
        o['answer'] = []
        if len(ans) == 1:
            o['type'] = 'single'
        if len(ans) > 1:
            o['type'] = 'multi'
        if i.has_key('choice'):
            c = i['choice']
            if u'A．' in c:
                if u'B．' in c:
                    s = c[c.index(u'A．')+2:c.index(u'B．')]
                    o['answer'].append({'text':s.strip(), 'correct':(u'A' in ans)})
                    if u'C．' in c:
                        s = c[c.index(u'B．')+2:c.index(u'C．')]
                        o['answer'].append({'text':s.strip(), 'correct':(u'B' in ans)})   
                        if u'D．' in c:
                            s = c[c.index(u'C．')+2:c.index(u'D．')]
                            o['answer'].append({'text':s.strip(), 'correct':(u'C' in ans)})     
                            s = c[c.index(u'D．')+2:]
                            o['answer'].append({'text':s.strip(), 'correct':(u'D' in ans)})
                        else:
                            s = c[c.index(u'C．')+2:]
                            o['answer'].append({'text':s.strip(), 'correct':(u'C' in ans)})
                    else:
                        s = c[c.index(u'B．')+2:]
                        o['answer'].append({'text':s.strip(), 'correct':(u'B' in ans)})
                else:
                    s = c[c.index(u'A．')+2:]
                    o['answer'].append({'text':s.strip(), 'correct':(u'A' in ans)})
        else:
            o['type'] = 'bool'
            if u'对' in ans:
                o['answer'] = True
            if u'错' in ans:
                o['answer'] = False
        ret.append(o)
    return ret
        
        
                            
                
    
    
    
if __name__ == "__main__":
    total = []
    files = get_txt_files()
    for i in files:
        total.extend (parse_txt(i))
    #print(total)
    #export_to_xls(total)
    ret = export_to_json(total)
    body = json.dumps(ret, ensure_ascii=False, indent=4)
    with open(EXPORT_PATH, 'w') as f:
        f.write(enc(body))
    