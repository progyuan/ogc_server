# -*- coding: utf-8 -*-
from __future__ import absolute_import
import codecs
import os, sys
import random
import json
import math
import decimal
import datetime
from gevent import pywsgi
import gevent
import gevent.fileobject
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
import cgi
import configobj
#from gmapcatcher import mapUtils
from lxml import etree

#from wfs_server import WFSServer
#import gmapcatcher.mapConf as mapConf
#import gmapcatcher.mapConst as mapConst
#from gmapcatcher.mapServices import MapServ
#from gmapcatcher.mapDownloader import MapDownloader

import pypyodbc
import uuid
import db_util
from module_locator import module_path

try:
    from geventhttpclient import HTTPClient, URL
except ImportError:
    pass

try:
    import geventwebsocket
except ImportError:
    pass

#try:
    #import arcpy
    #from arcpy import env
#except ImportError:
    #print('import arcpy error:%s' % sys.exc_info()[1])
#except RuntimeError:
    #print('import arcpy error:%s' % sys.exc_info()[1])



ENCODING = 'utf-8'
ENCODING1 = 'gb18030'
STATICRESOURCE_DIR = os.path.join(module_path(), 'static')
STATICRESOURCE_TPL_DIR = os.path.join(module_path(), 'template')
STATICRESOURCE_CSS_DIR = os.path.join(module_path(), 'static', 'css')
STATICRESOURCE_JS_DIR = os.path.join(module_path(), 'static', 'js')
STATICRESOURCE_IMG_DIR = os.path.join(module_path(), 'static', 'img')
INDEXPAGE = os.path.join(STATICRESOURCE_DIR, 'index.html')
CONFIGFILE = os.path.join(module_path(), 'ogc-config.ini')
UPLOAD_IMG_DIR = os.path.join(module_path(),'static','img','upload')
UPLOAD_PHOTOS_DIR = os.path.join(module_path(),'static','photos', 'upload')
UPLOAD_VOICE_DIR = os.path.join(module_path(),'static','voice')


gConfig = configobj.ConfigObj(CONFIGFILE, encoding='UTF8')
gTileCache = {}
gTerrainCache = {}
gGreenlets = {}
gClusterProcess = {}

try:
    gWFSService = WFSServer(CONFIGFILE)
    gWFSService.load()
    gMapConf = mapConf.MapConf()
    gCtxMap = MapServ(gMapConf)
    gMapDownloader = MapDownloader(gCtxMap, 1)
except:
    pass

