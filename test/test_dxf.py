# -*- coding: utf-8 -*-
import os
import sys
import json
import shutil
import dxfgrabber


def export_zt():
    p = ur'H:\work\云南接图表.dxf'
    p1 = ur'H:\work\yn_tiles_index.json'
    p2 = ur'H:\work\yn_tiles_index_zt.json'
    
    dxf = dxfgrabber.readfile(p)
    print("DXF version: {%s}" % str(dxf.dxfversion))
    cnt = 0
    l = []
    #d = {}
    coordlist = {}
    for entity in dxf.entities:
        if entity.layer=='0':
            cnt += 1
            d = {}
            if hasattr(entity, 'points'):
                #print('len(entity.points)=%d' %  len(entity.points))
                if len(entity.points) == 4:
                    coordlist['ld'] = entity.points[0]
                    coordlist['rd'] = entity.points[1]
                    coordlist['ru'] = entity.points[2]
                    coordlist['lu'] = entity.points[3]
            if hasattr(entity, 'text'):
                if len(coordlist.keys())>0:
                    d[entity.text] = coordlist
            if len(d.keys())>0:
                l.append(d)
                coordlist = {}
                
                
    with open(p1, 'w') as f:
        f.write(json.dumps(l))
    d = {}
    for i in l:
        key = i.keys()[0]
        keyintrow = int(key[0:3])
        keyintcol = int(key[3:])
        if keyintrow <= 34 and keyintrow + keyintcol >= 62:
            d[key] = i[key]
    with open(p2, 'w') as f:
        f.write(json.dumps(d))
    print(len(d.keys()))
    #for k in d.keys():
        #print(k)
        
    
def copy_files():
    root = ur'J:\云南dat任务文件'
    root1 = ur'J:\云南dat任务文件\zt'
    p2 = ur'static/json/yn_tiles_index_zt.json'
    p2 = os.path.abspath(p2)
    obj = None
    with open(p2) as f:
        obj = json.loads(f.read())
    if not os.path.exists(root1):
        os.mkdir(root1)
    if obj:
        cnt = 0
        for key in obj.keys():
            psrc = os.path.join(root, key + '.dat')
            pdst = os.path.join(root1, key + '.dat')
            shutil.copy2(psrc, root1)
            psrc = os.path.join(root, key + '.idx')
            pdst = os.path.join(root1, key + '.idx')
            shutil.copy2(psrc, root1)
            cnt += 1
        print('copied %d' % cnt)
            
    
if __name__=="__main__":
    copy_files()
    
    
    
    
    
    
    