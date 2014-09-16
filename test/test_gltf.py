# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import shutil

COLLADA2GLTF = ur'F:\work\cpp\glTF\converter\COLLADA2GLTF\vcbuild\bin\Release\collada2gltf.exe'
#COLLADA2GLTF = ur'collada2gltf.exe'

DAEDIR = ur'F:\work\kmdae0.5'
DESTDIR = ur'F:\work\python\ogc_server\static\gltf'

DAEDIR = ur'F:\work\ztdae0.5'
DESTDIR = ur'F:\work\python\ogc_server\static\gltf1\zt'

DAEDIR = ur'F:\work\ztdae0.5'
DESTDIR = ur'F:\work\python\ogc_server\static\gltf\zt'


def collada2gltf(input_path=None):
    os.chdir(DAEDIR)
    #exefile = os.path.basename(COLLADA2GLTF)
    #exepath = os.path.join(DAEDIR, exefile)
    #if not os.path.exists(exepath):
        #shutil.copy(COLLADA2GLTF, DAEDIR)
    if input_path:
        srcfile = os.path.basename(input_path)
        out = subprocess.check_output([COLLADA2GLTF, '-f', "%s" % srcfile])
        print(out)
    else:
        out = subprocess.check_output([COLLADA2GLTF, ])
    
    #if input_file_name and len(input_file_name)>0:
        #srcfile = os.path.join(DAEDIR, input_file_name)
        #dstfile = os.path.join(DESTDIR, input_file_name.replace('.dae', '.gltf'))
        ##out = subprocess.check_output([COLLADA2GLTF, '-c','Open3DGC', '-m','binary', '-f', "%s" % srcfile, '-o', "%s" % dstfile])
        ##out = subprocess.check_output([COLLADA2GLTF, '-c','Open3DGC', '-m','ascii', '-f', "%s" % srcfile, '-o', "%s" % dstfile])
        ##out = subprocess.check_output([COLLADA2GLTF, '-c','Open3DGC',  '-f', "%s" % srcfile, '-o', "%s" % dstfile])
        #out = subprocess.check_output([COLLADA2GLTF, '-s',  '-f', "%s" % srcfile, '-o', "%s" % dstfile])
    #else:
        #out = subprocess.check_output([COLLADA2GLTF, ])
    #print(out)
    
def convert():
    for i in os.listdir(DAEDIR):
        p = os.path.join(DAEDIR, i)
        if os.path.isfile(p) and p[-4:] == '.dae':
            collada2gltf(p)
def movefiles():
    for i in os.listdir(DAEDIR):
        p = os.path.join(DAEDIR, i)
        if os.path.isfile(p) and (p[-5:] == '.gltf' or p[-5:] == '.json' or p[-5:] == '.glsl' or p[-4:] == '.bin'):
            p1 = os.path.join(DESTDIR, i)
            if not os.path.exists(p1):
                print('moving %s to %s...' % (p, DESTDIR))
                shutil.move(p, DESTDIR)

if __name__=="__main__":
    ##if os.path.exists(DESTDIR):
        ##shutil.rmtree(DESTDIR)
    if not os.path.exists(DESTDIR):
        os.mkdir(DESTDIR)
    convert()
    movefiles()
    #collada2gltf('GDSSFL241_39_0.dae')
    #collada2gltf()
