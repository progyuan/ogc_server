# -*- coding: utf-8 -*-

import os, sys
import codecs
import json
from pydash import py_ as _

STATICRESOURCE_DIR = ur'F:\work\html\webgis'

def test():
    standard_template = []
    with codecs.open(os.path.join(STATICRESOURCE_DIR, 'standard_template2009.json'), 'r', 'utf-8-sig') as f:
        standard_template = json.loads(f.read())
    a = _.result(_.find(_.result(_.find(standard_template, {'unit':'unit_1'}), 'children'),{'a':'aaa'}), 'bbb')
    print (a)

if __name__ == '__main__':
    test()
    