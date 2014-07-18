# -*- coding: utf-8 -*-

import codecs
import os, sys
import random
import json
import math
import decimal
import datetime
import threading
from gevent import pywsgi
import gevent
import gevent.fileobject
import geventwebsocket
from geventwebsocket.handler import WebSocketHandler
from pysimplesoap.server import SoapDispatcher, WSGISOAPHandler
from pysimplesoap.client import SoapClient, SoapFault
import exceptions
import time
import base64
#import numpy as np
import socket
import urllib, urllib2, urlparse
from socket import error
import errno
import subprocess
from multiprocessing import Process, Queue, current_process, freeze_support
import shutil
import re
#from PIL import Image
import StringIO
import cgi, multipart
import configobj
#from gmapcatcher import mapUtils
from lxml import etree
import czml
#from wfs_server import WFSServer
#import gmapcatcher.mapUtils as mapUtils
#import gmapcatcher.mapConf as mapConf
#import gmapcatcher.mapConst as mapConst
#from gmapcatcher.mapServices import MapServ
#from gmapcatcher.mapDownloader import MapDownloader, MapDownloaderGevent, MapDownloaderSocks5

import pypyodbc
import uuid
import db_util
from module_locator import module_path, dec, dec1, enc, enc1
from geventhttpclient import HTTPClient, URL





ENCODING = None
ENCODING1 = None
STATICRESOURCE_DIR = None
CONFIGFILE = None

    

STATICRESOURCE_CSS_DIR = None
STATICRESOURCE_JS_DIR = None
STATICRESOURCE_IMG_DIR = None
UPLOAD_PHOTOS_DIR = None
UPLOAD_VOICE_DIR = None

gConfig = None
gStaticCache = {}
gTileCache = {}

#deprecated
gSatTileCache = {}
gMapTileCache = {}
gTerrainCache = {}

gGreenlets = {}
gClusterProcess = {}

#gMapDownloader = None
#gCtxMap = None

_SPECIAL = re.escape('()<>@,;:\\"/[]?={} \t')
_RE_SPECIAL = re.compile('[%s]' % _SPECIAL)
_QSTR = '"(?:\\\\.|[^"])*"' # Quoted string
_VALUE = '(?:[^%s]+|%s)' % (_SPECIAL, _QSTR) # Save or quoted string
_OPTION = '(?:;|^)\s*([^%s]+)\s*=\s*(%s)' % (_SPECIAL, _VALUE)
_RE_OPTION = re.compile(_OPTION) # key=value part of an Content-Type like header


def init_global():
    global ENCODING, ENCODING1, STATICRESOURCE_DIR, CONFIGFILE, STATICRESOURCE_CSS_DIR, STATICRESOURCE_JS_DIR, STATICRESOURCE_IMG_DIR, UPLOAD_PHOTOS_DIR, UPLOAD_VOICE_DIR
    global gConfig, gStaticCache, gGreenlets, gClusterProcess
    ENCODING = 'utf-8'
    ENCODING1 = 'gb18030'
    
    STATICRESOURCE_DIR = os.path.join(module_path(), 'static')
    
    CONFIGFILE = os.path.join(module_path(), 'ogc-config.ini')
    gConfig = configobj.ConfigObj(CONFIGFILE, encoding='UTF8')
    if gConfig['web'].has_key('webroot') and len(gConfig['web']['webroot'])>0:
        if os.path.exists(gConfig['web']['webroot']):
            STATICRESOURCE_DIR = gConfig['web']['webroot']
        
    
    STATICRESOURCE_CSS_DIR = os.path.join(STATICRESOURCE_DIR, 'css')
    STATICRESOURCE_JS_DIR = os.path.join(STATICRESOURCE_DIR, 'js')
    STATICRESOURCE_IMG_DIR = os.path.join(STATICRESOURCE_DIR, 'img')
    UPLOAD_PHOTOS_DIR = os.path.join(STATICRESOURCE_DIR,'photos', 'upload')
    UPLOAD_VOICE_DIR = os.path.join(STATICRESOURCE_DIR,'voice')
    
    
    #try:
        #gCtxMap = MapServ()
        #proxy, port = None, None
        #try:
            #proxy = str(gConfig['proxy']['host'])
            #port = int(gConfig['proxy']['port'])
            #if len(proxy)>0:
                #gMapDownloader = MapDownloaderSocks5(gCtxMap, proxy, port)
            #else:
                #gMapDownloader = MapDownloaderGevent(gCtxMap, None, None)
        #except:
            #gMapDownloader = MapDownloaderGevent(gCtxMap, None, None)
            
    #except:
        #print(sys.exc_info()[1])
        #pass
    


def handle_static(aUrl):
    global ENCODING, gConfig
    global STATICRESOURCE_DIR, STATICRESOURCE_JS_DIR, STATICRESOURCE_CSS_DIR, STATICRESOURCE_IMG_DIR, UPLOAD_VOICE_DIR
    statuscode, contenttype, body = '404 Not Found', 'text/plain;charset=' + ENCODING, '404 Not Found'
    surl = dec(aUrl)#.replace('//', '').replace('/', os.path.sep)
    if surl[0:2] == '//':
        surl = surl[2:]
    if surl[0] == '/':
        surl = surl[1:]
    p = os.path.join(STATICRESOURCE_DIR , surl)
    isBin = False
    ext = os.path.splitext(p)[1]
    if '.' in surl:
        ext = surl[surl.rindex('.'):]
    else:
        ext = os.path.splitext(p)[1]
    print('handle_static p=%s' % p)
    
    if len(ext)>0:
        if gConfig['mime_type'].has_key(ext):
            if 'image/' in gConfig['mime_type'][ext]:
                isBin = True
            contenttype = gConfig['mime_type'][ext]
            if ext == '.js':
                if not os.path.exists(p):
                    p = os.path.join(STATICRESOURCE_JS_DIR, aUrl[aUrl.rindex('/')+1:])
            elif ext == '.css':
                if not os.path.exists(p):
                    p = os.path.join(STATICRESOURCE_CSS_DIR, aUrl[aUrl.rindex('/')+1:])
            elif 'image/' in gConfig['mime_type'][ext]:
                if not os.path.exists(p):
                    p = os.path.abspath(os.path.join(STATICRESOURCE_IMG_DIR, aUrl[aUrl.rindex('/')+1:]))
            
            if not os.path.exists(p):
                p = os.path.join(STATICRESOURCE_DIR ,  aUrl)
                #p = os.path.abspath(p)
                p = dec(p)
            if os.path.exists(p):
                statuscode = '200 OK'
                mode = 'r'
                if isBin:
                    mode = 'rb'
                with open(p, mode) as f:
                    f1 = gevent.fileobject.FileObjectThread(f, mode)
                    body = f1.read()
            else:
                statuscode = '404 Not Found'
                body = '404 Not Found'
            
                
        else:
            contenttype = 'application/octet-stream'
            if os.path.exists(p):
                statuscode = '200 OK'
                with open(p, 'rb') as f:
                    f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                    body = f1.read()
            else:
                if ext == '.3gp':
                    id = surl[surl.rindex('/') + 1:]
                    id = id.replace('.3gp', '')
                    fn = get_voice_file_latest(id)
                    if fn:
                        with open(os.path.join(UPLOAD_VOICE_DIR, fn), 'rb') as f:
                            f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                            body = f1.read()
                            statuscode = '200 OK'
                        
                    
            
    else:
        contenttype = 'text/plain;charset=' + ENCODING
        statuscode = '500 Internal Server Error'
        body = '500 Internal Server Error'
        
    return statuscode, str(contenttype), body

def handle_wfs_GetCapabilities(params, Start_response):
    Start_response('200 OK', [('Content-Type', 'text/xml;charset=' + ENCODING)])
    s = create_wfs_GetCapabilities()
    return [s]

def handle_wfs_GetFeature(params, Start_response):
    Start_response('200 OK', [('Content-Type', 'text/xml;charset=' + ENCODING)])
    s = create_wfs_GetFeature()
    return [s]


