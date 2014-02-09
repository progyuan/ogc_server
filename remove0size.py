# -*- coding: utf-8 -*-
import os, sys

IMAGE_ROOT = r'tilesCache/sat_tiles'

def remove(isremove=False):
    ret = 0
    for root, dirs, files in os.walk(IMAGE_ROOT):
        for f in files:
            p = os.path.join(root, f)
            if os.path.getsize(p)==0:
                print(p)
                if isremove:
                    os.remove(p)
                ret += 1
    return ret
        

if __name__=="__main__":
    print(remove())
    
    