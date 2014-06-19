# -*- coding: utf-8 -*-
import os, sys
import json
from generateDS import xsd2py

XSD_ROOT = ur'D:\xsd'
#XML_ROOT = ur'../static/cim'
XML_ROOT = os.path.abspath(ur'.')
XSD_FILES = ['InfAssets', 'Core', 'Domain',  'Wires']
XSD_FILES = [ 'Meas']
#F:\work\python\ogc_server -o "F:/work/python/ogc_server/InfAssets.py" "D:/xsd/IEC61968/InfIEC61968/InfAssets.xsd"   

def get_full_path(fname):
    for root, dirs, files  in os.walk(XSD_ROOT, topdown=False):
        for name in files:
            bname = name[:name.index('.')]
            if bname == fname:
                p = os.path.join(root, name)
                return p
    return None
    
    
if __name__ == "__main__":
    for i in XSD_FILES:
        xsd = get_full_path(i)
        print(xsd)
        py = os.path.join(XML_ROOT, i + '.py')
        xsd2py(xsd, py)
        from InfAssets import WindingInsulation 
        #wi = WindingInsulation(insulationPFStatus=1, insulationResistance=1, leakageReactance=1, status=1, ToWinding=1, FromWinding=1)
        #with open('aaa.xml', 'w') as f:
            #wi.export(f, 0)
    
    