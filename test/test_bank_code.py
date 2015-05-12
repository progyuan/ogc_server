# -*- coding: utf-8 -*-
import os
import sys
import codecs
import json
import time
import requests

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

HOST = 'http://www.zybank.com.cn'
CITIESJSON = ur'F:\work\html\combiz\china_cities.json'
BANKSJSON = ur'F:\work\html\combiz\bank_code.json'
BRANCHDIR = ur'F:\work\html\combiz\bank'


def getbranches(city, bank):
    url = HOST + "/zyb/queryallrtgsnode.do"
    response = requests.post(url, {'cityCode':city, 'clsCode':bank})
    #s = dec(response.content)
    s = response.content
    ret = json.loads(s)
    #ret = json.dumps(o, ensure_ascii=False, indent=4)
    #with codecs.open(ur'F:\work\html\combiz\aaa.json', 'w', 'utf-8-sig') as f:
        #f.write(ret)
    return ret


def getcities(path, province_code=None):
    ret = []
    with open(path) as f:
        arr = json.loads(f.read().decode("utf-8-sig"))
    if province_code:
        for province in arr:
            if province['provinceCode'] == province_code:
                ret.append(province)
    else:
        ret = arr
    return ret

def getbanks(path):
    ret = []
    with open(path) as f:
        ret = json.loads(f.read().decode("utf-8-sig"))
    return ret

def build_branches_by_province(province_code):
    provinces = getcities(CITIESJSON, province_code)
    banks = getbanks(BANKSJSON)
    ret = []
    for bank in banks:
        #if bank['bankId'] > 500 or bank['bankId'] < 301:
        if bank['bankId'] != 102:
            continue
        idx2 = banks.index(bank)
        print(bank['bankName'])
        bank1 = {}
        bank1['bankId'] = bank['bankId']
        bank1['bankName'] = bank['bankName']
        bank1['bankBranches'] = []
        for province in provinces:
            province1 = {}
            province1['provinceCode'] = province['provinceCode']
            province1['provinceName'] = province['provinceName']
            province1['cities'] = []
            print('    %s' % province['provinceName'])
            for city in province['city']:
                city1 = {}
                city1['cityCode'] = city['cityCode']
                city1['cityName'] = city['cityName']
                city1['branches'] = getbranches(city['cityCode'], bank['bankId'])
                time.sleep(0.5)
                province1['cities'].append(city1)
            bank1['bankBranches'].append(province1)
        ret.append(bank1)
        savebank(bank['bankId'], bank1)
    return ret
                
def savebank(bankid, bank):
    ret = json.dumps(bank, ensure_ascii=False, indent=4)
    with codecs.open(os.path.join(BRANCHDIR, str(bankid) + '.json'), 'w', 'utf-8-sig') as f:
        f.write(ret)
    
    
    
    
def test():
    banks = build_branches_by_province(53)
    #ret = json.dumps(banks, ensure_ascii=False, indent=4)
    #with codecs.open(ur'F:\work\html\combiz\aaa.json', 'w', 'utf-8-sig') as f:
        #f.write(ret)
    

if __name__=="__main__":
    test()
    #print(getbank(2320, 104))
    
    

        
    
    
    