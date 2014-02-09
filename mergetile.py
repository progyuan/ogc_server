# -*- coding: utf-8 -*-

import os
import sys
import traceback
import time
from multiprocessing import Process, Pipe
from PIL import Image

TILES_ROOT = r'.GMapCatcher/sat_tiles/-2/402'
TILES_ROOT = r'.GMapCatcher/sat_tiles/5/3'
TILES_ROOT = r'.GMapCatcher/sat_tiles/4/6'
OUTPUT_ROOT = r'.GMapCatcher/output'
TILE_WIDTH = 256
TILE_HEIGHT = 256

def merge_column(directory, pipe):
    #print(os.path.abspath(directory))
    files = os.listdir(directory)
    #print(files)
    w, h = TILE_WIDTH, len(files)*TILE_HEIGHT
    result = Image.new("RGBA", (w, h))
    try:
        for i in files:
            f = Image.open(os.path.join(directory,i))
            result.paste(f, (0, files.index(i)*TILE_HEIGHT))
        return result, h
    except:
        print(traceback.format_exc())
        if pipe:
            pipe.send('error: %s in %s' % (sys.exc_info()[1], directory) )
        return None,None
        
def save_columns(dirlist, pipe):
    if not os.path.exists(OUTPUT_ROOT):
        os.mkdir(OUTPUT_ROOT)
    for i in dirlist:
        p = os.path.join(TILES_ROOT,'%d/219' % i)
        p = os.path.join(TILES_ROOT,'%d/1' % i)
        p = os.path.join(TILES_ROOT,'%d/3' % i)
        col, h = merge_column(p, pipe)
        if col:
            p = os.path.join(OUTPUT_ROOT, 'col_%d.png' % i)
            p = os.path.abspath(p)
            col.save(p)
            if pipe:
                pipe.send('OK_%d_%d' % (i, h))
    
        
def merge_row(directory, procnum=10):
    dirs = os.listdir(directory)
    dirs = [int(i) for i in dirs]
    dirs.sort()
    #print(dirs)
    dirs_complete = dirs[:]
    tasks = []
    i = 0
    every = len(dirs)/(procnum-1)
    while not (i+1)*every>len(dirs):
        tasks.append(dirs[i*every:(i+1)*every])
        i += 1
    tasks.append(dirs[i*every:])
    #print(tasks)
    #print(len(tasks))
    procs, local_pipes =[],  []
    for task in tasks:
        local_pipe, remote_pipe = Pipe()
        proc = Process(target=save_columns, args=(task,  remote_pipe))
        procs.append(proc)
        local_pipes.append(local_pipe)
        proc.start()
        print('process [%d] started' % tasks.index(task))
    running = True
    height = 0
    while running:
        for pipe in local_pipes:
            if pipe.poll():
                req = pipe.recv()
                if req[:3]=='OK_':
                    l = req.split('_')
                    idx = int(l[1])
                    height = int(l[2])
                    dirs_complete.remove(idx)
                    print('column %d complete' % idx)
                    if len(dirs_complete)==0:
                        running = False
                else:
                    print(req)
                    print('process terminating...')
                    proc = procs[local_pipes.index(pipe)]
                    if proc.is_alive():
                        proc.terminate()
    if len(dirs_complete)==0:
        print('start merge row...')
        if height>0:
            print('height=%d' % height)
            save(height, 'N25E103_google_4_sat.png')
    else:
        print('error')
    
                    
        
def save(height, name):
    cols = os.listdir(OUTPUT_ROOT)
    l = []
    for i in cols:
        if not 'col_' in i:
            l.append(i)
    for i in l:
        cols.remove(i)
    
    cols = [int(i.replace('col_','').replace('.png','')) for i in cols]
    cols.sort()
    w, h = height, height
    try:
        result = Image.new("RGBA", (w, h))
        for i in cols:
            p = 'col_%d.png' % i
            f = Image.open(os.path.join(OUTPUT_ROOT, p))
            result.paste(f, (cols.index(i)*TILE_WIDTH, 0))
            print('column %d OK' % cols.index(i))
        
        p = os.path.join(OUTPUT_ROOT, name)
        p = os.path.abspath(p)
        result.save(p)
    except:
        print(traceback.format_exc())
    
        
    


if __name__ == "__main__":
    #p = os.path.join(TILES_ROOT,'3/219')
    #col = merge_column(p)
    #col.save(os.path.join(p, 'col3.png'))
    try:
        merge_row(TILES_ROOT, 4)
        #save(37376, 'aaa.png')
    except:
        print(traceback.format_exc())
    
