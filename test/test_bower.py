# -*- coding: utf-8 -*-

import os, sys
from bowerlib import main

ROOT = ur'F:\work\js\editor.md'
ROOT = ur'F:\work\js\stackedit'


if __name__ == '__main__':
    os.chdir(ROOT)
    sys.argv = ['bower', 'install', 'editor.md']
    main.main()
    