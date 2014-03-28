# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import shutil

COLLADA2GLTF = ur'F:\work\cpp\glTF\converter\COLLADA2GLTF\vcbuild\bin\Release\collada2gltf.exe'
#COLLADA2GLTF = ur'F:\work\cpp\glTF\converter\COLLADA2GLTF\vcbuild\bin\Debug\collada2gltf.exe'
DAEDIR = ur'F:\work\kmdae0.5'
DESTDIR = ur'F:\work\python\ogc_server\static\gltf'
def collada2gltf(input_path):
    os.chdir(DAEDIR)
    exefile = os.path.basename(COLLADA2GLTF)
    exepath = os.path.join(DAEDIR, exefile)
    if not os.path.exists(exepath):
        shutil.copy(COLLADA2GLTF, DAEDIR)
    srcfile = os.path.basename(input_path)
    out = subprocess.check_output([exefile, '-f', "%s" % srcfile])
    print(out)
    


if __name__=="__main__":
    for i in os.listdir(DAEDIR):
        p = os.path.join(DAEDIR, i)
        if os.path.isfile(p) and p[-4:] == '.dae':
            collada2gltf(p)
    for i in os.listdir(DAEDIR):
        p = os.path.join(DAEDIR, i)
        if os.path.isfile(p) and (p[-5:] == '.json' or p[-5:] == '.glsl' or p[-4:] == '.bin'):
            shutil.move(p, DESTDIR)
    #collada2gltf(ur'H:\kmmodel_dae\BJ1_25_0.dae')

