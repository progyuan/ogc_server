# -*- coding: utf-8 -*-
import os, sys
import json
import xlrd
import codecs
from collections import  OrderedDict

XLS_FILE = ur'G:\work\matlab\dn\bayes_rset\data_bus.xls'
XLS_FILE = ur'G:\work\matlab\dn\bayes_rset\data_lnbr.xls'
XLS_FILE = ur'G:\work\matlab\dn\bayes_rset\data_conlnbr.xls'

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

if __name__ == "__main__":
    test1()
    
    