def create_wfs_GetCapabilities():
    namespace = {'ows':"http://www.opengis.net/ows",
                 'ogc':"http://www.opengis.net/ogc",
                 'wfs':"http://www.opengis.net/wfs", 
                 'gml':"http://www.opengis.net/gml", 
                 'xlink':"http://www.w3.org/1999/xlink", 
                 'xsi':"http://www.w3.org/2001/XMLSchema-instance", 
                 'schemaLocation':"http://www.opengis.net/wfs/1.1.0/WFS.xsd",
                 'my':"http://localhost:88/my"
                 }
    wfs = '{%s}' % namespace['wfs']
    ogc = '{%s}' % namespace['ogc']
    ows = '{%s}' % namespace['ows']
    xlink = '{%s}' % namespace['xlink']
    root = etree.Element(wfs+"WFS_Capabilites", xmlns="http://www.opengis.net/wfs", nsmap=namespace, version="1.1.0", updateSequence="0")
    #ServiceIdentification
    ServiceIdentification = etree.SubElement(root, ows + "ServiceIdentification")
    Title = etree.SubElement(ServiceIdentification, ows + "Title").text = gConfig['wfs']['ServiceIdentification_Title']
    ServiceType = etree.SubElement(ServiceIdentification, ows + "ServiceType").text = 'WFS'
    ServiceTypeVersion = etree.SubElement(ServiceIdentification, ows + "ServiceTypeVersion").text = '1.1.0'
    
    #OperationsMetadata
    OperationsMetadata = etree.SubElement(root, ows + "OperationsMetadata")
    Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="GetCapabilities")
    DCP= etree.SubElement(Operation, ows + "DCP")
    HTTP= etree.SubElement(DCP, ows + "HTTP")
    href = xlink + 'href'
    Get= etree.SubElement(HTTP, ows + "Get", {href:gConfig['wfs']['url']})
    #Constraint= etree.SubElement(Get, ows + "Constraint", name="GetEncoding")
    #AllowedValues= etree.SubElement(Constraint, ows + "AllowedValues")
    #Value= etree.SubElement(AllowedValues, ows + "Value").text = 'KVP'
    
    #Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="GetTile")
    #DCP= etree.SubElement(Operation, ows + "DCP")
    #HTTP= etree.SubElement(DCP, ows + "HTTP")
    #Get= etree.SubElement(HTTP, ows + "Get", {href:gConfig['wmts']['url']})
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="AcceptVersions")
    Value = etree.SubElement(Parameter, ows + "Value").text = "1.1.0"
    Value = etree.SubElement(Parameter, ows + "Value").text = "1.0.0"
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="AcceptFormats")
    Value = etree.SubElement(Parameter, ows + "Value").text = "text/xml"
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="Sections")
    Value = etree.SubElement(Parameter, ows + "Value").text = "ServiceIdentification"
    Value = etree.SubElement(Parameter, ows + "Value").text = "OperationsMetadata"
    Value = etree.SubElement(Parameter, ows + "Value").text = "FeatureTypeList"
    Value = etree.SubElement(Parameter, ows + "Value").text = "ServesGMLObjectTypeList"
    Value = etree.SubElement(Parameter, ows + "Value").text = "SupportsGMLObjectTypeList"
    Value = etree.SubElement(Parameter, ows + "Value").text = "Filter_Capabilities"
    
    Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="DescribeFeatureType")
    DCP= etree.SubElement(Operation, ows + "DCP")
    HTTP= etree.SubElement(DCP, ows + "HTTP")
    Get= etree.SubElement(HTTP, ows + "Get", {href:gConfig['wfs']['url']})#+'/wfs.cgi?'})
    Post= etree.SubElement(HTTP, ows + "Post", {href:gConfig['wfs']['url']})#+'/wfs.cgi'})
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="outputFormat")
    Value = etree.SubElement(Parameter, ows + "Value").text = "text/xml; subtype=gml/3.1.1"
    
    Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="GetFeature")
    DCP= etree.SubElement(Operation, ows + "DCP")
    HTTP= etree.SubElement(DCP, ows + "HTTP")
    Get= etree.SubElement(HTTP, ows + "Get", {href:gConfig['wfs']['url']})#+'/wfs.cgi?'})
    Post= etree.SubElement(HTTP, ows + "Post", {href:gConfig['wfs']['url']})#+'/wfs.cgi'})
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="resultType")
    Value = etree.SubElement(Parameter, ows + "Value").text = "results"
    Value = etree.SubElement(Parameter, ows + "Value").text = "hits"
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="outputFormat")
    Value = etree.SubElement(Parameter, ows + "Value").text = "text/xml; subtype=gml/3.1.1"
    
    Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="GetFeatureWithLock")
    DCP= etree.SubElement(Operation, ows + "DCP")
    HTTP= etree.SubElement(DCP, ows + "HTTP")
    Post= etree.SubElement(HTTP, ows + "Post", {href:gConfig['wfs']['url']})
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="resultType")
    Value = etree.SubElement(Parameter, ows + "Value").text = "results"
    Value = etree.SubElement(Parameter, ows + "Value").text = "hits"
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="outputFormat")
    Value = etree.SubElement(Parameter, ows + "Value").text = "text/xml; subtype=gml/3.1.1"
    
    Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="GetGMLObject")
    DCP= etree.SubElement(Operation, ows + "DCP")
    HTTP= etree.SubElement(DCP, ows + "HTTP")
    Post= etree.SubElement(HTTP, ows + "Post", {href:gConfig['wfs']['url']})
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="outputFormat")
    Value = etree.SubElement(Parameter, ows + "Value").text = "text/xml; subtype=gml/3.1.1"
    Value = etree.SubElement(Parameter, ows + "Value").text = "text/xhtml"
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="LocalTraverseXLinkScope")
    Value = etree.SubElement(Parameter, ows + "Value").text = "0"
    Value = etree.SubElement(Parameter, ows + "Value").text = "*"
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="RemoteTraverseXLinkScope")
    Value = etree.SubElement(Parameter, ows + "Value").text = "0"
    Value = etree.SubElement(Parameter, ows + "Value").text = "*"
    
    Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="LockFeature")
    DCP= etree.SubElement(Operation, ows + "DCP")
    HTTP= etree.SubElement(DCP, ows + "HTTP")
    Post= etree.SubElement(HTTP, ows + "Post", {href:gConfig['wfs']['url']})
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="lockAction")
    Value = etree.SubElement(Parameter, ows + "Value").text = "ALL"
    Value = etree.SubElement(Parameter, ows + "Value").text = "SOME"
    
    Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="Transaction")
    DCP= etree.SubElement(Operation, ows + "DCP")
    HTTP= etree.SubElement(DCP, ows + "HTTP")
    Post= etree.SubElement(HTTP, ows + "Post", {href:gConfig['wfs']['url']})
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="inputFormat")
    Value = etree.SubElement(Parameter, ows + "Value").text = "text/xml; subtype=gml/3.1.1"
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="idgen")
    Value = etree.SubElement(Parameter, ows + "Value").text = "GenerateNew"
    Value = etree.SubElement(Parameter, ows + "Value").text = "UseExisting"
    Value = etree.SubElement(Parameter, ows + "Value").text = "ReplaceDuplicate"
    Parameter = etree.SubElement(Operation, ows + "Parameter", name="releaseAction")
    Value = etree.SubElement(Parameter, ows + "Value").text = "ALL"
    Value = etree.SubElement(Parameter, ows + "Value").text = "SOME"
    
    Parameter = etree.SubElement(OperationsMetadata, ows + "Parameter", name="srsName")
    Value = etree.SubElement(Parameter, ows + "Value").text = "EPSG:4326"
    Constraint = etree.SubElement(OperationsMetadata, ows + "Constraint", name="DefaultMaxFeatures")
    Value = etree.SubElement(Constraint, ows + "Value").text = "10000"
    Constraint = etree.SubElement(OperationsMetadata, ows + "Constraint", name="LocalTraverseXLinkScope")
    Value = etree.SubElement(Constraint, ows + "Value").text = "0"
    Value = etree.SubElement(Constraint, ows + "Value").text = "*"
    Constraint = etree.SubElement(OperationsMetadata, ows + "Constraint", name="RemoteTraverseXLinkScope")
    Value = etree.SubElement(Constraint, ows + "Value").text = "0"
    Value = etree.SubElement(Constraint, ows + "Value").text = "*"
    Constraint = etree.SubElement(OperationsMetadata, ows + "Constraint", name="DefaultLockExpiry")
    Value = etree.SubElement(Constraint, ows + "Value").text = "5"
    
    
    FeatureTypeList = etree.SubElement(root, wfs + "FeatureTypeList")
    FeatureType = etree.SubElement(FeatureTypeList, wfs + "FeatureType")
    Name = etree.SubElement(FeatureType, wfs + "Name").text = "PointType"
    Title = etree.SubElement(FeatureType, wfs + "Title").text = "Point Type"
    DefaultSRS = etree.SubElement(FeatureType, wfs + "DefaultSRS").text = "EPSG:4326"
    OutputFormats = etree.SubElement(FeatureType, wfs + "OutputFormats")
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xml; subtype=gml/3.1.1"
    WGS84BoundingBox = etree.SubElement(FeatureType, ows + "WGS84BoundingBox")
    LowerCorner = etree.SubElement(WGS84BoundingBox, ows + "LowerCorner").text = "-180 -90"
    UpperCorner = etree.SubElement(WGS84BoundingBox, ows + "UpperCorner").text = "180 90"
    
    ServesGMLObjectTypeList = etree.SubElement(root, wfs + "ServesGMLObjectTypeList")
    GMLObjectType = etree.SubElement(ServesGMLObjectTypeList, wfs + "GMLObjectType")
    Name = etree.SubElement(GMLObjectType, wfs + "Name").text = "PointType"
    Title = etree.SubElement(GMLObjectType, wfs + "Title").text = "Point Type"
    OutputFormats = etree.SubElement(GMLObjectType, wfs + "OutputFormats")
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xml; subtype=gml/3.1.1"
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xhmtl"
    
    SupportsGMLObjectTypeList = etree.SubElement(root, wfs + "SupportsGMLObjectTypeList")
    GMLObjectType = etree.SubElement(SupportsGMLObjectTypeList, wfs + "GMLObjectType")
    Name = etree.SubElement(GMLObjectType, wfs + "Name").text = "gml:AbstractGMLFeatureType"
    OutputFormats = etree.SubElement(GMLObjectType, wfs + "OutputFormats")
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xml; subtype=gml/3.1.1"
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xhmtl"
    GMLObjectType = etree.SubElement(SupportsGMLObjectTypeList, wfs + "GMLObjectType")
    Name = etree.SubElement(GMLObjectType, wfs + "Name").text = "gml:PointType"
    OutputFormats = etree.SubElement(GMLObjectType, wfs + "OutputFormats")
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xml; subtype=gml/3.1.1"
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xhmtl"
    GMLObjectType = etree.SubElement(SupportsGMLObjectTypeList, wfs + "GMLObjectType")
    Name = etree.SubElement(GMLObjectType, wfs + "Name").text = "gml:LineStringType"
    OutputFormats = etree.SubElement(GMLObjectType, wfs + "OutputFormats")
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xml; subtype=gml/3.1.1"
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xhmtl"
    GMLObjectType = etree.SubElement(SupportsGMLObjectTypeList, wfs + "GMLObjectType")
    Name = etree.SubElement(GMLObjectType, wfs + "Name").text = "gml:PolygonType"
    OutputFormats = etree.SubElement(GMLObjectType, wfs + "OutputFormats")
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xml; subtype=gml/3.1.1"
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xhmtl"
    GMLObjectType = etree.SubElement(SupportsGMLObjectTypeList, wfs + "GMLObjectType")
    Name = etree.SubElement(GMLObjectType, wfs + "Name").text = "gml:MultiPointType"
    OutputFormats = etree.SubElement(GMLObjectType, wfs + "OutputFormats")
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xml; subtype=gml/3.1.1"
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xhmtl"
    GMLObjectType = etree.SubElement(SupportsGMLObjectTypeList, wfs + "GMLObjectType")
    Name = etree.SubElement(GMLObjectType, wfs + "Name").text = "gml:MultiCurveType"
    OutputFormats = etree.SubElement(GMLObjectType, wfs + "OutputFormats")
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xml; subtype=gml/3.1.1"
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xhmtl"
    GMLObjectType = etree.SubElement(SupportsGMLObjectTypeList, wfs + "GMLObjectType")
    Name = etree.SubElement(GMLObjectType, wfs + "Name").text = "gml:MultiSurfaceType"
    OutputFormats = etree.SubElement(GMLObjectType, wfs + "OutputFormats")
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xml; subtype=gml/3.1.1"
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xhmtl"
    GMLObjectType = etree.SubElement(SupportsGMLObjectTypeList, wfs + "GMLObjectType")
    Name = etree.SubElement(GMLObjectType, wfs + "Name").text = "gml:AbstractMetaDataType"
    OutputFormats = etree.SubElement(GMLObjectType, wfs + "OutputFormats")
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xml; subtype=gml/3.1.1"
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xhmtl"
    GMLObjectType = etree.SubElement(SupportsGMLObjectTypeList, wfs + "GMLObjectType")
    Name = etree.SubElement(GMLObjectType, wfs + "Name").text = "gml:AbstractTopologyType"
    OutputFormats = etree.SubElement(GMLObjectType, wfs + "OutputFormats")
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xml; subtype=gml/3.1.1"
    Format = etree.SubElement(OutputFormats, wfs + "Format").text = "text/xhmtl"
    
    
    Filter_Capabilities = etree.SubElement(root, ogc + "Filter_Capabilities")
    Spatial_Capabilities = etree.SubElement(Filter_Capabilities, ogc + "Spatial_Capabilities")
    GeometryOperands = etree.SubElement(Spatial_Capabilities, ogc + "GeometryOperands")
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:Envelope"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:Point"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:LineString"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:Polygon"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:ArcByCenterPoint"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:CircleByCenterPoint"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:Arc"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:Circle"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:ArcByBulge"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:Bezier"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:Clothoid"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:CubicSpline"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:Geodesic"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:OffsetCurve"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:Triangle"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:PolyhedralSurface"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:TriangulatedSurface"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:Tin"
    GeometryOperand = etree.SubElement(GeometryOperands, ogc + "GeometryOperand").text = "gml:Solid"
    SpatialOperators = etree.SubElement(Spatial_Capabilities, ogc + "SpatialOperators")
    SpatialOperator = etree.SubElement(GeometryOperands, ogc + "SpatialOperator", name="BBOX")
    SpatialOperator = etree.SubElement(GeometryOperands, ogc + "SpatialOperator", name="Equals")
    SpatialOperator = etree.SubElement(GeometryOperands, ogc + "SpatialOperator", name="Disjoint")
    SpatialOperator = etree.SubElement(GeometryOperands, ogc + "SpatialOperator", name="Intersects")
    SpatialOperator = etree.SubElement(GeometryOperands, ogc + "SpatialOperator", name="Touches")
    SpatialOperator = etree.SubElement(GeometryOperands, ogc + "SpatialOperator", name="Crosses")
    SpatialOperator = etree.SubElement(GeometryOperands, ogc + "SpatialOperator", name="Within")
    SpatialOperator = etree.SubElement(GeometryOperands, ogc + "SpatialOperator", name="Contains")
    SpatialOperator = etree.SubElement(GeometryOperands, ogc + "SpatialOperator", name="Overlaps")
    SpatialOperator = etree.SubElement(GeometryOperands, ogc + "SpatialOperator", name="Beyond")

    Scalar_Capabilities = etree.SubElement(Filter_Capabilities, ogc + "Scalar_Capabilities")
    LogicalOperators = etree.SubElement(Scalar_Capabilities, ogc + "LogicalOperators")
    ComparisonOperators = etree.SubElement(Scalar_Capabilities, ogc + "ComparisonOperators")
    ComparisonOperator = etree.SubElement(Scalar_Capabilities, ogc + "ComparisonOperator").text = "LessThan"
    ComparisonOperator = etree.SubElement(Scalar_Capabilities, ogc + "ComparisonOperator").text = "GreaterThan"
    ComparisonOperator = etree.SubElement(Scalar_Capabilities, ogc + "ComparisonOperator").text = "LessThanEqualTo"
    ComparisonOperator = etree.SubElement(Scalar_Capabilities, ogc + "ComparisonOperator").text = "GreaterThanEqualTo"
    ComparisonOperator = etree.SubElement(Scalar_Capabilities, ogc + "ComparisonOperator").text = "EqualTo"
    ComparisonOperator = etree.SubElement(Scalar_Capabilities, ogc + "ComparisonOperator").text = "NotEqualTo"
    ComparisonOperator = etree.SubElement(Scalar_Capabilities, ogc + "ComparisonOperator").text = "Like"
    ComparisonOperator = etree.SubElement(Scalar_Capabilities, ogc + "ComparisonOperator").text = "Between"
    ComparisonOperator = etree.SubElement(Scalar_Capabilities, ogc + "ComparisonOperator").text = "NullCheck"
    ArithmeticOperators = etree.SubElement(Scalar_Capabilities, ogc + "ArithmeticOperators")
    SimpleArithmetic = etree.SubElement(ArithmeticOperators, ogc + "SimpleArithmetic")
    Functions = etree.SubElement(ArithmeticOperators, ogc + "Functions")
    FunctionNames = etree.SubElement(Functions, ogc + "FunctionNames")
    FunctionName = etree.SubElement(FunctionNames, ogc + "FunctionName", nArgs="1").text = "MIN"
    FunctionName = etree.SubElement(FunctionNames, ogc + "FunctionName", nArgs="1").text = "MAX"
    FunctionName = etree.SubElement(FunctionNames, ogc + "FunctionName", nArgs="1").text = "SIN"
    FunctionName = etree.SubElement(FunctionNames, ogc + "FunctionName", nArgs="1").text = "COS"
    FunctionName = etree.SubElement(FunctionNames, ogc + "FunctionName", nArgs="1").text = "TAN"

    Id_Capabilities = etree.SubElement(Filter_Capabilities, ogc + "Id_Capabilities")
    EID = etree.SubElement(Id_Capabilities, ogc + "EID")
    FID = etree.SubElement(Id_Capabilities, ogc + "FID")
    #WGS84BoundingBox = etree.SubElement(Layer, ows + "WGS84BoundingBox")
    #SupportedCRS = etree.SubElement(TileMatrixSet, ows + "SupportedCRS" ).text = gConfig['wmts']['SupportedCRS']
    
    ret = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding=ENCODING)
    print(ret)
    return ret


