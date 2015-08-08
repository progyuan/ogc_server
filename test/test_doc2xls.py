# -*- coding: utf-8 -*-
import os, sys, subprocess
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



#DIR_ROOT = ur'D:\TDDOWNLOAD\附件3：安规学习资料'
LIBREOFFICE_EXECUTEABLE = ur'E:\Program Files (x86)\LibreOffice\program\soffice.exe'
DIR_ROOT = ur'D:\TDDOWNLOAD\附件5 昆明供电局2015年安全工作规程考试复习题'
DIR_ROOT = ur'D:\客观题\客观题'
TXT_DIR = ur'D:\TDDOWNLOAD\附件5 昆明供电局2015年安全工作规程考试复习题\txt'
EXPORT_PATH = os.path.join(DIR_ROOT, u'result.xls')
EXPORT_PATH = os.path.join(DIR_ROOT, u'result.json')
EXPORT_PATH1 = os.path.join(DIR_ROOT, u'result1.json')



def doc_to_mediawiki(fileext):
    ret = []
    if not os.path.exists(TXT_DIR):
        os.mkdir(TXT_DIR)
    for root, dirs, files  in os.walk(DIR_ROOT, topdown=False):
        for name in files:
            ext = name[name.rindex('.'):]
            if ext == '.%s' % fileext:
                p = os.path.join(root, name)
                print('converting to txt: %s ...' % p)
                #cmd = ur'"%s" --headless --convert-to txt:MediaWiki --outdir "%s" "%s"' % (LIBREOFFICE_EXECUTEABLE, TXT_DIR, p)
                cmd = [
                    enc1(LIBREOFFICE_EXECUTEABLE),
                       '--headless',
                       '--convert-to',
                       'txt:MediaWiki',
                       '--outdir',
                       enc1(TXT_DIR),
                       enc1(p)
                ]
                p1 = os.path.join(TXT_DIR, name.replace(ext, '.txt'))
                if os.path.exists(p1):
                    os.remove(p1)
                subprocess.check_output(cmd)
                ret.append(p1)
    return ret
    

def get_txt_files(adir):
    ret = []
    for root, dirs, files  in os.walk(adir, topdown=False):
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
            if "<center>'''" in s or '</center>' in s:
                continue
            if u"答案要点： " in s:
                continue
            if u"、单选题" in s:
                continue
            if u"、多选题" in s:
                continue
            if u"姓名 单位 准考证号 分数" in s:
                continue
            if u"密封线 " in s:
                continue
            #if len(re.findall(r'^\d+\.', s))>0:
                #l = re.findall(r'^\d+\.', s)
            if len(re.findall(ur'^\d+．', s))>0:
                l = re.findall(ur'^\d+．', s)
                o['title'] = s.replace(l[0], '')
            if len(re.findall(ur'^[ABCDEFGHI]．', s))>0:
                if not o.has_key('choice'):
                    o['choice'] = ''
                o['choice'] += ' ' + s
            if u'答案：' in s:
                #o['answer'] = s
                o['answer'] = s.upper()
                
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
                            if u'E．' in c:
                                s = c[c.index(u'D．')+2:c.index(u'E．')]
                                o['answer'].append({'text':s.strip(), 'correct':(u'D' in ans)})
                                if u'F．' in c:
                                    s = c[c.index(u'E．')+2:c.index(u'F．')]
                                    o['answer'].append({'text':s.strip(), 'correct':(u'E' in ans)})
                                    if u'G．' in c:
                                        s = c[c.index(u'F．')+2:c.index(u'G．')]
                                        o['answer'].append({'text':s.strip(), 'correct':(u'F' in ans)})
                                        if u'H．' in c:
                                            s = c[c.index(u'G．')+2:c.index(u'H．')]
                                            o['answer'].append({'text':s.strip(), 'correct':(u'G' in ans)})
                                            if u'I．' in c:
                                                s = c[c.index(u'H．')+2:c.index(u'I．')]
                                                o['answer'].append({'text':s.strip(), 'correct':(u'H' in ans)})
                            
                                            else:
                                                s = c[c.index(u'H．')+2:]
                                                o['answer'].append({'text':s.strip(), 'correct':(u'H' in ans)})
                                        else:
                                            s = c[c.index(u'G．')+2:]
                                            o['answer'].append({'text':s.strip(), 'correct':(u'G' in ans)})
                                    else:
                                        s = c[c.index(u'F．')+2:]
                                        o['answer'].append({'text':s.strip(), 'correct':(u'F' in ans)})
                                else:
                                    s = c[c.index(u'E．')+2:]
                                    o['answer'].append({'text':s.strip(), 'correct':(u'E' in ans)})
                            else:
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
        
        
    

def json_to_mongodb_import(path):
    ret = ''
    with open(path) as f: 
        arr = json.loads(f.read())
        print('total [%d], converting to mongodb import format...' % len(arr))
        for i in arr:
            ret += json.dumps(i, ensure_ascii=False, indent=4) + '\n'
    with open(EXPORT_PATH1, 'w') as f1:
        f1.write(enc(ret))
    print('Done')
            
def main():
    total = []
    files = doc_to_mediawiki('doc')
    for i in files:
        print('parsing %s ...' % i)
        l = parse_txt(i)
        total.extend (l)
    #print(total)
    #export_to_xls(total)
    ret = export_to_json(total)
    body = json.dumps(ret, ensure_ascii=False, indent=4)
    with open(EXPORT_PATH, 'w') as f:
        f.write(enc(body))
    json_to_mongodb_import(EXPORT_PATH)

def get_xls_files(adir):
    ret = []
    for root, dirs, files  in os.walk(adir, topdown=False):
        for name in files:
            ext = name[-4:]
            if ext == '.xls':
                p = os.path.join(root, name)
                ret.append( p)
    return ret

def parse_one_sheet(sheet):
    ret = []
    for row in range(1, sheet.nrows):
        o = {}
        o['question'] = sheet.cell_value(row,  1).strip()
        o['answer'] = []
        ans = sheet.cell_value(row,  6).strip().upper()
        if len(ans) == 1:
            o['type'] = 'single'
        else:
            o['type'] = 'multi'
        for i in range(2, 6):
            o1 = {}
            v = sheet.cell_value(row,  i)
            if isinstance(v, float) or isinstance(v, int):
                v = str(v)
            o1['text'] = v.strip()
            o1['correct'] = False
            choice = ''
            if i == 2:
                choice = u'A'
            if i == 3:
                choice = u'B'
            if i == 4:
                choice = u'C'
            if i == 5:
                choice = u'D'
            if choice in ans:
                o1['correct'] = True
            o['answer'].append(o1)
        ret.append(o)
    return ret

def parse_one_book(path):
    ret = []
    print('processing %s...' % enc1(path))
    book = xlrd.open_workbook(path)
    for sheet in  book.sheets():
        ret.extend(parse_one_sheet(sheet))
        # break
    return ret



def exam():
    l = get_xls_files(DIR_ROOT)
    ret = []
    for path in l:
        ret.extend(parse_one_book(path))
        # break
    print(len(ret))
    with codecs.open(ur'd:\aaa.json', 'w', 'utf-8-sig' ) as f:
        f.write(json.dumps(ret, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    exam()
    