def dec(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
    text, length = gb18030_decode(aStr, 'replace')
    return text
def enc(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
    text, length = gb18030_encode(aStr, 'replace')
    return text
def dec1(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING1)
    text, length = gb18030_decode(aStr, 'replace')
    return text
def enc1(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING1)
    text, length = gb18030_encode(aStr, 'replace')
    return text




def handle_static(aUrl):
    global gConfig
    statuscode, contenttype, body = '404 Not Found', 'text/plain;charset=' + ENCODING, '404 Not Found'
    surl = aUrl#.replace('//', '').replace('/', os.path.sep)
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

def handle_terrain_GetCapabilities(params, Start_response):
    Start_response('200 OK', [('Content-Type', 'text/xml;charset=' + ENCODING),('Access-Control-Allow-Origin', '*')])
    s = create_terrain_GetCapabilities()
    return [s]

def handle_wmts_GetCapabilities(params, Start_response):
    #clear_tmp()
    Start_response('200 OK', [('Content-Type', 'text/xml;charset=' + ENCODING),('Access-Control-Allow-Origin', '*')])
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
    Get= etree.SubElement(HTTP, ows + "Get", {href:gConfig['wmts']['url']})
    Constraint= etree.SubElement(Get, ows + "Constraint", name="GetEncoding")
    AllowedValues= etree.SubElement(Constraint, ows + "AllowedValues")
    Value= etree.SubElement(AllowedValues, ows + "Value").text = 'KVP'
    Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="GetTile")
    DCP= etree.SubElement(Operation, ows + "DCP")
    HTTP= etree.SubElement(DCP, ows + "HTTP")
    Get= etree.SubElement(HTTP, ows + "Get", {href:gConfig['wmts']['url']})
    
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

def create_terrain_GetCapabilities():
    upps = ['5.62500000000000000000',
        '2.81250000000000000000',
        '1.40625000000000000000',
        '0.70312500000000000000',
        '0.35156250000000000000',
        '0.17578125000000000000',
        '0.08789062500000000000',
        '0.04394531250000000000',
        '0.02197265625000000000',
        '0.01098632812500000000',
        '0.00549316406250000000',
        '0.00274658203125000000',
        '0.00137329101562500000',
        '0.00068664550781250000',
        '0.00034332275390625000',
        '0.00017166137695312500',
        '0.00008583068847656250',
        '0.00004291534423828125',
        '0.00002145767211914062',
        '0.00001072883605957031',
        '0.00000536441802978516',
        '0.00000268220901489258',
        '0.00000134110450744629']
        
    namespace = {'ows':"http://www.opengis.net/ows/1.1", 'xlink':"http://www.w3.org/1999/xlink", 'xsi':"http://www.w3.org/2001/XMLSchema-instance", 'gml':"http://www.opengis.net/gml", 'schemaLocation':"http://schemas.opengis.net/wmts/1.0/wmtsGetCapabilities_response.xsd"}
    ows = '{%s}' % namespace['ows']
    xlink = '{%s}' % namespace['xlink']
    root = etree.Element("TileMap",  version="1.0.0")
    
    Title = etree.SubElement(root, "Title").text = gConfig['terrain']['Title']
    Abstract = etree.SubElement(root, "Abstract").text = gConfig['terrain']['Abstract']
    SRS = etree.SubElement(root, "SRS").text = gConfig['terrain']['SRS']
    BoundingBox  = etree.SubElement(root, "BoundingBox",
                                    minx=gConfig['terrain']['BoundingBox']['minx'],
                                    miny=gConfig['terrain']['BoundingBox']['miny'],
                                    maxx=gConfig['terrain']['BoundingBox']['maxx'],
                                    maxy=gConfig['terrain']['BoundingBox']['maxy'],
                                    )
    Origin  = etree.SubElement(root, "Origin",
                                    x=gConfig['terrain']['Origin']['x'],
                                    y=gConfig['terrain']['Origin']['y'],
                                    )
    TileFormat  = etree.SubElement(root, "TileFormat",
                                    width=gConfig['terrain']['TileFormat']['width'],
                                    height=gConfig['terrain']['TileFormat']['height'],
                                    extension=gConfig['terrain']['TileFormat']['extension'],
                                    )
    TileFormat.set('mime-type', gConfig['mime_type']['.'+gConfig['terrain']['TileFormat']['extension']])
    
    TileSets = etree.SubElement(root, "TileSets" )
    
    max_zoom_level, min_zoom_level = int(gConfig['terrain']['max_zoom_level']), int(gConfig['terrain']['min_zoom_level'])
    if max_zoom_level < min_zoom_level:
        max_zoom_level, min_zoom_level =  min_zoom_level, max_zoom_level  
    zoomlist = range(min_zoom_level, max_zoom_level+1, 1)
    
    for i in zoomlist:
        href = '%sREQUEST=GetTile&level=%d' % (gConfig['terrain']['url'], i)
        TileSet = etree.SubElement(TileSets, "TileSet", href=href)
        TileSet.set('units-per-pixel',upps[i])
        TileSet.set('order',str(i))
        
    DataExtents = etree.SubElement(root, "DataExtents")
    for k in gConfig['terrain']['DataExtents'].keys():
        DataExtent = etree.SubElement(DataExtents, "DataExtent", 
                                      minx=gConfig['terrain']['DataExtents'][k]['minx'],
                                      miny=gConfig['terrain']['DataExtents'][k]['miny'],
                                      maxx=gConfig['terrain']['DataExtents'][k]['maxx'],
                                      maxy=gConfig['terrain']['DataExtents'][k]['maxy'],
                                      minlevel=gConfig['terrain']['DataExtents'][k]['minlevel'],
                                      maxlevel=gConfig['terrain']['DataExtents'][k]['maxlevel'],
                                      )
    
    
    
    #ret = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding=ENCODING).replace('&amp;','&')
    #ret = etree.tostring(root, pretty_print=True,  encoding=ENCODING).replace('&amp;','&')
    ret = etree.tostring(root, pretty_print=True,  encoding=ENCODING)
    print(ret)
    return ret
    
 
def download_callback(*args, **kwargs):
    #print(kwargs)
    #print(args)
    zoom, col, row = args[1][2], args[1][0], args[1][1]
    root = gConfig['wmts']['tiles_sat_root']
    p = os.path.join(root,
                    str(zoom),
                    str(col / 1024),
                    str(col % 1024),
                    str(row / 1024),
                    str(row % 1024) + gConfig['wmts']['format']
                    )
    print('Not exist %s, downloading...' % p)
    p = os.path.abspath(p)
    if os.path.exists(p):
        key = '%d-%d-%d' % (zoom, col, row)
        with open(p, 'rb') as f:
            f1 = gevent.fileobject.FileObjectThread(f, 'rb')
            gTileCache[key] = f1.read()
    
    
    #print(kwargs)
    
def handle_terrain_GetTile(params, Start_response):
    zoomlevel, row, col = None, None, None
    if params.has_key('level'):
        zoomlevel = int(params['level'])
    if params.has_key('y'):
        y = int(params['y'])
    if params.has_key('x'):
        x = int(params['x'])
    print('level=%d, x=%d, y=%d' % (zoomlevel, x, y))
    Start_response('200 OK', [('Content-Type',str(gConfig['mime_type']['.'+gConfig['terrain']['TileFormat']['extension']])), ('Access-Control-Allow-Origin', '*')])
    return ['']
    
def handle_wmts_GetTile(params, Start_response):
    picpath = os.path.join(STATICRESOURCE_IMG_DIR, gConfig['wmts']['missing'])
    root = gConfig['wmts']['tiles_sat_root']
    if params.has_key('TILEMATRIXSET'):
        if 'sat_tiles' in params['TILEMATRIXSET']:
            root = gConfig['wmts']['tiles_sat_root']
        elif 'map_tiles' in params['TILEMATRIXSET']:
            root = gConfig['wmts']['tiles_map_root']
    zoomlevel, row, col = None, None, None
    if params.has_key('TILEMATRIX'):
        #zoomlevel = int(params['TILEMATRIX'])
        #zoomlevel = int(params['TILEMATRIX'][params['TILEMATRIX'].index('_')+1:])
        if params['TILEMATRIX']=='undefined':
            zoomlevel = 1
        else:
            zoomlevel = int(params['TILEMATRIX'])
    if params.has_key('TILEROW'):
        if params['TILEROW']=='undefined':
            row = 0
        else:
            row = int(params['TILEROW'])
    if params.has_key('TILECOL'):
        if params['TILECOL']=='undefined':
            col = 0
        else:
            col = int(params['TILECOL'])
        
    
    
    #zoom = int(gConfig['wmts']['max_zoom_level'])-3-zoomlevel
    zoom = int(gConfig['wmts']['max_zoom_level'])-2-zoomlevel
    
        
    p = os.path.join(root,
                    str(zoom),
                    #str(zoomlevel),
                    str(col / 1024),
                    str(col % 1024),
                    str(row / 1024),
                    str(row % 1024) + gConfig['wmts']['format']
                    )
    p = os.path.abspath(p)
    #print(p)
    if os.path.exists(p):
        picpath = p
        key = '%d-%d-%d' % (zoom, col, row)
    else:
        #key = 'loading'
        key = '%d-%d-%d' % (zoom, col, row)
        #url = 
        #urlobj = URL(url)
        #http = HTTPClient.from_url(urlobj)
        #y = http.get(urlobj.request_uri)
        lyrtype = mapConst.LAYER_SAT
        gMapDownloader.query_tile((col, row, zoom),lyrtype, download_callback, conf=gMapConf)
        
        
    
    Start_response('200 OK', [('Content-Type',str(gConfig['mime_type'][gConfig['wmts']['format']])), ('Access-Control-Allow-Origin', '*')])
    
    
    if True:    
        if not gTileCache.has_key(key):
            try:
                with open(picpath, 'rb') as f:
                    f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                    gTileCache[key] = f1.read()
                #print(key + ' row=%d,col=%d' % (row, col))
            except:
                foundit = False
                #for i in range(3):
                    #if gTileCache.has_key(key):
                        #foundit = True
                        #break
                    #gevent.sleep(0.5)
                if not foundit:
                    key = 'missing'
                if not gTileCache.has_key(key):
                    picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['wmts']['missing'])
                    with open(picpath, 'rb') as f:
                        f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                        gTileCache[key] = f1.read()
                    print(key)
         
        #Start_response('200 OK', [('Content-Type',gConfig['mime_type'][gConfig['wmts']['format']]), ('Content-Length', str(len(ret)))])
    
    return [gTileCache[key]]