def handle_wmts_GetCapabilities(params, Start_response):
    #clear_tmp()
    Start_response('200 OK', [('Content-Type', 'text/xml;charset=' + ENCODING),])
    s = create_wmts_GetCapabilities()
    #s = ''
    #with open(gConfig['wmts']['GetCapabilities']) as f:
        #s = f.read()
    return [s]
    
def create_wmts_GetCapabilities():
    namespace = {'ows':"http://www.opengis.net/ows/1.1", 'xlink':"http://www.w3.org/1999/xlink", 'xsi':"http://www.w3.org/2001/XMLSchema-instance", 'gml':"http://www.opengis.net/gml", 'schemaLocation':"http://schemas.opengis.net/wmts/1.0/wmtsGetCapabilities_response.xsd"}
    ows = '{%s}' % namespace['ows']
    xlink = '{%s}' % namespace['xlink']
    root = etree.Element("Capabilities", xmlns="http://www.opengis.net/wmts/1.0", nsmap=namespace, version="1.0.0")
    #ServiceIdentification
    ServiceIdentification = etree.SubElement(root, ows + "ServiceIdentification")
    Title = etree.SubElement(ServiceIdentification, ows + "Title").text = gConfig['wmts']['ServiceIdentification_Title']
    ServiceType = etree.SubElement(ServiceIdentification, ows + "ServiceType").text = 'OGC WMTS'
    ServiceTypeVersion = etree.SubElement(ServiceIdentification, ows + "ServiceTypeVersion").text = '1.0.0'
    
    #OperationsMetadata
    OperationsMetadata = etree.SubElement(root, ows + "OperationsMetadata")
    Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="GetCapabilities")
    DCP= etree.SubElement(Operation, ows + "DCP")
    HTTP= etree.SubElement(DCP, ows + "HTTP")
    href = xlink + 'href'
    Get= etree.SubElement(HTTP, ows + "Get", {href:gConfig['wmts']['url'] + '?'})
    Constraint= etree.SubElement(Get, ows + "Constraint", name="GetEncoding")
    AllowedValues= etree.SubElement(Constraint, ows + "AllowedValues")
    Value= etree.SubElement(AllowedValues, ows + "Value").text = 'KVP'
    Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="GetTile")
    DCP= etree.SubElement(Operation, ows + "DCP")
    HTTP= etree.SubElement(DCP, ows + "HTTP")
    Get= etree.SubElement(HTTP, ows + "Get", {href:gConfig['wmts']['url'] + '?'})
    
    #Contents
    Contents = etree.SubElement(root, "Contents")
    Layer = etree.SubElement(Contents, "Layer")
    Title = etree.SubElement(Layer, ows + "Title").text = gConfig['wmts']['Layer_Title']
    WGS84BoundingBox = etree.SubElement(Layer, ows + "WGS84BoundingBox")
    LowerCorner = etree.SubElement(WGS84BoundingBox, ows + "LowerCorner").text = gConfig['wmts']['WGS84BoundingBox']['LowerCorner']
    UpperCorner = etree.SubElement(WGS84BoundingBox, ows + "UpperCorner").text = gConfig['wmts']['WGS84BoundingBox']['UpperCorner']
    Identifier = etree.SubElement(Layer, ows + "Identifier").text = gConfig['wmts']['Layer_Identifier']
    Style = etree.SubElement(Layer, "Style", isDefault="true")
    Title = etree.SubElement(Style, ows + "Title" ).text = 'Default'
    Identifier = etree.SubElement(Style, ows + "Identifier" ).text = 'default'
    Format = etree.SubElement(Layer, "Format" ).text = gConfig['mime_type'][gConfig['wmts']['format']]
    TileMatrixSetLink = etree.SubElement(Layer, "TileMatrixSetLink" )
    TileMatrixSet = etree.SubElement(TileMatrixSetLink, "TileMatrixSet" ).text = gConfig['wmts']['TileMatrixSet']
    
    TileMatrixSet = etree.SubElement(Contents, "TileMatrixSet")
    Identifier = etree.SubElement(TileMatrixSet, ows + "Identifier" ).text = gConfig['wmts']['TileMatrixSet']
    SupportedCRS = etree.SubElement(TileMatrixSet, ows + "SupportedCRS" ).text = gConfig['wmts']['SupportedCRS']
    WellKnownScaleSet = etree.SubElement(TileMatrixSet, "WellKnownScaleSet" ).text = gConfig['wmts']['WellKnownScaleSet']
    
    max_zoom_level, min_zoom_level = int(gConfig['wmts']['max_zoom_level']), int(gConfig['wmts']['min_zoom_level'])
    if max_zoom_level < min_zoom_level:
        max_zoom_level, min_zoom_level =  min_zoom_level, max_zoom_level  
    #zoomlist = range(max_zoom_level,min_zoom_level, -1)
    zoomlist = range(min_zoom_level, max_zoom_level+1, 1)
    
    
    pixelSize = float(gConfig['wmts']['pixelSize'])
    tileWidth,tileHeight = int(gConfig['wmts']['TileWidth']), int(gConfig['wmts']['TileHeight'])
    minLonLat,maxLonLat  = (float(gConfig['wmts']['minLonLat'][0]), float(gConfig['wmts']['minLonLat'][1])), (float(gConfig['wmts']['maxLonLat'][0]), float(gConfig['wmts']['maxLonLat'][1]))
    #tileMatrixMinX, tileMatrixMaxX = (26.0, 102.0), (26.0, 104.0)
    #tileMatrixMinY, tileMatrixMaxY = (24.0, 102.0), (26.0, 102.0)
    tileMatrixMinX, tileMatrixMaxX = (maxLonLat[1], minLonLat[0]), (maxLonLat[1], maxLonLat[0])
    tileMatrixMinY, tileMatrixMaxY = (minLonLat[1], minLonLat[0]), (maxLonLat[1], minLonLat[0])
    
    metersPerUnit = 0.0
    if gConfig['wmts'].has_key('metersPerUnit'):
        metersPerUnit = float(gConfig['wmts']['metersPerUnit'])
    else:
        metersPerUnitX = mapUtils.countDistanceFromLatLon(tileMatrixMaxX , tileMatrixMinX)/2*1000
        #print('metersPerUnitX=%f' % metersPerUnitX)
        metersPerUnitY = mapUtils.countDistanceFromLatLon(tileMatrixMaxY , tileMatrixMinY)/2*1000
        #print('metersPerUnitY=%f' % metersPerUnitY)
        metersPerUnit = metersPerUnitY 
    #print('metersPerUnit=%f' % metersPerUnit)
    for i in zoomlist:
        #matrixHeight = matrixWidth = mapUtils.tiles_on_level(i)
        matrixHeight = matrixWidth = mapUtils.tiles_on_level(max_zoom_level-(i-1))
        #print('%d=%d' % (i , matrixHeight))
        #scaleDenominatorX   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxX , tileMatrixMinX) * 1000./(tileWidth * matrixWidth)
        #scaleDenominatorY   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxY , tileMatrixMinY) * 1000./(tileHeight * matrixHeight)
        #print('scaleDenominatorX=%f, scaleDenominatorY=%f' % (scaleDenominatorX, scaleDenominatorY))
        #scaleDenominator   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxY , tileMatrixMinY) * 1000. /(tileHeight * matrixHeight)
        scaleDenominator   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxY , tileMatrixMinY)  /(tileHeight * matrixHeight)
        TileMatrix = etree.SubElement(TileMatrixSet, "TileMatrix" )
        #Identifier = etree.SubElement(TileMatrix, ows + "Identifier" ).text = "ynsat_" + str(i)
        Identifier = etree.SubElement(TileMatrix, ows + "Identifier" ).text = str(i)
        ScaleDenominator = etree.SubElement(TileMatrix, "ScaleDenominator" ).text = '%.8f' % scaleDenominator
        TopLeftCorner = etree.SubElement(TileMatrix, "TopLeftCorner" ).text = gConfig['wmts']['TopLeftCorner']
        TileWidth = etree.SubElement(TileMatrix, "TileWidth" ).text = str(tileWidth)
        TileHeight = etree.SubElement(TileMatrix, "TileHeight" ).text = str(tileHeight)
        MatrixWidth = etree.SubElement(TileMatrix, "MatrixWidth" ).text = str(matrixWidth)
        MatrixHeight = etree.SubElement(TileMatrix, "MatrixHeight" ).text = str(matrixHeight)
        #print("var m_%d = new Object();" % i)
        #print('m_%d.identifier = "%s";' % (i, Identifier))
        #print('m_%d.scaleDenominator = %.8f;' % (i, scaleDenominator))
        #print('m_%d.topLeftCorner = new OpenLayers.LonLat(%s);' % (i, gConfig['wmts']['TopLeftCorner'].replace(' ',',')))
        #print('m_%d.tileWidth = %s;' % (i, gConfig['wmts']['TileWidth']))
        #print('m_%d.tileHeight = %s;' % (i, gConfig['wmts']['TileHeight']))
        #print("matrixIds[%d] = m_%d;" % (i, i))
    
    ret = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding=ENCODING)
    print(ret)
    return ret

    
 
def download_callback(*args, **kwargs):
    global gConfig,  gMapTileCache, gSatTileCache, gTerrainCache
    global STATICRESOURCE_IMG_DIR
    zoom, col, row = args[1][2], args[1][0], args[1][1]
    root = os.path.abspath(gConfig['wmts']['tiles_map_root'])
    if args[2] == mapConst.LAYER_SAT:
        root = os.path.abspath(gConfig['wmts']['tiles_sat_root'])
    if args[2] == mapConst.LAYER_MAP:
        root = os.path.abspath(gConfig['wmts']['tiles_map_root'])
        
    p = os.path.join(root,
                    str(zoom),
                    str(col / 1024),
                    str(col % 1024),
                    str(row / 1024),
                    str(row % 1024) + gConfig['wmts']['format']
                    )
    if os.path.exists(p):
        key = '%d-%d-%d' % (zoom, col, row)
        with open(p, 'rb') as f:
            f1 = gevent.fileobject.FileObjectThread(f, 'rb')
            if args[2] == mapConst.LAYER_SAT:
                gSatTileCache[key] = f1.read()
            if args[2] == mapConst.LAYER_MAP:
                gMapTileCache[key] = f1.read()
    
    
