# -*- coding: utf-8 -*-

import os, sys, codecs
import json
from pydash import py_ as _




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

VCFPATH = ur'd:\联系人_002.vcf'

def test():
    lines = []
    contacts = []
    with open(VCFPATH) as f:
        lines = f.readlines()
    begin = False
    o = None
    for line in lines:
        line = line.strip()
        if line == 'BEGIN:VCARD':
            begin = True
            o = {}
            continue
        if line == 'END:VCARD':
            begin = False
            if o and o.has_key('tel') and o.has_key('name'):
                contacts.append(o)
            continue
        if begin:
            if _.starts_with(line, 'N;'):
                o['name'] = line[line.index(':')+1:]
                o['name'] = o['name'].split(';')
                o['name'] = filter(lambda x:len(x)>0, o['name'])
                o['name'] = map(convert, o['name'])
                o['name'] = ''.join(o['name'])
            if _.starts_with(line, 'TEL;'):
                if not o.has_key('tel'):
                    o['tel'] = []
                o['tel'].append(line[line.index(':')+1:])
    # print(contacts)
    s = json.dumps(contacts, ensure_ascii=False, indent=4)
    with codecs.open(ur'd:\contacts.json', 'w', 'utf-8-sig') as f:
        f.write(s)

def convert(s):
    s = s.replace('=', '\\x')
    return dec(codecs.escape_decode(s)[0])
def printf():
    contacts = []
    with codecs.open(ur'd:\contacts.json', 'r', 'utf-8-sig') as f:
        contacts = json.loads(f.read())
    for contact in contacts:
        print('%s:%s' % (contact['name'], ','.join(contact['tel'])))


if __name__ == "__main__":
    printf()