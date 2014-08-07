# -*- coding: utf-8 -*-
import os, sys, json
import db_util


TILESDIR = ur'I:\tilesCache\terrain_tiles'

DATAFILEPATH = ur'I:\tilesCache\terrain_tiles.json'
DATAFILEPATH = ur'I:\tilesCache\terrain_tiles.json'

def get_files():
    l = []
    for root, dirs, files  in os.walk(TILESDIR, topdown=False):
        for name in files:
            if name[-8:] == '.terrain':
                p = os.path.join(root, name)
                filename = p.replace(TILESDIR + '\\', '').replace('\\', '/')
                o = {'filename':filename, 'path':p}
                #print(o)
                l.append(o)
    return l
    

if __name__ == "__main__":
    l = get_files()
    for i in l:
        filename = i.filename
        p = i.path
        mimetype = 'application/octet-stream'
        db_util.gridfs_tile_find('terrain', 'quantized_mesh', p, mimetype, i.read())
            
    #print(len(l))
    #with open(DATAFILEPATH, 'w') as f:
        #f.write(json.dumps(l))
    