#def handle_wmts_GetTile(params, Start_response):
    #global gConfig,  gMapTileCache, gSatTileCache, gTerrainCache
    #global STATICRESOURCE_IMG_DIR
    #picpath = os.path.join(STATICRESOURCE_IMG_DIR, gConfig['wmts']['missing'])
    #root = gConfig['wmts']['tiles_sat_root']
    ##gMapConf.map_service = 'Google'
    #lyrtype = mapConst.LAYER_SAT
    #if params.has_key('TILEMATRIXSET'):
        #if 'google_sat' in params['TILEMATRIXSET']:
            #root = os.path.abspath(gConfig['wmts']['tiles_sat_root'])
            #lyrtype = mapConst.LAYER_SAT
        #elif 'google_map' in params['TILEMATRIXSET']:
            #root = os.path.abspath(gConfig['wmts']['tiles_map_root'])
            #lyrtype = mapConst.LAYER_MAP
        #elif 'osm_map' in params['TILEMATRIXSET']:
            #root = os.path.abspath(gConfig['wmts']['tiles_map_root'])
            #lyrtype = mapConst.LAYER_MAP
        #if not os.path.exists(os.path.abspath(gConfig['wmts']['tiles_root'])):
            #os.mkdir(gConfig['wmts']['tiles_root'])
        #if not os.path.exists(root):
            #os.mkdir(root)
    #zoomlevel, row, col = None, None, None
    #if params.has_key('TILEMATRIX'):
        #if params['TILEMATRIX']=='undefined' or len(params['TILEMATRIX'])==0:
            #zoomlevel = 1
        #else:
            #zoomlevel = int(params['TILEMATRIX'])
    #if params.has_key('TILEROW'):
        #if params['TILEROW']=='undefined':
            #row = 0
        #else:
            #row = int(params['TILEROW'])
    #if params.has_key('TILECOL'):
        #if params['TILECOL']=='undefined':
            #col = 0
        #else:
            #col = int(params['TILECOL'])
        
    
    #zoom = int(gConfig['wmts']['max_zoom_level'])-2-zoomlevel
        
        
    #p = os.path.join(root,
                    #str(zoom),
                    #str(col / 1024),
                    #str(col % 1024),
                    #str(row / 1024),
                    #str(row % 1024) + gConfig['wmts']['format']
                    #)
    #p = os.path.abspath(p)
    #if os.path.exists(p):
        #picpath = p
        #key = '%d-%d-%d' % (zoom, col, row)
    #else:
        #key = '%d-%d-%d' % (zoom, col, row)
        #gMapDownloader.query_tile((col, row, zoom),lyrtype, download_callback)
    #Start_response('200 OK', [('Content-Type',str(gConfig['mime_type'][gConfig['wmts']['format']])), ])
    #if lyrtype == mapConst.LAYER_SAT:    
        #if not gSatTileCache.has_key(key):
            #try:
                #with open(picpath, 'rb') as f:
                    #f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                    #gSatTileCache[key] = f1.read()
            #except:
                #foundit = False
                #if not foundit:
                    #key = 'missing'
                #if not gSatTileCache.has_key(key):
                    #picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['wmts']['missing'])
                    #with open(picpath, 'rb') as f:
                        #f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                        #gSatTileCache[key] = f1.read()
                    #print(key)
    #if lyrtype == mapConst.LAYER_MAP:    
        #if not gMapTileCache.has_key(key):
            #try:
                #with open(picpath, 'rb') as f:
                    #f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                    #gMapTileCache[key] = f1.read()
            #except:
                #foundit = False
                #if not foundit:
                    #key = 'missing'
                #if not gMapTileCache.has_key(key):
                    #picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['wmts']['missing'])
                    #with open(picpath, 'rb') as f:
                        #f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                        #gMapTileCache[key] = f1.read()
                    #print(key)
         
    #ret = None
    #if lyrtype == mapConst.LAYER_SAT:
        #ret = gSatTileCache[key]
    #if lyrtype == mapConst.LAYER_MAP:
        #ret = gMapTileCache[key]
    #return [ret,]

def handle_tiles(Env, Start_response):
    global gConfig, gTileCache
    def get_blank_tile(image_type):
        blank_tile = ''
        picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['tiles'][image_type]['missing'])
        with open(picpath, 'rb') as f:
            f1 = gevent.fileobject.FileObjectThread(f, 'rb')
            blank_tile = f1.read()
        return blank_tile
        
    path_info = Env['PATH_INFO']
    d = cgi.parse(None, Env)
    ret = None
    mimetype = 'image/png'
    #key = path_info.replace('/tiles/','')
    if d.has_key('image_type') and d.has_key('x') and d.has_key('y') and d.has_key('level'):
        image_type = d['image_type'][0]
        x, y, level = d['x'][0], d['y'][0], d['level'][0]
        tilepath = '%s/%s/%s%s' % (level, x, y, gConfig['tiles'][image_type]['mimetype'])
        if not gTileCache.has_key(image_type):
            gTileCache[image_type] = {}
        if not gTileCache[image_type].has_key('missing'):
            gTileCache[image_type]['missing'] = get_blank_tile(image_type)
        if gTileCache[image_type].has_key(tilepath):
            ret = gTileCache[image_type][tilepath]
        else:
            try:
                mimetype, ret = db_util.gridfs_tile_find('tiles', image_type, tilepath, d)
                gTileCache[image_type][tilepath] = ret
            except:
                ret = gTileCache[image_type]['missing']
    else:
        ret = gTileCache[image_type]['missing']
    if ret is None:
        ret = gTileCache[image_type]['missing']
    #bytestr = bytearray(ret) 
    #Start_response('200 OK', [('Content-Type', mimetype), ('Content-Length', str(len(bytestr)))])
    #return [bytestr]
    Start_response('200 OK', [('Content-Type', mimetype), ])
    return [ret]
        
            

def handle_terrain(Env, Start_response):
    global gConfig, gTileCache
    path_info = Env['PATH_INFO']
    d = cgi.parse(None, Env)
    ret = None
    mimetype = str('application/octet-stream')
    key = path_info.replace('/terrain/','')
    terrain_type = 'quantized_mesh'
    if d.has_key('terrain_type'):
        terrain_type = d['terrain_type'][0]
    
    if not gTileCache.has_key(terrain_type):
        gTileCache[terrain_type] = {}
    if gTileCache[terrain_type].has_key(key):
        ret = gTileCache[terrain_type][key]
    else:
        tilepath = key
        if tilepath == 'layer.json':
            mimetype, ret = db_util.gridfs_tile_find('terrain', terrain_type, tilepath, d)
            gTileCache[terrain_type][key] = ret
            Start_response('200 OK', [('Content-Type', mimetype),])
            return [ret]
        else:
            print('tilepath:%s' % tilepath)
            mimetype, ret = db_util.gridfs_tile_find('terrain', terrain_type, tilepath, d)
            if ret:
                gTileCache[terrain_type][key] = ret
                Start_response('200 OK', [('Content-Type', mimetype),])
                return [ret]
            else:
                if not gTileCache[terrain_type].has_key('missing'):
                    print('reading mongo blank_terrain...')
                    tilepath = gConfig['terrain'][terrain_type]['missing'] #'0/0/0.terrain'
                    mimetype, ret = db_util.gridfs_tile_find('terrain', terrain_type, tilepath, d)
                    gTileCache[terrain_type]['missing'] = ret
                ret = gTileCache[terrain_type]['missing']
                
    Start_response('200 OK', [('Content-Type', mimetype),])
    return [ret]

        
def handle_terrain1(Env, Start_response):
    global gConfig,  gMapTileCache, gSatTileCache, gTerrainCache
    path_info = Env['PATH_INFO']
    #d = cgi.parse(None, Env)
    ret = None
    key = path_info.replace('/terrain/','')
    if gTerrainCache.has_key(key):
        ret = gTerrainCache[key]
    else:
        arr = key.split('/')
        tilepath = gConfig['terrain']['tiles_dir']
        for i in arr:
            tilepath = os.path.join(tilepath, i)
        tilepath = os.path.abspath(tilepath)
        ret = '' 
        if os.path.exists(tilepath):
            #print('reading %s...' % tilepath)
            with open(tilepath, 'rb') as f:
                f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                ret = f1.read()
            gTerrainCache[key] = ret
        else:
            if gTerrainCache.has_key('missing'):
                ret = gTerrainCache['missing']
            else:
                print('reading blank_terrain...')
                with open(gConfig['terrain']['blank_terrain'], 'rb') as f:
                    f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                    ret = f1.read()
                gTerrainCache['missing'] = ret
    Start_response('200 OK', [('Content-Type', 'application/octet-stream'),])
    return [ret]
    
    
def handle_arcgistile(Env, Start_response):
    global gConfig, gMapTileCache, gSatTileCache
    global STATICRESOURCE_IMG_DIR
    ret = None
    dd = cgi.parse(None, Env)
    d = {}
    for k in dd.keys():
        d[k] = dd[k][0]
    if d.has_key('zoom') and d.has_key('col')  and d.has_key('row'):
        zoom  = int(d['zoom'])
        col = int(d['col'])
        row = int(d['row'])
        key = '%d-%d-%d' % (zoom, col, row)
        if not gSatTileCache.has_key(key):
            try:
                #picpath = os.path.join(gConfig['wmts']['arcgis_tiles_root'], '_alllayers', 'L%02d' % zoom, 'R%08x' % row, 'C%08x%s' % (col, gConfig['wmts']['format']))
                picpath = os.path.join(gConfig['wmts']['arcgis_tiles_root'],   '%d' % zoom, '%d' % col, '%d%s' % (row, gConfig['wmts']['format']))
                print('%s, %s' % (key, picpath))
                with open(picpath, 'rb') as f:
                    f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                    gSatTileCache[key] = f1.read()
                
            except:
                foundit = False
                if not foundit:
                    key = 'missing'
                if not gSatTileCache.has_key(key):
                    picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['wmts']['missing'])
                    with open(picpath, 'rb') as f:
                        f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                        gSatTileCache[key] = f1.read()
        
        ret = gSatTileCache[key]
    elif d.has_key('is_esri') :
        key = Env['PATH_INFO'].replace('/arcgistile/','')
        if not gSatTileCache.has_key(key):
            try:
                #picpath = os.path.join(gConfig['wmts']['arcgis_tiles_root'], '_alllayers', 'L%02d' % zoom, 'R%08x' % row, 'C%08x%s' % (col, gConfig['wmts']['format']))
                picpath = os.path.join(gConfig['wmts']['arcgis_tiles_root'],   key)
                print('%s, %s' % (key, picpath))
                with open(picpath, 'rb') as f:
                    f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                    gSatTileCache[key] = f1.read()
                
            except:
                foundit = False
                if not foundit:
                    key = 'missing'
                if not gSatTileCache.has_key(key):
                    picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['wmts']['missing'])
                    with open(picpath, 'rb') as f:
                        f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                        gSatTileCache[key] = f1.read()
        
        ret = gSatTileCache[key]
    else:
        if not gSatTileCache.has_key('missing'):
            picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['wmts']['missing'])
            with open(picpath, 'rb') as f:
                f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                gSatTileCache['missing'] = f1.read()
        ret = gSatTileCache['missing']
        
    Start_response('200 OK', [('Content-Type',str(gConfig['mime_type'][gConfig['wmts']['format']])), ])
    return [ret]    
        
    
def handle_wmts(Env, Start_response):
    dd = cgi.parse(None, Env)
    d = {}
    #s = 'method=' + Env['REQUEST_METHOD'] + '\n'
    for k in dd.keys():
        d[k.upper()] = dd[k][0]
    #print(d)
    #Start_response('200 OK', [('Content-Type', 'text/plain;charset=' + ENCODING)])
    if d.has_key('SERVICE') and d['SERVICE'] in ['WMTS'] :
        #if d.has_key('VERSION') and d['VERSION'] in ['1.0.0', '1.0']:
        if d.has_key('REQUEST') :
            if d['REQUEST'] in ['GetCapabilities']:
                return handle_wmts_GetCapabilities(d, Start_response)
            elif d['REQUEST'] in ['GetTile']:
                return handle_wmts_GetTile(d, Start_response)
            else:
                Start_response('200 OK', [('Content-Type', 'text/plain;charset=' + ENCODING)])
                s = 'Unsupported WMTS request'
        else:
            Start_response('200 OK', [('Content-Type', 'text/plain;charset=' + ENCODING)])
            s = 'Unsupported WMTS version'
    else:
        Start_response('200 OK', [('Content-Type', 'text/plain;charset=' + ENCODING)])
        s = 'Unsupported service'
        
    return [s]