def handle_terrain(Env, Start_response):
    path_info = Env['PATH_INFO']
    print(path_info)
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
            print('reading %s...' % tilepath)
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
        
    
    Start_response('200 OK', [('Content-Type', 'application/octet-stream'),('Access-Control-Allow-Origin', '*')])
    return [ret]
    
    
def handle_arcgistile(Env, Start_response):
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
        if not gTileCache.has_key(key):
            try:
                #picpath = os.path.join(gConfig['wmts']['arcgis_tiles_root'], '_alllayers', 'L%02d' % zoom, 'R%08x' % row, 'C%08x%s' % (col, gConfig['wmts']['format']))
                picpath = os.path.join(gConfig['wmts']['arcgis_tiles_root'],   '%d' % zoom, '%d' % col, '%d%s' % (row, gConfig['wmts']['format']))
                print('%s, %s' % (key, picpath))
                with open(picpath, 'rb') as f:
                    f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                    gTileCache[key] = f1.read()
                
            except:
                foundit = False
                if not foundit:
                    key = 'missing'
                if not gTileCache.has_key(key):
                    picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['wmts']['missing'])
                    with open(picpath, 'rb') as f:
                        f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                        gTileCache[key] = f1.read()
        
        ret = gTileCache[key]
    else:
        ret = gTileCache['missing']
        
    Start_response('200 OK', [('Content-Type',str(gConfig['mime_type'][gConfig['wmts']['format']])), ('Access-Control-Allow-Origin', '*')])
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
    Start_response('200 OK', [('Content-Type', 'text/json;charset=' + ENCODING),('Access-Control-Allow-Origin', '*')])
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
    Start_response('200 OK', [('Content-Type', 'text/json;charset=' + ENCODING),('Access-Control-Allow-Origin', '*')])
    #if d.has_key('id') :
        #obj = TEST_DATA[d['id'][0]]
    #s = json.dumps(obj, ensure_ascii=False)
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
    
