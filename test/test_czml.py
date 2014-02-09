import os, sys
import json
import czml

CZML_PATH = r'../static/czml/simple.czml'


def load_czml(path):
    s = ''
    with open(path) as f:
        s = f.read()
    #obj = json.loads(s)
    czmlobj = czml.CZML()
    czmlobj.loads(s)
    for p in czmlobj.packets:
        print(p.data())
    
    
if __name__ == "__main__":
    load_czml(CZML_PATH)
    
    