def handle_wfs(Env, Start_response):
    global gWFSService
    return gWFSService.dispatchRequest(Env, Start_response)
    
def handle_cluster(Env, Start_response):
    global gConfig
    Start_response('200 OK', [('Content-Type', 'text/json;charset=' + ENCODING),])
    if int(Env['SERVER_PORT'])==int(gConfig['cluster']['manager_port']) and gConfig['cluster']['enable_cluster'] in ['true','True']:
        op = ''
        if Env['PATH_INFO']=='/create_cluster':
            if len(get_pid_from_name('nginx'))==0:
                op = 'create ok'
                create_cluster()
        elif Env['PATH_INFO']=='/kill_cluster':
            op = 'kill ok'
            kill_cluster()
        #print(Env)
        return [json.dumps({'result':op})]
    else:
        return [json.dumps({'result':'cluster is disabled or not by manager'})]
    
    
    
def handle_test(Env, Start_response):
    s = '测试OK'
    d = cgi.parse(None, Env)
    print(d)
    Start_response('200 OK', [('Content-Type', 'text/json;charset=' + ENCODING),])
    print(s)
    return [s]
    
    
def get_condition_from_dict(dct):
    cond = '1=1'            
    for k in dct.keys():
        if k in ['voltage', 'line_id', 'id', 'tower_id', 'start_tower_id', 'end_tower_id', 'model_code', 'side', 'position']:
            if k == 'side':
                if dct[k][0]=='1':
                    cond += " AND %s='%s'" % (k, u'正')
                elif dct[k][0]=='0':
                    cond += " AND %s='%s'" % (k, u'反')
            else:    
                cond += " AND %s='%s'" % (k, dct[k][0])
        else:
            cond += " AND %s=%s" % (k, dct[k][0])
    print(cond)
    return cond

def mongo_get_condition_from_dict(dct):
    ret = {}            
    for k in dct.keys():
        ret[k] =  dct[k][0]
    print(ret)
    return ret
    
def handle_get_method(Env, Start_response):
    global ENCODING
    global STATICRESOURCE_DIR, UPLOAD_PHOTOS_DIR, UPLOAD_VOICE_DIR
    global gConfig
    ret = {}
    s = ''
    d = cgi.parse(None, Env)
    isgrid = False
    area = ''
    data = {}
    if d.has_key('grid'):
        isgrid = True
        del d['grid']
    if d.has_key('area'):
        area = d['area'][0]
        del d['area']
    if d.has_key('geojson'):
        if d['geojson'][0]=='line_towers':
            data = db_util.gen_geojson_by_lines(area)
            s = json.dumps(data, ensure_ascii=True, indent=4)        
        elif d['geojson'][0]=='tracks':
            data = db_util.gen_geojson_tracks(area)
            s = json.dumps(data, ensure_ascii=True, indent=4)        
        else:
            k = d['geojson'][0]
            p = os.path.abspath(STATICRESOURCE_DIR)
            if k == 'potential_risk':
                k = 'geojson_%s_%s' % (k, area)
            p = os.path.join(p, 'geojson', area, '%s.json' % k)
            print(p)
            if os.path.exists(p):
                with open(p) as f:
                    f1 = gevent.fileobject.FileObjectThread(f, 'r')
                    s = f1.read()
            else:
                p = os.path.abspath(STATICRESOURCE_DIR)
                p = os.path.join(p, 'geojson', '%s.json' % k)
                if os.path.exists(p):
                    with open(p) as f:
                        f1 = gevent.fileobject.FileObjectThread(f, 'r')
                        s = f1.read()
        del d['geojson']
        
        
    if d.has_key('table'):
        table = d['table'][0]
        del d['table']
        #cond = '1=1'
        dbtype = 'odbc'
        if d.has_key('dbtype'):
            dbtype = d['dbtype'][0]
            del d['dbtype']
        if  dbtype == 'pg':
            data = db_util.pg_get_records(table, get_condition_from_dict(d))
            
        else:
            data = db_util.odbc_get_records(table, get_condition_from_dict(d), area)
            if table in ['TABLE_TOWER']:
                if d.has_key('line_id'):
                    data = db_util.odbc_get_sorted_tower_by_line(d['line_id'][0], area)
                
        if isgrid:
            data = {'Rows':data}
        s = json.dumps(data, ensure_ascii=True, indent=4)
        
    if d.has_key('check_file'):
        fn = dec(d['check_file'][0])
        dir_name = dec(d['dir_name'][0])
        del d['check_file']
        del d['dir_name']
        ret["result"] = {}
        ret["result"]["filename"] = fn
        if dir_name == 'voice':
            if check_voice_file_by_fault(fn):
                ret["result"]["exist"] = "true"
            else:
                ret["result"]["exist"] = "false"
        else:
            if os.path.exists(os.path.join(UPLOAD_PHOTOS_DIR, dir_name, fn)):
                ret["result"]["exist"] = "true"
            else:
                ret["result"]["exist"] = "false"
        s = json.dumps(ret, ensure_ascii=True, indent=4)
    if d.has_key('delete_file'):
        fn = dec(d['delete_file'][0])
        dir_name = dec(d['dir_name'][0])
        del d['delete_file']
        del d['dir_name']
        ret["result"] = {}
        ret["result"]["filename"] = fn
        if dir_name == 'voice':
            pl = get_voice_file_by(fn)
            if len(pl)>0:
                for i in pl:
                    p = os.path.join(UPLOAD_VOICE_DIR, fn)
                    if os.path.exists(p):
                        os.remove(p)
                ret["result"]["removed"] = "true"
            else:
                ret["result"]["removed"] = "false"
                
        else:
            p = os.path.join(UPLOAD_PHOTOS_DIR, dir_name, fn)
            if os.path.exists(p):
                os.remove(p)
                ret["result"]["removed"] = "true"
            else:
                ret["result"]["removed"] = "false"
        s = json.dumps(ret, ensure_ascii=True, indent=4)
    if d.has_key('list_file_dir_name'):
        dir_name = dec(d['list_file_dir_name'][0])
        del d['list_file_dir_name']
        ret["result"] = {}
        ret["result"]["dirs"] = [dir_name, ]
        p = os.path.join(UPLOAD_PHOTOS_DIR, dir_name)
        if os.path.exists(p):
            l = os.listdir(p)
            ret["result"]["files"] = l
        else:
            ret["result"]["files"] = []
        s = json.dumps(ret, ensure_ascii=True, indent=4)
    if d.has_key('get_voice_files'):
        get_voice_files = d['get_voice_files'][0]
        ret["result"] = {}
        ret["result"]["ids"] = get_voice_file_all()
        s = json.dumps(ret, ensure_ascii=True, indent=4)
    if d.has_key('op'):
        op = d['op'][0]
        del d['op']
        if op == "get_mongodb_server_tree":
            host = d['host'][0]
            del d['host']
            port = d['port'][0]
            del d['port']
            ret["result"] = {}
            ret["result"]["data"] = db_util.mongodb_get_server_tree(host, port)
            s = json.dumps(ret, ensure_ascii=True, indent=4)
        elif op == "gridfs":
            ret = db_util.gridfs_find(d)
            if isinstance(ret, tuple) and ret[0] and ret[1]:
                Start_response('200 OK', [('Content-Type', str(ret[0])),])
                s = ret[1]
                return [s]
            if isinstance(ret, list):
                s = json.dumps(ret, ensure_ascii=True, indent=4)
        elif op == "gridfs_delete":
            try:
                db_util.gridfs_delete(d)
                s = ''
            except:
                ret["result"] = sys.exc_info()[1].message
                s = json.dumps(ret, ensure_ascii=True, indent=4)
        
    Start_response('200 OK', [('Content-Type', 'text/json;charset=' + ENCODING),])
    if isinstance(ret, dict) and len(ret.keys())==0:
        ret["result"] = "ok"
    if isinstance(s, list) and len(s)==0:
        s = json.dumps(ret, ensure_ascii=True, indent=4)
    return [s]

def create_upload_xls_dir():
    global STATICRESOURCE_DIR
    p = os.path.join(STATICRESOURCE_DIR, 'upload')
    if not os.path.exists(p):
        os.mkdir(p)
    p = os.path.join(p, 'xls')
    if not os.path.exists(p):
        os.mkdir(p)
    return p
        
def create_voice_dir():
    global STATICRESOURCE_DIR, UPLOAD_VOICE_DIR
    if not os.path.exists(UPLOAD_VOICE_DIR):
        os.mkdir(UPLOAD_VOICE_DIR)

def check_voice_file_by_fault(id):
    global STATICRESOURCE_DIR, UPLOAD_VOICE_DIR
    create_voice_dir()
    ret = False
    for fn in os.listdir(UPLOAD_VOICE_DIR):
        if id in fn:
            ret = True
            break
    return ret

def get_voice_file_latest(id):
    global STATICRESOURCE_DIR, UPLOAD_VOICE_DIR
    create_voice_dir()
    l = []
    for fn in os.listdir(UPLOAD_VOICE_DIR):
        if id in fn:
            l.append(fn)
    ret = None
    if len(l)>0:
        l.sort()
        ret = l[-1]
    return ret

def get_voice_file_by(id):
    global STATICRESOURCE_DIR, UPLOAD_VOICE_DIR
    create_voice_dir()
    l = []
    for fn in os.listdir(UPLOAD_VOICE_DIR):
        if id in fn:
            l.append(fn)
    return l

def get_voice_file_all():
    global STATICRESOURCE_DIR, UPLOAD_VOICE_DIR
    s = set()
    for fn in os.listdir(UPLOAD_VOICE_DIR):
        p = os.path.join(UPLOAD_VOICE_DIR, fn)
        if os.path.isfile(p):
            arr = fn.split('@')
            if len(arr)==3:
                id = arr[1]
                s.add(id)
    return list(s)
    


def create_pic_dir():
    global STATICRESOURCE_DIR, UPLOAD_PHOTOS_DIR
    if not os.path.exists(os.path.join(STATICRESOURCE_DIR,'photos')):
        os.mkdir(os.path.join(STATICRESOURCE_DIR,'photos'))
    if not os.path.exists(UPLOAD_PHOTOS_DIR):
        os.mkdir(UPLOAD_PHOTOS_DIR)