def handle_get_method(Env, Start_response):
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
            s = json.dumps(data, ensure_ascii=True)        
        elif d['geojson'][0]=='tracks':
            data = db_util.gen_geojson_tracks(area)
            s = json.dumps(data, ensure_ascii=True)        
        else:
            k = d['geojson'][0]
            p = os.path.abspath(STATICRESOURCE_DIR)
            if k == 'potential_risk':
                k = 'geojson_%s_%s' % (k, area)
            p = os.path.join(p, 'geojson', area, '%s.json' % k)
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
        s = json.dumps(data, ensure_ascii=True)
        
    if d.has_key('check_file'):
        fn = d['check_file'][0]
        dir_name = d['dir_name'][0]
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
        s = json.dumps(ret, ensure_ascii=True)
    if d.has_key('delete_file'):
        fn = d['delete_file'][0]
        dir_name = d['dir_name'][0]
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
        s = json.dumps(ret, ensure_ascii=True)
    if d.has_key('list_file_dir_name'):
        dir_name = d['list_file_dir_name'][0]
        del d['list_file_dir_name']
        ret["result"] = {}
        ret["result"]["dirs"] = [dir_name, ]
        p = os.path.join(UPLOAD_PHOTOS_DIR, dir_name)
        if os.path.exists(p):
            l = os.listdir(p)
            ret["result"]["files"] = l
        else:
            ret["result"]["files"] = []
        s = json.dumps(ret, ensure_ascii=True)
    if d.has_key('get_voice_files'):
        get_voice_files = d['get_voice_files'][0]
        ret["result"] = {}
        ret["result"]["ids"] = get_voice_file_all()
        s = json.dumps(ret, ensure_ascii=True)
    Start_response('200 OK', [('Content-Type', 'text/json;charset=' + ENCODING),('Access-Control-Allow-Origin', '*')])
    if len(ret.keys())==0:
        ret["result"] = "ok"
    if len(s)==0:
        s = json.dumps(ret, ensure_ascii=True)
    #return [str(current_process().pid) + '_' + s]
    #time.sleep(5.5)
    return [s]

