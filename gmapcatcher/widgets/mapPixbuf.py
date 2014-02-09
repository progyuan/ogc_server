# -*- coding: utf-8 -*-
## @package gmapcatcher.widgets.mapPixbuf
# Get the Pixbuf from image files.

#import gtk
from gmapcatcher.mapConst import *
from os.path import join, dirname, abspath, exists, isfile
from PIL import Image


## Absolute Path to the images directory
if 'library.zip' in __file__:
    _prefix = abspath(join(dirname(__file__), "../../../images"))
    _prefix = abspath( "static/img")
else:
    _prefix = abspath(join(dirname(__file__), "../../images"))

if not isfile(join(_prefix, 'missing.png')):
    _prefix = '/usr/share/pixmaps/gmapcatcher'


def ico():
    pix_ico = False
    try:
        pix_ico = image_data_fs(join(_prefix, 'map.png'))
    except Exception:
        pix_ico = False
    return pix_ico


## Get the Pixbuf from missing.png
def missing():
    pix_missing = False
    try:
        pix_missing = image_data_fs(join(_prefix, 'missing.png'))
    except Exception:
        pix_missing = image_data_direct("missing")
    return pix_missing


## Get the Pixbuf of a Cross
def cross():
    return image_data_direct("cross")


def downloading():
    pix_dl = False
    try:
        pix_dl = image_data_fs(join(_prefix, 'downloading.png'))
    except Exception:
        pix_dl = image_data_direct("downloading")
    return pix_dl


## Get the Pixbuf from the given image.
# This is used in myToolTip
def getImage(filename, intWidth=56, intHeight=56):
    pix_buf = False
    try:
        if not exists(filename):
            filename = join(_prefix, filename)
        #pix_buf = gtk.gdk.pixbuf_new_from_file_at_size(
                #filename, intWidth, intHeight)
        pix_buf = image_data_fs( filename, intWidth, intHeight)
    except Exception:
        #wCo = int(intWidth / 3)
        #wMe = intWidth - 2 * wCo
        #hCo = int(intHeight / 3)
        #hMe = intHeight - 2 * wCo
        #pix_buf = gtk.gdk.pixbuf_new_from_data(
                #('\255\0\0\127' * wCo + '\0\0\255\127' *
                #wMe + '\255\0\0\127' * wCo) * hCo +
                #('\0\0\255\127' * intWidth) * hMe +
                #('\255\0\0\127' * wCo + '\0\0\255\127' *
                #wMe + '\255\0\0\127' * wCo) * hCo,
                #gtk.gdk.COLORSPACE_RGB, True, 8, intWidth, intHeight,
                #intHeight * 4)
        pix_buf = image_data_fs(join(_prefix, 'missing.png'), intWidth, intHeight)
    return pix_buf


def image_data_fs(filename, w=256, h=256):
    #return gtk.gdk.pixbuf_new_from_file(filename)
    im = Image.new("RGB", (256, 256))
    return Image.open(filename)


def image_data_direct(name):
    if name == "missing":
        #return gtk.gdk.pixbuf_new_from_data(
                #('\0\0\0' + '\255\255\255' * 3) * (TILES_WIDTH / 4) +
                #(('\0\0\0' + '\255\255\255' * (TILES_WIDTH - 1)) +
                #('\255\255\255' * 3 * TILES_WIDTH)) * (TILES_HEIGHT / 4),
                #gtk.gdk.COLORSPACE_RGB, False, 8,
                #TILES_WIDTH, TILES_HEIGHT, TILES_HEIGHT * 3)
        
        return image_data_fs(join(_prefix, 'missing.png'))
        
    elif name == "cross":
        #return gtk.gdk.pixbuf_new_from_data(
                #('\0\0\0\0' * 5 + '\0\0\255\350' * 2 + '\0\0\0\0' * 5)
                #* 5 + ('\0\0\255\350' * 12) * 2 +
                #('\0\0\0\0' * 5 + '\0\0\255\350' * 2 + '\0\0\0\0' * 5)
                #* 5,
                #gtk.gdk.COLORSPACE_RGB, True, 8, 12, 12, 12 * 4)
        return image_data_fs(join(_prefix, 'marker_gps.png'))
    elif name == "downloading":
        #return gtk.gdk.pixbuf_new_from_data(
                #'\0\255\0\127' * 150 * 38,
                #gtk.gdk.COLORSPACE_RGB, True, 8, 150, 38, 150 * 4)
        return image_data_fs(join(_prefix, 'downloading.png'))
    else:
        raise Exception('image type not recognized')