def handle_upload_file(Env, qsdict, filedata):
    global STATICRESOURCE_DIR, UPLOAD_PHOTOS_DIR, UPLOAD_VOICE_DIR
    
    def parse_options_header(header, options=None):
        if ';' not in header:
            return header.lower().strip(), {}
        ctype, tail = header.split(';', 1)
        options = options or {}
        for match in _RE_OPTION.finditer(tail):
            key = match.group(1).lower()
            value = header_unquote(match.group(2), key=='filename')
            options[key] = value
        return ctype, options
    def header_quote(val):
        if not _RE_SPECIAL.search(val):
            return val
        return '"' + val.replace('\\','\\\\').replace('"','\\"') + '"'
    
    def header_unquote(val, filename=False):
        if val[0] == val[-1] == '"':
            val = val[1:-1]
            if val[1:3] == ':\\' or val[:2] == '\\\\': 
                val = val.split('\\')[-1] # fix ie6 bug: full path --> filename
            return val.replace('\\\\','\\').replace('\\"','"')
        return val
    
    def tob(data, encode='utf8'): # Convert strings to bytes (py2 and py3)
        return data.encode(encode) if isinstance(data, unicode) else data
    def parse_form_data(environ, mimetype, filedata):
        filename, ret = None, None
        try:
            if environ.get('REQUEST_METHOD','GET').upper() not in ('POST', 'PUT'):
                raise Exception("Request method other than POST or PUT.")
            content_length = int(environ.get('CONTENT_LENGTH', '-1'))
            content_type = environ.get('CONTENT_TYPE', '')
            if not content_type:
                raise Exception("Missing Content-Type header.")
            content_type, options = parse_options_header(content_type)
            if content_type == 'multipart/form-data':
                boundary = options.get('boundary','')
            content_type_token = tob('Content-Type: ' + mimetype)
            if boundary:
                _bcrnl = tob('\r\n')
                s = content_type_token + _bcrnl * 2
                s1 = _bcrnl + tob('--') + boundary + tob('--') + _bcrnl
                ret = filedata[filedata.index(s)+len(s):-len(s1)]
                head = filedata[:filedata.index(s)]
                arr = head.split(_bcrnl)
                for i in arr:
                    if 'Content-Disposition' in i:
                        arr1 = i.split(';')
                        for ii in arr1:
                            if 'filename=' in ii:
                                arr2 = ii.split('=')
                                filename = dec(arr2[1].strip().replace('"',''))
                                break
                        break
        except:
            raise
        return filename, ret
    
    ret = False
    root = os.path.abspath(STATICRESOURCE_DIR)
    create_pic_dir()
    create_voice_dir()
    try:
        #task item picture
        if qsdict.has_key('pic_file_name'):
            fn = dec(qsdict['pic_file_name'][0])
            dir_name = dec(qsdict['dir_name'][0])
            #pic_type = qsdict['pic_type'][0]
            p = os.path.join(root, 'photos')
            if not os.path.exists(p):
                os.mkdir(p)
            p = os.path.join(root, 'photos', 'upload')
            if not os.path.exists(p):
                os.mkdir(p)
            save_file_to(UPLOAD_PHOTOS_DIR, dir_name,  fn, filedata)
            ret = True
        if qsdict.has_key('voice_file_name'):
            fn = qsdict['voice_file_name'][0]
            p = os.path.join(root, 'voice')
            if not os.path.exists(p):
                os.mkdir(p)
            save_file_to(UPLOAD_VOICE_DIR, None, fn, filedata)
            ret = True
        if qsdict.has_key('import_xls'):
            root = create_upload_xls_dir()
            area = urllib.unquote_plus( qsdict['area'][0])
            line_name = urllib.unquote_plus( qsdict['line_name'][0])
            voltage = urllib.unquote_plus( qsdict['voltage'][0])
            category = urllib.unquote_plus( qsdict['category'][0])
            fn = str(uuid.uuid4()) + '.xls'
            import_xls(os.path.join(root, fn), filedata, dec(area), dec(line_name), dec(voltage),  dec(category))
            ret = True
        if qsdict.has_key('db'):
            mimetype = urllib.unquote_plus(qsdict['mimetype'][0])
            filename, filedata1 = parse_form_data(Env, mimetype, filedata)
            #with open(ur'd:\aaa.png','wb') as f:
                #f.write(filedata)
            db_util.gridfs_save(qsdict, filename, filedata1)
            ret = True
    except:
        #print(sys.exc_info()[1])
        raise
    return ret


def import_xls(path, fileobj, area, line_name, voltage,  category):
    with open(path, 'wb') as f:
        f.write(fileobj)
    return db_util.import_tower_xls_file(area, line_name, voltage,  category, path)

    
def save_file_to(category, dir_id, filename, fileobj):
    root = os.path.abspath(category)
    if not os.path.exists(root):
        os.mkdir(root)
        
    p = os.path.join(root, filename)
    if dir_id:
        p = os.path.join(root, dir_id)
        if not os.path.exists(p):
            os.mkdir(p)
        p = os.path.join(root, dir_id, filename)
    with open(p, 'wb') as f:
        f1 = gevent.fileobject.FileObjectThread(f, 'wb')
        f1.write(fileobj)
    
    
    
    
#def save_upload_file1(buf):
    #ret = False
    #try:
        #arr = buf.split('\r\n')
        #ds_plus = urllib.unquote_plus(arr[0])
        #print(ds_plus)
        #obj = json.loads(ds_plus)
        #op = ''
        #if obj.has_key('op'):
            #op = obj['op']
            #if op=='upload_task':
                #filename = 'unknown.zip'
                #if obj.has_key('filename'):
                    #filename = obj['filename']
                #save_upload_task(filename, buf[buf.index('\r\n')+2:], obj)
        #if obj.has_key('filename') and op != 'upload_task':
            #save_upload_image(obj['filename'], buf[buf.index('\r\n')+2:], obj)
            #ret = True
    #except:
        #print(sys.exc_info()[1])
    #return ret
    

def geojson_to_czml(aList):
    cz = czml.CZML()
    for i in aList:
        if i.has_key('properties') and i['properties'].has_key('id'):
            packet = czml.CZMLPacket(id=i['properties']['id'])
            #tower
            if i['properties'].has_key('tower_code'):
                packet = czml.CZMLPacket(id=i['properties']['id'], name=i['properties']['tower_name'])
                packet.position = czml.Position(cartographicDegrees = [i['geometry']['coordinates'][0], i['geometry']['coordinates'][1], i['properties']['geo_z'],])
                packet.point = czml.Point(show=True, color={'rgba': [255, 255, 0, 255]}, pixelSize=10, outlineColor={'rgba': [0, 0, 0, 255]}, outlineWidth=1)
                #packet.label = czml.Label(text=i['properties']['tower_name'], show=True, scale=0.5)
                packet.description = i['properties']['tower_name']
                #packet.billboard = czml.Billboard(image='http://localhost:88/img/tower.png')
                cz.append(packet)
    return cz
        
    
def handle_post_method(Env, Start_response):
    global ENCODING
    buf = Env['wsgi.input'].read()
    
    querydict = {}
    if Env.has_key('QUERY_STRING'):
        querydict = urlparse.parse_qs(Env['QUERY_STRING'])
    #for k in d.keys():
        #kv = pair.split('=')
        #try:
            #d[kv[0]] = eval(kv[1])
        #except:
            #d[kv[0]] = kv[1]
    ret = {}
    is_upload = False
    is_mongo = False
    use_czml = False
    get_extext = False
    try:
        ds_plus = urllib.unquote_plus(buf)
        obj = json.loads(dec(ds_plus))
        if obj.has_key(u'db') and obj.has_key(u'collection'):
            is_mongo = True
            dbname = obj[u'db']
            collection = obj[u'collection']
            action = None
            data = None
            if obj.has_key(u'action') and obj.has_key(u'data'):
                action = obj[u'action']
                data = obj[u'data']
                del obj[u'action']
                del obj[u'data']
            if obj.has_key(u'use_czml') and obj[u'use_czml']:
                use_czml = True
                del obj[u'use_czml']
            if obj.has_key(u'get_extext') and obj[u'get_extext']:
                get_extext = True
                del obj[u'get_extext']
            del obj[u'db']
            del obj[u'collection']
            if action:
                l = db_util.mongo_action(dbname, collection, action, data, obj)
            else:
                l = db_util.mongo_find(dbname, collection, obj)
            if get_extext:
                l = db_util.find_extent(l)
            if use_czml:
                l = geojson_to_czml(l)
            if isinstance(l, list) and len(l) > 0:
                ret = l
            elif isinstance(l, dict) and len(l.keys()) > 0:
                ret = l
            elif isinstance(l, czml.CZML):
                Start_response('200 OK', [('Content-Type', 'text/json;charset=' + ENCODING), ])
                return [enc(l.dumps()),]
            else:
                ret["result"] = "%s.%s return 0 record" % (dbname, collection)
        else:
            ret["result"] = "unknown query operation"
        
    except:
        if len(querydict.keys())>0:
            try:
                #forms, files = multipart.parse_form_data(Env)
                #with open(ur'd:\aaa.png','wb') as f:
                    #f.write(buf)
                is_upload = handle_upload_file(Env, querydict, buf)
                ret['result'] = ''
            except:
                ret['result'] = sys.exc_info()[1]
        obj = {}
    if not is_mongo:
        if obj.has_key('thunder_counter'):
            try:
                ret = handle_thunder_soap(obj)
            except:
                e = sys.exc_info()[1]
                if hasattr(e, 'message'):
                    ret['result'] = e.message
                else:
                    ret['result'] = str(e)
                
        elif obj.has_key('op'):
            if obj.has_key('area') and obj['area'] and len(obj['area'])>0:
                if obj['op'] in ['save','delete','update']:
                    ret = db_util.odbc_save_data_to_table(obj['table'], obj['op'], obj['data'], obj['line_id'], obj['start_tower_id'], obj['end_tower_id'], obj['area'])
                else:
                    ret = handle_requset_sync(obj)
            elif obj['op'] in ['alt','height'] :
                if obj.has_key('lng') and obj.has_key('lat') and isinstance(obj['lng'], float) and isinstance(obj['lat'], float):
                    ret = extract_one_altitude(obj['lng'], obj['lat'])
                if obj.has_key('data')  and isinstance(obj['data'], list):
                    ret = extract_many_altitudes(obj['data'])
            else:
                ret["result"] = "unknown area"
        elif obj.has_key('tracks') and obj.has_key('area'):
            ret = db_util.save_tracks(obj['tracks'], obj['area'])
        
    if isinstance(ret, list): 
        pass
    elif isinstance(ret, str) or isinstance(ret, unicode) or isinstance(ret, int) or isinstance(ret, float):
        pass
    elif isinstance(ret, dict):
        if len(ret.keys())==0:
            pass
        elif ret.has_key('result'):
            if isinstance(ret['result'], exceptions.Exception):
                if hasattr(ret['result'], 'message'):
                    ret['result'] = ret['result'].message
                else:
                    ret['result'] = str(ret['result'])
            elif isinstance(ret['result'], str) or isinstance(ret['result'], unicode) or isinstance(ret['result'], int) or isinstance(ret['result'], float):
                pass
            elif isinstance(ret['result'], list) or isinstance(ret['result'], dict):
                pass
        else:    
            ret["result"] = "unknown operation"
    else:    
        ret["result"] = "unknown operation"
    Start_response('200 OK', [('Content-Type', 'text/json;charset=' + ENCODING), ])
    #time.sleep(6)
    #print(ret)
    #return [urllib.quote(enc(json.dumps(ret)))]
    return [json.dumps(ret, ensure_ascii=True, indent=4)]

def handle_thunder_soap(obj):
    ret = {}
    if obj['thunder_counter'] == 'GetFlashofDate':
        ret = soap_GetFlashofDate(obj['start_time'], obj['end_time'])
    if obj['thunder_counter'] == 'GetFlashofEnvelope':
        ret = soap_GetFlashofEnvelope(obj['start_time'], obj['end_time'], obj['lng1'], obj['lng2'], obj['lat1'], obj['lat2'])
    return ret    

def dishen_ws_loop(aWebSocket, aHash):
    while 1:
        #now = time.strftime('%Y-%m-%d %H:%M:%S')[:10]
        #ws.send("%d,%f\n" % ((time.time() - time.timezone)*1000, random.random()*10))
        #t = (time.time() - time.timezone) * 1000
        t = time.time()  * 1000
        if aWebSocket:
            #message = aWebSocket.receive()
            #print("message=%s" % message)
            aWebSocket.send( '%s\n%d' % (str(aHash),int(t)) )
        else:
            break
        gevent.sleep(1.0)

def handle_websocket(environ, start_response):
    global gCapture, gGreenlets
    for k, v in environ.iteritems():
        print('%s=%s' % (k,str(v)))

    ws = environ["wsgi.websocket"]
    print(dir(ws))
    #print(dir(ws.rfile))
    #print(dir(ws.socket))
    if environ['PATH_INFO'] == '/dishen_ws':
        glet = gevent.getcurrent()
        ghash = glet.__hash__()
        gGreenlets[str(ghash)] = (glet, ws)
        dishen_ws_loop(ws, ghash)
    s = 'version=%s' % ( environ['wsgi.websocket_version'])
    start_response('200 OK', [('Content-Type', 'text/plain;charset=' + ENCODING)])
    return [s]
    