def create_voice_dir():
    if not os.path.exists(UPLOAD_VOICE_DIR):
        os.mkdir(UPLOAD_VOICE_DIR)

def check_voice_file_by_fault(id):
    create_voice_dir()
    ret = False
    for fn in os.listdir(UPLOAD_VOICE_DIR):
        if id in fn:
            ret = True
            break
    return ret

def get_voice_file_latest(id):
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
    create_voice_dir()
    l = []
    for fn in os.listdir(UPLOAD_VOICE_DIR):
        if id in fn:
            l.append(fn)
    return l

def get_voice_file_all():
    s = set()
    for fn in os.listdir(UPLOAD_VOICE_DIR):
        p = os.path.join(UPLOAD_VOICE_DIR, fn)
        if os.path.isfile(p):
            arr = fn.split('@')
            if len(arr)==3:
                id = arr[1]
                s.add(id)
    return list(s)
    


def handle_upload_file(fileobj, qsdict):
    ret = False
    root = os.path.abspath(STATICRESOURCE_DIR)
    try:
        #task item picture
        if qsdict.has_key('pic_file_name'):
            fn = qsdict['pic_file_name'][0]
            dir_name = qsdict['dir_name'][0]
            pic_type = qsdict['pic_type'][0]
            p = os.path.join(root, 'photos')
            if not os.path.exists(p):
                os.mkdir(p)
            p = os.path.join(root, 'photos', 'upload')
            if not os.path.exists(p):
                os.mkdir(p)
            save_file_to(UPLOAD_PHOTOS_DIR, dir_name,  fn, fileobj)
            ret = True
        if qsdict.has_key('voice_file_name'):
            fn = qsdict['voice_file_name'][0]
            p = os.path.join(root, 'voice')
            if not os.path.exists(p):
                os.mkdir(p)
            save_file_to(UPLOAD_VOICE_DIR, None, fn, fileobj)
            ret = True
    except:
        print(sys.exc_info()[1])
    return ret
    
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
    
    
def handle_post_method(Env, Start_response):
    buf = Env['wsgi.input'].read()
    #forms, files = multipart.parse_form_data(Env)
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
    try:
        ds_plus = urllib.unquote_plus(buf)
        obj = json.loads(ds_plus)
    except:
        if len(querydict.keys())>0:
            is_upload = handle_upload_file(buf, querydict)
        obj = {}
    
    if obj.has_key('thunder_counter'):
        try:
            ret = handle_thunder_soap(obj)
        except:
            e = sys.exc_info()[1]
            if hasattr(e, 'message'):
                ret['err'] = e.message
            else:
                ret['err'] = str(e)
            
    elif obj.has_key('arcpy') \
       or obj.has_key('odbc') :
        ret = handle_requset_sync(obj)
    elif obj.has_key('op'):
        if obj.has_key('area') and obj['area'] and len(obj['area'])>0:
            if obj['op'] in ['save','delete','update']:
                ret = db_util.odbc_save_data_to_table(obj['table'], obj['op'], obj['data'], obj['line_id'], obj['start_tower_id'], obj['end_tower_id'], obj['area'])
            else:
                ret = handle_requset_sync(obj)
        else:
            ret["result"] = "unknown area"
    elif obj.has_key('tracks') and obj.has_key('area'):
        ret = db_util.save_tracks(obj['tracks'], obj['area'])
    else:
        if is_upload:
            ret["result"] = "ok"
        else:    
            ret["result"] = "unknown operation"
    if (isinstance(ret, list) and len(ret)==0) or (isinstance(ret, dict) and len(ret.keys())==0):
        ret["result"] = "ok"
    Start_response('200 OK', [('Content-Type', 'text/json;charset=' + ENCODING), ('Access-Control-Allow-Origin', '*')])
    #time.sleep(6)
    return [urllib.quote(json.dumps(ret))]

