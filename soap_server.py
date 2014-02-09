# -*- coding: utf-8 -*-
import os, sys
import json
import datetime
from gevent import pywsgi
import gevent
from pysimplesoap.server import SoapDispatcher, WSGISOAPHandler
import exceptions
import time
import socket
import urllib, urllib2, urlparse
from socket import error
import errno
import cgi
import configobj
from lxml import etree



ENCODING = 'utf-8'

CONFIGFILE = 'ogc-config.ini'
gConfig = configobj.ConfigObj(CONFIGFILE, encoding='UTF8')


def webservice_login(username, password):
    return 'OK'


#in0（开始时间）、in1（结束时间）参数以字符串方式传递(例如：”20070808200800”, “20070808200810”)
#时间要精确到秒 YYYYMMddHHmmss
def webservice_GetFlashofDate(in0, in1):
    #1、这段时间有数据
     #<?xml version="1.0" encoding="UTF-8"?>
    
    #<Flashs>
    #<Flash>
    #<Time>2007-01-01 16:00:06</Time>
    #<Lat>26.860467</Lat>
    #<Long>119.207484</Long>
    #<Current>-11.8</Current>
    #<Mult>1</Mult>
    #<Tdf>3</Tdf>
    #</Flash>
    #</Flashs>
    
    #2、这段时间无数据
    #<?xml version="1.0" encoding="UTF-8"?>
    #<Flashs>
    #</Flashs>    
    root = etree.Element("Flashs")#, xmlns=gConfig['webservice']['namespace'], version="1.0.0")
    for i in range(500):
        Flash = etree.SubElement(root, "Flash")
        Time = etree.SubElement(Flash, "Time").text = time.strftime('%Y-%m-%d %H:%M:%S')
        Lat = etree.SubElement(Flash, "Lat").text = '26.860467'
        Long = etree.SubElement(Flash, "Long").text = '119.207484'
        Current = etree.SubElement(Flash, "Current").text = '-11.8'
        Mult = etree.SubElement(Flash, "Mult").text = '1'
        Tdf = etree.SubElement(Flash, "Tdf").text = '3'
    
    ret = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding=ENCODING)
    #time.sleep(4)
    return ret



#in0-startTime、in1-endTime、in2-经度(西) in3-经度(东)  in4-纬度(北) in5- 纬度(南)。
def webservice_GetFlashofEnvelope(in0, in1, in2, in3, in4, in5):
    root = etree.Element("Flashs")
    for i in range(500):
        Flash = etree.SubElement(root, "Flash")
        Time = etree.SubElement(Flash, "Time").text = time.strftime('%Y-%m-%d %H:%M:%S')
        Lat = etree.SubElement(Flash, "Lat").text = '26.860467'
        Long = etree.SubElement(Flash, "Long").text = '119.207484'
        Current = etree.SubElement(Flash, "Current").text = '-11.8'
        Mult = etree.SubElement(Flash, "Mult").text = '1'
        Tdf = etree.SubElement(Flash, "Tdf").text = '3'
    
    ret = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding=ENCODING)
    return ret
    

def get_wsapplication():
    dispatcher = SoapDispatcher(
        'thunder_counter_dispatcher',
        location = str(gConfig['webservice']['location']),
        action = str(gConfig['webservice']['action']),
        namespace = str(gConfig['webservice']['namespace']), 
        prefix = str(gConfig['webservice']['prefix']),
        trace = True,
        ns = True)
    dispatcher.register_function('login', 
                                 webservice_login,
                                 returns={'Result': str}, 
                                 args={'username': str, 'password': str})    
    dispatcher.register_function('GetFlashofDate', 
                                 webservice_GetFlashofDate,
                                 returns={'Result': str}, 
                                 args={'in0': str, 'in1': str})    
    dispatcher.register_function('GetFlashofEnvelope', 
                                 webservice_GetFlashofEnvelope,
                                 returns={'Result': str}, 
                                 args={'in0': str, 'in1': str, 'in2': str,'in3': str, 'in4': str, 'in5': str})    
    wsapplication = WSGISOAPHandler(dispatcher)
    return wsapplication

if __name__=="__main__":
    if gConfig['webservice']['enable']  in [u'true', u'TRUE']:
        h, p = gConfig['webservice']['host'], int(gConfig['webservice']['port'])
        print('listening webservice at http://%s:%d/webservice' % (h, p))
        server = pywsgi.WSGIServer((h, p), get_wsapplication())
        server.start()
        server.serve_forever()
