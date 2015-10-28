# -*- coding: utf-8 -*-
import os
import sys
import json
import codecs
import xlrd
from pydash import py_ as _

XLSPATH = ur'D:\2014项目\贝叶斯\json2014excel.xls'


def test():
    ret = []
    book = xlrd.open_workbook(XLSPATH)
    sheet = book.sheet_by_index(0)
    startrowidx = 1
    units = set()
    for i in range(startrowidx, sheet.nrows):
        id = sheet.cell_value(i, 1).strip().lower()
        unit = sheet.cell_value(i, 2).strip().lower()
        cat = sheet.cell_value(i, 4).strip()
        name = sheet.cell_value(i, 5).strip()
        level = sheet.cell_value(i, 6).strip()
        base_score = int(sheet.cell_value(i, 7))
        weight = int(sheet.cell_value(i, 8))
        total_score = int(sheet.cell_value(i, 9))
        p0_I = float(sheet.cell_value(i, 10))
        p0_II = float(sheet.cell_value(i, 11))
        p0_III = float(sheet.cell_value(i, 12))
        p0_IV = float(sheet.cell_value(i, 13))
        according = sheet.cell_value(i, 14).strip()
        if not unit in units:
            units.add(unit)
            ret.append({'unit':unit, 'children':[]})
        uuu = _.find(ret, {'unit':unit})
        if uuu:
            o = {}
            o['id'] = id
            o['cat'] = cat
            o['name'] = name
            o['level'] = level
            o['base_score'] = base_score
            o['weight'] = weight
            o['total_score'] = total_score
            o['according'] = according
            o['p0'] = {'I':p0_I, 'II':p0_II, 'III':p0_III, 'IV':p0_IV,}
            uuu['children'].append(o)

    with codecs.open(ur'd:\aaa.json', 'w', 'utf-8-sig' ) as f:
        f.write(json.dumps(ret, ensure_ascii=False, indent=4))



if __name__=="__main__":
    test()
    
    
    