def application(environ, start_response):
    global gConfig
    path_info = environ['PATH_INFO']
    
    if 'proxy.cgi' in path_info:
        return handle_proxy_cgi(environ, start_response)
    elif path_info == '/test':
        return handle_test(environ, start_response)
    elif path_info == '/get':
        return handle_get_method(environ, start_response)
    elif path_info == '/post':
        return handle_post_method(environ, start_response)
    #elif path_info == '/wmts':
        #return handle_wmts(environ, start_response)
    elif path_info == '/tiles':
        return handle_tiles(environ, start_response)
    elif '/arcgistile' in path_info:
        return handle_arcgistile(environ, start_response)
    elif path_info == '/terrain/layer.json' or path_info[-8:] == '.terrain':
        return handle_terrain(environ, start_response)
    #elif path_info[-8:] == '.terrain':
        #return handle_terrain1(environ, start_response)
    elif path_info == '/wfs':
        return handle_wfs(environ, start_response)
    elif path_info =='/create_cluster' or  path_info =='/kill_cluster':
        return handle_cluster(environ, start_response)
    elif path_info == gConfig['websocket']['services']:
        #if p=='/control':
            #print('websocket_version=%s' % environ['wsgi.websocket_version'])
        try:
            return handle_websocket(environ, start_response)
        except geventwebsocket.WebSocketError,e:
            print('application Exception:%s' % str(e))
    else:
        if path_info[-1:] == '/':
            path_info += gConfig['web']['indexpage']
        statuscode, contenttype, body =  handle_static(path_info)
        if start_response:
            start_response(statuscode, [('Content-Type', contenttype), ])
            return [body]
        
def handle_proxy_cgi(environ, start_response):
    global gConfig
    method = environ['REQUEST_METHOD']
    post_data = ''
    if method == "POST":
        qs = environ['PATH_INFO']
        buf = environ['wsgi.input'].read()
        post_data = urllib.unquote_plus(buf)
        
        d = cgi.parse(None, environ)
        
        if d.has_key("url"):
            url = d["url"][0]
        else:
            url = 'http://XIEJUN-DESKTOP:88'
    else:
        fs = cgi.FieldStorage()
        url = fs.getvalue('url', "http://XIEJUN-DESKTOP:88")
    s = ''
    start_response('200 OK', [('Content-Type', 'text/plain;charset=' + ENCODING)])
    try:
        #host = url.split("/")[2]
        #if allowedHosts and not host in allowedHosts:
            #s += "Status: 502 Bad Gateway"
            #s += "Content-Type: text/plain"
            #s += "This proxy does not allow you to access that location (%s)." % (host,)
            
      
        if url.startswith("http://") or url.startswith("https://"):
            request = None
            response = None
            http = None
            urlobj = URL(url)
            if method == "POST":
                #length = int(environ["CONTENT_LENGTH"])
                headers = {"Content-Type": environ["CONTENT_TYPE"]}
                #body = sys.stdin.read(length)
                #r = urllib2.Request(url, body, headers)
                #request = urllib2.Request(url, post_data, headers=headers)
                #request = urllib2.Request(url, post_data, headers=headers)
                #y = urllib2.urlopen(request, data=post_data)
                http = HTTPClient.from_url(urlobj)
                #y = http.post(urlobj.request_uri, post_data, headers)
                g = gevent.spawn(http.post, urlobj.request_uri, post_data, headers)
                g.start()
                while not g.ready():
                    if g.exception:
                        break
                    gevent.sleep(0.1)
                response = g.value
            else:
                http = HTTPClient.from_url(urlobj)
                #y = http.get(urlobj.request_uri)
                g = gevent.spawn(http.get, urlobj.request_uri)
                g.start()
                while not g.ready():
                    if g.exception:
                        break
                    gevent.sleep(0.1)
                response = g.value
                
            
            if response:
                h = str(response.info())
                #if i.has_key("Content-Type"):
                    #print("Content-Type: %s" % (i["Content-Type"]))
                hh = eval(h)
                responseh = []
                for i in hh:
                    if i[0] in ['Content-Type', 'Date', 'Server', ]:
                        responseh.append(i)
                s = response.read()
                #response.release()
                http.close()
                responseh.append(('Content-Length', str(len(s))))
                #print(responseh)
                start_response('200 OK', responseh)
        else:
            #print("Content-Type: text/plain")
            s += "Illegal request."
    
    except Exception, E:
        s += "Status: 500 Unexpected Error"
        s += "Content-Type: text/plain"
        s += "Some unexpected error occurred. Error text was:%s" % E.message
    return [s]
    
            


def get_host_ip():
    ret = []
    ret.append('127.0.0.1')
    localIP = socket.gethostbyname(socket.gethostname())
    #print ("local ip:%s " % localIP)
    ipList = socket.gethostbyname_ex(socket.gethostname())
    for i in ipList:
        if i != localIP:
            #if isinstance(i, str):
                #print(re.findall('\d+\.\d+\.\d+\.\d+',i))
            if isinstance(i, list):
                for ii in i:
                    if len(re.findall('\d+\.\d+\.\d+\.\d+',ii))>0:
                        ret.append(ii)
            #print("external IP:%s" % i )
    return ret
           
        
def clear_tmp():
    tmp_dir = r'C:\Users\Jeffrey\AppData\Local\ESRI\Local Caches\MapCacheV1'
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    tmp_dir = r'C:\Users\Jeffrey\AppData\Local\ESRI\Local Caches\GlobeCache'
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

def get_scaleDenominator(zoomlist):
    #tileMatrixMaxX = tileMatrixMinX +  tileWidth * (scaleDenominator * pixelSize / metersPerUnit) * matrixWidth 
    #tileMatrixMinY = tileMatrixMaxY -  tileHeight * (scaleDenominator * pixelSize / metersPerUnit) * matrixHeight
    
    #tileWidth * (scaleDenominator * pixelSize / metersPerUnit) * matrixWidth    = tileMatrixMaxX - tileMatrixMinX   
    #tileHeight * (scaleDenominator * pixelSize / metersPerUnit) * matrixHeight  = tileMatrixMaxY - tileMatrixMinY
    
    #scaleDenominator * pixelSize / metersPerUnit     = (tileMatrixMaxX - tileMatrixMinX)/(tileWidth * matrixWidth)
    #scaleDenominator * pixelSize / metersPerUnit   = (tileMatrixMaxY - tileMatrixMinY)/(tileHeight * matrixHeight)
    
    #scaleDenominator * pixelSize  = metersPerUnit * (tileMatrixMaxX - tileMatrixMinX)/(tileWidth * matrixWidth)
    #scaleDenominator * pixelSize  = metersPerUnit * (tileMatrixMaxY - tileMatrixMinY)/(tileHeight * matrixHeight)
    
    #scaleDenominator   = metersPerUnit/pixelSize * (tileMatrixMaxX - tileMatrixMinX)/(tileWidth * matrixWidth)
    #scaleDenominator   = metersPerUnit/pixelSize * (tileMatrixMaxY - tileMatrixMinY)/(tileHeight * matrixHeight)
    
    metersPerUnit = float(gConfig['wmts']['metersPerUnit'])
    pixelSize = float(gConfig['wmts']['pixelSize'])
    tileWidth,tileHeight = 256.0, 256.0
    tileMatrixMinX, tileMatrixMaxX = (26.0, 102.0), (26.0, 104.0)
    tileMatrixMinY, tileMatrixMaxY = (24.0, 102.0), (26.0, 102.0)
    for i in zoomlist:
        #print('%d=%d' % (i , mapUtils.tiles_on_level(i)))
        #mapUtils.countDistanceFromLatLon()
        matrixHeight = matrixWidth = mapUtils.tiles_on_level(i)
        print('%d=%d' % (i , matrixHeight))
        #scaleDenominatorX   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxX , tileMatrixMinX) * 1000./(tileWidth * matrixWidth)
        #scaleDenominatorY   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxY , tileMatrixMinY) * 1000./(tileHeight * matrixHeight)
        #print('scaleDenominatorX=%f, scaleDenominatorY=%f' % (scaleDenominatorX, scaleDenominatorY))
        #scaleDenominator   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxY , tileMatrixMinY) * 1000. /(tileHeight * matrixHeight)
        scaleDenominator   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxY , tileMatrixMinY)  /(tileHeight * matrixHeight)
        print('scaleDenominator=%f' % scaleDenominator)
    

def ToGeographic(mercatorX_lon, mercatorY_lat):
    if abs(mercatorX_lon) < 180 and  abs(mercatorY_lat) < 90:
        return 0, 0
    if abs(mercatorX_lon) > 20037508.3427892 or abs(mercatorY_lat) > 20037508.3427892 :
        return 0, 0

    x = mercatorX_lon;
    y = mercatorY_lat;
    num3 = x / 6378137.0;
    num4 = num3 * 57.295779513082323;
    num5 = math.floor(float(num4 + 180.0) / 360.0)
    num6 = num4 - (num5 * 360.0)
    num7 = 1.5707963267948966 - (2.0 * math.atan(math.exp((-1.0 * y) / 6378137.0)))
    lon = num6
    lat = num7 * 57.295779513082323
    return lon, lat


def ToWebMercator(lon, lat):
    if abs(lon) > 180 or abs(lat) > 90:
        return 0, 0
    num = lon * 0.017453292519943295
    x = 6378137.0 * num
    a = lat * 0.017453292519943295

    mercatorX_lon = x
    mercatorY_lat = 3189068.5 * math.log((1.0 + math.sin(a)) / (1.0 - math.sin(a)))
    return mercatorX_lon, mercatorY_lat




            
def handle_requset_sync(obj):
    ret = {'result':''}
    if obj.has_key('area') and obj['area'] and len(obj['area'])>0:
        kmgd, kmgdgeo, kmgdgeotmp = db_util.create_sde_conn(obj['area'])
        if obj.has_key('arcpy'):
            if obj['arcpy'] == 'ListFeatureClasses':
                env.workspace = kmgdgeo
                l = []#arcpy.ListFeatureClasses(obj['feature_name'])
                ret['result'] = l
        elif obj.has_key('odbc'):
            if obj['odbc'] == 'TABLE_LINE':
                l = db_util.odbc_get_records('TABLE_LINE', '1=1', obj['area'])
                ret['result']= l
                
                    
            elif obj['odbc'] == 'TABLE_TOWER':
                l = db_util.odbc_get_records('TABLE_TOWER', '1=1', obj['area'])
                ret['result']= l
        elif obj.has_key('op'):
            if obj['op']=='download_task':
                condition = '1=1'
                if obj.has_key('team_id'):
                    condition += " AND team_id='%s'" % obj['team_id']
                l = db_util.odbc_get_records('VIEW_TASK_ITEM', condition, obj['area'])
                ret['result']= l
            #elif obj['op']=='get_latest_stamp':
                #f = '%Y-%m-%d %H:%M:%S'
                #if obj.has_key('format'):
                    #f  = obj['format']
                #ret['result']= db_util.get_latest_stamp(f, obj['area'])
            #elif obj['op']=='get_latest_3dd_stamp':
                #f = '%Y-%m-%d %H:%M:%S'
                #if obj.has_key('format'):
                    #f  = obj['format']
                #ret['result']= db_util.get_latest_3dd_stamp(f, obj['area'])
            #elif obj['op']=='analyse_buffer2d':
                #result, msg = db_util.analyse_buffer2d(kmgdgeo)
    else:
        print('unknown area')
        ret['result'] = ['']
    return ret




def soap_login():
    client = SoapClient(wsdl='%s?wsdl' % gConfig['webservice']['location'], namespace = gConfig['webservice']['namespace'], timeout=int(gConfig['webservice']['timeout']))
    response = client.login(username='', password='')
    result = response['Result']
    return result

def parse_thunder_counter_xml(xml):
    ret = []
    root = etree.fromstring(xml)
    if root:
        for Flash in root:
            obj = {}
            for child in Flash:
                obj[child.tag] = child.text
            ret.append(obj)
    return ret
    
    
def soap_GetFlashofDate(start_time, end_time):
    ret = {}
    try:
        client = SoapClient(wsdl='%s?wsdl' % gConfig['webservice']['location'], namespace = gConfig['webservice']['namespace'], timeout=int(gConfig['webservice']['timeout']))
        response = client.GetFlashofDate(in0=start_time, in1=end_time)
        result = response['Result']
        ret = parse_thunder_counter_xml(result)
    except:
        if hasattr(sys.exc_info()[1], 'message'):
            ret['err'] = sys.exc_info()[1].message
        if hasattr(sys.exc_info()[1], 'reason'):
            ret['err'] = str(sys.exc_info()[1].reason)
    return ret




