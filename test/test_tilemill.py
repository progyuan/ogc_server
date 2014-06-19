# -*- coding: utf-8 -*-
import os
import sys
import json
import shutil
import subprocess


NODEROOT = r'E:\Program Files (x86)\TileMill-v0.10.1\tilemill'
NODEEXE = os.path.join(NODEROOT, 'node.exe')
INDEXJS = os.path.join(NODEROOT, 'index.js')
INDEXJS = './index.js'
PROJECTROOT = r'I:\MapBox\project'
EXPORTROOT = r'I:\MapBox\export'
TIFFROOT = r'I:\geotiff'


def get_tiles_obj(area):
    ret = {}
    with open(os.path.abspath('static/json/yn_tiles_index_%s.json' % area )) as f:
        ret = json.loads(f.read())
    return ret

def move_files():
    lsrc = []
    for root, dirs, files  in os.walk(TIFFROOT, topdown=False):
        for name in files:
            if name[-4:]== '.tif':
                p = os.path.join(root, name)
                lsrc.append(p)
    for i in lsrc:
        shutil.move(i, TIFFROOT)
    
def build_project(project_id, tiles_dict={}, min_zoom=9, max_zoom=17):
    print('Generating project[%s]...' % project_id)
    projectdir  = os.path.join(PROJECTROOT, project_id)
    
    if os.path.exists(projectdir):
        shutil.rmtree(projectdir, ignore_errors=True)
    if not os.path.exists(projectdir):
        os.mkdir(projectdir)
    currdir = os.path.dirname(__file__)
    templatename = os.path.abspath(os.path.join(currdir, 'data/project_template.mml'))
    templatestyle = os.path.abspath(os.path.join(currdir, 'data/style_template.mss'))
    projectfilename = 'project.mml'
    projectstyle = 'style.mss'
    obj = None
    style_template = ''
    with open(templatestyle) as f:
        style_template = f.read()
    with open(os.path.join(projectdir, projectstyle), 'w') as f:
        style_template = style_template.replace('@', project_id)
        f.write(style_template)
    if tiles_dict.has_key(project_id):
        with open(templatename) as f:
            obj = json.loads(f.read())
        if obj:
            bounds = obj['bounds'] = [tiles_dict[project_id]['ld'][0], tiles_dict[project_id]['ld'][1], tiles_dict[project_id]['ru'][0], tiles_dict[project_id]['ru'][1] ]
            obj['center'] = [(bounds[0]+bounds[2])/2.0, (bounds[1]+bounds[3])/2.0,  11]
            obj['minzoom'] = min_zoom
            obj['maxzoom'] = max_zoom
            obj['Layer'][0]['extent'] = bounds
            obj['Layer'][0]['id'] = project_id
            obj['Layer'][0]['Datasource']['file'] = os.path.join(TIFFROOT, 'offset_%s_WGS84.tif' % project_id)
            obj['Layer'][0]['name'] = project_id
            obj['name'] = project_id
            obj['description'] = project_id
    
            with open(os.path.join(projectdir, projectfilename), 'w') as f:
                f.write(json.dumps(obj, indent=4))
    
def build_projects(min_zoom=9, max_zoom=17):
    tiles_dict = get_tiles_obj('zt')
    idx = 0
    for key in tiles_dict.keys():
        if idx<3:
            build_project(key, tiles_dict, min_zoom, max_zoom)
            p = os.path.join(EXPORTROOT, '%s.mbtiles' % key)
            #cmd = ['"%s"' % NODEEXE, '"%s"' % INDEXJS, 'export', key, '"%s"' % p, '--minzoom=%d' % min_zoom, '--maxzoom=%d' % max_zoom]
            #cmd = '"%s" "%s" export "%s" "%s" --minzoom=%d --maxzoom=%d'  % (NODEEXE, INDEXJS, os.path.join(PROJECTROOT,key), p, min_zoom, max_zoom)
            cmd = '"%s" "%s" export "./%s" "tile%s.mbtiles" --minzoom=%d --maxzoom=%d'  % (NODEEXE, INDEXJS, key, key, min_zoom, max_zoom)
            os.chdir(NODEROOT)
            print(cmd)
            print(subprocess.check_output(cmd))
            idx += 1
if __name__=="__main__":
    #os.chdir(NODEROOT)
    #cmd = [NODEEXE, INDEXJS, 'export', '--help']
    #print(subprocess.check_output(cmd))
    #mb = landez.MBTilesBuilder(filepath=u"J:\mbtiles\aaa.mbtiles")
    #move_files()
    build_projects()
    
    
    