# -*- coding: utf-8 -*-
import os, sys
import json
import xlrd
import uuid

XLS_FILE = ur'F:\work\csharp\kmgdnew10.2-2014-1-17\交流220kV永发II回线杆塔明细表.xls'

def get_full_path(fname):
    for root, dirs, files  in os.walk(XSD_ROOT, topdown=False):
        for name in files:
            bname = name[:name.index('.')]
            if bname == fname:
                p = os.path.join(root, name)
                return p
    return None
    
def parse_tower_xls_file(line_name, xls_file):
    
    #TABLE_TOWER
    def extract_tower(sheet, line_id):
        towers = []
        towers_id_name_mapping = {}
        for i in range(sheet.nrows):
            if i >= 7:
                tower_id = str(uuid.uuid4())
                tower = {'id':tower_id, 'line_id':line_id}
                for j in range(sheet.ncols):
                    v = sheet.cell_value(i,j)
                    if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                        if '\n' in v:
                            arr = v.split('\n')
                            s = ''
                            for k in arr:
                                s += k + ','
                            if len(s)>0:
                                s = s[:-1]
                            v = s
                        print('(%d,%d)=%s' % (i, j, v))
                        if j == 2:
                            tower['tower_name'] = line_name + v
                            towers_id_name_mapping[v] = tower['id']
                        elif j == 4:
                            arr = v.split(' - ')
                            tower['model_code'] = arr[0]
                            tower['denomi_height'] = int(arr[1])
                        elif j == 7:
                            tower['model_code'] = arr[0]
                    elif isinstance(v, int):
                        print('(%d,%d)=%d' % (i, j, v))
                    elif isinstance(v, float):
                        print('(%d,%d)=%f' % (i, j, v))
                        if j == 7:
                            tower['horizontal_span'] = v
                        elif j == 8:
                            tower['vertical_span'] = v
                        elif j == 9:
                            tower['building_level'] = v
                        elif j == 10:
                            tower['line_rotate'] = v
                        elif j == 42:
                            tower['geo_x'] = v
                        elif j == 43:
                            tower['geo_y'] = v
                if tower.has_key('tower_name'):
                    towers.append(tower)
        return towers, towers_id_name_mapping
    
    #TABLE_STRAIN_SECTION
    def extract_strain(sheet, line_id):
        for i in range(sheet.nrows):
            if i >= 7:
                strain_id = str(uuid.uuid4())
                strain = {'id':strain_id, 'line_id':line_id}
                for j in range(sheet.ncols):
                    if j == 1:
                        v = sheet.cell_value(i,j)
                        if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                            if '/' in v:
                                arr = v.split('/')
                                print('(%d,%d)=%f, %f, %f' % (i, j, float(arr[0]), float(arr[1]), float(arr[2])))
                                v1 = heet.cell_value(i-1,j+1)
                                v2 = heet.cell_value(i+1,j+1)
                                print('start=%s, end=%s' % (v1))
    
    book = xlrd.open_workbook(xls_file)
    sheet = book.sheet_by_index(0)
    line_id = str(uuid.uuid4())
    #towers, towers_id_name_mapping = extract_tower(sheet, line_id)
    extract_strain(sheet, line_id)
            
    
    #print(towers)
    #print(len(towers))
    #print(len(towers_id_name_mapping.keys()))




    
if __name__ == "__main__":
    parse_tower_xls_file(u'永发II回线', XLS_FILE)
    
    