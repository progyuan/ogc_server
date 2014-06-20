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
                        #print('(%d,%d)=%s' % (i, j, v))
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
                        #print('(%d,%d)=%d' % (i, j, v))
                        pass
                    elif isinstance(v, float):
                        #print('(%d,%d)=%f' % (i, j, v))
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
    def extract_strain(sheet, line_id, id_mapping):
        l = []
        lastrow = 0
        for i in range(sheet.nrows):
            if i >= 7:
                for j in range(sheet.ncols):
                    if j == 1:
                        v = sheet.cell_value(i,j)
                        if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                            if '/' in v:
                                arr = v.split('/')
                                #print('(%d,%d)=%f, %f, %f' % (i, j, float(arr[0]), float(arr[1]), float(arr[2])))
                                l.append({'row':i, 'total_length':float(arr[0]), 'typical_span':float(arr[1]), 'k_value':float(arr[2])})
                    if j == 2:
                        v = sheet.cell_value(i,j)
                        if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                            lastrow = i
                                
        #print('lastrow = %d' % lastrow)
        strains = []
        for i in l:
            strain_id = str(uuid.uuid4())
            strain = {'id':strain_id, 'line_id':line_id}
            
            idx = l.index(i)
            v1 = sheet.cell_value(i['row']-1,2)
            if idx+1 < len(l):
                v2 = sheet.cell_value(l[idx+1]['row']-1,2)
            else:
                v2 = sheet.cell_value(lastrow,2)
            #print('start=%s, end=%s, total_length=%f, typical_span=%f, k_value=%f' % (v1, v2, i['total_length'], i['typical_span'], i['k_value']))
            strain['start_tower'] = id_mapping[v1]
            strain['end_tower'] = id_mapping[v2]
            strain['total_length'] = i['total_length']
            strain['typical_span'] = i['typical_span']
            strain['k_value'] = i['k_value']
            strain['conductor_type'] = ''
            strain['ground_type_left'] = ''
            strain['ground_type_right'] = ''
            strains.append(strain)
        return strains
    
    #TABLE_SEGMENT
    def extract_segment(sheet, line_id, id_mapping):
        l = []
        m = {}
        lastrow = 0
        for i in range(sheet.nrows):
            if i >= 7:
                for j in range(sheet.ncols):
                    if j == 6:
                        v = sheet.cell_value(i,j)
                        if isinstance(v, float) :
                            l.append({'row':i, 'length':v,})
                    if j == 2:
                        v = sheet.cell_value(i,j)
                        if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                            lastrow = i
                                
        segs = []
        for i in l:
            seg_id = str(uuid.uuid4())
            seg = {'id':seg_id, 'line_id':line_id}
            
            idx = l.index(i)
            v1 = sheet.cell_value(i['row']-1,2)
            if idx+1 < len(l):
                v2 = sheet.cell_value(l[idx+1]['row']-1,2)
            else:
                v2 = sheet.cell_value(lastrow,2)
            print('small=%s, big=%s, length=%f' % (v1, v2, i['length']))
            m[v1+v2] = seg_id
            seg['small_tower'] = id_mapping[v1]
            seg['big_tower'] = id_mapping[v2]
            seg['splitting'] = 2
            seg['conductor_count'] = 0
            seg['crosspoint_count'] = 0
            seg['length'] = i['length']
            seg['seperator_bar'] = 0
            seg['connector_count'] = 0
            seg['connector_type'] = ''
            segs.append(seg)
        return segs, m
    
    
    #TABLE_CROSS_POINT
    def extract_crosspoint(sheet, line_id, id_mapping, seg_mapping):
        l = []
        lastrow = 0
        for i in range(sheet.nrows):
            if i >= 7:
                for j in range(sheet.ncols):
                    if j >= 30 and j<=41:
                        v = sheet.cell_value(i,j)
                        if isinstance(v, float) :
                            cp_type = ''
                            if j == 30:
                                cp_type = u'低压线'
                            if j == 31:
                                cp_type = u'通讯线'
                            if j == 32:
                                cp_type = u'电力线'
                            if j == 33:
                                cp_type = u'铁路'
                            if j == 34:
                                cp_type = u'公路'
                            if j == 35:
                                cp_type = u'电车道'
                            if j == 36:
                                cp_type = u'通航河流'
                            if j == 37:
                                cp_type = u'不通航河流'
                            if j == 38:
                                cp_type = u'管道'
                            if j == 39:
                                cp_type = u'索道'
                            if j == 40:
                                cp_type = u'房屋'
                            if j == 41:
                                cp_type = u'林木'
                            if len(cp_type)>0:
                                l.append({'row':i, 'col':j, 'cp_type':cp_type})
                    if j == 2:
                        v = sheet.cell_value(i,j)
                        if (isinstance(v, str) or isinstance(v, unicode)) and len(v)>0:
                            lastrow = i
                                
        cps = []
        for i in l:
            cp_id = str(uuid.uuid4())
            cp = {'id':seg_id, 'line_id':line_id}
            
            idx = l.index(i)
            v1 = sheet.cell_value(i['row']-1,2)
            if idx+1 < len(l):
                v2 = sheet.cell_value(l[idx+1]['row']-1,2)
            else:
                v2 = sheet.cell_value(lastrow,2)
            print('small=%s, big=%s, length=%f' % (v1, v2, i['length']))
            seg['small_tower'] = id_mapping[v1]
            seg['big_tower'] = id_mapping[v2]
            seg['splitting'] = 2
            seg['conductor_count'] = 0
            seg['crosspoint_count'] = 0
            seg['length'] = i['length']
            seg['seperator_bar'] = 0
            seg['connector_count'] = 0
            seg['connector_type'] = ''
            segs.append(seg)
        return []
    
    
    
    
    book = xlrd.open_workbook(xls_file)
    sheet = book.sheet_by_index(0)
    line_id = str(uuid.uuid4())
    towers, towers_id_name_mapping = extract_tower(sheet, line_id)
    strains = extract_strain(sheet, line_id, towers_id_name_mapping)
    segs, seg_mapping = extract_segment(sheet, line_id, towers_id_name_mapping)
    #cps = extract_crosspoint(sheet, line_id, towers_id_name_mapping, seg_mapping)
            
    
    print(strains)
    print(len(strains))
    print(segs)
    print(len(segs))
    #print(len(towers_id_name_mapping.keys()))




    
if __name__ == "__main__":
    parse_tower_xls_file(u'永发II回线', XLS_FILE)
    
    