def soap_GetFlashofEnvelope(start_time, end_time, lng1, lng2, lat1, lat2):
    ret = {}
    try:
        client = SoapClient(wsdl='%s?wsdl' % gConfig['webservice']['location'], namespace = gConfig['webservice']['namespace'], timeout=int(gConfig['webservice']['timeout']))
        response = client.GetFlashofEnvelope(in0=start_time, in1=end_time, in2=lng1, in3=lng2, in4=lat1, in5=lat2)
        result = response['Result']
        ret = parse_thunder_counter_xml(result)
    except:
        if hasattr(sys.exc_info()[1], 'message'):
            ret['err'] = sys.exc_info()[1].message
        if hasattr(sys.exc_info()[1], 'reason'):
            ret['err'] = str(sys.exc_info()[1].reason)
    return ret




    
    
    
def mainloop_single( port=None, enable_cluster=False, enable_ssl=False):
    gen_model_app_cache()
    server = None
    if port and not enable_cluster:
        if enable_ssl:
            print('listening at host 127.0.0.1, port %d with ssl crypted' % port)
            server = pywsgi.WSGIServer(('127.0.0.1', port), application, handler_class = WebSocketHandler, keyfile = gConfig['listen_port']['keyfile'], certfile = gConfig['listen_port']['certfile'])
        else:    
            print('listening at host 127.0.0.1, port %d' % port)
            server = pywsgi.WSGIServer(('127.0.0.1', port), application, handler_class = WebSocketHandler)
            #server = pywsgi.WSGIServer(('127.0.0.1', port), application)
        server.start()
        server.serve_forever()
    else:
        if enable_ssl:
            pport = port
            if not pport:
                pport = gConfig['listen_port']['ssl_port']
        else:
            pport = port
            if not pport:
                pport = gConfig['listen_port']['port']
            
        host_list = get_host_ip()
        admin = ''
        if enable_cluster:
            admin = 'cluster manager '
        print('%slistening at host %s, port %s' % (admin, str(host_list), str(pport)))
        
        
        servers = []
        #if gConfig['webservice']['enable']  in [u'true', u'TRUE']:
            #h, p = gConfig['webservice']['host'], int(gConfig['webservice']['port'])
            #print('listening webservice at http://%s:%d/webservice' % (h, p))
            #server = pywsgi.WSGIServer((h, p), get_wsapplication())
            #servers.append(server)
            #server.start()
        
        if len(host_list)>0:
            idx = 0
            if isinstance(pport, int):
                for i in host_list:
                    if enable_ssl:
                        server = pywsgi.WSGIServer((i, pport), application, handler_class = WebSocketHandler, keyfile = gConfig['listen_port']['keyfile'], certfile = gConfig['listen_port']['certfile'])
                    else:
                        server = pywsgi.WSGIServer((i, pport), application, handler_class = WebSocketHandler)
                    servers.append(server)
                        
                    if idx < len(host_list)-1:
                        server.start()
    
                    idx += 1
                servers[-1].serve_forever()
            elif isinstance(pport, unicode):
                for i in host_list:
                    if enable_ssl:
                        server = pywsgi.WSGIServer((i, int(pport)), application, handler_class = WebSocketHandler, keyfile = gConfig['listen_port']['keyfile'], certfile = gConfig['listen_port']['certfile'])
                    else:
                        server = pywsgi.WSGIServer((i, int(pport)), application, handler_class = WebSocketHandler)
                        #server = pywsgi.WSGIServer((i, int(pport)), application)
                    servers.append(server)
                    if idx < len(host_list)-1:
                        server.start()
    
                    idx += 1
                servers[-1].serve_forever()
            elif isinstance(pport, list):
                for i in host_list:
                    for j in pport:
                        if enable_ssl:
                            server = pywsgi.WSGIServer((i, int(j)), application, handler_class = WebSocketHandler, keyfile = gConfig['listen_port']['keyfile'], certfile = gConfig['listen_port']['certfile'])
                        else:    
                            server = pywsgi.WSGIServer((i, int(j)), application, handler_class = WebSocketHandler)
                        servers.append(server)
                        if idx < len(host_list) * len(pport)-1:
                            server.start()
                        
                        idx += 1
                servers[-1].serve_forever()
        else:
            print('wrong host or port in %s' % CONFIGFILE)
    return server


def mainloop_nginx(popen):
    while True:
        stdoutdata, stderrdata = popen.communicate()
        #if stdoutdata:
            #queue.put(stdoutdata)
        gevent.sleep(0.01)
    
    
def mainloop_manager(queue):
    while True:
        qget = q.get()
        if qget:
            print(qget)
        gevent.sleep(0.01)
    
    
    
def create_cluster():
    #global gConfig,  gClusterProcess
    conf = ''
    with open(gConfig['cluster']['nginx_conf_template']) as f:
        conf = f.read()
    rg = gConfig['cluster']['port_range']
    node_list = '\n'
    for port in range(int(rg[0]), int(rg[1]), int(rg[2])):
        node_list += '        server 127.0.0.1:%d;\n' % port
    listen_port = gConfig['listen_port']['port']
    access_log = gConfig['cluster']['nginx_log']
    host = get_host_ip()
    host.append('localhost')
    server_name = ' '.join(host)
    conf = conf.replace('[node_list]', str(node_list))
    conf = conf.replace('[listen_port]', str(listen_port))
    conf = conf.replace('[access_log]', str(access_log))
    conf = conf.replace('[server_name]', str(server_name))
    p = os.path.abspath(gConfig['cluster']['nginx_conf_template'])
    p = os.path.join(os.path.dirname(p), 'nginx.conf')
    #print(conf)
    with open(p, 'w') as f:
        f.write(conf)
    
    idx = 0
    for port in range(int(rg[0]), int(rg[1]), int(rg[2])):
        print('process%d is starting...' % idx)
        proc = Process(target=mainloop_single, args=(port, False, False))
        proc.start()
        #gClusterProcess[str(proc.pid)] = proc
        idx += 1
    print('nginx is starting...')
    popen = subprocess.Popen([os.path.abspath(gConfig['cluster']['nginx_exe']), '-c', p ])
    #g1 = gevent.spawn(mainloop_nginx, popen)
    
    
    
        
def get_pid_from_name(name):
    out = subprocess.check_output(['tasklist','/SVC'])
    #print(out)
    l = out.split('\r\n')
    findlist = []
    for i in l:
        arr = i.split(' ')
        for j in arr:
            if len(j)>0 and name in j:
                for k in arr:
                    if arr.index(k)==0:
                        continue
                    if len(k)>0:
                        try:
                            pid = int(k)
                            findlist.append(pid)
                            break
                        except:
                            continue
                break
            
    #print(findlist)
    if current_process().pid in findlist:
        findlist.remove(current_process().pid)
    return findlist
    
    
def kill_cluster():
    #global gClusterProcess
    print('kill nginx...')
    for pid in get_pid_from_name('nginx'):
        try:
            out = subprocess.check_output(['taskkill', '/F',  '/PID', str(pid), '/T'])
            print(out)
        except:
            pass

    for pid in get_pid_from_name('python'):
        print('kill python.exe[%s]...' % pid)
        out = subprocess.check_output(['taskkill', '/F',  '/PID', str(pid), '/T'])
        print(out)
    #for pid in gClusterProcess.keys():
        #print('kill python.exe[%s]...' % pid)
        #gClusterProcess[pid].terminate()
    print('kill done')
    
    
def create_self_signed_cert(cert_dir, year=10):
    from OpenSSL import crypto, SSL
 
    CERT_FILE = "ssl_certificate.crt"    
    KEY_FILE = "ssl_self_signed.key"
    if not os.path.exists(os.path.join(cert_dir, CERT_FILE))  or not os.path.exists(os.path.join(cert_dir, KEY_FILE)):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)
        cert = crypto.X509()
        cert.get_subject().C = "AQ"
        cert.get_subject().ST = "State"
        cert.get_subject().L = "City"
        cert.get_subject().O = "Company"
        cert.get_subject().OU = "Organization"
        cert.get_subject().CN = socket.gethostname()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(year*365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')
 
        with open(os.path.join(cert_dir, CERT_FILE), "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        with open(os.path.join(cert_dir, KEY_FILE), "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
 
        #create_self_signed_cert('.')
        print('Create SSL key and cert done')
    else:
        print('SSL key and cert already exist')
 
    
    
def gen_model_app_cache():
    global gConfig
    s = 'CACHE MANIFEST\n'
    s += '#' + gConfig['web_cache']['version'] + '\n'
    
    if gConfig['web_cache']['gltf_cache_enable'].lower() == u'true':
        modelsdir = os.path.join(STATICRESOURCE_DIR, 'gltf')
        if not os.path.exists(modelsdir):
            return
        l = os.listdir(modelsdir)
        for i in l:
            s += '/gltf/' + i + '\n'
    file_or_dir_cache = gConfig['web_cache']['file_or_dir_cache']        
    if len(file_or_dir_cache) > 0 :
        for root, dirs, files  in os.walk(STATICRESOURCE_DIR, topdown=False):
            for name in dirs:
                if name in file_or_dir_cache:
                    p = os.path.join(root, name)
                    for root1, dirs1, files1  in os.walk(p, topdown=False):
                        for name1 in files1:
                            p1 = os.path.join(root1, name1)
                            p1 = p1.replace(STATICRESOURCE_DIR, '').replace('\\', '/')
                            s += p1 + '\n'
            for name in files:
                if name in file_or_dir_cache:
                    p = os.path.join(root, name)
                    p = p.replace(STATICRESOURCE_DIR, '').replace('\\', '/')
                    s += p + '\n'
                
            
    s += 'NETWORK:\n'
    s += '*\n'
    with open(os.path.join(STATICRESOURCE_DIR, 'kmgd.appcache'), 'w') as f:
        f.write(s)
   

def extract_one_altitude(lng, lat):
    global gConfig
    ret = None
    exe_path = os.path.join(module_path(), 'gdal-bin', 'gdallocationinfo.exe')
    dem_path = gConfig['terrain']['dem_file']
    out = subprocess.check_output([exe_path, '-wgs84', "%s" % dem_path, "%f" % lng, "%f" % lat])
    t = 'Value:'
    if t in out:
        idx = out.index(t) + len(t)
        ret = float(out[idx:].strip())
    else:
        print('extract_altitude_from_dem:out of range!')
    return ret

def extract_many_altitudes(lnglatlist):
    ret = []
    for i in lnglatlist:
        if isinstance(i, dict) and i.has_key('lng') and i.has_key('lat'):
            ret.append({'lng':i['lng'], 'lat':i['lat'], 'alt':extract_one_altitude(i['lng'], i['lat'])})
    return ret


if __name__=="__main__":
    freeze_support()
    init_global()
    if len(sys.argv) == 1:
        if gConfig['cluster']['enable_cluster'] in ['true','True']:
            mainloop_single(int(gConfig['cluster']['manager_port']), True, False)
        else:
            if gConfig['listen_port']['enable_ssl'].lower() == u'true':
                port = 443
                try:
                    port = int(gConfig['listen_port']['ssl_port'])
                except:
                    pass
                mainloop_single(port, False, True)
            else:
                mainloop_single()
    elif len(sys.argv) == 2:
        folder = sys.argv[1]
        year = 10
        create_self_signed_cert(folder, year)
    elif len(sys.argv) == 3:
        folder = sys.argv[1]
        year = 10
        try:
            year = int(sys.argv[2])
        except:
            pass
        create_self_signed_cert(folder, year)
    #print(webservice_GetFlashofDate('',''))
    
    
class Win32ServiceHandler(object):

    # no parameters are permitted; all configuration should be placed in the
    # configuration file and handled in the Initialize() method
    def __init__(self):
        pass

    # called when the service is starting
    def Initialize(self, configFileName):
        self.server = None
        self.stopEvent = threading.Event()
        self.stopRequestedEvent = threading.Event()

    # called when the service is starting immediately after Initialize()
    # use this to perform the work of the service; don't forget to set or check
    # for the stop event or the service GUI will not respond to requests to
    # stop the service
    def Run(self):
        #self.stopRequestedEvent.wait()
        self.stopEvent.set()
        init_global()
        self.server = mainloop_single()

    # called when the service is being stopped by the service manager GUI
    def Stop(self):
        self.stopRequestedEvent.set()
        self.stopEvent.wait()
        if self.server:
            self.server.stop()
    
    
    
    
    
    