def handle_thunder_soap(obj):
    ret = {}
    if obj['thunder_counter'] == 'GetFlashofDate':
        ret = soap_GetFlashofDate(obj['start_time'], obj['end_time'])
    if obj['thunder_counter'] == 'GetFlashofEnvelope':
        ret = soap_GetFlashofEnvelope(obj['start_time'], obj['end_time'], obj['lng1'], obj['lng2'], obj['lat1'], obj['lat2'])
    return ret    

def dishen_ws_loop(aWebSocket, aHash):
    while True:
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
    elif path_info == '/wmts':
        return handle_wmts(environ, start_response)
    elif path_info == '/arcgistile':
        return handle_arcgistile(environ, start_response)
    #elif path_info == '/terrain':
    elif path_info[-8:] == '.terrain':
        return handle_terrain(environ, start_response)
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
            start_response(statuscode, [('Content-Type', contenttype), ('Access-Control-Allow-Origin', '*')])
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
                y = http.post(urlobj.request_uri, post_data, headers)
            else:
                http = HTTPClient.from_url(urlobj)
                y = http.get(urlobj.request_uri)
                #y = urllib2.urlopen(url)
            
            # print content type header
            h = str(y.info())
            #if i.has_key("Content-Type"):
                #print("Content-Type: %s" % (i["Content-Type"]))
            hh = eval(h)
            responseh = []
            for i in hh:
                if i[0] in ['Content-Type', 'Date', 'Server', ]:
                    responseh.append(i)
            
            
            #s = ''
            n = y.next()
            while n:
                s += n
                try:
                    n = y.next()
                except StopIteration:
                    break
            #print(s)
            #y.close()
            y.release()
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




    
    
    
def mainloop_single( port=None, enable_cluster=False):
    if port and not enable_cluster:
        print('listening at host 127.0.0.1, port %d' % port)
        try:
            server = pywsgi.WSGIServer(('127.0.0.1', port), application, handler_class = geventwebsocket.WebSocketHandler)
        except:
            server = pywsgi.WSGIServer(('127.0.0.1', port), application)
        server.start()
        server.serve_forever()
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
                    server = pywsgi.WSGIServer((i, pport), application, handler_class = geventwebsocket.WebSocketHandler)
                    servers.append(server)
                        
                    if idx < len(host_list)-1:
                        server.start()
    
                    idx += 1
                servers[-1].serve_forever()
            elif isinstance(pport, unicode):
                for i in host_list:
                    #server = pywsgi.WSGIServer((i, int(pport)), application, handler_class = geventwebsocket.WebSocketHandler)
                    server = pywsgi.WSGIServer((i, int(pport)), application)
                    servers.append(server)
                    if idx < len(host_list)-1:
                        server.start()
    
                    idx += 1
                servers[-1].serve_forever()
            elif isinstance(pport, list):
                for i in host_list:
                    for j in pport:
                        server = pywsgi.WSGIServer((i, int(j)), application, handler_class = geventwebsocket.WebSocketHandler)
                        servers.append(server)
                        if idx < len(host_list) * len(pport)-1:
                            server.start()
                        
                        idx += 1
                servers[-1].serve_forever()
        else:
            print('wrong host or port in %s' % CONFIGFILE)



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
        proc = Process(target=mainloop_single, args=(port, False))
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
    
    
    
    

if __name__=="__main__":
    freeze_support()
    if gConfig['cluster']['enable_cluster'] in ['true','True']:
        mainloop_single(int(gConfig['cluster']['manager_port']), True)
    else:
        mainloop_single()
    #print(webservice_GetFlashofDate('',''))
    
    
    
    
    
    
    
    