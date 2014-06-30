# -*- coding: utf-8 -*-
import os
import sys
import subprocess


GDALLOCATIONINFO_PATH = ur'E:\Python27\Lib\site-packages\osgeo\gdallocationinfo.exe'
DEM_PATH = ur'H:\gis\YN_DEM.tif'

def extract_alt(lng, lat):
    out = subprocess.check_output([GDALLOCATIONINFO_PATH, '-wgs84', "%s" % DEM_PATH, "%f" % lng, "%f" % lat])
    t = 'Value:'
    if t in out:
        idx = out.index(t) + len(t)
        print(out[idx:])
    else:
        print('out of range')
        

if __name__=="__main__":
    extract_alt(103.036471, 25.599314)
    extract_alt(-102.803284, 26.555857)

