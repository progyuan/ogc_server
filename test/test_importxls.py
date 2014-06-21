# -*- coding: utf-8 -*-
import os, sys
import json
import xlrd
import uuid

XLS_FILE = ur'F:\work\csharp\kmgdnew10.2-2014-1-17\交流220kV永发II回线杆塔明细表.xls'

def get_full_path(fname):
    for root, dirs, files  in os.walk(XSD_ROOT, topdown=False):
        for name in files:
            bname = name[:name.index('.')]
            if bname == fname:
                p = os.path.join(root, name)
                return p
    return None
    



    
if __name__ == "__main__":
    import_tower_xls_file(u'永发II回线', '13', u'架空线', XLS_FILE)
    
    