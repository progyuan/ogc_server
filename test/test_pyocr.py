# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from PIL import Image
import sys

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'tesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'

IMGPATH = u'D:\\2014项目\\Untitled.png'

#if __name__=="__main__":
txt = tool.image_to_string(Image.open(IMGPATH),
                           lang=lang,
                           builder=pyocr.builders.TextBuilder())
print(unicode(txt))
#word_boxes = tool.image_to_string(Image.open(IMGPATH),
                                  #lang=lang,
                                  #builder=pyocr.builders.WordBoxBuilder())
#print(word_boxes)

#line_and_word_boxes = tool.image_to_string(
        #Image.open(IMGPATH), lang=lang,
        #builder=pyocr.builders.LineBoxBuilder())

#print(line_and_word_boxes)

