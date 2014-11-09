# -*- coding: utf-8 -*-

import os,sys


ROOT = ur'F:\work\python\ogc_server\static\gltf'

def change_color(path):
    l = []
    with open(path) as f:
        l = f.readlines()
    if len(l)>0:
        for i in l:
            #if 'vec4 color = vec4(0., 0., 0., 0.);' in i:
                #l[l.index(i)] = i.replace('vec4 color = vec4(0., 0., 0., 0.);', 'vec4 color = vec4(1., 1., 1., 1.);')
            if 'vec4 color = vec4(0.5, 0.5, 0.5, 1.);' in i:
                l[l.index(i)] = i.replace('vec4 color = vec4(0.5, 0.5, 0.5, 1.);', 'vec4 color = vec4(0.9, 0.9, 0.9, 1.);')
            if 'vec4 diffuse = vec4(0., 0., 0., 1.);' in i:
                l[l.index(i)] = i.replace('vec4 diffuse = vec4(0., 0., 0., 1.);', 'vec4 diffuse = vec4(1., 1., 1., 1.);')
    ll = []
    for i in l:
        if len(i.strip())>0:
            ll.append(i)
    s = ''.join(ll)    
    with open(path, 'w') as f:
        f.write(s)

def test():
    for i in os.listdir(ROOT):
        if i[-7:] == 'FS.glsl':
            p = os.path.join(ROOT, i)
            change_color(p)
            
        
if __name__=="__main__":
    test()
    
    
    