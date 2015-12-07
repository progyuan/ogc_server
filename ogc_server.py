# -*- coding: utf-8 -*-

import codecs
import os, sys
import copy
import random
import json
import math
import decimal
import datetime
import threading
import exceptions
import time
import base64
import md5
from gevent import socket
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
import uuid
import copy
from contextlib import contextmanager

from gevent import pywsgi
import gevent
import gevent.fileobject
from gevent.local import local
from gevent.subprocess import check_output

import pymongo
import gridfs
from bson.objectid import ObjectId
try:
    from geventhttpclient import HTTPClient, URL
except:
    print('geventhttpclient import error')
try:
    import geventwebsocket
    from geventwebsocket.handler import WebSocketHandler
except:
    print('geventwebsocket import error')
# try:
#     from pysimplesoap.server import SoapDispatcher, WSGISOAPHandler
#     from pysimplesoap.client import SoapClient, SoapFault
# except:
#     print('pysimplesoap import error')
try:
    from PIL import Image
except :
    print('PIL import error')
try:
    from lxml import etree
except:
    print('lxml import error')
try:
    import czml
except:
    print('czml import error')
try:
    from py3o.template import Template
except:
    print('import py3o.template error')

    

import werkzeug
from werkzeug.wrappers import Request, BaseResponse
from werkzeug.local import LocalProxy
from werkzeug.contrib.sessions import FilesystemSessionStore
from werkzeug.utils import dump_cookie, parse_cookie
from werkzeug.routing import Map, Rule, BaseConverter, ValidationError, HTTPException


from sessions import MongoClient, MongodbSessionStore
import configobj
import db_util
import bayes_util
from module_locator import module_path, dec, dec1, enc, enc1
from pydash import py_ as _
from collections import OrderedDict




ENCODING = None
ENCODING1 = None
STATICRESOURCE_DIR = None

    

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
gLoginToken = {}
gSecurityConfig = {}
gWebSocketsMap = {}
gTcpReconnectCounter = 0
gTcpSock = None
gHttpClient = {}
gFormTemplate = []

_SPECIAL = re.escape('()<>@,;:\\"/[]?={} \t')
_RE_SPECIAL = re.compile('[%s]' % _SPECIAL)
_QSTR = '"(?:\\\\.|[^"])*"' # Quoted string
_VALUE = '(?:[^%s]+|%s)' % (_SPECIAL, _QSTR) # Save or quoted string
_OPTION = '(?:;|^)\s*([^%s]+)\s*=\s*(%s)' % (_SPECIAL, _VALUE)
_RE_OPTION = re.compile(_OPTION) # key=value part of an Content-Type like header



gSessionStore = None

gRequests = None
gRequest = None
gProxyRequest = None
gJoinableQueue = None



class BooleanConverter(BaseConverter):
    def __init__(self, url_map, randomify=False):
        super(BooleanConverter, self).__init__(url_map)
        self.regex = '(?:true|false)'

    def to_python(self, value):
        return value == 'true'

    def to_url(self, value):
        return value and 'true' or 'false'


class Py3oItem(object):
    pass


gUrlMap = Map([
    Rule('/', endpoint='firstaccess'),
    Rule('/websocket', endpoint='handle_websocket'),
    #Rule('/auth_check/<username>/isnew/<bool:isnew>', endpoint='saveuser'),
    Rule('/get_salt', endpoint='get_salt'),
    Rule('/auth_check/<username>', endpoint='auth_check'),
    Rule('/auth_check', endpoint='auth_check'),
    Rule('/register/<username>/<password>', endpoint='user_add'),
    Rule('/register/<username>', endpoint='user_add'),
    Rule('/register', endpoint='user_add'),
    Rule('/unregister/<username>', endpoint='user_delete'),
    Rule('/unregister', endpoint='user_delete'),
    Rule('/login/<username>/<password>', endpoint='login'),
    Rule('/login/<username>', endpoint='login'),
    Rule('/login', endpoint='login'),
    Rule('/logout', endpoint='logout'),
    Rule('/reset_password/<username>/<password>', endpoint='reset_password'),
    Rule('/reset_password/<username>', endpoint='reset_password'),
    Rule('/reset_password', endpoint='reset_password'),
    Rule('/user_check', endpoint='user_check'),
    Rule('/user_query', endpoint='user_query'),
    Rule('/user_update', endpoint='user_update'),
    Rule('/function_add', endpoint='function_add'),
    Rule('/function_query', endpoint='function_query'),
    Rule('/function_update', endpoint='function_update'),
    Rule('/function_delete', endpoint='function_delete'),
    Rule('/role_add', endpoint='role_add'),
    Rule('/role_update', endpoint='role_update'),
    Rule('/role_query', endpoint='role_query'),
    Rule('/role_delete', endpoint='role_delete'),
    Rule('/role_template_save', endpoint='role_template_save'),
    Rule('/role_template_get', endpoint='role_template_get'),
    Rule('/workflow_add', endpoint='workflow_add'),
    Rule('/workflow_query', endpoint='workflow_query'),
    Rule('/workflow_query/<_id>', endpoint='workflow_query'),
    Rule('/workflow_update', endpoint='workflow_update'),
    Rule('/workflow_delete', endpoint='workflow_delete'),
    Rule('/workflow_delete/<_id>', endpoint='workflow_delete'),
    Rule('/workflow_template_add', endpoint='workflow_template_add'),
    Rule('/workflow_template_query', endpoint='workflow_template_query'),
    Rule('/workflow_template_query/<_id>', endpoint='workflow_template_query'),
    Rule('/workflow_template_update', endpoint='workflow_template_update'),
    Rule('/workflow_template_delete', endpoint='workflow_template_delete'),
    Rule('/workflow_template_delete/<_id>', endpoint='workflow_template_delete'),
    Rule('/workflow_form_fill', endpoint='workflow_form_fill'),
    Rule('/workflow_form_blank', endpoint='workflow_form_blank'),
    Rule('/user_add', endpoint='user_add'),
    Rule('/user_get', endpoint='user_get'),
    Rule('/all_user_get', endpoint='all_user_get'),
    Rule('/user_remove', endpoint='user_remove'),
    Rule('/group_add', endpoint='group_add'),
    Rule('/group_get', endpoint='group_get'),
    Rule('/group_update', endpoint='group_update'),
    Rule('/group_remove', endpoint='group_remove'),
    Rule('/user_group_get', endpoint='user_group_get'),
    Rule('/user_contact_get', endpoint='user_contact_get'),
    Rule('/chat_broadcast', endpoint='chat_broadcast'),
    Rule('/chat_log_query', endpoint='chat_log_query'),
    Rule('/chat_log_remove', endpoint='chat_log_remove'),
    Rule('/gridfs/upload', endpoint='gridfs_upload'),
    Rule('/gridfs/get', endpoint='gridfs_get'),
    Rule('/gridfs/get/<_id>', endpoint='gridfs_get'),
    Rule('/gridfs/get/<_id>/thumbnail/<width>/<height>', endpoint='gridfs_get'),
    Rule('/gridfs/query/<width>/<height>', endpoint='gridfs_query'),
    Rule('/gridfs/query/<width>/<height>/<limit>', endpoint='gridfs_query'),
    Rule('/gridfs/query/<width>/<height>/<limit>/<skip>', endpoint='gridfs_query'),
    Rule('/gridfs/delete', endpoint='gridfs_delete'),
    Rule('/gridfs/delete/<_id>', endpoint='gridfs_delete'),
    Rule('/antibird/get_equip_list', endpoint='get_equip_list'),
    Rule('/antibird/get_latest_records_by_imei', endpoint='get_latest_records_by_imei'),
    Rule('/antibird/equip_tower_mapping', endpoint='equip_tower_mapping'),
    Rule('/state_examination/save', endpoint='state_examination_save'),
    Rule('/state_examination/query', endpoint='state_examination_query'),
    Rule('/state_examination/query/line_names', endpoint='state_examination_query_line_names'),
    Rule('/state_examination/save_strategy_2009', endpoint='state_examination_save_strategy_2009'),
    Rule('/state_examination/save_strategy_2014', endpoint='state_examination_save_strategy_2014'),
    Rule('/state_examination/delete', endpoint='state_examination_delete'),
    Rule('/state_examination/delete/<_id>', endpoint='state_examination_delete'),
    Rule('/bayesian/query/graphiz', endpoint='bayesian_query_graphiz'),
    Rule('/bayesian/query/node', endpoint='bayesian_query_node'),
    Rule('/bayesian/query/predict', endpoint='bayesian_query_predict'),
    Rule('/bayesian/save/node', endpoint='bayesian_save_node'),
    Rule('/bayesian/delete/node', endpoint='bayesian_delete_node'),
    Rule('/bayesian/delete/node/<_id>', endpoint='bayesian_delete_node'),
    Rule('/bayesian/query/domains_range', endpoint='bayesian_query_domains_range'),
    Rule('/bayesian/save/domains_range', endpoint='bayesian_save_domains_range'),
    Rule('/bayesian/delete/domains_range', endpoint='bayesian_delete_domains_range'),
    Rule('/bayesian/delete/domains_range/<_id>', endpoint='bayesian_delete_domains_range'),
    Rule('/bayesian/reset/unit', endpoint='bayesian_reset_unit'),
    Rule('/distribute_network/query/network_nodes', endpoint='distribute_network_query_network_nodes'),
    Rule('/distribute_network/query/edges', endpoint='distribute_network_query_edges'),
    Rule('/distribute_network/query/network_names', endpoint='distribute_network_query_network_names'),
    Rule('/distribute_network/remove/network', endpoint='distribute_network_remove_network'),
    Rule('/distribute_network/save/network', endpoint='distribute_network_save_network'),
    Rule('/distribute_network/fault_position/position', endpoint='distribute_network_fault_position'),

], converters={'bool': BooleanConverter})





@contextmanager
def session_manager(environ):
    global gRequests, gRequest
    if gRequests is None:
        gRequests = local()
        gRequest = LocalProxy(lambda: gRequests.request)
    gRequests.request = Request(environ)
    yield
    gRequests.request = None



def init_global():
    global ENCODING, ENCODING1, STATICRESOURCE_DIR, STATICRESOURCE_CSS_DIR, STATICRESOURCE_JS_DIR, STATICRESOURCE_IMG_DIR, UPLOAD_PHOTOS_DIR, UPLOAD_VOICE_DIR
    global gConfig, gStaticCache, gGreenlets, gClusterProcess, gSecurityConfig, gJoinableQueue
    ENCODING = 'utf-8'
    ENCODING1 = 'gb18030'
    
    STATICRESOURCE_DIR = os.path.join(module_path(), 'static')
    
    #CONFIGFILE = os.path.join(module_path(), 'ogc-config.ini')
    #gConfig = configobj.ConfigObj(db_util.CONFIGFILE, encoding='UTF8')
    gConfig = db_util.gConfig
    
    if gConfig['web'].has_key('webroot') and len(gConfig['web']['webroot'])>0:
        if os.path.exists(gConfig['web']['webroot']):
            STATICRESOURCE_DIR = gConfig['web']['webroot']
        
    
    STATICRESOURCE_CSS_DIR = os.path.join(STATICRESOURCE_DIR, 'css')
    STATICRESOURCE_JS_DIR = os.path.join(STATICRESOURCE_DIR, 'js')
    STATICRESOURCE_IMG_DIR = os.path.join(STATICRESOURCE_DIR, 'img')
    UPLOAD_PHOTOS_DIR = os.path.join(STATICRESOURCE_DIR,'photos', 'upload')
    UPLOAD_VOICE_DIR = os.path.join(STATICRESOURCE_DIR,'voice')
    
    if gConfig['wsgi']['application'].lower() == 'authorize_platform':
        gSecurityConfig = db_util.mongo_find_one(gConfig['authorize_platform']['mongodb']['database'],
                                             gConfig['authorize_platform']['mongodb']['collection_security_config'],
                                             {},
                                             'authorize_platform'
                                             )
        if gSecurityConfig is None:
            gSecurityConfig = {}
    
    if gConfig['wsgi']['application'].lower() in ['pay_platform', 'fake_gateway_alipay']:
        gJoinableQueue = gevent.queue.JoinableQueue(maxsize=int(gConfig['pay_platform']['queue']['max_queue_size']))
        l = db_util.mongo_find(gConfig['pay_platform']['mongodb']['database'],
                                             gConfig['pay_platform']['mongodb']['collection_config'],
                                             {},
                                             0,
                                             'pay_platform'
                                             )
        for i in l:
            del i['_id']
            key = i.keys()[0]
            gSecurityConfig[key] = i[key]
        if len(l) == 0:
            gSecurityConfig = {}
    if gConfig['wsgi']['application'].lower() == 'chat_platform':
        gJoinableQueue = gevent.queue.JoinableQueue(maxsize=int(gConfig['chat_platform']['queue']['max_queue_size']))


def handle_static(environ, aUrl):
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
            if '/octet-stream' in gConfig['mime_type'][ext]:
                isBin = True
            if '/pdf' in gConfig['mime_type'][ext]:
                isBin = True
            if 'application/msword' in gConfig['mime_type'][ext] or 'application/vnd.' in gConfig['mime_type'][ext]:
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
    headers = {}
    headers['Content-Type'] = str(contenttype)
    return statuscode, headers, body

def handle_wfs_GetCapabilities(params):
    headers = {}
    headers['Content-Type'] = 'text/xml;charset=' + ENCODING
    s = create_wfs_GetCapabilities()
    return '200 OK', headers, s

def handle_wfs_GetFeature(params):
    headers = {}
    headers['Content-Type'] = 'text/xml;charset=' + ENCODING
    s = create_wfs_GetFeature()
    return '200 OK', headers, s


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


def handle_wmts_GetCapabilities(params={}):
    headers = {}
    mimetype = 'text/xml;charset=' + ENCODING
    s = ''
    if params.has_key('TILETYPE') and params.has_key('SUBTYPE'):
        s = create_wmts_GetCapabilities(params['TILETYPE'], params['SUBTYPE'])
    return mimetype, s
    
def create_wmts_GetCapabilities(tiletype, subtype):
    global gConfig
    #'''
    #namespace = {'ows':"http://www.opengis.net/ows/1.1", 'xlink':"http://www.w3.org/1999/xlink", 'xsi':"http://www.w3.org/2001/XMLSchema-instance", 'gml':"http://www.opengis.net/gml", 'schemaLocation':"http://schemas.opengis.net/wmts/1.0/wmtsGetCapabilities_response.xsd"}
    #ows = '{%s}' % namespace['ows']
    #xlink = '{%s}' % namespace['xlink']
    #root = etree.Element("Capabilities", xmlns="http://www.opengis.net/wmts/1.0", nsmap=namespace, version="1.0.0")
    ##ServiceIdentification
    #ServiceIdentification = etree.SubElement(root, ows + "ServiceIdentification")
    #Title = etree.SubElement(ServiceIdentification, ows + "Title").text = gConfig['webgis']['wmts']['ServiceIdentification_Title']
    #ServiceType = etree.SubElement(ServiceIdentification, ows + "ServiceType").text = 'OGC WMTS'
    #ServiceTypeVersion = etree.SubElement(ServiceIdentification, ows + "ServiceTypeVersion").text = '1.0.0'
    
    ##OperationsMetadata
    #OperationsMetadata = etree.SubElement(root, ows + "OperationsMetadata")
    #Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="GetCapabilities")
    #DCP= etree.SubElement(Operation, ows + "DCP")
    #HTTP= etree.SubElement(DCP, ows + "HTTP")
    #href = xlink + 'href'
    #Get= etree.SubElement(HTTP, ows + "Get", {href:gConfig['webgis']['wmts']['url'] + '?'})
    #Constraint= etree.SubElement(Get, ows + "Constraint", name="GetEncoding")
    #AllowedValues= etree.SubElement(Constraint, ows + "AllowedValues")
    #Value= etree.SubElement(AllowedValues, ows + "Value").text = 'KVP'
    #Operation= etree.SubElement(OperationsMetadata, ows + "Operation", name="GetTile")
    #DCP= etree.SubElement(Operation, ows + "DCP")
    #HTTP= etree.SubElement(DCP, ows + "HTTP")
    #Get= etree.SubElement(HTTP, ows + "Get", {href:gConfig['webgis']['wmts']['url'] + '?'})
    
    ##Contents
    #Contents = etree.SubElement(root, "Contents")
    #Layer = etree.SubElement(Contents, "Layer")
    #Title = etree.SubElement(Layer, ows + "Title").text = gConfig['webgis']['wmts']['Layer_Title']
    #WGS84BoundingBox = etree.SubElement(Layer, ows + "WGS84BoundingBox")
    #LowerCorner = etree.SubElement(WGS84BoundingBox, ows + "LowerCorner").text = gConfig['webgis']['wmts']['WGS84BoundingBox']['LowerCorner']
    #UpperCorner = etree.SubElement(WGS84BoundingBox, ows + "UpperCorner").text = gConfig['webgis']['wmts']['WGS84BoundingBox']['UpperCorner']
    #Identifier = etree.SubElement(Layer, ows + "Identifier").text = gConfig['webgis']['wmts']['Layer_Identifier']
    #Style = etree.SubElement(Layer, "Style", isDefault="true")
    #Title = etree.SubElement(Style, ows + "Title" ).text = 'Default'
    #Identifier = etree.SubElement(Style, ows + "Identifier" ).text = 'default'
    #Format = etree.SubElement(Layer, "Format" ).text = gConfig['mime_type'][gConfig['wmts']['format']]
    #TileMatrixSetLink = etree.SubElement(Layer, "TileMatrixSetLink" )
    #TileMatrixSet = etree.SubElement(TileMatrixSetLink, "TileMatrixSet" ).text = gConfig['webgis']['wmts']['TileMatrixSet']
        
    #TileMatrixSet = etree.SubElement(Contents, "TileMatrixSet")
    #Identifier = etree.SubElement(TileMatrixSet, ows + "Identifier" ).text = gConfig['webgis']['wmts']['TileMatrixSet']
    #SupportedCRS = etree.SubElement(TileMatrixSet, ows + "SupportedCRS" ).text = gConfig['webgis']['wmts']['SupportedCRS']
    #WellKnownScaleSet = etree.SubElement(TileMatrixSet, "WellKnownScaleSet" ).text = gConfig['webgis']['wmts']['WellKnownScaleSet']
    
    #max_zoom_level, min_zoom_level = int(gConfig['wmts']['max_zoom_level']), int(gConfig['webgis']['wmts']['min_zoom_level'])
    #if max_zoom_level < min_zoom_level:
        #max_zoom_level, min_zoom_level =  min_zoom_level, max_zoom_level  
    ##zoomlist = range(max_zoom_level,min_zoom_level, -1)
    #zoomlist = range(min_zoom_level, max_zoom_level+1, 1)
    
    
    #pixelSize = float(gConfig['webgis']['wmts']['pixelSize'])
    #tileWidth,tileHeight = int(gConfig['webgis']['wmts']['TileWidth']), int(gConfig['webgis']['wmts']['TileHeight'])
    #minLonLat,maxLonLat  = (float(gConfig['webgis']['wmts']['minLonLat'][0]), float(gConfig['webgis']['wmts']['minLonLat'][1])), (float(gConfig['webgis']['wmts']['maxLonLat'][0]), float(gConfig['webgis']['wmts']['maxLonLat'][1]))
    ##tileMatrixMinX, tileMatrixMaxX = (26.0, 102.0), (26.0, 104.0)
    ##tileMatrixMinY, tileMatrixMaxY = (24.0, 102.0), (26.0, 102.0)
    #tileMatrixMinX, tileMatrixMaxX = (maxLonLat[1], minLonLat[0]), (maxLonLat[1], maxLonLat[0])
    #tileMatrixMinY, tileMatrixMaxY = (minLonLat[1], minLonLat[0]), (maxLonLat[1], minLonLat[0])
    
    #metersPerUnit = 0.0
    #if gConfig['webgis']['wmts'].has_key('metersPerUnit'):
        #metersPerUnit = float(gConfig['webgis']['wmts']['metersPerUnit'])
    #else:
        #metersPerUnitX = mapUtils.countDistanceFromLatLon(tileMatrixMaxX , tileMatrixMinX)/2*1000
        ##print('metersPerUnitX=%f' % metersPerUnitX)
        #metersPerUnitY = mapUtils.countDistanceFromLatLon(tileMatrixMaxY , tileMatrixMinY)/2*1000
        ##print('metersPerUnitY=%f' % metersPerUnitY)
        #metersPerUnit = metersPerUnitY 
    ##print('metersPerUnit=%f' % metersPerUnit)
    #for i in zoomlist:
        ##matrixHeight = matrixWidth = mapUtils.tiles_on_level(i)
        #matrixHeight = matrixWidth = mapUtils.tiles_on_level(max_zoom_level-(i-1))
        ##print('%d=%d' % (i , matrixHeight))
        ##scaleDenominatorX   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxX , tileMatrixMinX) * 1000./(tileWidth * matrixWidth)
        ##scaleDenominatorY   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxY , tileMatrixMinY) * 1000./(tileHeight * matrixHeight)
        ##print('scaleDenominatorX=%f, scaleDenominatorY=%f' % (scaleDenominatorX, scaleDenominatorY))
        ##scaleDenominator   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxY , tileMatrixMinY) * 1000. /(tileHeight * matrixHeight)
        #scaleDenominator   = metersPerUnit/pixelSize * mapUtils.countDistanceFromLatLon(tileMatrixMaxY , tileMatrixMinY)  /(tileHeight * matrixHeight)
        #TileMatrix = etree.SubElement(TileMatrixSet, "TileMatrix" )
        ##Identifier = etree.SubElement(TileMatrix, ows + "Identifier" ).text = "ynsat_" + str(i)
        #Identifier = etree.SubElement(TileMatrix, ows + "Identifier" ).text = str(i)
        #ScaleDenominator = etree.SubElement(TileMatrix, "ScaleDenominator" ).text = '%.8f' % scaleDenominator
        #TopLeftCorner = etree.SubElement(TileMatrix, "TopLeftCorner" ).text = ['webgis']['wmts']['TopLeftCorner']
        #TileWidth = etree.SubElement(TileMatrix, "TileWidth" ).text = str(tileWidth)
        #TileHeight = etree.SubElement(TileMatrix, "TileHeight" ).text = str(tileHeight)
        #MatrixWidth = etree.SubElement(TileMatrix, "MatrixWidth" ).text = str(matrixWidth)
        #MatrixHeight = etree.SubElement(TileMatrix, "MatrixHeight" ).text = str(matrixHeight)
    
    #ret = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding=ENCODING)
    #print(ret)
    #return ret
    #'''
    ret = '''<?xml version="1.0" encoding="UTF-8"?>
<Capabilities xmlns="http://www.opengis.net/wmts/1.0"
xmlns:ows="http://www.opengis.net/ows/1.1"
xmlns:xlink="http://www.w3.org/1999/xlink"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:gml="http://www.opengis.net/gml" xsi:schemaLocation="http://www.opengis.net/wmts/1.0 http://schemas.opengis.net/wmts/1.0/wmtsGetCapabilities_response.xsd"
version="1.0.0">
<ows:ServiceIdentification>
  <ows:Title>%s</ows:Title>
  <ows:ServiceType>OGC WMTS</ows:ServiceType>
  <ows:ServiceTypeVersion>1.0.0</ows:ServiceTypeVersion>
</ows:ServiceIdentification>
<ows:OperationsMetadata>
  <ows:Operation name="GetCapabilities">
    <ows:DCP>
      <ows:HTTP>
        <ows:Get xlink:href="http://%s:%s/wmts?REQUEST=getcapabilities">
          <ows:Constraint name="GetEncoding">
            <ows:AllowedValues>
              <ows:Value>KVP</ows:Value>
            </ows:AllowedValues>
          </ows:Constraint>
        </ows:Get>
      </ows:HTTP>
    </ows:DCP>
  </ows:Operation>
  <ows:Operation name="GetTile">
    <ows:DCP>
      <ows:HTTP>
        <ows:Get xlink:href="http://%s:%s/wmts?REQUEST=gettile">
          <ows:Constraint name="GetEncoding">
            <ows:AllowedValues>
              <ows:Value>KVP</ows:Value>
            </ows:AllowedValues>
          </ows:Constraint>
        </ows:Get>
      </ows:HTTP>
    </ows:DCP>
  </ows:Operation>
</ows:OperationsMetadata>
<Contents>
  <Layer>
    <ows:Title>%s</ows:Title>
    <ows:WGS84BoundingBox>
      <ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
      <ows:UpperCorner>180.0 90.0</ows:UpperCorner>
    </ows:WGS84BoundingBox>
    <ows:Identifier>%s</ows:Identifier>
    <Style isDefault="true">
      <ows:Identifier>_null</ows:Identifier>
    </Style>
    <Format>%s</Format>
    <TileMatrixSetLink>
      <TileMatrixSet>%s</TileMatrixSet>
    </TileMatrixSetLink> 
  </Layer>

  <TileMatrixSet>
    <ows:Identifier>%s</ows:Identifier>
    <ows:SupportedCRS>urn:ogc:def:crs:EPSG::900913</ows:SupportedCRS>
    <TileMatrix>
      <ows:Identifier>0</ows:Identifier>
      <ScaleDenominator>5.590822639508929E8</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>1</MatrixWidth>
      <MatrixHeight>1</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>1</ows:Identifier>
      <ScaleDenominator>2.7954113197544646E8</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>2</MatrixWidth>
      <MatrixHeight>2</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>2</ows:Identifier>
      <ScaleDenominator>1.3977056598772323E8</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>4</MatrixWidth>
      <MatrixHeight>4</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>3</ows:Identifier>
      <ScaleDenominator>6.988528299386162E7</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>8</MatrixWidth>
      <MatrixHeight>8</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>4</ows:Identifier>
      <ScaleDenominator>3.494264149693081E7</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>16</MatrixWidth>
      <MatrixHeight>16</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>5</ows:Identifier>
      <ScaleDenominator>1.7471320748465404E7</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>32</MatrixWidth>
      <MatrixHeight>32</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>6</ows:Identifier>
      <ScaleDenominator>8735660.374232702</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>64</MatrixWidth>
      <MatrixHeight>64</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>7</ows:Identifier>
      <ScaleDenominator>4367830.187116351</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>128</MatrixWidth>
      <MatrixHeight>128</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>8</ows:Identifier>
      <ScaleDenominator>2183915.0935581755</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>256</MatrixWidth>
      <MatrixHeight>256</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>9</ows:Identifier>
      <ScaleDenominator>1091957.5467790877</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>512</MatrixWidth>
      <MatrixHeight>512</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>10</ows:Identifier>
      <ScaleDenominator>545978.7733895439</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>1024</MatrixWidth>
      <MatrixHeight>1024</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>11</ows:Identifier>
      <ScaleDenominator>272989.38669477194</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>2048</MatrixWidth>
      <MatrixHeight>2048</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>12</ows:Identifier>
      <ScaleDenominator>136494.69334738597</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>4096</MatrixWidth>
      <MatrixHeight>4096</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>13</ows:Identifier>
      <ScaleDenominator>68247.34667369298</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>8192</MatrixWidth>
      <MatrixHeight>8192</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>14</ows:Identifier>
      <ScaleDenominator>34123.67333684649</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>16384</MatrixWidth>
      <MatrixHeight>16384</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>15</ows:Identifier>
      <ScaleDenominator>17061.836668423246</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>32768</MatrixWidth>
      <MatrixHeight>32768</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>16</ows:Identifier>
      <ScaleDenominator>8530.918334211623</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>65536</MatrixWidth>
      <MatrixHeight>65536</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>17</ows:Identifier>
      <ScaleDenominator>4265.4591671058115</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>131072</MatrixWidth>
      <MatrixHeight>131072</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>18</ows:Identifier>
      <ScaleDenominator>2132.7295835529058</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>262144</MatrixWidth>
      <MatrixHeight>262144</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>19</ows:Identifier>
      <ScaleDenominator>1066.3647917764529</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>524288</MatrixWidth>
      <MatrixHeight>524288</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>20</ows:Identifier>
      <ScaleDenominator>533.1823958882264</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>1048576</MatrixWidth>
      <MatrixHeight>1048576</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>21</ows:Identifier>
      <ScaleDenominator>266.5911979441132</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>2097152</MatrixWidth>
      <MatrixHeight>2097152</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>22</ows:Identifier>
      <ScaleDenominator>133.2955989720566</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>4194304</MatrixWidth>
      <MatrixHeight>4194304</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>23</ows:Identifier>
      <ScaleDenominator>66.6477994860283</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>8388608</MatrixWidth>
      <MatrixHeight>8388608</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>24</ows:Identifier>
      <ScaleDenominator>33.32389974301415</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>16777216</MatrixWidth>
      <MatrixHeight>16777216</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>25</ows:Identifier>
      <ScaleDenominator>16.661949871507076</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>33554432</MatrixWidth>
      <MatrixHeight>33554432</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>26</ows:Identifier>
      <ScaleDenominator>8.330974935753538</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>67108864</MatrixWidth>
      <MatrixHeight>67108864</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>27</ows:Identifier>
      <ScaleDenominator>4.165487467876769</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>134217728</MatrixWidth>
      <MatrixHeight>134217728</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>28</ows:Identifier>
      <ScaleDenominator>2.0827437339383845</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>268435456</MatrixWidth>
      <MatrixHeight>268435456</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>29</ows:Identifier>
      <ScaleDenominator>1.0413718669691923</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>536870912</MatrixWidth>
      <MatrixHeight>536870912</MatrixHeight>
    </TileMatrix>
    <TileMatrix>
      <ows:Identifier>30</ows:Identifier>
      <ScaleDenominator>0.5206859334845961</ScaleDenominator>
      <TopLeftCorner>-2.003750834E7 2.0037508E7</TopLeftCorner>
      <TileWidth>256</TileWidth>
      <TileHeight>256</TileHeight>
      <MatrixWidth>1073741824</MatrixWidth>
      <MatrixHeight>1073741824</MatrixHeight>
    </TileMatrix>
  </TileMatrixSet>
</Contents>
</Capabilities>''' % (
            str(tiletype),
            str(gConfig['webgis']['wmts']['host']), 
            str(gConfig['webgis']['wmts']['port']),
            str(gConfig['webgis']['wmts']['host']), 
            str(gConfig['webgis']['wmts']['port']),
            str(subtype),
            str(subtype),
            str(gConfig['mime_type'][gConfig['webgis'][tiletype][subtype]['mimetype']]),
            str(subtype),
            str(subtype),
                   )
#<ServiceMetadataURL xlink:href="http://%s:%s/wmts?REQUEST=getcapabilities"/>
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
    
    
def handle_wmts_GetTile(params):
    global gConfig
    mimetype, ret = None, None
    tiletype = 'webgis/tiles'
    arr = tiletype.split('/')
    subtype = None
    if params.has_key('TILEMATRIXSET'):
        subtype = params['TILEMATRIXSET']
    level, y, x = None, None, None
    if params.has_key('TILEMATRIX'):
        level = int(params['TILEMATRIX'])
    if params.has_key('TILEROW'):
        y = int(params['TILEROW'])
    if params.has_key('TILECOL'):
        x = int(params['TILECOL'])
    if subtype is not None and level is not None and y is not None and x is not None:
        tilepath = '%d/%d/%d%s' % (level, x, y, str(gConfig['webgis'][arr[1]][subtype]))
        d = {}
        d['x'] = str(x)
        d['y'] = str(y)
        d['level'] = str(level)
        mimetype, ret = db_util.gridfs_tile_find(tiletype, subtype, tilepath, d)
    return mimetype, ret

def handle_tiles(environ):
    global gConfig, gTileCache
    global STATICRESOURCE_IMG_DIR
    def get_blank_tile(image_type):
        blank_tile = ''
        picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['webgis']['tiles'][image_type]['missing'])
        with open(picpath, 'rb') as f:
            f1 = gevent.fileobject.FileObjectThread(f, 'rb')
            blank_tile = f1.read()
        return blank_tile
    headers = {}    
    #path_info = environ['PATH_INFO']
    #d = cgi.parse(None, environ)
    querydict, buf = get_querydict_by_GET_POST(environ)
    ret = None
    mimetype = 'image/png'
    image_type = None
    #key = path_info.replace('/tiles/','')
    if querydict.has_key('image_type') and querydict.has_key('x') and querydict.has_key('y') and querydict.has_key('level'):
        image_type = querydict['image_type']
        x, y, level = querydict['x'], querydict['y'], querydict['level']
        tilepath = '%s/%s/%s%s' % (level, x, y, gConfig['webgis']['tiles'][image_type]['mimetype'])
        if not gTileCache.has_key(image_type):
            gTileCache[image_type] = {}
        if not gTileCache[image_type].has_key('missing'):
            gTileCache[image_type]['missing'] = get_blank_tile(image_type)
        if gTileCache[image_type].has_key(tilepath):
            ret = gTileCache[image_type][tilepath]
        else:
            try:
                mimetype, ret = db_util.gridfs_tile_find('webgis/tiles', image_type, tilepath, querydict)
                gTileCache[image_type][tilepath] = ret
            except:
                print(sys.exc_info())
                ret = gTileCache[image_type]['missing']
    else:
        if image_type:
            if not gTileCache.has_key(image_type):
                gTileCache[image_type] = {}
            if not gTileCache[image_type].has_key('missing'):
                gTileCache[image_type]['missing'] = get_blank_tile(image_type)
            ret = gTileCache[image_type]['missing']
        else:
            ret = get_blank_tile('arcgis_sat')
    if ret is None:
        ret = gTileCache[image_type]['missing']
    headers['Content-Type'] = mimetype
    return '200 OK', headers, ret
        
            

def handle_terrain(environ):
    global gConfig, gTileCache
    path_info = environ['PATH_INFO']
    #d = cgi.parse(None, environ)
    querydict, buf = get_querydict_by_GET_POST(environ)
    ret = None
    headers = {}
    mimetype = str('application/octet-stream')
    key = path_info.replace('/terrain/','')
    terrain_type = 'quantized_mesh'
    if querydict.has_key('terrain_type'):
        terrain_type = querydict['terrain_type']
    
    if not gTileCache.has_key(terrain_type):
        gTileCache[terrain_type] = {}
    if gTileCache[terrain_type].has_key(key):
        ret = gTileCache[terrain_type][key]
    else:
        tilepath = key
        if tilepath == 'layer.json':
            mimetype, ret = db_util.gridfs_tile_find('webgis/terrain', terrain_type, tilepath, querydict)
            gTileCache[terrain_type][key] = ret
            headers['Content-Type'] = mimetype
            return '200 OK', headers, ret
        else:
            print('tilepath:%s' % tilepath)
            mimetype, ret = db_util.gridfs_tile_find('webgis/terrain', terrain_type, tilepath, querydict)
            if ret:
                gTileCache[terrain_type][key] = ret
                headers['Content-Type'] = mimetype
                return '200 OK', headers, ret
            else:
                if not gTileCache[terrain_type].has_key('missing'):
                    print('reading mongo blank_terrain...')
                    tilepath = gConfig['webgis']['terrain'][terrain_type]['missing'] #'0/0/0.terrain'
                    mimetype, ret = db_util.gridfs_tile_find('webgis/terrain', terrain_type, tilepath, querydict)
                    gTileCache[terrain_type]['missing'] = ret
                ret = gTileCache[terrain_type]['missing']
                
    headers['Content-Type'] = mimetype
    return '200 OK', headers, ret

        
def handle_terrain1(environ):
    global gConfig,  gMapTileCache, gSatTileCache, gTerrainCache
    path_info = environ['PATH_INFO']
    #d = cgi.parse(None, environ)
    ret = None
    headers = {}
    key = path_info.replace('/terrain/','')
    if gTerrainCache.has_key(key):
        ret = gTerrainCache[key]
    else:
        arr = key.split('/')
        tilepath = gConfig['webgis']['terrain']['tiles_dir']
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
                with open(gConfig['webgis']['terrain']['blank_terrain'], 'rb') as f:
                    f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                    ret = f1.read()
                gTerrainCache['missing'] = ret
    headers['Content-Type'] = 'application/octet-stream'
    return '200 OK', headers, ret
    
    
def handle_arcgistile(environ):
    global gConfig, gMapTileCache, gSatTileCache
    global STATICRESOURCE_IMG_DIR
    ret = None
    headers = {}
    dd = cgi.parse(None, environ)
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
                picpath = os.path.join(gConfig['webgis']['wmts']['arcgis_tiles_root'],   '%d' % zoom, '%d' % col, '%d%s' % (row, gConfig['webgis']['wmts']['format']))
                print('%s, %s' % (key, picpath))
                with open(picpath, 'rb') as f:
                    f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                    gSatTileCache[key] = f1.read()
                
            except:
                foundit = False
                if not foundit:
                    key = 'missing'
                if not gSatTileCache.has_key(key):
                    picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['webgis']['wmts']['missing'])
                    with open(picpath, 'rb') as f:
                        f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                        gSatTileCache[key] = f1.read()
        
        ret = gSatTileCache[key]
    elif d.has_key('is_esri') :
        key = environ['PATH_INFO'].replace('/arcgistile/','')
        if not gSatTileCache.has_key(key):
            try:
                #picpath = os.path.join(gConfig['webgis']['wmts']['arcgis_tiles_root'], '_alllayers', 'L%02d' % zoom, 'R%08x' % row, 'C%08x%s' % (col, gConfig['webgis']['wmts']['format']))
                picpath = os.path.join(gConfig['webgis']['wmts']['arcgis_tiles_root'],   key)
                print('%s, %s' % (key, picpath))
                with open(picpath, 'rb') as f:
                    f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                    gSatTileCache[key] = f1.read()
                
            except:
                foundit = False
                if not foundit:
                    key = 'missing'
                if not gSatTileCache.has_key(key):
                    picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['webgis']['wmts']['missing'])
                    with open(picpath, 'rb') as f:
                        f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                        gSatTileCache[key] = f1.read()
        
        ret = gSatTileCache[key]
    else:
        if not gSatTileCache.has_key('missing'):
            picpath = os.path.join(STATICRESOURCE_IMG_DIR,  gConfig['webgis']['wmts']['missing'])
            with open(picpath, 'rb') as f:
                f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                gSatTileCache['missing'] = f1.read()
        ret = gSatTileCache['missing']
        
    headers['Content-Type'] = str(gConfig['mime_type'][gConfig['webgis']['wmts']['format']])
    return '200 OK', headers, ret   
        
    
def handle_wmts(environ):
    dd = cgi.parse(None, environ)
    d = {}
    headers = {}
    mimetype, ret = None, None
    for k in dd.keys():
        d[k.upper()] = dd[k][0]
    ret, mimetype = None, None
    if d.has_key('REQUEST') :
        d['REQUEST'] = d['REQUEST'].replace('/1.0.0/WMTSCapabilities.xml', '')
        if d.has_key('TILETYPE'):
            d['TILETYPE'] = d['TILETYPE'].replace('/1.0.0/WMTSCapabilities.xml', '')
        if d.has_key('SUBTYPE'):
            d['SUBTYPE'] = d['SUBTYPE'].replace('/1.0.0/WMTSCapabilities.xml', '')
        if d['REQUEST'].lower() in ['getcapabilities']:
            mimetype, ret = handle_wmts_GetCapabilities(d)
        elif d['REQUEST'].lower() in ['gettile']:
            mimetype, ret = handle_wmts_GetTile(d)
    headers['Content-Type'] = mimetype
    return '200 OK', headers, ret

    
def handle_cluster(environ):
    global gConfig
    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    if int(environ['SERVER_PORT'])==int(gConfig['cluster']['manager_port']) and gConfig['cluster']['enable_cluster'] in ['true','True']:
        op = ''
        if environ['PATH_INFO']=='/create_cluster':
            if len(get_pid_from_name('nginx'))==0:
                op = 'create ok'
                create_cluster()
        elif environ['PATH_INFO']=='/kill_cluster':
            op = 'kill ok'
            kill_cluster()
        #print(environ)
        return '200 OK', headers, json.dumps({'result':op})
    else:
        return '200 OK', headers, json.dumps({'result':'cluster is disabled or not by manager'})
    
    
    
def handle_test(environ):
    s = '测试OK'
    headers = {}
    d = cgi.parse(None, environ)
    #print(d)
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    #print(s)
    return '200 OK', headers, s
    
    
def get_condition_from_dict(dct):
    cond = '1=1'            
    for k in dct.keys():
        if k in ['voltage', 'line_id', 'id', 'tower_id', 'start_tower_id', 'end_tower_id', 'model_code', 'side', 'position']:
            if k == 'side':
                if dct[k]=='1':
                    cond += " AND %s='%s'" % (k, u'正')
                elif dct[k]=='0':
                    cond += " AND %s='%s'" % (k, u'反')
            else:    
                cond += " AND %s='%s'" % (k, dct[k])
        else:
            cond += " AND %s=%s" % (k, dct[k])
    #print(cond)
    return cond

def mongo_get_condition_from_dict(dct):
    ret = {}            
    for k in dct.keys():
        ret[k] =  dct[k][0]
    print(ret)
    return ret
    
def handle_get_method(environ):
    global ENCODING
    global STATICRESOURCE_DIR, UPLOAD_PHOTOS_DIR, UPLOAD_VOICE_DIR
    global gConfig
    ret = {}
    s = ''
    querydict, buf = get_querydict_by_GET_POST(environ)
    
    isgrid = False
    area = ''
    data = {}
    headers = {}
    clienttype = 'default'
    if querydict.has_key('clienttype'):
        clienttype = querydict['clienttype']
    if querydict.has_key('grid'):
        isgrid = True
    if querydict.has_key('area'):
        area = querydict['area']
    # if querydict.has_key('geojson'):
    #     if querydict['geojson']=='line_towers':
    #         data = db_util.gen_geojson_by_lines(area)
    #         s = json.dumps(data, ensure_ascii=True, indent=4)
    #     elif querydict['geojson']=='tracks':
    #         data = db_util.gen_geojson_tracks(area)
    #         s = json.dumps(data, ensure_ascii=True, indent=4)
    #     else:
    #         k = querydict['geojson']
    #         p = os.path.abspath(STATICRESOURCE_DIR)
    #         if k == 'potential_risk':
    #             k = 'geojson_%s_%s' % (k, area)
    #         p = os.path.join(p, 'geojson', area, '%s.json' % k)
    #         #print(p)
    #         if os.path.exists(p):
    #             with open(p) as f:
    #                 f1 = gevent.fileobject.FileObjectThread(f, 'r')
    #                 s = f1.read()
    #         else:
    #             p = os.path.abspath(STATICRESOURCE_DIR)
    #             p = os.path.join(p, 'geojson', '%s.json' % k)
    #             if os.path.exists(p):
    #                 with open(p) as f:
    #                     f1 = gevent.fileobject.FileObjectThread(f, 'r')
    #                     s = f1.read()
    #
    #
    #
    # if querydict.has_key('table'):
    #     table = querydict['table']
    #     dbtype = 'odbc'
    #     if querydict.has_key('dbtype'):
    #         dbtype = querydict['dbtype']
    #
    #     if dbtype == 'pg':
    #         data = db_util.pg_get_records(table, get_condition_from_dict(querydict))
    #     else:
    #         data = db_util.odbc_get_records(table, get_condition_from_dict(querydict), area)
    #         if table in ['TABLE_TOWER']:
    #             if querydict.has_key('line_id'):
    #                 data = db_util.odbc_get_sorted_tower_by_line(querydict['line_id'], area)
    #
    #     if isgrid:
    #         data = {'Rows':data}
    #     s = json.dumps(data, ensure_ascii=True, indent=4)
        
    # if querydict.has_key('check_file'):
    #     fn = querydict['check_file']
    #     dir_name = querydict['dir_name']
    #     ret["result"] = {}
    #     ret["result"]["filename"] = fn
    #     if dir_name == 'voice':
    #         if check_voice_file_by_fault(fn):
    #             ret["result"]["exist"] = "true"
    #         else:
    #             ret["result"]["exist"] = "false"
    #     else:
    #         if os.path.exists(os.path.join(UPLOAD_PHOTOS_DIR, dir_name, fn)):
    #             ret["result"]["exist"] = "true"
    #         else:
    #             ret["result"]["exist"] = "false"
    #     s = json.dumps(ret, ensure_ascii=True, indent=4)
    # if querydict.has_key('delete_file'):
    #     fn = querydict['delete_file']
    #     dir_name = querydict['dir_name']
    #     ret["result"] = {}
    #     ret["result"]["filename"] = fn
    #     if dir_name == 'voice':
    #         pl = get_voice_file_by(fn)
    #         if len(pl)>0:
    #             for i in pl:
    #                 p = os.path.join(UPLOAD_VOICE_DIR, fn)
    #                 if os.path.exists(p):
    #                     os.remove(p)
    #             ret["result"]["removed"] = "true"
    #         else:
    #             ret["result"]["removed"] = "false"
    #
    #     else:
    #         p = os.path.join(UPLOAD_PHOTOS_DIR, dir_name, fn)
    #         if os.path.exists(p):
    #             os.remove(p)
    #             ret["result"]["removed"] = "true"
    #         else:
    #             ret["result"]["removed"] = "false"
    #     s = json.dumps(ret, ensure_ascii=True, indent=4)
    # if querydict.has_key('list_file_dir_name'):
    #     dir_name = querydict['list_file_dir_name']
    #     ret["result"] = {}
    #     ret["result"]["dirs"] = [dir_name, ]
    #     p = os.path.join(UPLOAD_PHOTOS_DIR, dir_name)
    #     if os.path.exists(p):
    #         l = os.listdir(p)
    #         ret["result"]["files"] = l
    #     else:
    #         ret["result"]["files"] = []
    #     s = json.dumps(ret, ensure_ascii=True, indent=4)
    # if querydict.has_key('get_voice_files'):
    #     get_voice_files = querydict['get_voice_files']
    #     ret["result"] = {}
    #     ret["result"]["ids"] = get_voice_file_all()
    #     s = json.dumps(ret, ensure_ascii=True, indent=4)
    if querydict.has_key('op'):
        op = querydict['op']
        if op == "gridfs":
            ret = db_util.gridfs_find(querydict, str(gConfig['wsgi']['application']))
            if isinstance(ret, tuple) and ret[0] and ret[1]:
                headers['Content-Type'] = str(ret[0])
                if querydict.has_key('attachmentdownload'):
                    headers['Content-Disposition'] = 'attachment;filename="' + enc(ret[2]) + '"'
                s = ret[1]
                return '200 OK', headers , s
            if isinstance(ret, list):
                s = json.dumps(ret, ensure_ascii=True, indent=4)
        elif op == "gridfs_delete":
            try:
                db_util.gridfs_delete(querydict, str(gConfig['wsgi']['application']))
                ret = ''
            except:
                ret["result"] = sys.exc_info()[1].message
            s = json.dumps(ret, ensure_ascii=True, indent=4)
        
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    if isinstance(ret, dict) and len(ret.keys())==0:
        ret["result"] = "ok"
    if isinstance(s, list) and len(s)==0:
        s = json.dumps(ret, ensure_ascii=True, indent=4)
    return '200 OK', headers, s

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

def handle_upload_file(querydict, buf):
    global STATICRESOURCE_DIR, UPLOAD_PHOTOS_DIR, UPLOAD_VOICE_DIR
    ret = False
    # root = os.path.abspath(STATICRESOURCE_DIR)
    try:
        if querydict.has_key('db'):
            db_util.gridfs_save(querydict, querydict['filename'], buf)
            ret = True
    except Exception,e:
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

def geojson_to_czml(aList):
    cz = czml.CZML()
    for i in aList:
        if i.has_key('properties') and i['properties'].has_key('id'):
            packet = czml.CZMLPacket(id=i['properties']['id'])
            #tower
            if i['properties'].has_key('tower_code'):
                packet = czml.CZMLPacket(id=i['properties']['id'], name=i['properties']['tower_name'])
                packet.position = czml.Position(cartographicDegrees = [i['geometry']['coordinates'][0], i['geometry']['coordinates'][1], i['geometry']['coordinates'][2],])
                packet.point = czml.Point(show=True, color={'rgba': [255, 255, 0, 255]}, pixelSize=10, outlineColor={'rgba': [0, 0, 0, 255]}, outlineWidth=1)
                #packet.label = czml.Label(text=i['properties']['tower_name'], show=True, scale=0.5)
                packet.description = i['properties']['tower_name']
                #packet.billboard = czml.Billboard(image='http://localhost:88/img/tower.png')
                cz.append(packet)
    return cz
        
    
def handle_post_method(environ):
    global ENCODING
    global gRequest
    
    querydict, buf = get_querydict_by_GET_POST(environ)
    ret = {}
    is_upload = False
    is_mongo = False
    use_czml = False
    get_extext = False
    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    
    if buf is not None:
        try:
            is_upload = handle_upload_file(querydict, buf)
        except:
            pass
    
                
    if querydict.has_key('db') and querydict.has_key('collection'):
        is_mongo = True
        dbname = querydict['db']
        collection = querydict['collection']
        action = None
        data = None
        if querydict.has_key('action'):
            action = querydict['action']
            del querydict['action']
        if querydict.has_key('data'):
            data = querydict['data']
            del querydict['data']
        if querydict.has_key('use_czml') and querydict['use_czml']:
            use_czml = True
            del querydict['use_czml']
        if querydict.has_key('get_extext') and querydict['get_extext']:
            get_extext = True
            del querydict['get_extext']
        del querydict['db']
        del querydict['collection']
        if action:
            if 'markdown_' in action or u'markdown_' in action:
                l = db_util.mongo_action(dbname, collection, action, data, querydict, 'markdown')
            else:
                l = db_util.mongo_action(dbname, collection, action, data, querydict)
        else:
            l = db_util.mongo_find(dbname, collection, querydict)
        if get_extext:
            l = db_util.find_extent(l)
        if use_czml:
            l = geojson_to_czml(l)
        if isinstance(l, list) and len(l) >= 0:
            ret = l
        elif isinstance(l, dict) and len(l.keys()) > 0:
            ret = l
        elif isinstance(l, czml.CZML):
            headers['Content-Type'] = 'text/json;charset=' + ENCODING
            return '200 OK', headers, enc(l.dumps())
        #else:
            #ret["result"] = "%s.%s return 0 record" % (dbname, collection)
    #else:
        #ret["result"] = "unknown query operation"
    
        
        
    if not is_mongo:
        if querydict.has_key('thunder_counter'):
            try:
                ret = handle_thunder_soap(querydict)
            except:
                e = sys.exc_info()[1]
                if hasattr(e, 'message'):
                    ret['result'] = e.message
                else:
                    ret['result'] = str(e)
                
        elif querydict.has_key('op'):
            if querydict.has_key('area') and querydict['area'] and len(querydict['area'])>0:
                if querydict['op'] in ['save','delete','update']:
                    ret = db_util.odbc_save_data_to_table(querydict['table'], querydict['op'], querydict['data'], querydict['line_id'], querydict['start_tower_id'], querydict['end_tower_id'], querydict['area'])
                else:
                    ret = handle_requset_sync(querydict)
            elif querydict['op'] in ['alt','height'] :
                if querydict.has_key('lng') and querydict.has_key('lat') and isinstance(querydict['lng'], float) and isinstance(querydict['lat'], float):
                    ret = db_util.extract_one_altitude(querydict['lng'], querydict['lat'])
                if querydict.has_key('data')  and isinstance(querydict['data'], list):
                    ret = db_util.extract_many_altitudes(querydict['data'])
            else:
                ret["result"] = "unknown area"
        elif querydict.has_key('tracks') and querydict.has_key('area'):
            ret = db_util.save_tracks(querydict['tracks'], querydict['area'])
        elif querydict.has_key('mobile_action') and querydict.has_key('area') and querydict.has_key('data'):
            ret = db_util.mobile_action(querydict['mobile_action'], querydict['area'], querydict['data'])
        
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
    #time.sleep(6)
    #print(ret)
    
    return '200 OK', headers, json.dumps(ret, ensure_ascii=True, indent=4)

    
    
# def handle_login(environ):
#     global ENCODING
#     global gRequest
#     buf = environ['wsgi.input'].read()
#     ret = None
#     try:
#         ds_plus = urllib.unquote_plus(buf)
#         obj = json.loads(dec(ds_plus))
#         if obj.has_key(u'db') and obj.has_key(u'collection'):
#             is_mongo = True
#             dbname = obj[u'db']
#             collection = obj[u'collection']
#             action = None
#             data = None
#             if obj.has_key(u'action'):
#                 action = obj[u'action']
#                 del obj[u'action']
#             if obj.has_key(u'data'):
#                 data = obj[u'data']
#                 del obj[u'data']
#             if obj.has_key(u'url'):
#                 del obj[u'url']
#             if obj.has_key(u'redirect'):
#                 del obj[u'redirect']
#             del obj[u'db']
#             del obj[u'collection']
#             if action:
#                 ret = db_util.mongo_action(dbname, collection, action, data, obj)
#     except:
#         raise
#     return ret

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




def check_session(environ, request, session_store):
    global gConfig
    def set_cookie(key, value):
        secure = False
        if gConfig['listen_port']['enable_ssl'].lower() == 'true':
            secure = True
        max_age = int(gConfig['authorize_platform']['session']['session_age'])
        cookie = ('Set-Cookie', dump_cookie(key, value, domain=str(gConfig['authorize_platform']['session']['session_domain']), max_age=max_age, secure=secure))
        return cookie
    
    sid = request.cookies.get('authorize_platform_session_id')
    cookie = None
    is_expire = False
    sess = None
    

    if sid is None or len(sid)==0:
        request.session = session_store.new({})
        #session_store.save(request.session)
        is_expire = True
        cookie = set_cookie('authorize_platform_session_id', request.session.sid )
        sess = request.session
    else:
        request.session = session_store.get(sid)
        if request.session:
            cookie = set_cookie('authorize_platform_session_id', request.session.sid)
            session_store.save_if_modified(request.session)
        else:
            cookie = set_cookie('authorize_platform_session_id', '')
            is_expire = True
        sess = request.session
    return sess, cookie, is_expire



def get_token_from_env(environ):
    global gConfig, gLoginToken
    cookie = parse_cookie(environ)
    session_id = None
    ret = None
    if cookie.has_key('session_id'):
        session_id = cookie['session_id']
        if gLoginToken.has_key(session_id):
            ret = gLoginToken[session_id]
    return session_id, ret

def get_session_from_env(environ):
    global gSessionStore
    cookie = parse_cookie(environ)
    session_id = None
    ret = None
    if cookie.has_key('session_id'):
        session_id = cookie['session_id']
        ret = gSessionStore.get(session_id)
    return ret

def get_userinfo_from_env(environ):
    global gConfig, gLoginToken
    cookie = parse_cookie(environ)
    session_id = None
    ret = None
    if cookie.has_key('session_id'):
        session_id = cookie['session_id']
        if gLoginToken.has_key(session_id):
            ret = gLoginToken[session_id]
    return session_id, ret
    



def get_sign_alipay(sign_data):
    global gConfig
    ret = ''
    text = sign_data + gConfig['pay_platform']['alipay']['partner_key']
    text = enc_by_code(gConfig['pay_platform']['alipay']['input_charset'], text)
    if (gConfig['pay_platform']['alipay']['sign_type']).lower() == 'md5':
        md5.digest_size = 32
        ret = md5.new(text).hexdigest()
    return ret

def check_sign_alipay(input_charset, signature, sign_type, original_data):
    global gConfig
    text = original_data + gConfig['pay_platform']['alipay']['partner_key']
    text = enc_by_code(str(input_charset), text)
    ret = ''
    if str(sign_type).lower() == 'md5':
        md5.digest_size = 32
        ret = md5.new(text).hexdigest()
    return ret == str(signature)
    
def build_query_string(data={}):
    ret = ''
    keys = data.keys()
    keys.sort()
    for k in keys:
        ret += '%s=%s' % (k, data[k])
        if keys.index(k) < len(keys) - 1:
            ret += '&'
    return ret
        
def get_pay_record_by_id(querydict):
    ret = None
    if querydict['pay_channel'] == 'alipay':
        out_trade_no = querydict['out_trade_no']
        db_util.mongo_init_client('pay_platform')
        client = db_util.gClientMongo['pay_platform']
        db = client['pay']
        if 'pay_log' in db.collection_names(False):
            collection = db['pay_log']
            ret = collection.find_one({"out_trade_no":out_trade_no})
    return ret
    
    
def refund_alipay(querydict):
    global ENCODING
    global gConfig,  gSecurityConfig, gJoinableQueue
    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    statuscode = '200 OK'
    body = ''
    href = str(gConfig['pay_platform']['alipay']['submit_gateway'])
    sign_data = {}
    sign_data['_input_charset'] = gConfig['pay_platform']['alipay']['input_charset']
    sign_data['partner'] = gConfig['pay_platform']['alipay']['partner_id']
    sign_data['service'] = 'refund_fastpay_by_platform_pwd'
    sign_data['refund_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sign_data['batch_no'] = datetime.datetime.now().strftime("%Y%m%d") + str(ObjectId())
    sign_data['batch_num'] = '1'
    querydict['refund_date'] = sign_data['refund_date']
    querydict['batch_no'] = sign_data['batch_no']
    querydict['batch_num'] = int(sign_data['batch_num'])
    if len(gConfig['pay_platform']['alipay']['return_url'])>0:
        sign_data['return_url'] = gConfig['pay_platform']['alipay']['return_url']
    if len(gConfig['pay_platform']['alipay']['error_notify_url'])>0:
        sign_data['error_notify_url'] =  gConfig['pay_platform']['alipay']['error_notify_url']
    if len(gConfig['pay_platform']['alipay']['notify_url'])>0:
        sign_data['notify_url'] = gConfig['pay_platform']['alipay']['notify_url']
    
    rec = get_pay_record_by_id(querydict)
    if rec:
        if rec.has_key('error_code'):
            body = json.dumps({'result':'refund_fail_pay_has_fail' }, ensure_ascii=True, indent=4)
        else:
            if rec.has_key('seller_email') \
               and rec.has_key('trade_no') :
                trade_no = rec['trade_no']
                sign_data['seller_email'] = rec['seller_email']
                querydict['seller_email'] = sign_data['seller_email']
                querydict['trade_no'] = trade_no
                detail_data = '%s^%.2f^%s' % (trade_no, float(querydict['refund_fee']), querydict['refund_desc'] )
                sign_data['detail_data'] = detail_data
            if not rec.has_key('seller_email'):
                body = json.dumps({'result':'refund_fail_seller_email_required' }, ensure_ascii=True, indent=4)
            if not rec.has_key('trade_no'):
                body = json.dumps({'result':'refund_fail_trade_no_required' }, ensure_ascii=True, indent=4)
    else:
        body = json.dumps({'result':'refund_fail_pay_trade_not_found:%s' % querydict['out_trade_no']}, ensure_ascii=True, indent=4)
        
    
    if len(body) == 0:
        #querydict['refund_result'] = 'refund_sending_to_alipay'
        querydict['refund_result'] = 'refund_adding_to_queue'
        querydict['refund_fee'] = float(querydict['refund_fee'])
        g = gevent.spawn(update_refund_log, querydict['out_trade_no'], querydict)
        #g1 = sign_and_send_alipay('post', href, sign_data)
        #g1.join()
        #resp = g1.value
        #s = resp.read()
        #print('refund response: [%s]' % dec(s))
        #body = json.dumps({'result':'refund_sending_to_alipay'}, ensure_ascii=True, indent=4)
        
        try:
            gJoinableQueue.put({'thirdpay':'alipay', 'method':'post', 'url':href, 'data':sign_data})
        except gevent.queue.Full:
            body = json.dumps({'result':'refund_err_queue_full'}, ensure_ascii=True, indent=4)
        body = json.dumps({'result':'refund_adding_to_queue'}, ensure_ascii=True, indent=4)
        
    return statuscode, headers, body
    
    
    
def pay_alipay(querydict):
    global ENCODING
    global gConfig,  gSecurityConfig, gJoinableQueue
    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    statuscode = '200 OK'
    body = ''
    href = str(gConfig['pay_platform']['alipay']['submit_gateway'])
    if not href[-1:] == '?':
        href += '?'
    sign_data = {}
    sign_data['_input_charset'] = gConfig['pay_platform']['alipay']['input_charset']
    sign_data['total_fee'] = querydict['total_fee']
    sign_data['out_trade_no'] = querydict['out_trade_no']
    sign_data['partner'] = gConfig['pay_platform']['alipay']['partner_id']
    sign_data['payment_type']  =  '1'
    sign_data['seller_email'] = querydict['seller_email']
    sign_data['buyer_email'] =  querydict['buyer_email']
    sign_data['service'] = 'create_direct_pay_by_user'
    sign_data['subject'] = querydict['subject']
    if len(gConfig['pay_platform']['alipay']['return_url'])>0:
        sign_data['return_url'] = gConfig['pay_platform']['alipay']['return_url']
    if len(gConfig['pay_platform']['alipay']['error_notify_url'])>0:
        sign_data['error_notify_url'] =  gConfig['pay_platform']['alipay']['error_notify_url']
    if len(gConfig['pay_platform']['alipay']['notify_url'])>0:
        sign_data['notify_url'] = gConfig['pay_platform']['alipay']['notify_url']
    
    #querydict['trade_status'] = 'pay_sending_to_alipay'
    querydict['trade_status'] = 'pay_adding_to_queue'
    querydict['total_fee'] = float(querydict['total_fee'])
    
    if querydict.has_key('defaultbank'):
        if gSecurityConfig['alipay']['bank_code'].has_key(querydict['defaultbank']):
            sign_data['defaultbank'] = querydict['defaultbank']
            sign_data['paymethod'] = 'bankPay'
        else:
            body = json.dumps({'result':'pay_fail_wrong_bank_code'}, ensure_ascii=True, indent=4)
            return statuscode, headers, body
        
    if gConfig['pay_platform']['alipay']['need_ctu_check'].lower() == 'true':
        sign_data['need_ctu_check'] = 'Y'
    if gConfig['pay_platform']['alipay']['anti_fishing'].lower() == 'true':
        sign_data['anti_phishing_key'] = ''
        sign_data['exter_invoke_ip'] = ''
        
    g = gevent.spawn(update_pay_log, querydict['out_trade_no'], querydict)
    #g1 = sign_and_send_alipay('post', href, sign_data)
    #body = json.dumps({'result':'pay_sending_to_alipay'}, ensure_ascii=True, indent=4)
    try:
        gJoinableQueue.put({'thirdpay':'alipay','method':'post', 'url':href, 'data':sign_data})
    except gevent.queue.Full:
        body = json.dumps({'result':'pay_err_queue_full'}, ensure_ascii=True, indent=4)
    body = json.dumps({'result':'pay_adding_to_queue'}, ensure_ascii=True, indent=4)
    return statuscode, headers, body
    

def handle_refund(environ):
    global ENCODING
    global gConfig
    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    statuscode = '200 OK'
    body = ''
    querydict = {}
    if environ.has_key('QUERY_STRING') and len(environ['QUERY_STRING'])>0:
        querystring = environ['QUERY_STRING']
        querystring = urllib.unquote_plus(querystring)
        querydict = urlparse.parse_qs(dec(querystring))
        d = {}
        for k in querydict.keys():
            d[k] = querydict[k][0]
        querydict = d
    
    try:
        buf = environ['wsgi.input'].read()
        ds_plus = urllib.unquote_plus(buf)
        d = json.loads(dec(ds_plus))
        for k in d.keys():
            querydict[k] = d[k]
    except:
        pass
            
    if len(querydict.keys()) > 0:        
        if querydict.has_key('out_trade_no') and len(querydict['out_trade_no'])>0\
           and querydict.has_key('pay_channel') and len(querydict['pay_channel'])>0\
           and querydict.has_key('refund_fee') and len(querydict['refund_fee'])>0\
           and querydict.has_key('refund_desc') and len(querydict['refund_desc'])>0:
            if querydict['pay_channel'] == 'alipay':
                refund_fee = 0
                try:
                    refund_fee = float(querydict['refund_fee'])
                except:
                    body = json.dumps({'result':'refund_fail_refund_fee_wrong_format'}, ensure_ascii=True, indent=4)
                    refund_fee = 0
                if '^' in querydict['refund_desc'] \
                   or '#' in querydict['refund_desc'] \
                   or '|' in querydict['refund_desc'] \
                   or '$' in querydict['refund_desc'] \
                   or len(querydict['refund_desc'])>128 :
                    refund_fee = 0
                    body = json.dumps({'result':'refund_fail_refund_desc_wrong_charactor'}, ensure_ascii=True, indent=4) 
                if refund_fee>0:
                    statuscode, headers, body = refund_alipay(querydict)
                #else:
                    #body = json.dumps({'result':'refund_fail_refund_fee_wrong_format'}, ensure_ascii=True, indent=4)
            else:
                body = json.dumps({'result':'refund_fail_unsupport_pay_channel'}, ensure_ascii=True, indent=4) 
            
        if not querydict.has_key('out_trade_no') or len(querydict['out_trade_no'])==0:
            body = json.dumps({'result':'refund_fail_out_trade_no_required'}, ensure_ascii=True, indent=4)
        if not querydict.has_key('refund_fee') \
           or (isinstance(querydict['refund_fee'], unicode) and len(querydict['refund_fee'])==0) \
           or (isinstance(querydict['refund_fee'], float) and querydict['refund_fee']==0.0):
            body = json.dumps({'result':'refund_fail_refund_fee_required'}, ensure_ascii=True, indent=4)
        if not querydict.has_key('refund_desc') or len(querydict['refund_desc'])==0:
            body = json.dumps({'result':'refund_fail_refund_desc_required'}, ensure_ascii=True, indent=4)
        if not querydict.has_key('pay_channel') or len(querydict['pay_channel'])==0:
            body = json.dumps({'result':'refund_fail_pay_channel_required'}, ensure_ascii=True, indent=4)
    else:
        body = json.dumps({'result':'refund_fail_wrong_data_format'}, ensure_ascii=True, indent=4)
        
    return statuscode, headers, body
    
    
    
def handle_pay_getinfo(environ):
    global ENCODING
    global gConfig, gSecurityConfig
    
    def get_collection(collection):
        ret = None
        db_util.mongo_init_client('pay_platform')
        db = db_util.gClientMongo['pay_platform'][gConfig['pay_platform']['mongodb']['database']]
        if not collection in db.collection_names(False):
            ret = db.create_collection(collection)
        else:
            ret = db[collection]
        return ret
    def query_pay_log(condition):
        ret = []
        collection = get_collection(gConfig['pay_platform']['mongodb']['collection_pay_log'])
        ret = list(collection.find(condition))
        #for i in cur:
            #ret.append(i)
        return ret
        
    
    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    statuscode = '200 OK'
    body = ''
    querydict = {}
    if environ.has_key('QUERY_STRING') and len(environ['QUERY_STRING'])>0:
        querystring = environ['QUERY_STRING']
        querystring = urllib.unquote_plus(querystring)
        querydict = urlparse.parse_qs(dec(querystring))
        d = {}
        for k in querydict.keys():
            d[k] = querydict[k][0]
        querydict = d
    
    try:
        buf = environ['wsgi.input'].read()
        ds_plus = urllib.unquote_plus(buf)
        d = json.loads(dec(ds_plus))
        for k in d.keys():
            querydict[k] = d[k]
    except:
        pass
    if len(querydict.keys()) > 0:
        if querydict.has_key('q'):
            if querydict['q'] == 'bank_info':
                if querydict.has_key('bank_code'):
                    if querydict['bank_code'] == 'all' or len(querydict['bank_code'])==0:
                        body = json.dumps(gSecurityConfig['alipay']['bank_code'], ensure_ascii=True, indent=4)
                    else:
                        if gSecurityConfig['alipay']['bank_code'].has_key(querydict['bank_code']):
                            body = json.dumps(gSecurityConfig['alipay']['bank_code'][querydict['bank_code']], ensure_ascii=True, indent=4)
                        else:
                            body = json.dumps({'result':'wrong_bank_code'}, ensure_ascii=True, indent=4)
                else:
                    body = json.dumps({'result':'unknown_query_type'}, ensure_ascii=True, indent=4)
            elif querydict['q'] == 'error_info':
                if querydict.has_key('error_code'):
                    if querydict['error_code'] == 'all' or len(querydict['error_code'])==0:
                        body = json.dumps(gSecurityConfig['alipay']['error_code'], ensure_ascii=True, indent=4)
                    else:
                        if gSecurityConfig['alipay']['error_code'].has_key(querydict['error_code']):
                            body = json.dumps(gSecurityConfig['alipay']['error_code'][querydict['error_code']], ensure_ascii=True, indent=4)
                        else:
                            body = json.dumps({'result':'wrong_error_code'}, ensure_ascii=True, indent=4)
                else:
                    body = json.dumps({'result':'unknown_query_type'}, ensure_ascii=True, indent=4)
            elif querydict['q'] == 'trade_status':
                if querydict.has_key('out_trade_no'):
                    if len(querydict['out_trade_no'])>0:
                        l = []
                        if isinstance(querydict['out_trade_no'], unicode):
                            l = query_pay_log({'out_trade_no': querydict['out_trade_no']})
                        elif isinstance(querydict['out_trade_no'], list):
                            idlist = [ObjectId(i) for i in querydict['out_trade_no']]
                            l = query_pay_log({'out_trade_no': {'$in': idlist}})
                        if len(l) > 0:
                            ll = []
                            for i in l:
                                o = {}
                                o['out_trade_no'] = i['out_trade_no']
                                if i.has_key('trade_status'):
                                    o['trade_status'] = i['trade_status']
                                else:
                                    o['trade_status'] = None
                                if i.has_key('error_code'):
                                    o['error_code'] = i['error_code']
                                else:
                                    o['error_code'] = None
                                if i.has_key('refund_status'):
                                    o['refund_status'] = i['refund_status']
                                else:
                                    o['refund_status'] = None
                                ll.append(o)
                            body = json.dumps(db_util.remove_mongo_id(ll), ensure_ascii=True, indent=4)
                        else:
                            body = json.dumps({'result':'out_trade_no_not_exist'}, ensure_ascii=True, indent=4)
                    else:
                        body = json.dumps({'result':'out_trade_cannot_be_null'}, ensure_ascii=True, indent=4)
                else:
                    body = json.dumps({'result':'out_trade_no_required'}, ensure_ascii=True, indent=4)
            else:
                body = json.dumps({'result':'unknown_query_type'}, ensure_ascii=True, indent=4)
    return statuscode, headers, body
                
    
def handle_pay(environ):
    global ENCODING
    global gConfig
    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    statuscode = '200 OK'
    body = ''
    querydict = {}
    if environ.has_key('QUERY_STRING') and len(environ['QUERY_STRING'])>0:
        querystring = environ['QUERY_STRING']
        querystring = urllib.unquote_plus(querystring)
        querydict = urlparse.parse_qs(dec(querystring))
        d = {}
        for k in querydict.keys():
            d[k] = querydict[k][0]
        querydict = d
    
    try:
        buf = environ['wsgi.input'].read()
        ds_plus = urllib.unquote_plus(buf)
        d = json.loads(dec(ds_plus))
        for k in d.keys():
            querydict[k] = d[k]
    except:
        pass
            
    if len(querydict.keys()) > 0:        
        if querydict.has_key('out_trade_no') and len(querydict['out_trade_no'])>0 \
           and querydict.has_key('subject') and len(querydict['subject'])>0 \
           and querydict.has_key('total_fee')  and len(querydict['total_fee'])>0 \
           and querydict.has_key('buyer_email')  and len(querydict['buyer_email'])>0 \
           and querydict.has_key('seller_email')  and len(querydict['seller_email'])>0 \
           and querydict.has_key('pay_channel') and len(querydict['pay_channel'])>0 :
            if querydict['pay_channel'] == 'alipay':
                #if querydict.has_key('service'):
                
                total_fee = 0
                try:
                    total_fee = float(querydict['total_fee'])
                except:
                    body = json.dumps({'result':'pay_fail_total_fee_wrong_format'}, ensure_ascii=True, indent=4)
                    total_fee = 0
                    
                if '^' in querydict['subject'] \
                   or '#' in querydict['subject'] \
                   or '|' in querydict['subject'] \
                   or '$' in querydict['subject'] \
                   or '%' in querydict['subject'] \
                   or '&' in querydict['subject'] \
                   or '+' in querydict['subject'] \
                   or len(querydict['subject'])>128 :
                    total_fee = 0
                    body = json.dumps({'result':'pay_fail_subject_wrong_charactor'}, ensure_ascii=True, indent=4) 
                if total_fee>0:
                    statuscode, headers, body = pay_alipay(querydict)
                else:
                    body = json.dumps({'result':'pay_fail_total_fee_wrong_format'}, ensure_ascii=True, indent=4) 
            else:
                body = json.dumps({'result':'pay_fail_unsupport_pay_channel'}, ensure_ascii=True, indent=4) 
            
        if not querydict.has_key('out_trade_no') or len(querydict['out_trade_no'])==0:
            body = json.dumps({'result':'pay_fail_out_trade_no_required'}, ensure_ascii=True, indent=4)
        if not querydict.has_key('subject') or len(querydict['subject'])==0:
            body = json.dumps({'result':'pay_fail_subject_required'}, ensure_ascii=True, indent=4)
        if not querydict.has_key('total_fee') \
           or (isinstance(querydict['total_fee'], unicode) and len(querydict['total_fee'])==0) \
           or (isinstance(querydict['total_fee'], float) and querydict['total_fee']==0.0):
            body = json.dumps({'result':'pay_fail_total_fee_required'}, ensure_ascii=True, indent=4)
        if not querydict.has_key('buyer_email') or len(querydict['buyer_email'])==0:
            body = json.dumps({'result':'pay_fail_buyer_email_required'}, ensure_ascii=True, indent=4)
        if not querydict.has_key('seller_email') or len(querydict['seller_email'])==0:
            body = json.dumps({'result':'pay_fail_seller_email_required'}, ensure_ascii=True, indent=4)
        if not querydict.has_key('pay_channel') or len(querydict['pay_channel'])==0:
            body = json.dumps({'result':'pay_fail_pay_channel_required'}, ensure_ascii=True, indent=4)
    else:
        body = json.dumps({'result':'pay_fail_wrong_data_format'}, ensure_ascii=True, indent=4)
        
    return statuscode, headers, body


    
def update_refund_log(out_trade_no, data, is_insert=True):
    db_util.mongo_init_client('pay_platform')
    client = db_util.gClientMongo['pay_platform']
    db = client['pay']
    if not 'refund_log' in db.collection_names(False):
        collection = db.create_collection('refund_log')
        collection.ensure_index([("out_trade_no", pymongo.ASCENDING),])
    else:        
        collection = db['refund_log']
    rec = collection.find_one({"out_trade_no":out_trade_no})
    if data.has_key('refund_fee') and (isinstance(data['refund_fee'], unicode) or isinstance(data['refund_fee'], str)):
        data['refund_fee'] = float(data['refund_fee'])
    if rec:
        for k in data.keys():
            rec[k] = data[k]
        wr = collection.update({'_id':rec['_id']}, db_util.add_mongo_id(rec),  multi=False, upsert=False)
        
        if wr and wr['n'] == 0:
            print('update out_trade_no [%s] failed' % out_trade_no)
    else:
        if is_insert:
            try:
                _id = collection.insert( db_util.add_mongo_id(data))
                #print('refund_log insert _id=%s' % str(_id))
            except:
                print('refund_log insert out_trade_no [%s] failed' % out_trade_no)

    
    
def update_pay_log(out_trade_no, data, is_insert=True):
    db_util.mongo_init_client('pay_platform')
    client = db_util.gClientMongo['pay_platform']
    db = client['pay']
    if not 'pay_log' in db.collection_names(False):
        collection = db.create_collection('pay_log')
        collection.ensure_index([("out_trade_no", pymongo.ASCENDING),])
    else:        
        collection = db['pay_log']
    rec = collection.find_one({"out_trade_no":out_trade_no})
    if data.has_key('total_fee') and (isinstance(data['total_fee'], unicode) or isinstance(data['total_fee'], str)):
        data['total_fee'] = float(data['total_fee'])
    if data.has_key('refund_fee') and (isinstance(data['refund_fee'], unicode) or isinstance(data['refund_fee'], str)):
        data['refund_fee'] = float(data['refund_fee'])
    if data.has_key('price') and (isinstance(data['price'], unicode) or isinstance(data['price'], str)):
        data['price'] = float(data['price'])
    if data.has_key('quantity') and (isinstance(data['quantity'], unicode) or isinstance(data['quantity'], str)):
        data['quantity'] = int(data['quantity'])
    if rec:
        for k in data.keys():
            rec[k] = data[k]
        wr = collection.update({'_id':rec['_id']}, db_util.add_mongo_id(rec),  multi=False, upsert=False)
        #print(wr)
        if wr and wr['n'] == 0:
            print('update out_trade_no [%s] failed' % out_trade_no)
    else:
        if is_insert:
            try:
                _id = collection.insert( db_util.add_mongo_id(data))
                #print('pay_log insert _id=%s' % str(_id))
            except:
                print('pay_log insert out_trade_no [%s] failed' % out_trade_no)
        
            
    
def handle_alipay_return_url(environ):
    global ENCODING
    global gConfig,  gSecurityConfig
    querydict = {}
    data = {}
    data['pay_channel'] = 'alipay'
    querystring = ''
    if environ.has_key('QUERY_STRING'):
        querystring = environ['QUERY_STRING']
        querystring = urllib.unquote_plus(querystring)
        querystring = dec_by_code(gConfig['pay_platform']['alipay']['input_charset'], querystring)
        querydict = urlparse.parse_qs(querystring)
        d = {}
        for k in querydict.keys():
            d[k] = querydict[k][0]
        querydict = d
    if querydict.has_key('notify_type') and 'trade_status_' in querydict['notify_type'] and  querydict.has_key('out_trade_no'):
        if querydict.has_key('is_success'):
            if querydict['is_success'] == 'T':
                data['trade_status'] = 'send_to_alipay_success'
            
        if querydict.has_key('seller_email'):
            data['seller_email'] = querydict['seller_email']
        if querydict.has_key('buyer_email'):
            data['buyer_email'] = querydict['buyer_email']
        if querydict.has_key('seller_id'):
            data['seller_id'] = querydict['seller_id']
        if querydict.has_key('buyer_id'):
            data['buyer_id'] = querydict['buyer_id']
        if querydict.has_key('notify_time'):
            data['notify_time'] = querydict['notify_time']
        if querydict.has_key('notify_type'):
            data['notify_type'] = querydict['notify_type']
        if querydict.has_key('notify_id'):
            data['notify_id'] = querydict['notify_id']
        if querydict.has_key('out_trade_no'):
            data['out_trade_no'] = querydict['out_trade_no']
        if querydict.has_key('subject'):
            data['subject'] = querydict['subject']
        if querydict.has_key('payment_type'):
            data['payment_type'] = querydict['payment_type']
            
        if querydict.has_key('trade_no'):
            data['trade_no'] = querydict['trade_no']
        if querydict.has_key('trade_status'):
            data['trade_status'] = querydict['trade_status']
            if gSecurityConfig['alipay']['trade_status'].has_key(data['trade_status']):
                data['trade_status_desc'] = gSecurityConfig['alipay']['trade_status'][data['trade_status']]
        if querydict.has_key('gmt_create'):
            data['gmt_create'] = querydict['gmt_create']
        if querydict.has_key('gmt_payment'):
            data['gmt_payment'] = querydict['gmt_payment']
        if querydict.has_key('gmt_close'):
            data['gmt_close'] = querydict['gmt_close']
        if querydict.has_key('gmt_refund'):
            data['gmt_refund'] = querydict['gmt_refund']
        if querydict.has_key('body'):
            data['body'] = querydict['body']
        if querydict.has_key('error_code'):
            data['error_code'] = querydict['error_code']
        if querydict.has_key('bank_seq_no'):
            data['bank_seq_no'] = querydict['bank_seq_no']
        if querydict.has_key('out_channel_type'):
            data['out_channel_type'] = querydict['out_channel_type']
        if querydict.has_key('out_channel_amount'):
            data['out_channel_amount'] = querydict['out_channel_amount']
        if querydict.has_key('out_channel_inst'):
            data['out_channel_inst'] = querydict['out_channel_inst']
        if querydict.has_key('business_scene'):
            data['business_scene'] = querydict['business_scene']
        if querydict.has_key('total_fee'):
            data['total_fee'] = querydict['total_fee']
        if data.has_key('out_trade_no'):
            g = gevent.spawn(update_pay_log, data['out_trade_no'], data, False)
    
    
        
    
        
    
def handle_alipay_notify_url(environ):
    global gConfig, gSecurityConfig
    buf = environ['wsgi.input'].read()
    ds_plus = urllib.unquote_plus(buf)
    ds_plus = dec_by_code(gConfig['pay_platform']['alipay']['input_charset'], ds_plus)
    querydict = {}
    data = {}
    data['pay_channel'] = 'alipay'
    try:
        querydict = urlparse.parse_qs(ds_plus)
        d = {}
        for k in querydict.keys():
            d[k] = querydict[k][0]
        querydict = d
    except:
        querydict = {}
    if querydict.has_key('seller_email'):
        data['seller_email'] = querydict['seller_email']
    if querydict.has_key('buyer_email'):
        data['buyer_email'] = querydict['buyer_email']
    if querydict.has_key('seller_id'):
        data['seller_id'] = querydict['seller_id']
    if querydict.has_key('buyer_id'):
        data['buyer_id'] = querydict['buyer_id']
    if querydict.has_key('notify_time'):
        data['notify_time'] = querydict['notify_time']
    if querydict.has_key('notify_id'):
        data['notify_id'] = querydict['notify_id']
    if querydict.has_key('notify_type'):
        data['notify_type'] = querydict['notify_type']
    if querydict.has_key('out_trade_no'):
        data['out_trade_no'] = querydict['out_trade_no']
    if querydict.has_key('subject'):
        data['subject'] = querydict['subject']
    if querydict.has_key('payment_type'):
        data['payment_type'] = querydict['payment_type']
        
    if querydict.has_key('trade_no'):
        data['trade_no'] = querydict['trade_no']
    if querydict.has_key('trade_status'):
        data['trade_status'] = querydict['trade_status']
        if gSecurityConfig['alipay']['trade_status'].has_key(data['trade_status']):
            data['trade_status_desc'] = gSecurityConfig['alipay']['trade_status'][data['trade_status']]
    
    if querydict.has_key('gmt_create'):
        data['gmt_create'] = querydict['gmt_create']
    if querydict.has_key('gmt_payment'):
        data['gmt_payment'] = querydict['gmt_payment']
    if querydict.has_key('gmt_close'):
        data['gmt_close'] = querydict['gmt_close']
    if querydict.has_key('gmt_refund'):
        data['gmt_refund'] = querydict['gmt_refund']
    if querydict.has_key('body'):
        data['body'] = querydict['body']
    if querydict.has_key('error_code'):
        data['error_code'] = querydict['error_code']
    if querydict.has_key('bank_seq_no'):
        data['bank_seq_no'] = querydict['bank_seq_no']
        
        
    if querydict.has_key('out_channel_type'):
        data['out_channel_type'] = querydict['out_channel_type']
    if querydict.has_key('out_channel_amount'):
        data['out_channel_amount'] = querydict['out_channel_amount']
    if querydict.has_key('out_channel_inst'):
        data['out_channel_inst'] = querydict['out_channel_inst']
    if querydict.has_key('business_scene'):
        data['business_scene'] = querydict['business_scene']
    
    
    if querydict.has_key('total_fee'):
        data['total_fee'] = querydict['total_fee']
    if querydict.has_key('notify_type') and 'trade_status_' in querydict['notify_type']  and data.has_key('out_trade_no'):
        g = gevent.spawn(update_pay_log, data['out_trade_no'], data, False)
    if querydict.has_key('notify_type') and querydict['notify_type'] == 'batch_refund_notify':
        if querydict.has_key('batch_no'):
            data['batch_no'] = querydict['batch_no']
        if querydict.has_key('success_num'):
            data['success_num'] = int(querydict['success_num'])
        if querydict.has_key('result_details'):
            arr = querydict['result_details'].split('^')
            trade_no = arr[0]
            refund_fee = float(arr[1])
            refund_status = arr[2]
            data['trade_no'] = trade_no
            data['refund_fee'] = refund_fee
            data['refund_status'] = refund_status
        g = gevent.spawn(update_refund_log, data['trade_no'], data, False)
        
        
    
def handle_alipay_error_notify_url(environ):
    global gConfig, gSecurityConfig
    buf = environ['wsgi.input'].read()
    ds_plus = urllib.unquote_plus(buf)
    ds_plus = dec_by_code(gConfig['pay_platform']['alipay']['input_charset'], ds_plus)
    querydict = {}
    data = {}
    data['pay_channel'] = 'alipay'
    try:
        querydict = urlparse.parse_qs(ds_plus)
        d = {}
        for k in querydict.keys():
            d[k] = querydict[k][0]
        querydict = d
    except:
        querydict = {}
    if querydict.has_key('out_trade_no'):
        data['out_trade_no'] = querydict['out_trade_no']
    if querydict.has_key('error_code'):
        data['error_code'] = querydict['error_code']
        if gSecurityConfig['alipay']['error_code'].has_key(data['error_code']):
            data['error_desc'] = gSecurityConfig['alipay']['error_code'][data['error_code']]
    if data.has_key('out_trade_no'):
        g = gevent.spawn(update_pay_log, data['out_trade_no'], data, False)
        #g.join()
    
def get_querydict_by_GET_POST(environ):
    querydict = {}
    buf = None
    if environ.has_key('QUERY_STRING'):
        querystring = environ['QUERY_STRING']
        querystring = urllib.unquote_plus(querystring)
        querystring = dec(querystring)
        try:
            d = json.loads(querystring)
            if isinstance(d, dict):
                for k in d.keys():
                    querydict[k] = d[k]
        except:
            querydict = urlparse.parse_qs(querystring)
            d = {}
            for k in querydict.keys():
                d[k] = querydict[k][0]
            querydict = d
    # try:
    #     # buf = environ['wsgi.input'].read()
    #     buf = stream.read()
    #     print('buf=')
    #     print(buf)
    #     ds_plus = urllib.unquote_plus(buf)
    #     obj = json.loads(dec(ds_plus))
    #     for k in obj.keys():
    #         querydict[k] = obj[k]
    # except:
    #     pass
    stream, form, files = werkzeug.formparser.parse_form_data(environ, charset='utf-8')
    if len(form.keys()) > 0:
        for key in form.keys():
            try:
                if isinstance(key, str):
                    key = dec(key)
                obj = json.loads(key)
                if isinstance(obj, dict):
                    for k in obj.keys():
                        querydict[k] = obj[k]
                if isinstance(obj, list):
                    querydict = obj
            except Exception,e:
                print(e)
                querydict[key] = form[key]
    file_storage_list = []
    if len(files.keys()) > 0:
        for key in files.keys():
            file_storage_list.extend(files.getlist(key))
    for file_storage in  file_storage_list:
        if isinstance(file_storage, werkzeug.datastructures.FileStorage):
            querydict['filename'] = file_storage.filename
            querydict['content_type'] = file_storage.content_type
            querydict['mimetype'] = file_storage.mimetype
            # querydict['content_length'] = file_storage.content_length
            buf = file_storage.read()
            break
    return querydict, buf
    
def handle_combiz_platform(environ):
    global ENCODING
    global gConfig, gRequest, gFormTemplate
    
       
    def get_collection(collection):
        ret = None
        db_util.mongo_init_client('combiz_platform')
        db = db_util.gClientMongo['combiz_platform'][gConfig['combiz_platform']['mongodb']['database']]
        if not collection in db.collection_names(False):
            ret = db.create_collection(collection)
        else:
            ret = db[collection]
        return ret
    #Rule('/workflow_add', endpoint='workflow_add'),
    #Rule('/workflow_query', endpoint='workflow_query'),
    #Rule('/workflow_query/<_id>', endpoint='workflow_query'),
    #Rule('/workflow_update', endpoint='workflow_update'),
    #Rule('/workflow_delete', endpoint='workflow_delete'),
    #Rule('/workflow_delete/<_id>', endpoint='workflow_delete'),
    #Rule('/workflow_template_add', endpoint='workflow_template_add'),
    #Rule('/workflow_template_query', endpoint='workflow_template_query'),
    #Rule('/workflow_template_query/<_id>', endpoint='workflow_template_query'),
    #Rule('/workflow_template_update', endpoint='workflow_template_update'),
    #Rule('/workflow_template_delete', endpoint='workflow_template_delete'),
    #Rule('/workflow_template_delete/<_id>', endpoint='workflow_template_delete'),
    
    def workflow_add(querydict):
        ret = ''
        if  querydict.has_key('order_id'):
            try:
                collection = get_collection(gConfig['combiz_platform']['mongodb']['collection_workflow'])
                existone = collection.find_one({'order_id':querydict['order_id']})
                if existone:
                    ret = json.dumps({'result':u'workflow_add_order_id_already_exist' }, ensure_ascii=True, indent=4)
                else:    
                    _id = collection.save(querydict)
                    o = collection.find_one({'_id':_id})
                    ret = json.dumps(db_util.remove_mongo_id(o), ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'workflow_add_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'workflow_add_fail' }, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'workflow_add_order_id_required' }, ensure_ascii=True, indent=4)
            
        return ret
        
        
    def workflow_query(querydict):
        ret = ''
        o = None
        try:
            #print(querydict)
            collection = get_collection(gConfig['combiz_platform']['mongodb']['collection_workflow'])
            limit = 10
            skip = 0
            ssort = None
            cond = {}
            if querydict.has_key('limit'):
                limit = int(querydict['limit'])
            if querydict.has_key('offset'):
                skip = int(querydict['offset'])
            if querydict.has_key('order'):
                ssort = []
                if querydict['order'] == 'asc':
                    ssort = [('order_id', pymongo.ASCENDING),]
                if querydict['order'] == 'desc':
                    ssort = [('order_id', pymongo.DESCENDING),]
            
            if querydict.has_key('_id'):
                o = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
            elif querydict.has_key('order_id'):
                if '*' in querydict['order_id']:
                    cond = {'order_id': {'$regex':'^.*' + querydict['order_id'].replace('*', '') + '.*$'}}
                    #print(cond)
                    o = list(collection.find(cond, skip=skip, limit=limit, sort=ssort))
                    #print(o)
                else:
                    o = collection.find_one({'order_id':querydict['order_id']})
            else:
                ssort = None
                cond = {}
                if querydict.has_key('search_field') and querydict.has_key('search'):
                    cond = {str(querydict['search_field']): {'$regex':'^.*' + querydict['search'].replace('*', '') + '.*$'}}
                if querydict.has_key('order'):
                    ssort = []
                    if querydict['order'] == 'asc':
                        ssort = [(str(querydict['search_field']), pymongo.ASCENDING),]
                    if querydict['order'] == 'desc':
                        ssort = [(str(querydict['search_field']), pymongo.DESCENDING),]
                o = list(collection.find(cond, skip=skip, limit=limit, sort=ssort))
            if o:
                ret = json.dumps(db_util.remove_mongo_id(o), ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'workflow_query_workflow_not_exist' }, ensure_ascii=True, indent=4)
            #if not querydict.has_key('_id') and not querydict.has_key('order_id'):
                #ret = json.dumps({'result':u'workflow_query_id_or_order_id_required' }, ensure_ascii=True, indent=4)
        except:
            if hasattr(sys.exc_info()[1], 'message'):
                ret = json.dumps({'result':u'workflow_query_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'workflow_query_fail' }, ensure_ascii=True, indent=4)
        return ret
            
    def workflow_update(querydict):
        ret = ''
        try:
            collection = get_collection(gConfig['combiz_platform']['mongodb']['collection_workflow'])
            if querydict.has_key('_id'):
                existone = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
                if existone:
                    collection.update({'_id':existone['_id']}, {'$set': db_util.add_mongo_id(querydict)}, multi=False, upsert=False)
                    one = collection.find_one(db_util.add_mongo_id({'_id':existone['_id']}))
                    ret = json.dumps(db_util.remove_mongo_id(one), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'workflow_update_workflow_not_exist' }, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'workflow_update_id_required' }, ensure_ascii=True, indent=4)
        except:
            if hasattr(sys.exc_info()[1], 'message'):
                ret = json.dumps({'result':u'workflow_update_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'workflow_update_fail' }, ensure_ascii=True, indent=4)
        return ret
            
    def workflow_delete(querydict):
        ret = ''
        try:
            collection = get_collection(gConfig['combiz_platform']['mongodb']['collection_workflow'])
            if querydict.has_key('_id'):
                if isinstance(querydict['_id'], str) or isinstance(querydict['_id'], unicode):
                    existone = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
                    if existone:
                        collection.remove({'_id':existone['_id']})
                        ret = json.dumps(db_util.remove_mongo_id(existone), ensure_ascii=True, indent=4)
                    else:
                        ret = json.dumps({'result':u'workflow_delete_workflow_not_exist' }, ensure_ascii=True, indent=4)
                if isinstance(querydict['_id'], list):
                    ids = db_util.add_mongo_id(querydict['_id'])
                    cond = {'_id':{'$in':ids}}
                    collection.remove(cond)
                    ret = json.dumps(db_util.remove_mongo_id(querydict['_id']), ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'workflow_delete_id_required' }, ensure_ascii=True, indent=4)
        except:
            if hasattr(sys.exc_info()[1], 'message'):
                ret = json.dumps({'result':u'workflow_delete_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'workflow_delete_fail' }, ensure_ascii=True, indent=4)
        return ret
    
    def workflow_template_add(querydict):
        ret = ''
        if  querydict.has_key('name') \
            and querydict.has_key('nodes') \
            and querydict.has_key('edges'):
            try:
                collection = get_collection(gConfig['combiz_platform']['mongodb']['collection_workflow_template'])
                existone = collection.find_one({'name':querydict['name']})
                if existone:
                    ret = json.dumps({'result':u'workflow_template_add_name_already_exist' }, ensure_ascii=True, indent=4)
                else:    
                    _id = collection.save(db_util.add_mongo_id(querydict))
                    o = collection.find_one({'_id':_id})
                    ret = json.dumps(db_util.remove_mongo_id(o), ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'workflow_template_add_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'workflow_template_add_fail' }, ensure_ascii=True, indent=4)
        else:
            if not querydict.has_key('name'):
                ret = json.dumps({'result':u'workflow_template_add_name_required' }, ensure_ascii=True, indent=4)
            if not querydict.has_key('nodes'):
                ret = json.dumps({'result':u'workflow_template_add_nodes_required' }, ensure_ascii=True, indent=4)
            if not querydict.has_key('edges'):
                ret = json.dumps({'result':u'workflow_template_add_edges_required' }, ensure_ascii=True, indent=4)
            
        return ret
    def workflow_template_query(querydict):
        ret = ''
        o = None
        try:
            collection = get_collection(gConfig['combiz_platform']['mongodb']['collection_workflow_template'])
            o = None
            limit = 10
            skip = 0
            ssort = None
            cond = {}
            if querydict.has_key('limit'):
                limit = int(querydict['limit'])
            if querydict.has_key('offset'):
                skip = int(querydict['offset'])
            if querydict.has_key('order'):
                ssort = []
                if querydict['order'] == 'asc':
                    ssort = [('name', pymongo.ASCENDING),]
                if querydict['order'] == 'desc':
                    ssort = [('name', pymongo.DESCENDING),]
            if querydict.has_key('name'):
                if '*' in querydict['name']:
                    cond = {'name': {'$regex':'^.*' + querydict['name'].replace('*', '') + '.*$'}}
                    o = list(collection.find(cond, skip=skip, limit=limit, sort=ssort))
                else:
                    o = collection.find_one({'name':querydict['name']})
            elif querydict.has_key('_id'):
                o = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
                if o:
                    ret = json.dumps(db_util.remove_mongo_id(o), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'workflow_template_query_workflow_not_exist' }, ensure_ascii=True, indent=4)
            else:
                ssort = None
                cond = {}
                if querydict.has_key('search_field') and querydict.has_key('search'):
                    cond = {str(querydict['search_field']): {'$regex':'^.*' + querydict['search'].replace('*', '') + '.*$'}}
                if querydict.has_key('order'):
                    ssort = []
                    if querydict['order'] == 'asc':
                        ssort = [(str(querydict['search_field']), pymongo.ASCENDING),]
                    if querydict['order'] == 'desc':
                        ssort = [(str(querydict['search_field']), pymongo.DESCENDING),]
                o = list(collection.find(cond, skip=skip, limit=limit, sort=ssort))
                ret = json.dumps(db_util.remove_mongo_id(o), ensure_ascii=True, indent=4)
        except:
            if hasattr(sys.exc_info()[1], 'message'):
                ret = json.dumps({'result':u'workflow_template_query_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'workflow_template_query_fail' }, ensure_ascii=True, indent=4)
        return ret
    def workflow_template_update(querydict):
        ret = ''
        try:
            collection = get_collection(gConfig['combiz_platform']['mongodb']['collection_workflow_template'])
            if querydict.has_key('_id'):
                existone = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
                if existone:
                    collection.update({'_id':existone['_id']}, {'$set': db_util.add_mongo_id(querydict)}, multi=False, upsert=False)
                    one = collection.find_one({'_id':existone['_id']})
                    ret = json.dumps(db_util.remove_mongo_id(one), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'workflow_template_update_workflow_not_exist' }, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'workflow_template_update_id_required' }, ensure_ascii=True, indent=4)
        except:
            if hasattr(sys.exc_info()[1], 'message'):
                ret = json.dumps({'result':u'workflow_template_update_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'workflow_template_update_fail' }, ensure_ascii=True, indent=4)
        return ret
    def workflow_template_delete(querydict):
        ret = ''
        try:
            collection = get_collection(gConfig['combiz_platform']['mongodb']['collection_workflow'])
            if querydict.has_key('_id'):
                if isinstance(querydict['_id'], str) or isinstance(querydict['_id'], unicode):
                    existone = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
                    if existone:
                        collection.remove({'_id':existone['_id']})
                        ret = json.dumps(db_util.remove_mongo_id(existone), ensure_ascii=True, indent=4)
                    else:
                        ret = json.dumps({'result':u'workflow_template_delete_workflow_not_exist' }, ensure_ascii=True, indent=4)
                if isinstance(querydict['_id'], list):
                    ids = db_util.add_mongo_id(querydict['_id'])
                    cond = {'_id':{'$in':ids}}
                    collection.remove(cond)
                    ret = json.dumps(db_util.remove_mongo_id(querydict['_id']), ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'workflow_template_delete_id_required' }, ensure_ascii=True, indent=4)
        except:
            if hasattr(sys.exc_info()[1], 'message'):
                ret = json.dumps({'result':u'workflow_template_delete_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'workflow_template_delete_fail' }, ensure_ascii=True, indent=4)
        return ret
    
    
    def get_form(form_id):
        global gFormTemplate
        ret = None
        for i in gFormTemplate:
            if i['form_path'] == form_id:
                ret = i
                break
        return ret
    def get_out_tmp_dir(dirname):
        out_dir = os.path.join(dirname, 'export_tmp')
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        now = time.strftime('%Y-%m-%d %H:%M:%S')[:19].replace('-','').replace(' ','').replace(':','')
        out_dir = os.path.join(out_dir, '%s-%s' % ( now , uuid.uuid4()))
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        return out_dir
        
    def form_blank(querydict):
        global gFormTemplate
        ret = ''
        content_type = 'text/json'
        filename = None
        if len(gFormTemplate) == 0:
            p = os.path.join(STATICRESOURCE_DIR, 'form_templates', 'list.json')
            if os.path.exists(p):
                try:
                    with open(p, 'r') as f:
                        f1 = gevent.fileobject.FileObjectThread(f, 'r')
                        gFormTemplate = json.loads(f1.read())
                except:
                    ret = json.dumps({'result':u'form_blank_list_json_parse_error'}, ensure_ascii=True, indent=4)
                    return ret, content_type, filename
            else:
                ret = json.dumps({'result':u'form_blank_list_json_not_exist'}, ensure_ascii=True, indent=4)
                return ret, content_type, filename
        if querydict.has_key('form_id'):
            form = get_form(querydict['form_id'])
            if form and form.has_key('blank_document'):
                out_path = form['blank_document']
                out_path = os.path.join(STATICRESOURCE_DIR, out_path)
                if os.path.exists(out_path):
                    ext = 'pdf'
                    if querydict.has_key('format'):
                        ext = querydict['format']
                    ret,content_type = form_export(out_path,  ext)
                    if querydict.has_key('attachmentdownload') and querydict['attachmentdownload'] is True:
                        filename = os.path.basename(form['blank_document'])
                        filename = filename[:filename.rindex('.')]
                        filename = '%s%s.%s' % (filename , u'(空白)', ext)
                else:
                    ret = json.dumps({'result':u'form_blank_generated_document_not_exist'}, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'form_blank_blank_document_need_specify_in_list_json'}, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'form_blank_form_id_required'}, ensure_ascii=True, indent=4)
        return ret, content_type, filename
        
    def form_fill(querydict):
        global gFormTemplate
        def check_is_bool(form, fld):
            ret = False
            if form.has_key('bool') and isinstance(form['bool'], list):
                for i in form['bool']:
                    if i == fld:
                        ret = True
                        break
            return ret
            
        def chinese_date(value):
            ret = value
            if len(ret) == 19 :
                if ret[4] == u'-' and ret[7] == u'-' and ret[10] == u' ':
                    ret1 = ret[:4]
                    ret1 += u'年'
                    ret1 += ret[5:7]
                    ret1 +=  u'月'
                    ret1 += ret[8:10]
                    ret1 += u'日'
                    ret = ret1
            return ret
        def check_is_image(form, fld):
            ret = False
            if form.has_key('image') and isinstance(form['image'], list):
                for i in form['image']:
                    if i == fld:
                        ret = True
                        break
            return ret
        def check_is_list(form, fld):
            ret = False
            if form.has_key('list') and isinstance(form['list'], list):
                for i in form['list']:
                    if i == fld:
                        ret = True
                        break
            return ret
        def fill_tpl(form, form_data):
            template_document = os.path.join(STATICRESOURCE_DIR, form['template_document'])
            dirname = os.path.dirname(template_document)
            basename = os.path.basename(template_document)
            basename = basename.replace('_template', '')
            out_dir = get_out_tmp_dir(dirname)
            out_path = os.path.join(out_dir, basename)
            t = Template(template_document, out_path)
            data = {}
            document = Py3oItem()
            file_service_url = '%s://%s:%s/fileservice/rest/file/' % (gConfig['combiz_platform']['proxy_file']['protocol'], gConfig['combiz_platform']['proxy_file']['host'], gConfig['combiz_platform']['proxy_file']['port'])
            for k in form_data.keys():
                #listobj = check_is_list(form, k)
                if check_is_bool(form, k):
                    if form_data[k] is True:
                        setattr(document, k, u'\u2611')
                    if form_data[k] is False:
                        setattr(document, k, u'\u2610')
                elif check_is_list(form, k):
                    data[k] = []
                    for i in form_data[k]:
                        item = Py3oItem()
                        for kk in i.keys():
                            setattr(item, kk, chinese_date(i[kk]))
                        data[k].append(item)
                elif check_is_image(form, k):
                    out_path1 = os.path.join(out_dir, form_data[k])
                    url = URL(file_service_url + form_data[k])
                    client = HTTPClient.from_url(url)
                    try:
                        response = client.get(url.request_uri)
                        if hasattr(response, 'status_code') and (response.status_code == 200 or response.status_code == 304):
                            with open(out_path1, 'wb') as f:
                                f1 = gevent.fileobject.FileObjectThread(f, 'wb')
                                f1.write(response.read())
                            if os.path.exists(out_path1):
                                t.set_image_path(k, out_path1)
                    except Exception,e:
                        print(e)
                        out_path1 = os.path.join(STATICRESOURCE_DIR, 'form_templates', 'document', 'no-photo.jpg')
                        t.set_image_path(k, out_path1)
                else:
                    setattr(document, k, chinese_date(form_data[k]))
            data['document'] = document
            #print(dir(data))
            t.render(data)
            return out_path
        ret = ''
        content_type = 'text/json'
        filename = None
        if len(gFormTemplate) == 0:
            p = os.path.join(STATICRESOURCE_DIR, 'form_templates', 'list.json')
            if os.path.exists(p):
                try:
                    with open(p, 'r') as f:
                        f1 = gevent.fileobject.FileObjectThread(f, 'r')
                        gFormTemplate = json.loads(f1.read())
                except:
                    ret = json.dumps({'result':u'form_fill_list_json_parse_error'}, ensure_ascii=True, indent=4)
                    return ret, content_type, filename
            else:
                ret = json.dumps({'result':u'form_fill_list_json_not_exist'}, ensure_ascii=True, indent=4)
                return ret, content_type, filename
        o = json.loads(workflow_query(querydict))
        if o.has_key('result'):
            ret = json.dumps(o, ensure_ascii=True, indent=4)
        else:
            if querydict.has_key('form_id'):
                if o.has_key('form_data') and isinstance(o['form_data'], dict):
                    if querydict['form_id'] in o['form_data'].keys():
                        form_data = o['form_data'][querydict['form_id']]
                        form = get_form(querydict['form_id'])
                        if form and form.has_key('template_document'):
                            out_path = fill_tpl(form, form_data)
                            if os.path.exists(out_path):
                                ext = 'pdf'
                                if querydict.has_key('format'):
                                    ext = querydict['format']
                                ret, content_type = form_export(out_path,  ext)
                                if querydict.has_key('attachmentdownload') and querydict['attachmentdownload'] is True:
                                    filename = os.path.basename(form['template_document']).replace('_template', '')
                                    filename = filename[:filename.rindex('.')]
                                    filename = '%s%s.%s' % (filename , u'(已填)', ext)
                            else:
                                ret = json.dumps({'result':u'form_fill_generated_document_not_exist'}, ensure_ascii=True, indent=4)
                        else:
                            ret = json.dumps({'result':u'form_fill_template_document_need_specify_in_list_json'}, ensure_ascii=True, indent=4)
                    else:
                        ret = json.dumps({'result':u'form_fill_form_id_not_exist'}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'form_fill_form_data_is_none'}, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'form_fill_form_id_required'}, ensure_ascii=True, indent=4)
        return ret, content_type, filename
        
        
        
    def form_export(src,  ext):
        dirname = os.path.dirname(src)
        out_dir = get_out_tmp_dir(dirname)
        out_path = os.path.basename(src)
        idx = out_path.rindex('.') 
        out_path = out_path[:idx+1]  + ext
        out_path = os.path.join(out_dir, out_path)
        ret = json.dumps({'result':'unsupport export format.'}, ensure_ascii=True, indent=4)
        content_type = 'text/json'
        format = 'pdf'
        if ext == 'pdf':
            #format = 'pdf:writer pdf Export'
            format = 'pdf'
            content_type = 'application/pdf'
        elif ext == 'doc':
            format = 'doc:MS Word 97'
            content_type = 'application/msword'
        elif ext == 'docx':
            format = 'docx:MS Word 2007 XML'
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif ext == 'html':
            format = 'html:XHTML Writer File'
            content_type = 'text/html'
        encfunc = enc
        if sys.platform == 'win32':
            encfunc = enc1
        cmd = [
            encfunc(gConfig['combiz_platform']['libreoffice']['executable_path']),
               '--headless',
               '--convert-to',
               format,
               '--outdir',
               encfunc(out_dir),
               encfunc(src)
        ]
        
        output = check_output(cmd)
        print(output)
        #if len(output.strip())>0:
            #ret = json.dumps({'result':output}, ensure_ascii=True, indent=4)
            #content_type = 'text/json'
        if not os.path.exists(out_path):
            ret = json.dumps({'result':'export failed:file not exist.'}, ensure_ascii=True, indent=4)
            content_type = 'text/json'
        if os.path.exists(out_path):
            with open(out_path, 'rb') as f:
                f1 = gevent.fileobject.FileObjectThread(f, 'rb')
                ret = f1.read()
        return ret, content_type
    
    def check_url_token(querydict):
        is_token_pass = False
        enable_url_md5_check = False
        md5prefix = ''
        if gConfig['combiz_platform'].has_key('security') \
           and gConfig['combiz_platform']['security'].has_key('md5prefix'):
            md5prefix = str(gConfig['combiz_platform']['security']['md5prefix'])

        if gConfig['combiz_platform'].has_key('security') \
           and gConfig['combiz_platform']['security'].has_key('enable_url_md5_check') \
           and gConfig['combiz_platform']['security']['enable_url_md5_check'].lower() == 'true':
            enable_url_md5_check = True
        else:
            is_token_pass = True
        if enable_url_md5_check:
            print('checking token...')
            if querydict.has_key('_token'):
                plain = '%s_|_%s' % (md5prefix, time.strftime('%Y%m%d%H'))
                token = md5.new(plain).hexdigest()
                if token == str(querydict['_token']):
                    is_token_pass = True
        return is_token_pass

    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    statuscode = '200 OK'
    body = ''
    isnew = False
    urls = gUrlMap.bind_to_environ(environ)
    querydict, buf = get_querydict_by_GET_POST(environ)
    try:
        endpoint, args = urls.match()
        if args.has_key('_id'):
            querydict['_id'] = args['_id']
        if endpoint not in []:
            if not check_url_token(querydict):
                body = json.dumps({'result': u'invalid_token'}, ensure_ascii=True, indent=4)
                return statuscode, headers, body
        if querydict.has_key('_token'):
            del querydict['_token']
        if endpoint == 'workflow_add':
            body = workflow_add(querydict)
        elif endpoint == 'workflow_query':
            body = workflow_query(querydict)
        elif endpoint == 'workflow_update':
            body = workflow_update(querydict)
        elif endpoint == 'workflow_delete':
            body = workflow_delete(querydict)
        elif endpoint == 'workflow_template_add':
            body = workflow_template_add(querydict)
        elif endpoint == 'workflow_template_query':
            body = workflow_template_query(querydict)
        elif endpoint == 'workflow_template_update':
            body = workflow_template_update(querydict)
        elif endpoint == 'workflow_template_delete':
            body = workflow_template_delete(querydict)
        elif endpoint == 'workflow_form_fill':
            body, content_type, filename = form_fill(querydict)
            headers['Content-Type'] = content_type
            if filename:
                headers['Content-Disposition'] = 'attachment;filename="' + enc(filename) + '"'
        elif endpoint == 'workflow_form_blank':
            body, content_type, filename = form_blank(querydict)
            headers['Content-Type'] = content_type
            if filename:
                headers['Content-Disposition'] = 'attachment;filename="' + enc(filename) + '"'
        else:
            body = json.dumps({'result':u'access_deny'}, ensure_ascii=True, indent=4)
    except HTTPException, e:
        body = json.dumps({'result':u'access_deny'}, ensure_ascii=True, indent=4)
    return statuscode, headers, body



def handle_chat_platform(environ, session):
    global ENCODING
    global gConfig, gRequest, gSessionStore, gUrlMap, gSecurityConfig, gWebSocketsMap,  gJoinableQueue
    def get_collection(collection):
        ret = None
        db_util.mongo_init_client('chat_platform')
        db = db_util.gClientMongo['chat_platform'][gConfig['chat_platform']['mongodb']['database']]
        if not collection in db.collection_names(False):
            ret = db.create_collection(collection)
        else:
            ret = db[collection]
        return ret

    def user_query(session, querydict):
        ret = []
        collection = get_collection(gConfig['chat_platform']['mongodb']['collection_users'])
        q = {}
        limit = 0
        skip = 0
        user_detail = False
        if querydict.has_key('user_detail') and querydict['user_detail'] is True:
            user_detail = True
            del querydict['user_detail']
        if querydict.has_key('limit'):
            limit = int(querydict['limit'])
            del querydict['limit']
        if querydict.has_key('skip'):
            skip = int(querydict['skip'])
            del querydict['skip']
        if querydict.has_key('username'):
            if isinstance(querydict['username'], str) or isinstance(querydict['username'], unicode):
                q['username'] = querydict['username']
            if isinstance(querydict['username'], list):
                q['username'] = {'$in': querydict['username']}
            if isinstance(querydict['username'], dict):
                q['username'] = querydict['username']
        if querydict.has_key('_id'):
            if isinstance(querydict['_id'], str) or isinstance(querydict['_id'], unicode):
                q['_id'] = db_util.add_mongo_id(querydict['_id'])
            if isinstance(querydict['_id'], list):
                q['_id'] = {'$in': [db_util.add_mongo_id(i) for i in querydict['_id']]}
            if isinstance(querydict['_id'], dict):
                q['_id'] = querydict['_id']
        rec = list(collection.find(q).limit(limit).skip(skip))
        keys = gWebSocketsMap.keys()
        for i in rec:
            if user_detail:
                if str(i['_id']) in keys:
                    i['online_status'] = 'online'
                else:
                    i['online_status'] = 'offline'
            ret.append(i)
        return ret
    
    def group_query(session, querydict={}):
        ret = []
        collection = get_collection(gConfig['chat_platform']['mongodb']['collection_groups'])
        q = {}
        limit = 0
        skip = 0
        if querydict.has_key('limit'):
            limit = int(querydict['limit'])
            del querydict['limit']
        if querydict.has_key('skip'):
            skip = int(querydict['skip'])
            del querydict['skip']
        if querydict.has_key('group_name'):
            if isinstance(querydict['group_name'], str) or isinstance(querydict['group_name'], unicode):
                q['group_name'] = querydict['group_name']
            if isinstance(querydict['group_name'], list):
                q['group_name'] = {'$in': querydict['group_name']}
            if isinstance(querydict['group_name'], dict):
                q['group_name'] = querydict['group_name']
        if querydict.has_key('_id'):
            if isinstance(querydict['_id'], str) or isinstance(querydict['_id'], unicode):
                q['_id'] = querydict['_id']
            if isinstance(querydict['_id'], list):
                q['_id'] = {'$in': querydict['_id']}
        ret = list(collection.find(db_util.add_mongo_id(q)).limit(limit).skip(skip))
        if querydict.has_key('user_detail') and querydict['user_detail'] is True:
            keys = gWebSocketsMap.keys()
            for i in ret:
                idx = ret.index(i)
                detail = []
                userlist = user_query(session, {'_id':i['members']})
                for j in userlist:
                    if j.has_key('contacts'):
                        del j['contacts']
                    if j.has_key('password'):
                        del j['password']
                    if str(j['_id']) in keys:
                        j['online_status'] = 'online'
                    else:
                        j['online_status'] = 'offline'
                    detail.append(j)
                ret[idx]['members'] = detail
        return ret
    
    def group_get(session, querydict):
        rec = group_query(session, querydict)
        if len(rec)>0:
            ret = json.dumps(db_util.remove_mongo_id(rec), ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'query_no_record'}, ensure_ascii=True, indent=4)
        return ret
    
    
    
    def user_group_get(session, querydict):
        ret = []
        collection = get_collection(gConfig['chat_platform']['mongodb']['collection_groups'])
        q = {}
        if querydict.has_key('username'):
            if isinstance(querydict['username'], str) or isinstance(querydict['username'], unicode) or isinstance(querydict['username'], dict):
                q['username'] = querydict['username']
        if querydict.has_key('_id'):
            if isinstance(querydict['_id'], str) or isinstance(querydict['_id'], unicode):
                q['_id'] = db_util.add_mongo_id(querydict['_id'])
        if len(q.keys())>0:
            users = user_query(session, querydict)
            if len(users)>0:
                user0 = users[0]
                _id = user0['_id']
                grps = group_query(session)
                for i in grps:
                    if i.has_key('members') and _id in i['members']:
                        ret.append(i)
                ret = json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'user_group_get_user_not_exist'}, ensure_ascii=True, indent=4)
                
        else:
            ret = json.dumps({'result':u'user_group_get_one_user_required'}, ensure_ascii=True, indent=4)
        return ret

    def all_user_get(session, querydict):
        limit = 0
        skip = 0
        filter_str = ''
        if querydict.has_key('user_detail') and querydict['user_detail'] is True:
            user_detail = True
            del querydict['user_detail']
        if querydict.has_key('limit'):
            try:
                limit = int(querydict['limit'])
            except:
                pass
            del querydict['limit']
        if querydict.has_key('skip'):
            try:
                skip = int(querydict['skip'])
            except:
                pass
            del querydict['skip']

        if querydict.has_key('filter'):
            filter_str = querydict['filter']
            del querydict['filter']

        contactlist = user_query(session, {'username':{'$regex': '^.*' + filter_str + '.*$'}, 'limit':limit, 'skip':skip})
        ret = []
        keys = gWebSocketsMap.keys()
        for i in contactlist:
            for k in i.keys():
                if not k in ['_id', 'username', 'display_name', 'avatar']:
                    del i[k]
            if str(i['_id']) in keys:
                i['online_status'] = 'online'
            else:
                i['online_status'] = 'offline'
            ret.append(i)
        ret = json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
        return ret

    
    def user_contact_get(session, querydict):
        ret = []
        collection = get_collection(gConfig['chat_platform']['mongodb']['collection_users'])
        q = {}
        if querydict.has_key('username'):
            if isinstance(querydict['username'], str) or isinstance(querydict['username'], unicode):
                q['username'] = querydict['username']
                del querydict['username']
        if querydict.has_key('_id'):
            if isinstance(querydict['_id'], str) or isinstance(querydict['_id'], unicode):
                q['_id'] = db_util.add_mongo_id(querydict['_id'])
                del querydict['_id']
        if len(q.keys())>0:
            contacts = []
            selfid = None
            rec = collection.find_one(q)
            if rec and rec.has_key('contacts'):
                # contacts = rec['contacts']
                contacts = [db_util.add_mongo_id(i) for i in rec['contacts']]
                ret = contacts
                selfid = rec['_id']
            limit = 0
            skip = 0
            user_detail = False

            if querydict.has_key('user_detail') and querydict['user_detail'] is True:
                user_detail = True
                del querydict['user_detail']
            if querydict.has_key('limit'):
                try:
                    limit = int(querydict['limit'])
                except:
                    pass
                del querydict['limit']
            if querydict.has_key('skip'):
                try:
                    skip = int(querydict['skip'])
                except:
                    pass
                del querydict['skip']

            if user_detail:
                if querydict.has_key('filter'):
                    contactlist = user_query(session, {'username':{'$regex': '^.*' + querydict['filter'] + '.*$'}, '_id': {'$in':contacts, '$ne':selfid}, 'limit':limit, 'skip':skip})
                    del querydict['filter']
                else:
                    contactlist = user_query(session, {'_id':contacts, 'limit':limit, 'skip':skip})
                ret = []
                keys = gWebSocketsMap.keys()
                for i in contactlist:
                    if i.has_key('contacts'):
                        del i['contacts']
                    if i.has_key('password'):
                        del i['password']
                    if str(i['_id']) in keys:
                        i['online_status'] = 'online'
                    else:
                        i['online_status'] = 'offline'
                    ret.append(i)
            ret = json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'user_contact_query_one_user_required'}, ensure_ascii=True, indent=4)
        return ret
        
    def user_get(session, querydict):
        ret = ''
        rec = user_query(session, querydict)
        for i in rec:
            idx = rec.index(i)
            if i.has_key('contacts'):
                del i['contacts']
            if i.has_key('password'):
                del i['password']
            rec[idx] = i
            
        if len(rec)>0:
            ret = json.dumps(db_util.remove_mongo_id(rec), ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'query_no_record'}, ensure_ascii=True, indent=4)
        return ret
    
    def user_add(session, querydict):
        ret = ''
        if querydict.has_key('username') and querydict.has_key('password') and len(querydict['username'])>0 and len(querydict['password'])>0:        
            try:
                collection = get_collection(gConfig['chat_platform']['mongodb']['collection_users'])
                existone = collection.find_one({'username':querydict['username']})
                if existone:
                    ret = json.dumps({'result':u'user_add_fail_username_already_exist'}, ensure_ascii=True, indent=4)
                else:
                    obj = {}
                    obj['username'] = querydict['username']
                    obj['display_name'] = querydict['username']
                    obj['password'] = querydict['password']
                    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    obj['register_date'] = ts
                    obj['update_date'] = ts
                    obj['description'] = ''
                    obj['person_info'] = {}
                    obj['contacts'] = []
                    obj['avatar'] = None
                    if querydict.has_key('person_info') :
                        obj['person_info'] = querydict['person_info']
                    if querydict.has_key('contacts') and isinstance(querydict['contacts'], list):
                        obj['contacts'] = querydict['contacts']
                    if querydict.has_key('avatar') and len(querydict['avatar']) > 0:
                        obj['avatar'] = querydict['avatar']
                    _id = collection.save(db_util.add_mongo_id(obj))
                    rec = collection.find_one({'_id':_id})
                    ret = json.dumps(db_util.remove_mongo_id(rec), ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'user_add_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'user_add_fail' }, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'user_add_fail_username_password_required'}, ensure_ascii=True, indent=4)
        return ret
    
    def user_update(session, querydict):
        ret = ''
        if querydict.has_key('_id') and len(querydict['_id'])>0:
            try:
                _id = db_util.add_mongo_id(querydict['_id'])
                collection = get_collection(gConfig['chat_platform']['mongodb']['collection_users'])
                existone = collection.find_one({'_id':_id})
                if existone:
                    del querydict['_id']
                    querydict['update_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    collection.update({'_id':existone['_id']}, {'$set': db_util.add_mongo_id(querydict)}, multi=False, upsert=False)
                    one = collection.find_one({'_id':_id})
                    ret = json.dumps(db_util.remove_mongo_id(one), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'user_update_user_not_exist'}, ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'user_update_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'user_update_fail' }, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'user_update_fail_user_id_required'}, ensure_ascii=True, indent=4)
        return ret

    def user_delete(session, querydict):
        ret = ''
        if querydict.has_key('_id') and len(querydict['_id'])>0:
            try:
                collection = get_collection(gConfig['chat_platform']['mongodb']['collection_users'])
                existone = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
                if existone:
                    collection.remove({'_id':existone['_id']})
                    ret = json.dumps(db_util.remove_mongo_id(existone), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'user_remove_user_not_exist'}, ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'user_remove_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'user_remove_fail' }, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'user_remove_fail_user_id_required'}, ensure_ascii=True, indent=4)
        return ret


    def group_add(session, querydict):
        ret = ''
        if querydict.has_key('owner_id')\
           and len(querydict['owner_id']) > 0\
           and querydict.has_key('group_name')\
           and len(querydict['group_name']) > 0:        
            try:
                collection = get_collection(gConfig['chat_platform']['mongodb']['collection_groups'])
                existone = collection.find_one({'group_name':querydict['group_name']})
                if existone:
                    ret = json.dumps({'result':u'group_add_fail_group_name_already_exist'}, ensure_ascii=True, indent=4)
                else:
                    obj = {}
                    obj['owner_id'] = querydict['owner_id']
                    obj['group_name'] = querydict['group_name']
                    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    obj['found_date'] = ts
                    obj['update_date'] = ts
                    obj['members'] = [db_util.add_mongo_id(obj['owner_id']), ]
                    if querydict.has_key('avatar') and len(querydict['avatar']) > 0:
                        obj['avatar'] = querydict['avatar']
                    if querydict.has_key('description') and len(querydict['description']) > 0:
                        obj['description'] = querydict['description']
                    _id = collection.save(db_util.add_mongo_id(obj))
                    rec = collection.find_one({'_id':_id})
                    ret = json.dumps(db_util.remove_mongo_id(rec), ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'group_add_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'group_add_fail' }, ensure_ascii=True, indent=4)
        else:
            if not querydict.has_key('owner_id') or len(querydict['owner_id']) == 0:
                ret = json.dumps({'result':u'group_add_fail_owner_id_required'}, ensure_ascii=True, indent=4)
            if not querydict.has_key('group_name') or len(querydict['group_name']) == 0:
                ret = json.dumps({'result':u'group_add_fail_group_name_required'}, ensure_ascii=True, indent=4)
        return ret

    def group_update(session, querydict):
        ret = ''
        if querydict.has_key('_id') and len(querydict['_id'])>0:
            try:
                _id = db_util.add_mongo_id(querydict['_id'])
                collection = get_collection(gConfig['chat_platform']['mongodb']['collection_groups'])
                existone = collection.find_one({'_id':_id})
                if existone:
                    del querydict['_id']
                    querydict['update_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    collection.update({'_id':existone['_id']}, {'$set': db_util.add_mongo_id(querydict)}, multi=False, upsert=False)
                    one = collection.find_one({'_id':_id})
                    ret = json.dumps(db_util.remove_mongo_id(one), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'group_update_group_not_exist'}, ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'group_update_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'group_update_fail' }, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'group_update_fail_group_id_required'}, ensure_ascii=True, indent=4)
        return ret

    def group_remove(session, querydict):
        ret = ''
        if querydict.has_key('_id') and len(querydict['_id']) > 0:
            try:
                collection = get_collection(gConfig['chat_platform']['mongodb']['collection_groups'])
                existone = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
                if existone:
                    collection.remove({'_id':existone['_id']})
                    ret = json.dumps(db_util.remove_mongo_id(existone), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'group_remove_fail_group_not_exist'}, ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'group_remove_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'group_remove_fail' }, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'group_remove_fail_found_group_id_required'}, ensure_ascii=True, indent=4)
        return ret

    
    def check_contact_exist(_id, alist):
        ret = None
        for i in alist:
            if i['_id'] == _id:
                ret = i
                break
        return ret
    

    def online(user_id, websocket):
        if user_id and websocket and not websocket.closed:
            if not gWebSocketsMap.has_key(user_id):
                gWebSocketsMap[user_id] = []
            if not websocket in gWebSocketsMap[user_id]:
                gWebSocketsMap[user_id].append(websocket)
    def offline(user_id):
        if user_id and gWebSocketsMap.has_key(user_id):
            for i in gWebSocketsMap[user_id]:
                i.close()
            del gWebSocketsMap[user_id]
            chat_save_log({
                'op':'chat/offline',
                'from':user_id,
                'timestamp':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            })

    def get_destination(session, from_id, _id):
        ret = []
        if isinstance(_id, str) or isinstance(_id, unicode):
            userlist = user_query(session, {'_id':from_id})
            if len(userlist)==0:
                userlist = user_query(session, {'username':from_id})
            if len(userlist)>0:
                user0 = userlist[0]
                if user0.has_key('contacts'):
                    toid = _id
                    try:
                        toid = ObjectId(_id)
                    except:
                        ul = user_query(session, {'username':_id})
                        if len(ul)>0:
                            toid = ul[0]['_id']
                    if db_util.add_mongo_id(str(toid)) in user0['contacts']:
                        ret.append(str(toid))
        elif isinstance(_id, list):
            userlist = user_query(session, {'_id':from_id})
            if len(userlist)==0:
                userlist = user_query(session, {'username':from_id})
            if len(userlist)>0:
                user0 = userlist[0]
                if user0.has_key('contacts'):
                    for id in _id:
                        if db_util.add_mongo_id(id) in user0['contacts']:
                            ret.append(id)
        return ret
    def get_destination_group(session, from_id, _id):
        ret = []
        userset = set()
        grps = group_query(session, {'_id':_id})
        for grp in grps:
            if grp.has_key('members') and len(grp['members'])>0:
                if db_util.add_mongo_id(from_id) in grp['members']:
                    userset = userset.union(set(grp['members']))
        userlist = list(userset)
        for id in userlist:
            ret.append(id)
        return ret
                
    def resend_offline_msg(session, to_id, limit=10):
        offlinecol = 'chat_log_offline'
        if gConfig['chat_platform']['mongodb'].has_key('collection_chat_log_offline'):
            offlinecol = gConfig['chat_platform']['mongodb']['collection_chat_log_offline']
        collection = get_collection(offlinecol)
        arr = list(collection.find({'to':db_util.add_mongo_id(to_id)}).limit(limit).sort('timestamp', pymongo.DESCENDING))
        ids = [i['_id'] for i in arr]
        collection.remove({'_id':{'$in': ids}})
        for i in arr:
            gJoinableQueue.put(db_util.remove_mongo_id(i))

            
    def chat(session, websocket, obj={}):
        tolist = []
        if obj.has_key('from') and len(obj['from'])>0 and obj.has_key('msg') and len(obj['msg'])>0:
            if obj.has_key('to') and len(obj['to'])>0:
                tolist = get_destination(session,  obj['from'], obj['to'])
            if obj.has_key('to_group') and len(obj['to_group']) > 0:
                tolist = get_destination_group(session, obj['from'], obj['to_group'])
            for k in tolist:
                try:
                    d  = {'op': 'chat/chat', 'from': obj['from'], 'to': k, 'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'msg': obj['msg']}
                    gJoinableQueue.put(d)
                except gevent.queue.Full:
                    print('chat queue is full')
                    
    def request_response(session, websocket, obj={}):
        #'chat/request/contact/add', 
        #'chat/request/contact/remove', 
        #'chat/response/contact/add/accept', 
        #'chat/response/contact/add/reject'
        #'chat/request/group/join'
        #'chat/request/group/quit'
        #'chat/response/group/join/accept', 
        #'chat/response/group/join/reject', 
        tolist = []
        try:
            if obj['op'] == 'chat/response/contact/add/accept':
                if obj.has_key('from') and len(obj['from'])>0 and obj.has_key('to') and len(obj['to'])>0:
                    collection = get_collection(gConfig['chat_platform']['mongodb']['collection_users'])
                    userlist = user_query(session, {'_id':[obj['from'],  obj['to']]})
                    for user in userlist:
                        if str(user['_id']) == obj['from'] and not db_util.add_mongo_id(obj['to']) in user['contacts']:
                            user['contacts'].append(db_util.add_mongo_id(obj['to']))
                        if str(user['_id']) == obj['to'] and not db_util.add_mongo_id(obj['from']) in user['contacts']:
                            user['contacts'].append(db_util.add_mongo_id(obj['from']))
                        user['update_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        collection.save(user)
                    
                    fromuser = {}
                    fromuser['op'] = obj['op']
                    fromuser['_id'] = obj['from']
                    fromuser['from'] = obj['to']
                    fromuser['to'] = obj['from']
                    fromuser['contacts'] = json.loads(user_contact_get(session, {'_id':obj['from'],'user_detail':True}))
                    gJoinableQueue.put(db_util.remove_mongo_id(fromuser))
                    
                    touser = {}
                    touser['op'] = obj['op']
                    touser['_id'] = obj['to']
                    touser['from'] = obj['from']
                    touser['to'] = obj['to']
                    touser['contacts'] = json.loads(user_contact_get(session, {'_id':obj['to'],'user_detail':True}))
                    gJoinableQueue.put(db_util.remove_mongo_id(touser))
                        
            elif obj['op'] == 'chat/response/contact/add/reject':
                if obj.has_key('from') and len(obj['from'])>0 and obj.has_key('to') and len(obj['to'])>0:
                    userlist = user_query(session, {'_id':obj['from']})
                    if len(userlist)>0:
                        user0 = userlist[0]
                        user0['op'] = obj['op']
                        user0['from'] = obj['from']
                        user0['to'] = obj['to']
                        if user0.has_key('password'):
                            del user0['password']
                        if user0.has_key('contacts'):
                            del user0['contacts']
                        if obj.has_key('reject_reason') and len(obj['reject_reason'])>0:
                            user0['reject_reason'] = obj['reject_reason']
                        gJoinableQueue.put(db_util.remove_mongo_id(user0))
            elif obj['op'] == 'chat/request/contact/add':
                if obj.has_key('from') and len(obj['from'])>0 and obj.has_key('to') and len(obj['to'])>0:
                    userlist = user_query(session, {'_id':obj['from']})
                    if len(userlist)>0:
                        user0 = userlist[0]
                        user0['op'] = obj['op']
                        user0['from'] = obj['from']
                        user0['to'] = obj['to']
                        if user0.has_key('password'):
                            del user0['password']
                        if user0.has_key('contacts'):
                            del user0['contacts']
                        gJoinableQueue.put(db_util.remove_mongo_id(user0))
                
            elif obj['op'] == 'chat/request/contact/remove':
                if obj.has_key('from') and len(obj['from'])>0 and obj.has_key('to') and len(obj['to'])>0:
                    collection = get_collection(gConfig['chat_platform']['mongodb']['collection_users'])
                    userlist = user_query(session, {'_id':[obj['from'],  obj['to']]})
                    remover, removee = None, None
                    for user in userlist:
                        if str(user['_id']) == obj['from'] and db_util.add_mongo_id(obj['to']) in user['contacts']:
                            user['contacts'].remove(db_util.add_mongo_id(obj['to']))
                            remover = user['display_name']
                        if str(user['_id']) == obj['to'] and db_util.add_mongo_id(obj['from']) in user['contacts']:
                            user['contacts'].remove(db_util.add_mongo_id(obj['from']))
                            removee = user['display_name']
                        user['update_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        collection.save(user)
                        
                    fromuser = {}
                    fromuser['op'] = obj['op']
                    fromuser['_id'] = obj['from']
                    fromuser['from'] = obj['to']
                    fromuser['to'] = obj['from']
                    fromuser['remover'] = remover
                    fromuser['removee'] = removee
                    fromuser['remove_type'] = 'remover'
                    fromuser['contacts'] = json.loads(user_contact_get(session, {'_id':obj['from'], 'user_detail':True}))
                    gJoinableQueue.put(db_util.remove_mongo_id(fromuser))
                    
                    touser = {}
                    touser['op'] = obj['op']
                    touser['_id'] = obj['to']
                    touser['from'] = obj['from']
                    touser['to'] = obj['to']
                    touser['remover'] = remover
                    touser['removee'] = removee
                    touser['remove_type'] = 'removee'
                    touser['contacts'] = json.loads(user_contact_get(session, {'_id':obj['to'], 'user_detail':True}))
                    gJoinableQueue.put(db_util.remove_mongo_id(touser))
                    
            elif obj['op'] == 'chat/request/group/join':
                if obj.has_key('from') and len(obj['from'])>0 and obj.has_key('to_group') and len(obj['to_group'])>0:
                    grps = group_query(session, {'_id':obj['to_group']})
                    if len(grps)>0:
                        grp0 = grps[0]
                        userlist = user_query(session, {'_id':obj['from']})
                        if len(userlist)>0:
                            user0 = userlist[0]
                            user0['op'] = obj['op']
                            user0['from'] = obj['from']
                            user0['request_src'] = obj['from']
                            user0['to_group'] = obj['to_group']
                            user0['to'] = grp0['owner_id']
                            if user0.has_key('password'):
                                del user0['password']
                            if user0.has_key('contacts'):
                                del user0['contacts']
                            gJoinableQueue.put(db_util.remove_mongo_id(user0))
            elif obj['op'] == 'chat/request/group/quit':
                if obj.has_key('from') and len(obj['from'])>0 and obj.has_key('to_group') and len(obj['to_group'])>0:
                    grps = group_query(session, {'_id':obj['to_group']})
                    if len(grps)>0:
                        grp0 = grps[0]
                        members = []
                        if db_util.add_mongo_id(obj['from']) in grp0['members']:
                            grp0['members'].remove(db_util.add_mongo_id(obj['from']))
                            members = [str(i) for i in grp0['members']]
                            collection = get_collection(gConfig['chat_platform']['mongodb']['collection_groups'])
                            collection.save(grp0)
                            broadcast(session, websocket, members, {'op':obj['op'], 'from':obj['from'], 'to_group':obj['to_group']}  )
            elif obj['op'] == 'chat/response/group/join/accept':
                if obj.has_key('to_group') and len(obj['to_group'])>0 and obj.has_key('request_src') and len(obj['request_src'])>0:
                    grps = group_query(session, {'_id': obj['to_group']})
                    if len(grps)>0:
                        grp0 = grps[0]
                        if not db_util.add_mongo_id(obj['request_src']) in grp0['members']:
                            grp0['members'].append(db_util.add_mongo_id(obj['request_src']))
                            collection = get_collection(gConfig['chat_platform']['mongodb']['collection_groups'])
                            collection.save(grp0)
                            members = [str(i) for i in grp0['members']]
                            broadcast(session, websocket, members, obj)
            elif obj['op'] == 'chat/response/group/join/reject':
                if obj.has_key('from') and len(obj['from'])>0 and obj.has_key('to') and len(obj['to'])>0 and obj.has_key('to_group') and len(obj['to_group'])>0:
                    userlist = user_query(session, {'_id':obj['from']})
                    if len(userlist)>0:
                        user0 = userlist[0]
                        user0['op'] = obj['op']
                        user0['from'] = obj['from']
                        user0['to'] = obj['to']
                        user0['to_group'] = obj['to_group']
                        if user0.has_key('password'):
                            del user0['password']
                        if user0.has_key('contacts'):
                            del user0['contacts']
                        if obj.has_key('reject_reason') and len(obj['reject_reason'])>0:
                            user0['reject_reason'] = obj['reject_reason']
                        gJoinableQueue.put(db_util.remove_mongo_id(user0))
            #else:        
                #d  = {'op': obj['op'], 'from':obj['from'], 'to':k, 'timestamp':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),}
                #gJoinableQueue.put(d)
        except gevent.queue.Full:
            print('chat queue is full')
                    
    def broadcast(session, websocket, alist, obj={}):
        for i in alist:
            d = {}
            #d['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            for k in obj.keys():
                d[k] = obj[k]
            if isinstance(i, str) or isinstance(i, unicode):
                d['to'] = i
            elif isinstance(i, dict):
                if i.has_key('_id'):
                    d['to'] = i['_id']
            try:
                gJoinableQueue.put(d)
            except:
                pass
        
        
    def handle_websocket(environ):
        ws = get_websocket(environ)
        app = gConfig['wsgi']['application']
        #session_id = None
        #channel = ''
        #if environ.has_key('HTTP_COOKIE'):
            #arr = environ['HTTP_COOKIE'].split('=')
            #if len(arr)>1:
                #session_id = arr[1]
        interval = 1.0
        try:
            interval = float(gConfig[app]['websocket']['interval_poll'])
        except:
            interval = 1.0
        while ws and not ws.closed:
            obj = ws_recv(environ)
            if obj and isinstance(obj, dict) and obj.has_key('op'):
                if obj['op'] == 'queue_size':
                    qsize = 0
                    if gJoinableQueue:
                        qsize = gJoinableQueue.qsize()
                    ws.send(json.dumps({'queue_size':qsize}, ensure_ascii=True, indent=4))
                elif obj['op'] == 'chat/online':
                    rec = []
                    if obj.has_key('_id') and len(obj['_id'])>0:
                        rec = user_query(session, {'_id':obj['_id']})
                    elif obj.has_key('username') and len(obj['username'])>0:
                        rec = user_query(session, {'username':obj['username']})
                    if len(rec)>0:
                        r0 = rec[0]
                        _id = str(r0['_id'])
                        online(_id, ws)
                        r0['contacts'] = json.loads(user_contact_get(session, {'_id':_id,'user_detail':True}))
                        r0['groups'] = json.loads(user_group_get(session, {'_id':_id,'user_detail':True}))
                        d = db_util.remove_mongo_id(r0)
                        d['op'] = obj['op']
                        d['from'] = _id
                        d['to'] = _id
                        d['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        gJoinableQueue.put(d)
                        #ws.send(json.dumps(d, ensure_ascii=True, indent=4))
                        if obj.has_key('inform_contact') and obj['inform_contact'] is True:
                            other_contacts = gWebSocketsMap.keys()[:]
                            if _id in other_contacts:
                                other_contacts.remove(_id)
                            broadcast(session, ws, other_contacts, {'op':'chat/info/online','from':_id})
                        limit = 10
                        if gConfig['chat_platform'].has_key('resend') and  gConfig['chat_platform']['resend'].has_key('max_resend_record_num'):
                            try:
                                limit = int(gConfig['chat_platform']['resend']['max_resend_record_num'])
                            except:
                                pass
                        resend_offline_msg(session, _id, limit)
                    else:
                        ws.send(json.dumps({'result':'chat_online_user_not_exist'}, ensure_ascii=True, indent=4))
                elif obj['op'] == 'chat/offline':
                    if obj.has_key('_id'):
                        _id = obj['_id']
                        if obj.has_key('inform_contact') and obj['inform_contact'] is True:
                            other_contacts = gWebSocketsMap.keys()[:]
                            if _id in other_contacts:
                                other_contacts.remove(_id)
                            broadcast(session, ws, other_contacts,  {'op':'chat/info/offline','from':_id, 'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
                        offline(_id)
                    elif obj.has_key('username'):
                        rec = user_query(session, {'username':obj['username']})
                        if len(rec)>0:
                            _id = str(rec[0]['_id'])
                            if obj.has_key('inform_contact') and obj['inform_contact'] is True:
                                other_contacts = gWebSocketsMap.keys()[:]
                                if _id in other_contacts:
                                    other_contacts.remove(_id)
                                broadcast(session, ws, other_contacts, {'op':'chat/info/offline','from':_id})
                            offline(_id)
                        else:
                            ws.send(json.dumps({'result':'chat_offline_user_not_exist'}, ensure_ascii=True, indent=4))
                    else:
                        ws.send(json.dumps({'result':'chat_offline_username_or_id_required'}, ensure_ascii=True, indent=4))
                elif obj['op'] == 'chat/chat':
                    chat(session, ws, obj)
                elif 'chat/request' in obj['op'] or 'chat/response' in obj['op']:
                    request_response(session, ws, obj)
            else:
                try:
                    ws.send('')
                except:
                    _id = None
                    for k in gWebSocketsMap.keys():
                        if ws in gWebSocketsMap[k] :
                            _id = k
                            break
                    if _id:
                        print('websocket[%s] is closed2' % _id)
                        offline(_id)
                        broadcast(session, None, gWebSocketsMap.keys(), {'op':'chat/info/offline', 'from':_id})
            gevent.sleep(interval)
        if ws and ws.closed:
            del ws
            
    def check_url_token(querydict):
        is_token_pass = False
        enable_url_md5_check = False
        md5prefix = ''
        if gConfig['chat_platform'].has_key('security') \
           and gConfig['chat_platform']['security'].has_key('md5prefix'):
            md5prefix = str(gConfig['chat_platform']['security']['md5prefix'])

        if gConfig['chat_platform'].has_key('security') \
           and gConfig['chat_platform']['security'].has_key('enable_url_md5_check') \
           and gConfig['chat_platform']['security']['enable_url_md5_check'].lower() == 'true':
            enable_url_md5_check = True
        else:
            is_token_pass = True
        if enable_url_md5_check:
            print('checking token...')
            if querydict.has_key('_token'):
                plain = '%s_|_%s' % (md5prefix, time.strftime('%Y%m%d%H'))
                token = md5.new(plain).hexdigest()
                if token == str(querydict['_token']):
                    is_token_pass = True
        return is_token_pass

    def chat_broadcast(session, querydict):
        ret = '{}'
        tolist = []
        if querydict.has_key('from') and len(querydict['from'])>0:
            if querydict.has_key('to'):
                if isinstance(querydict['to'], str) or isinstance(querydict['to'], unicode):
                    tolist.append(querydict['to'])
                if isinstance(querydict['to'], list):
                    tolist.extend(querydict['to'])
            else:
                ret = json.dumps({'result':u'chat_broadcast_to_required'}, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'chat_broadcast_from_required'}, ensure_ascii=True, indent=4)
        if querydict.has_key('msg') and len(querydict['msg'])>0:
            for k in tolist:
                try:
                    d  = {'op': 'chat/chat', 'from': querydict['from'], 'to': k, 'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'msg': querydict['msg']}
                    gJoinableQueue.put(d)
                except gevent.queue.Full:
                    print('chat queue is full')
                    ret = json.dumps({'result':u'chat queue is full'}, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'chat_broadcast_msg_required'}, ensure_ascii=True, indent=4)
        return ret

    def chat_log_query(session, querydict):
        limit = 0
        skip = 0
        filter_str = ''
        from_id, to_id = None, None
        if querydict.has_key('from') and (isinstance(querydict['from'], str) or isinstance(querydict['from'], unicode)) and len(querydict['from'])>0:
            from_id = querydict['from']
        if querydict.has_key('to') and (isinstance(querydict['to'], str) or isinstance(querydict['to'], unicode)) and len(querydict['to'])>0:
            to_id = querydict['to']
        if from_id is None or to_id is None:
            return json.dumps({'result':u'chat_log_query_from_and_to_required'}, ensure_ascii=True, indent=4)
        if querydict.has_key('limit'):
            try:
                limit = int(querydict['limit'])
            except:
                pass
            del querydict['limit']
        if querydict.has_key('skip'):
            try:
                skip = int(querydict['skip'])
            except:
                pass
            del querydict['skip']

        if querydict.has_key('filter'):
            filter_str = querydict['filter']
            del querydict['filter']

        # offlinecol = 'chat_log_offline'
        # if gConfig['chat_platform']['mongodb'].has_key('collection_chat_log_offline'):
        #     offlinecol = gConfig['chat_platform']['mongodb']['collection_chat_log_offline']

        collection1 = get_collection(gConfig['chat_platform']['mongodb']['collection_chat_log'])
        # collection2 = get_collection(offlinecol)
        ret = list(collection1.find({'$or':[{'from':db_util.add_mongo_id(from_id), 'to':db_util.add_mongo_id(to_id)}, {'to':db_util.add_mongo_id(from_id), 'from':db_util.add_mongo_id(to_id)}]}).limit(limit).skip(skip).sort('timestamp', pymongo.DESCENDING))
        # arr2 = list(collection2.find({'$or':[{'from':db_util.add_mongo_id(from_id), 'to':db_util.add_mongo_id(to_id)}, {'to':db_util.add_mongo_id(from_id), 'from':db_util.add_mongo_id(to_id)}]}).limit(limit).skip(skip).sort('timestamp', pymongo.DESCENDING))
        ret = json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
        return ret

    def chat_log_remove(session, querydict):
        return ''

    
    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    statuscode = '200 OK'
    body = ''
    isnew = False
    urls = gUrlMap.bind_to_environ(environ)
    querydict, buf = get_querydict_by_GET_POST(environ)
    endpoint = ''
    try:
        endpoint, args = urls.match()
        if endpoint not in ['handle_websocket', 'gridfs_upload', 'gridfs_get', 'gridfs_delete', 'gridfs_query']:
            if not check_url_token(querydict):
                body = json.dumps({'result':u'invalid_token'}, ensure_ascii=True, indent=4)
                return statuscode, headers, body
        if querydict.has_key('_token'):
            del querydict['_token']

        if endpoint == 'user_add':
            body = user_add(session, querydict)
        elif endpoint == 'user_remove':
            body = user_delete(session, querydict)
        elif endpoint == 'user_get':
            body = user_get(session, querydict)
        elif endpoint == 'all_user_get':
            body = all_user_get(session, querydict)
        elif endpoint == 'user_update':
            body = user_update(session, querydict)
        elif endpoint == 'group_add':
            body = group_add(session, querydict)
        elif endpoint == 'group_get':
            body = group_get(session, querydict)
        elif endpoint == 'user_group_get':
            body = user_group_get(session, querydict)
        elif endpoint == 'user_contact_get':
            body = user_contact_get(session, querydict)
        elif endpoint == 'group_update':
            body = group_update(session, querydict)
        elif endpoint == 'group_remove':
            body = group_remove(session, querydict)
        elif endpoint == 'handle_websocket':
            handle_websocket(environ)
        elif endpoint == 'chat_broadcast':
            body = chat_broadcast(session, querydict)
        elif endpoint == 'chat_log_query':
            body = chat_log_query(session, querydict)
        elif endpoint == 'chat_log_remove':
            body = chat_log_remove(session, querydict)
        elif endpoint == 'gridfs_upload':
            body = gridfs_upload(environ, querydict, buf)
        elif endpoint == 'gridfs_get':
            if args.has_key('_id'):
                querydict['_id'] = args['_id']
            if args.has_key('width'):
                try:
                    querydict['width'] = int(args['width'])
                except:
                    querydict['width'] = 64
            if args.has_key('height'):
                try:
                    querydict['height'] = int(args['height'])
                except:
                    querydict['height'] = 64
            statuscode, headers, body = gridfs_get(environ, querydict)
        elif endpoint == 'gridfs_delete':
            if args.has_key('_id'):
                querydict['_id'] = args['_id']
            statuscode, headers, body = gridfs_delete(environ, querydict)
        elif endpoint == 'gridfs_query':
            if querydict.has_key('_id'):
                if isinstance(querydict['_id'], str) or isinstance(querydict['_id'], unicode):
                    if ',' in querydict['_id']:
                        querydict['_id'] = querydict['_id'].split(',')
                    else:
                        querydict['_id'] = [querydict['_id'],]
            if args.has_key('width'):
                try:
                    querydict['width'] = int(args['width'])
                except:
                    querydict['width'] = 64
            if args.has_key('height'):
                try:
                    querydict['height'] = int(args['height'])
                except:
                    querydict['height'] = 64
            if args.has_key('limit'):
                try:
                    querydict['limit'] = int(args['limit'])
                except:
                    querydict['limit'] = 10
            if args.has_key('skip'):
                try:
                    querydict['skip'] = int(args['skip'])
                except:
                    querydict['skip'] = 0
            statuscode, headers, body = gridfs_query(environ, querydict)

        else:
            body = json.dumps({'result':u'access_deny'}, ensure_ascii=True, indent=4)

    except HTTPException, e:
        body = json.dumps({'result':u'access_deny'}, ensure_ascii=True, indent=4)
    if session:
        gSessionStore.save(session)
    return statuscode, headers, body

def gridfs_get(environ, querydict):
    global gConfig, ENCODING, STATICRESOURCE_DIR
    def thumbnail(fp, size, use_base64=False):
        ret = None
        if 'image/' in fp.mimetype:
            im = Image.open(fp)
            im.thumbnail(size)
            buf = StringIO.StringIO()
            #print(im.format)
            im.save(buf, im.format)
            ret = buf.getvalue()
            if use_base64:
                ret = base64.b64encode(ret)
        if 'application/' in fp.mimetype or 'text/' in fp.mimetype:
            thumpath = gConfig['web']['thumbnail']['application/octet-stream']
            if gConfig['web']['thumbnail'].has_key(fp.mimetype):
                thumpath = gConfig['web']['thumbnail'][fp.mimetype]
            thumpath = os.path.join(STATICRESOURCE_DIR, 'img', 'thumbnail', thumpath)
            im = Image.open(thumpath)
            im.thumbnail(size)
            buf = StringIO.StringIO()
            im.save(buf, im.format)
            ret = buf.getvalue()
            if use_base64:
                ret = base64.b64encode(ret)
        return ret


    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    body = ''
    statuscode = '200 OK'
    if querydict.has_key('_'):
        del querydict['_']
    if querydict.has_key('_random'):
        del querydict['_random']
    if not querydict.has_key('_id'):
        body = json.dumps({'result': u'gridfs_get_id_required'}, ensure_ascii=True, indent=4)
        return statuscode, headers, body

    app = gConfig['wsgi']['application']
    if gConfig.has_key(app):
        collection = 'fs'
        if gConfig[app].has_key('mongodb') and gConfig[app]['mongodb'].has_key('gridfs_collection'):
            collection = str(gConfig[app]['mongodb']['gridfs_collection'])
        if len(collection) == 0:
            collection = 'fs'
        db_util.mongo_init_client(app)
        dbname = gConfig[app]['mongodb']['database']
        db = db_util.gClientMongo[app][dbname]
        fs = gridfs.GridFS(db, collection=collection)
        _id = db_util.add_mongo_id(querydict['_id'])
        try:
            f = fs.get(_id)
            headers['Content-Type'] = str(f.content_type)
            if querydict.has_key('width') and querydict.has_key('height') \
                and querydict['width']>0 and querydict['width']<8192 \
                and querydict['height']>0 and querydict['height']<8192 :
                if 'image/' in f.content_type:
                    body = thumbnail(f, (querydict['width'], querydict['height']), False)
                else:
                    body = thumbnail(f, (128, 128), False)
                    headers['Content-Type'] = 'image/png'
                if body is None:
                    body = json.dumps({'result': u'gridfs_get_error_invalid_image_format'}, ensure_ascii=True, indent=4)
            else:
                body = f.read()
                if querydict.has_key('attachmentdownload'):
                    headers['Content-Disposition'] = 'attachment;filename="' + enc(f.filename) + '"'

        except gridfs.errors.NoFile:
            body = json.dumps({'result': u'gridfs_get_file_not_exist'}, ensure_ascii=True, indent=4)
        except Exception,e:
            headers['Content-Type'] = 'text/json;charset=' + ENCODING
            body = json.dumps({'result': u'gridfs_get_error:%s' % e.message}, ensure_ascii=True, indent=4)
    else:
        body = json.dumps({'result': u'gridfs_get_cannot_find_wsgi_app [%s]' % app}, ensure_ascii=True, indent=4)
    return statuscode, headers, body

def gridfs_delete(environ, querydict):
    global gConfig, ENCODING

    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    body = ''
    statuscode = '200 OK'
    if querydict.has_key('_'):
        del querydict['_']
    if querydict.has_key('_random'):
        del querydict['_random']
    if not querydict.has_key('_id'):
        body = json.dumps({'result': u'gridfs_delete_id_required'}, ensure_ascii=True, indent=4)
        return statuscode, headers, body
    app = gConfig['wsgi']['application']
    if gConfig.has_key(app):
        collection = 'fs'
        if gConfig[app].has_key('mongodb') and gConfig[app]['mongodb'].has_key('gridfs_collection'):
            collection = str(gConfig[app]['mongodb']['gridfs_collection'])
        if len(collection) == 0:
            collection = 'fs'
        db_util.mongo_init_client(app)
        dbname = gConfig[app]['mongodb']['database']
        db = db_util.gClientMongo[app][dbname]
        fs = gridfs.GridFS(db, collection=collection)
        arr = querydict['_id'].split(',')
        ids = []
        for i in arr:
            ids.append(db_util.add_mongo_id(i))
        try:
            for i in ids:
                fs.delete(i)
            body = json.dumps(querydict, ensure_ascii=True, indent=4)
        except Exception,e:
            body = json.dumps({'result': u'gridfs_delete_error:%s' % e.message}, ensure_ascii=True, indent=4)
    else:
        body = json.dumps({'result': u'gridfs_delete_cannot_find_wsgi_app [%s]' % app}, ensure_ascii=True, indent=4)
    return statuscode, headers, body


def gridfs_query(environ, querydict):
    global gConfig, ENCODING, STATICRESOURCE_DIR
    def thumbnail(fp, size, use_base64=False):
        ret = None
        if 'image/' in fp.mimetype:
            im = Image.open(fp)
            im.thumbnail(size)
            buf = StringIO.StringIO()
            #print(im.format)
            im.save(buf, im.format)
            ret = buf.getvalue()
            if use_base64:
                ret = base64.b64encode(ret)
        if 'application/' in fp.mimetype or 'text/' in fp.mimetype:
            thumpath = gConfig['web']['thumbnail']['application/octet-stream']
            if gConfig['web']['thumbnail'].has_key(fp.mimetype):
                thumpath = gConfig['web']['thumbnail'][fp.mimetype]
            thumpath = os.path.join(STATICRESOURCE_DIR, 'img', 'thumbnail', thumpath)
            im = Image.open(thumpath)
            im.thumbnail(size)
            buf = StringIO.StringIO()
            im.save(buf, im.format)
            ret = buf.getvalue()
            if use_base64:
                ret = base64.b64encode(ret)
        return ret


    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    body = '[]'
    statuscode = '200 OK'
    app = gConfig['wsgi']['application']
    if querydict.has_key('_'):
        del querydict['_']
    if querydict.has_key('_random'):
        del querydict['_random']
    if gConfig.has_key(app):
        collection = 'fs'
        if gConfig[app].has_key('mongodb') and gConfig[app]['mongodb'].has_key('gridfs_collection'):
            collection = str(gConfig[app]['mongodb']['gridfs_collection'])
        if len(collection) == 0:
            collection = 'fs'
        db_util.mongo_init_client(app)
        dbname = gConfig[app]['mongodb']['database']
        db = db_util.gClientMongo[app][dbname]
        fs = gridfs.GridFS(db, collection=collection)
        limit = 10
        skip = 0
        if  querydict.has_key('limit'):
            limit = querydict['limit']
            del querydict['limit']
        if  querydict.has_key('skip'):
            skip = querydict['skip']
            del querydict['skip']
        try:
            if querydict.has_key('width') and querydict.has_key('height') \
                and querydict['width']>0 and querydict['width']<8192 \
                and querydict['height']>0 and querydict['height']<8192 :
                w, h = querydict['width'], querydict['height']
                del querydict['width']
                del querydict['height']
                cur = None
                if querydict.has_key('_id'):
                    ids = db_util.add_mongo_id(querydict['_id'])
                    cur = fs.find({'_id':{'$in':ids}}).limit(limit).skip(skip)
                else:
                    cur = fs.find(db_util.add_mongo_id(querydict)).limit(limit).skip(skip)
                arr = []
                for f in cur:
                    b64str = thumbnail(f, (w, h), True)
                    if 'application/' in f.content_type:
                        f.mimetype = 'image/png'
                    arr.append({'_id':db_util.remove_mongo_id(f._id), 'mimetype':f.mimetype,'filename':enc(f.filename), 'data': b64str})
                body = json.dumps(arr, ensure_ascii=True, indent=4)
            else:
                 body = json.dumps({'result': u'gridfs_query_size_required'}, ensure_ascii=True, indent=4)
        except gridfs.errors.NoFile:
            body = json.dumps({'result': u'gridfs_query_file_not_exist'}, ensure_ascii=True, indent=4)
        except Exception,e:
            body = json.dumps({'result': u'gridfs_query_error:%s' % e.message}, ensure_ascii=True, indent=4)
    else:
        body = json.dumps({'result': u'gridfs_query_cannot_find_wsgi_app [%s]' % app}, ensure_ascii=True, indent=4)
    return statuscode, headers, body



def gridfs_upload(environ, querydict, buf):
    global gConfig
    app = gConfig['wsgi']['application']
    body = ''
    if gConfig.has_key(app):
        collection = 'fs'
        if gConfig[app].has_key('mongodb') and gConfig[app]['mongodb'].has_key('gridfs_collection'):
            collection = str(gConfig[app]['mongodb']['gridfs_collection'])
        if len(collection) == 0:
            collection = 'fs'
        db_util.mongo_init_client(app)
        dbname = gConfig[app]['mongodb']['database']
        db = db_util.gClientMongo[app][dbname]
        if querydict.has_key('file_id'):
            del querydict['file_id']
        fs = gridfs.GridFS(db, collection=collection)
        _id = None
        try:
            querydict = db_util.add_mongo_id(querydict);
            if querydict.has_key('_uniqueIndex'):
                uniqueIndex = querydict['_uniqueIndex']
                cond = {}
                if (isinstance(uniqueIndex, unicode) or isinstance(uniqueIndex, str)) and len(uniqueIndex)>0:
                    arr = uniqueIndex.split(',')
                    for indexName in arr:
                        indexName = indexName.strip()
                        if querydict.has_key(indexName):
                            cond[indexName] = querydict[indexName]
                    if len(cond.keys())>1:
                        idlist = []
                        cur = fs.find(cond)
                        for i in cur:
                            idlist.append(i._id)
                        for i in idlist:
                            fs.delete(i)
                del querydict['_uniqueIndex']
            _id = fs.put(buf, **querydict)
        except gridfs.errors.FileExists:
            if querydict.has_key('_id'):
                _id = db_util.add_mongo_id(querydict['_id'])
                fs.delete(_id)
                _id = fs.put(buf, **querydict)
        except:
            raise

        body = json.dumps({'_id':db_util.remove_mongo_id(_id)}, ensure_ascii=True, indent=4)
    else:
        body = json.dumps({'result':u'cannot find wsgi app [%s]' % app}, ensure_ascii=True, indent=4)
    return body
    
def handle_authorize_platform(environ, session):
    global ENCODING
    global gConfig, gRequest, gSessionStore, gUrlMap, gSecurityConfig, gWebSocketsMap,  gJoinableQueue
        
    def get_collection(collection):
        ret = None
        db_util.mongo_init_client('authorize_platform')
        db = db_util.gClientMongo['authorize_platform'][gConfig['authorize_platform']['mongodb']['database']]
        if not collection in db.collection_names(False):
            ret = db.create_collection(collection)
        else:
            ret = db[collection]
        return ret
        
    def get_all_functions():
        ret = []
        collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_functions'])
        ret = list(collection.find({}))
        #for i in cur:
            #ret.append(i)
        return ret
    
    def get_all_roles(exclude_template=False):
        ret = []
        collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_roles'])
        if exclude_template:
            ret = list(collection.find({'name':{'$not':re.compile("template")}}))
        else:
            ret = list(collection.find({}))
        #for i in cur:
            #ret.append(i)
        return ret
    
    def check_role_can_be_delete(_id):
        def get_id_list(node):
            reet = []
            if node.has_key('roles'):
                for i in node['roles']:
                    reet.append(i)
            return reet
        ret = True
        for i in get_user():
            idlist = get_id_list(i)
            if _id in idlist:
                ret = False
                break
        return ret
        
        
        
    def check_function_can_be_delete(_id):
        def get_id_list(node):
            reet = []
            if node.has_key('_id'):
                reet.append(node['_id'])
            if node.has_key('children'):
                for i in node['children']:
                    reet.extend(get_id_list(i))
            return reet
        ret = True
        for i in get_all_roles():
            idlist = get_id_list(i)
            if _id in idlist:
                ret = False
                break
        return ret
    def check_valid_user(session, user=None):
        ret = False
        if session and session.has_key('username') and len(session['username'])>0:
            if user:
                ret = session['username'] == user
            else:
                ret = True
        return ret
    def function_add(session, querydict):
        if not check_valid_user(session, 'admin'):
            return json.dumps({'result':u'admin_permission_required'}, ensure_ascii=True, indent=4)
        ret = ''
        collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_functions'])
        if querydict.has_key('name'):
            existone = collection.find_one({'name':querydict['name']})
            if existone:
                ret = json.dumps({'result':u'function_add_fail_name_exist'}, ensure_ascii=True, indent=4)
            else:
                _id = collection.save(db_util.add_mongo_id(querydict))
                rec = collection.find_one({'_id':_id})
                ret = db_util.remove_mongo_id(rec)
                ret = json.dumps(ret, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'function_add_fail_name_required'}, ensure_ascii=True, indent=4)
        return ret
    def function_query(session, querydict):
        #if not check_valid_user(session, 'admin'):
            #return json.dumps({'result':u'admin_permission_required'}, ensure_ascii=True, indent=4)
        l = get_all_functions()
        ret = json.dumps(db_util.remove_mongo_id(l), ensure_ascii=True, indent=4)
        return ret
    
    def function_update(session, querydict):
        if not check_valid_user(session, 'admin'):
            return json.dumps({'result':u'admin_permission_required'}, ensure_ascii=True, indent=4)
        ret = ''
        collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_functions'])
        if querydict.has_key('_id'):
            wr = collection.update({'_id':db_util.add_mongo_id(querydict['_id'])}, db_util.add_mongo_id(querydict),  multi=False, upsert=False)
            rec = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
            ret = db_util.remove_mongo_id(rec)
            ret = json.dumps(ret, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'function_update_fail_id_required'}, ensure_ascii=True, indent=4)
        return ret
        
    def function_delete(session, querydict):
        if not check_valid_user(session, 'admin'):
            return json.dumps({'result':u'admin_permission_required'}, ensure_ascii=True, indent=4)
        ret = ''
        collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_functions'])
        
        if querydict.has_key('_id'):
            existone = collection.find_one({'_id': db_util.add_mongo_id(querydict['_id'])})
            if existone:
                if check_function_can_be_delete(existone['_id']):
                    wr = collection.remove({'_id':db_util.add_mongo_id(existone['_id'])})
                    ret = json.dumps(db_util.remove_mongo_id(existone), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'function_delete_fail_need_deleted_in_role_first'}, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'function_delete_fail_not_exist'}, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'function_delete_fail_id_required'}, ensure_ascii=True, indent=4)
        return ret
    
    def role_add(session, querydict):
        if not check_valid_user(session, 'admin'):
            return json.dumps({'result':u'admin_permission_required'}, ensure_ascii=True, indent=4)
        ret = ''
        collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_roles'])
        if querydict.has_key('name'):
            existone = collection.find_one({'name':querydict['name']})
            if existone:
                ret = json.dumps({'result':u'role_add_fail_name_already_exist'}, ensure_ascii=True, indent=4)
            else:
                _id = collection.save(db_util.add_mongo_id(querydict))
                rec = collection.find_one({'_id':_id})
                ret = db_util.remove_mongo_id(rec)
                ret = json.dumps(ret, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'role_add_fail_name_required'}, ensure_ascii=True, indent=4)
        return ret
    
    def role_query(session, querydict):    
        if not check_valid_user(session, 'admin'):
            return json.dumps({'result':u'admin_permission_required'}, ensure_ascii=True, indent=4)
        l = get_all_roles(True)
        ret = json.dumps(db_util.remove_mongo_id(l), ensure_ascii=True, indent=4)    
        return ret
    
    
    def role_update(session, querydict):
        if not check_valid_user(session, 'admin'):
            return json.dumps({'result':u'admin_permission_required'}, ensure_ascii=True, indent=4)
        ret = ''
        collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_roles'])
        if querydict.has_key('_id'):
            wr = collection.update({'_id':db_util.add_mongo_id(querydict['_id'])}, db_util.add_mongo_id(querydict),  multi=False, upsert=False)
            rec = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
            ret = db_util.remove_mongo_id(rec)
            ret = json.dumps(ret, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'role_update_fail_id_required'}, ensure_ascii=True, indent=4)
        return ret
    
    def role_delete(session, querydict):
        if not check_valid_user(session, 'admin'):
            return json.dumps({'result':u'admin_permission_required'}, ensure_ascii=True, indent=4)
        ret = ''
        collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_roles'])
        if querydict.has_key('_id'):
            existone = collection.find_one({'_id': db_util.add_mongo_id(querydict['_id'])})
            if existone:
                if check_role_can_be_delete(existone['_id']):
                    wr = collection.remove({'_id':db_util.add_mongo_id(existone['_id'])})
                    ret = json.dumps(db_util.remove_mongo_id(existone), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'role_delete_fail_need_delete_in_user_first'}, ensure_ascii=True, indent=4) 
            else:
                ret = json.dumps({'result':u'role_delete_fail_not_exist'}, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'role_delete_fail_id_required'}, ensure_ascii=True, indent=4)
        return ret
    
    
    
    def role_template_get(session, querydict):
        if not check_valid_user(session, 'admin'):
            return json.dumps({'result':u'admin_permission_required'}, ensure_ascii=True, indent=4)
        ret = ''
        l = get_all_roles()
        for i in l:
            if i['name'] == 'template':
                ret = json.dumps(db_util.remove_mongo_id(i), ensure_ascii=True, indent=4)
                break
        if len(ret) == 0:
            ret = json.dumps({}, ensure_ascii=True, indent=4)
        return ret
        
    def role_template_save(session, querydict):
        if not check_valid_user(session, 'admin'):
            return json.dumps({'result':u'admin_permission_required'}, ensure_ascii=True, indent=4)
        ret = ''
        collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_roles'])
        if querydict.has_key('_id'):
            wr = collection.update({'_id':db_util.add_mongo_id(querydict['_id'])}, db_util.add_mongo_id(querydict),  multi=False, upsert=False)
            rec = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
            ret = db_util.remove_mongo_id(rec)
            ret = json.dumps(ret, ensure_ascii=True, indent=4)
        else:
            #ret = json.dumps({'result':u'role_template_save_fail_id_required'}, ensure_ascii=True, indent=4)
            _id = collection.save(db_util.add_mongo_id(querydict))
            if _id:
                querydict['_id'] = _id
                ret = json.dumps(db_util.remove_mongo_id(querydict), ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'role_template_save_fail'}, ensure_ascii=True, indent=4)
        return ret
    
    def get_user(user=None):
        ret = []
        collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_user_account'])
        if user:
            ret = list(collection.find({'username':user}))
        else:
            ret = list(collection.find({}))
        #for i in cur:
            #ret.append(i)
        return ret
    
    def get_funclist_by_roles(roles):
        def get_func_list(node):
            ret = []
            if node.has_key('_id'):
                if node.has_key('checked') and node['checked'] is True:
                    ret.append(node['_id'])
            if node.has_key('children'):
                for i in node['children']:
                    ret.extend(get_func_list(i))
            return ret
                    
        ret = []
        rolelist = get_all_roles(True)
        for node in rolelist:
            if node.has_key('_id') and node['_id'] in roles: 
                ret.extend(get_func_list(node))
        return ret
        
        
    def check_user_has_function(session, querydict):
        ret = ''
        if not check_valid_user(session):
            return json.dumps({'result':u'username_required'}, ensure_ascii=True, indent=4)
    
        if querydict.has_key('username') :
            if querydict.has_key('functions') :
                if len(querydict['functions'])>0:
                    userlist = get_user(querydict['username'])
                    if len(userlist)>0:
                        if userlist[0].has_key('roles') and isinstance(userlist[0]['roles'], list) and len(userlist[0]['roles'])>0:
                            roles = userlist[0]['roles']
                            funclist = get_funclist_by_roles(roles)
                            retlist = []
                            for f in querydict['functions']:
                                o = {}
                                o['_id'] = f
                                if ObjectId(f) in funclist:
                                    o['enable'] = True
                                else:
                                    o['enable'] = False
                                retlist.append(o)
                            ret = json.dumps(retlist, ensure_ascii=True, indent=4)
                        else:
                            ret = json.dumps({'result':u'this_user_has_no_role'}, ensure_ascii=True, indent=4)
                    else:
                        ret = json.dumps({'result':u'username_not_exist'}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'function_id_list_required'}, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'functions_required'}, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'username_required'}, ensure_ascii=True, indent=4)
        return ret    
        
                    
        
        
    def user_query(session, querydict):
        if not check_valid_user(session, 'admin'):
            return json.dumps({'result':u'admin_permission_required'}, ensure_ascii=True, indent=4)
        ret = ''
        if querydict.has_key('username')  and len(querydict['username'])>0:
            l = get_user(querydict['username'])
            if len(l)>0:
                ret = json.dumps(db_util.remove_mongo_id(l[0]), ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'username_not_found'}, ensure_ascii=True, indent=4)
                
        else:
            l = get_user()
            ret = json.dumps(db_util.remove_mongo_id(l), ensure_ascii=True, indent=4)
        return ret
                    
            
        
    def user_add(session, querydict):
        ret = ''
        if querydict.has_key('username') and querydict.has_key('password') and len(querydict['username'])>0 and len(querydict['password'])>0:        
            try:
                collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_user_account'])
                existone = collection.find_one({'username':querydict['username']})
                if existone:
                    ret = json.dumps({'result':u'register_fail_username_already_exist'}, ensure_ascii=True, indent=4)
                else:
                    _id = collection.save(db_util.add_mongo_id(querydict))
                    rec = collection.find_one({'_id':_id})
                    ret = json.dumps(db_util.remove_mongo_id(rec), ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'register_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'register_fail' }, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'register_fail_username_password_required'}, ensure_ascii=True, indent=4)
        return ret
    
    def user_delete(session, querydict):
        ret = ''
        if querydict.has_key('username') and len(querydict['username'])>0:
            try:
                collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_user_account'])
                existone = collection.find_one({'username':querydict['username']})
                if existone:
                    collection.remove({'_id':existone['_id']})
                    ret = json.dumps(db_util.remove_mongo_id(existone), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'unregister_fail_not_exist' }, ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'unregister_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'unregister_fail' }, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'unregister_fail_username_required'}, ensure_ascii=True, indent=4)
        return ret
    
    def reset_password(session, querydict):
        ret = ''
        if querydict.has_key('username')  and len(querydict['username'])>0 and querydict.has_key('password')  and len(querydict['password'])>0:        
            try:
                collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_user_account'])
                one = collection.find_one({'username':querydict['username']})
                if one:
                    collection.update({'username':querydict['username']}, {'$set':{'password':querydict['password']}},  multi=False, upsert=False)
                    ret = json.dumps(db_util.remove_mongo_id(one), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'reset_password_fail_not_exist'}, ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'reset_password_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'reset_password_fail' }, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'reset_password_fail_username_password_required'}, ensure_ascii=True, indent=4)
        return ret
    
    def user_update(session, querydict):
        ret = ''
        if querydict.has_key('username')  and len(querydict['username'])>0 :        
            try:
                collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_user_account'])
                one = collection.find_one({'username':querydict['username']})
                if one:
                    collection.update({'username':querydict['username']}, db_util.add_mongo_id(querydict),  multi=False, upsert=False)
                    ret = json.dumps(db_util.remove_mongo_id(one), ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'user_update_fail_not_exist'}, ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'user_update_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'user_update_fail' }, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'user_update_fail_username_required'}, ensure_ascii=True, indent=4)
        return ret
        
    
    def login(session, querydict):
        ok = False
        ret = ''
        if querydict.has_key('username') and querydict.has_key('password') and len(querydict['username'])>0 and len(querydict['password'])>0:        
            try:
                check, ip = session_check_user_ip(environ, querydict['username'])
                if gSessionStore and not check:
                    ret = json.dumps({'result':u'other_ip_already_login:%s' % ip }, ensure_ascii=True, indent=4)
                    return ret, ok
                
                if gSessionStore and session:
                    collection = get_collection(gConfig['authorize_platform']['mongodb']['collection_user_account'])
                    one = collection.find_one({'username':querydict['username'], 'password':querydict['password']})
                    if one:
                        ret = json.dumps(db_util.remove_mongo_id(one), ensure_ascii=True, indent=4)
                        ok = True
                    else:
                        ret = json.dumps({'result':u'login_fail_wrong_username_or_password' }, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'login_fail_session_expired' }, ensure_ascii=True, indent=4)
            except:
                if hasattr(sys.exc_info()[1], 'message'):
                    ret = json.dumps({'result':u'login_fail:%s' % sys.exc_info()[1].message}, ensure_ascii=True, indent=4)
                else:
                    ret = json.dumps({'result':u'login_fail' }, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'login_fail_username_password_required'}, ensure_ascii=True, indent=4)
        return ret, ok
        
     
    def auth_check(session, querydict, isnew):
        ret = ''
        if session :
            if querydict.has_key('username') and len(querydict['username'])>0:
                if isnew is True:
                    session['username'] = querydict['username']
                    gSessionStore.save(session)
                    ret = json.dumps({'result':u'auth_check_ok_session_saved'}, ensure_ascii=True, indent=4)
                else:
                    if session.sid:
                        user = gSessionStore.get_data_by_username(session.sid, querydict['username'])
                        if user:
                            ret = json.dumps({'result':u'auth_check_ok_user_exist'}, ensure_ascii=True, indent=4)
                        else:
                            ret = json.dumps({'result':u'auth_check_fail_session_expired'}, ensure_ascii=True, indent=4)
                    else:
                        ret = json.dumps({'result':u'auth_check_fail_session_expired'}, ensure_ascii=True, indent=4)
            else:
                ret = json.dumps({'result':u'auth_check_fail_username_require'}, ensure_ascii=True, indent=4)
        else:
            ret = json.dumps({'result':u'auth_check_fail_session_expired'}, ensure_ascii=True, indent=4)
        return ret
    

    def sub(uid, channel, websocket):
        if uid and websocket and not websocket.closed:
            if not gWebSocketsMap.has_key(uid + '|' + channel):
                gWebSocketsMap[uid + '|' + channel] = websocket
    def unsub(uid, channels):
        keys = channels
        while len(keys)>0:
            key = keys[0]
            if uid and gWebSocketsMap.has_key(uid + '|' + key):
                del gWebSocketsMap[uid + '|' + key]
                del keys[0]
    
    def handle_websocket(environ):
        ws = get_websocket(environ)
        app = gConfig['wsgi']['application']
        session_id = None
        channel = ''
        if environ.has_key('HTTP_COOKIE'):
            arr = environ['HTTP_COOKIE'].split('=')
            if len(arr)>1:
                session_id = arr[1]
        interval = 1.0
        try:
            interval = float(gConfig[app]['websocket']['interval_poll'])
        except:
            interval = 1.0
        while ws and not ws.closed:
            obj = ws_recv(environ)
            if obj and isinstance(obj, dict) and obj.has_key('op'):
                #print(obj)
                if obj['op'] == 'session_list':
                    ws.send(ws_session_query())
                elif obj['op'] == 'subscribe/session_list':
                    sub(session_id, 'session_list', ws)
                elif obj['op'] == 'unsubscribe/session_list':
                    unsub(session_id, ['session_list',])
                elif obj['op'] == 'session_remove':
                    if obj.has_key('id') and len(obj['id'])>0:
                        print('remove session from client:')
                        print(obj['id'])
                        gSessionStore.delete_by_id(obj['id'])
                elif obj['op'] == 'queue_size':
                    qsize = 0
                    if gJoinableQueue:
                        qsize = gJoinableQueue.qsize()
                    ws.send(json.dumps({'queue_size':qsize}, ensure_ascii=True, indent=4))
            else:
                try:
                    ws.send('')
                except:
                    for k in gWebSocketsMap.keys():
                        if gWebSocketsMap[k] is ws:
                            gWebSocketsMap[k].close()
                            del gWebSocketsMap[k]
                            break
            gevent.sleep(interval)
        if ws and ws.closed:
            del ws
    
    
    
    
     
    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    statuscode = '200 OK'
    body = ''
    isnew = False
    urls = gUrlMap.bind_to_environ(environ)
    querydict, buf = get_querydict_by_GET_POST(environ)
    endpoint = ''
    try:
        endpoint, args = urls.match()
        if args.has_key('username'):
            querydict['username'] = args['username']
        if args.has_key('password'):
            querydict['password'] = args['password']
        if endpoint == 'auth_check':
            body = auth_check(session, querydict, False)
        elif endpoint == 'handle_websocket':
            handle_websocket(environ)
        elif endpoint == 'get_salt':
            if len(gSecurityConfig.keys())>0:
                body = json.dumps({'result':'get_salt_ok','salt':gSecurityConfig['password_salt']}, ensure_ascii=True, indent=4)
            else:
                body = json.dumps({'result':'get_salt_fail'}, ensure_ascii=True, indent=4)
        elif endpoint == 'user_add':
            body = user_add(session, querydict)
        elif endpoint == 'user_check':
            body = check_user_has_function(session, querydict)
        elif endpoint == 'user_delete':
            body = user_delete(session, querydict)
        elif endpoint == 'user_query':
            body = user_query(session, querydict)
        elif endpoint == 'user_update':
            body = user_update(session, querydict)
        elif endpoint == 'reset_password':
            body = reset_password(session, querydict)
        elif endpoint == 'login':
            body, loginok = login(session, querydict)
            if loginok:
                if querydict.has_key('username') and len(querydict['username'])>0:
                    session['username'] = querydict['username']
        elif endpoint == 'logout':
            if gSessionStore and session:
                gSessionStore.delete(session)
                session = None
            body = json.dumps({'result':u'logout_ok'}, ensure_ascii=True, indent=4)
        
        elif endpoint == 'function_add':
            body = function_add(session, querydict)
        elif endpoint == 'function_query':
            body = function_query(session, querydict)
        elif endpoint == 'function_update':
            body = function_update(session, querydict)
        elif endpoint == 'function_delete':
            body = function_delete(session, querydict)
        elif endpoint == 'role_add':
            body = role_add(session, querydict)
        elif endpoint == 'role_update':
            body = role_update(session, querydict)
        elif endpoint == 'role_query':
            body = role_query(session, querydict)
        elif endpoint == 'role_delete':
            body = role_delete(session, querydict)
        elif endpoint == 'role_template_save':
            body = role_template_save(session, querydict)
        elif endpoint == 'role_template_get':
            body = role_template_get(session, querydict)
        else:
            body = json.dumps({'result':u'access_deny'}, ensure_ascii=True, indent=4)
        
            
    except HTTPException, e:
        body = json.dumps({'result':u'access_deny'}, ensure_ascii=True, indent=4)
    if session:
        gSessionStore.save(session)
    return statuscode, headers, body




def CORS_header(h={}):
    global gConfig
    def default_header(h={}):
        ret = {};
        for k in h.keys():
            ret[k] = h[k]
        ret['Access-Control-Allow-Origin'] = '*'
        ret['Access-Control-Allow-Credentials'] = 'true'
        ret['Access-Control-Expose-Headers'] = 'true'
        ret['Access-Control-Max-Age'] = '3600'
        ret['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
        return ret
    headers = {}
    for k in h.keys():
        headers[k] = h[k]
    if gConfig['web']['cors']['enable_cors'].lower() == 'true':
        app = gConfig['wsgi']['application']
        if gConfig.has_key(app) and gConfig[app].has_key('cors'):
            try:
                if gConfig[app]['cors'].has_key('Access-Control-Allow-Origin'):
                    headers['Access-Control-Allow-Origin'] = str(gConfig[app]['cors']['Access-Control-Allow-Origin'])
                else:
                    headers['Access-Control-Allow-Origin'] = '*'
                if gConfig[app]['cors'].has_key('Access-Control-Allow-Credentials'):    
                    headers['Access-Control-Allow-Credentials'] = str(gConfig[app]['cors']['Access-Control-Allow-Credentials'])
                else:
                    headers['Access-Control-Allow-Credentials'] = 'true'
                if gConfig[app]['cors'].has_key('Access-Control-Expose-Headers'):  
                    headers['Access-Control-Expose-Headers'] = str(gConfig[app]['cors']['Access-Control-Expose-Headers'])
                else:
                    headers['Access-Control-Expose-Headers'] = 'true'
                if gConfig[app]['cors'].has_key('Access-Control-Max-Age'):
                    headers['Access-Control-Max-Age'] = str(gConfig[app]['cors']['Access-Control-Max-Age'])
                # else:
                #     headers['Access-Control-Max-Age'] = '3600'
                if gConfig[app]['cors'].has_key('Access-Control-Allow-Methods'):
                    s = gConfig[app]['cors']['Access-Control-Allow-Methods']
                    if isinstance(s, list):
                        s = ','.join(s)
                    headers['Access-Control-Allow-Methods'] = str(s)
            except:
                headers = default_header(h)
        else:
            try:
                if gConfig['web']['cors'].has_key('Access-Control-Allow-Origin'):
                    headers['Access-Control-Allow-Origin'] = str(gConfig['web']['cors']['Access-Control-Allow-Origin'])
                else:
                    headers['Access-Control-Allow-Origin'] = '*'
                if gConfig['web']['cors'].has_key('Access-Control-Allow-Credentials'):
                    headers['Access-Control-Allow-Credentials'] = str(gConfig['web']['cors']['Access-Control-Allow-Credentials'])
                else:
                    headers['Access-Control-Allow-Credentials'] = 'true'
                if gConfig['web']['cors'].has_key('Access-Control-Expose-Headers'):
                    headers['Access-Control-Expose-Headers'] = str(gConfig['web']['cors']['Access-Control-Expose-Headers'])
                else:
                    headers['Access-Control-Expose-Headers'] = 'true'
                if gConfig['web']['cors'].has_key('Access-Control-Max-Age'):
                    headers['Access-Control-Max-Age'] = str(gConfig['web']['cors']['Access-Control-Max-Age'])
                if gConfig['web']['cors'].has_key('Access-Control-Allow-Methods'):
                    s = gConfig['web']['cors']['Access-Control-Allow-Methods']
                    if isinstance(s, list):
                        s = ','.join(s)
                    headers['Access-Control-Allow-Methods'] = str(s)
            except:
                headers = default_header(h)
    return headers
    
def check_is_static(aUrl):
    global STATICRESOURCE_DIR
    global gConfig
    ret = False
    surl = dec(aUrl)
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
    if len(ext)>0 and  gConfig['mime_type'].has_key(ext):
        ret = True
    return ret

def whitelist_check(environ, start_response):
    global gConfig
    ret = True
    if gConfig['listen_port'].has_key('whitelist') and len(gConfig['listen_port']['whitelist'])>0:
        if isinstance(gConfig['listen_port']['whitelist'], unicode):
            s = str(gConfig['listen_port']['whitelist'])
            rere = re.compile(s)
            if environ.has_key('REMOTE_ADDR') and len(rere.findall(environ['REMOTE_ADDR']))==0:
                ret = False
        elif isinstance(gConfig['listen_port']['whitelist'], list):
            cnt = 0
            ret = False
            for i in gConfig['listen_port']['whitelist']:
                s = str(i)
                rere = re.compile(s)
                if environ.has_key('REMOTE_ADDR') and len(rere.findall(environ['REMOTE_ADDR']))>0:
                    cnt += 1
            if cnt>0:
                ret = True
    return ret

def blacklist_check(environ, start_response):
    global gConfig
    ret = True
    if gConfig['listen_port'].has_key('blacklist') and len(gConfig['listen_port']['blacklist'])>0:
        if isinstance(gConfig['listen_port']['blacklist'], unicode):
            s = str(gConfig['listen_port']['blacklist'])
            rere = re.compile(s)
            if environ.has_key('REMOTE_ADDR') and len(rere.findall(environ['REMOTE_ADDR']))>0:
                ret = False
        elif isinstance(gConfig['listen_port']['blacklist'], list):
            cnt = 0
            ret = True
            for i in gConfig['listen_port']['blacklist']:
                s = str(i)
                rere = re.compile(s)
                if environ.has_key('REMOTE_ADDR') and len(rere.findall(environ['REMOTE_ADDR']))>0:
                    cnt += 1
            if cnt>0:
                ret = False
            
    return ret

def ip_check(environ, start_response):
    ret = False
    if whitelist_check(environ, start_response) and blacklist_check(environ, start_response):
        ret = True
    return ret

def session_check_user_ip(environ, username):
    global gConfig,  gSessionStore
    ret = True
    ip = environ['REMOTE_ADDR']
    if gConfig['authorize_platform']['session']['session_check_ip'].lower() == 'true':
        l = gSessionStore.get_list_by_username(username)
        for i in l:
            if i.has_key('ip') and i['ip'] != environ['REMOTE_ADDR']:
                ret = False
                break
    return ret, ip


def get_websocket(environ):
    ret = None
    if environ.has_key("wsgi.websocket") and environ['wsgi.websocket']:
        ret = environ['wsgi.websocket']
    return ret

def ws_send(channel=None, string=''):
    global gWebSocketsMap
    
    for k in gWebSocketsMap.keys():
        ws = None
        if channel:
            if '|' + channel in k:
                ws = gWebSocketsMap[k]
        else:
            ws = gWebSocketsMap[k]
        if ws and not ws.closed:
            try:
                ws.send(string)
            except geventwebsocket.WebSocketError, e:
                print('ws_send exception:%s' % str(e))
        elif ws and ws.closed:
            del gWebSocketsMap[k]
            

def ws_session_query():
    ret = json.dumps(db_util.remove_mongo_id(gSessionStore.list()), ensure_ascii=True, indent=4)
    return ret


def ws_recv(environ):
    ret = None
    ws = get_websocket(environ)
    if ws and not ws.closed:
        msg = None
        try:
            msg = ws.receive()
        except geventwebsocket.WebSocketError, e:
            print('ws_recv exception:%s' % str(e))
        if msg:
            try:
                ret = json.loads(msg)
            except:
                ret = msg
        
    return ret

    
    



def application_combiz_platform(environ, start_response):
    global STATICRESOURCE_DIR
    global gConfig, gRequest, gSessionStore
    
    
    def proxy(environ):
        connection_timeout, network_timeout = 5.0, 10.0
        proxy_type = ''
        if '/proxy_platform' in path_info:
            proxy_type = 'proxy_platform'
        if '/proxy_file' in path_info:
            proxy_type = 'proxy_file'
        if '/proxy_pay' in path_info:
            proxy_type = 'proxy_pay'
        try:
            connection_timeout = float(gConfig['combiz_platform'][proxy_type]['www_connection_timeout'])
        except:
            pass
        try:
            network_timeout = float(gConfig['combiz_platform'][proxy_type]['www_network_timeout'])
        except:
            pass
        return handle_http_proxy(environ, proxy_type, gConfig['combiz_platform'][proxy_type]['protocol'],  gConfig['combiz_platform'][proxy_type]['host'], gConfig['combiz_platform'][proxy_type]['port'], '', connection_timeout, network_timeout)
        
    headers = {}
    headerslist = []
    cookie_header = None
    body = ''
    statuscode = '200 OK'
    if not ip_check(environ, start_response):
        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
        body = json.dumps({'result':u'your_ip_access_deny'}, ensure_ascii=True, indent=4)
        start_response(statuscode, headerslist)
        return [body]
    
    path_info = environ['PATH_INFO']
    
    statuscode = '200 OK'
    if path_info[-1:] == '/':
        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
        body = json.dumps({'result':u'access_deny'}, ensure_ascii=True, indent=4)
    elif check_is_static(path_info):
        statuscode, headers, body =  handle_static(environ, path_info)
    elif len(path_info)>7 and path_info[:7] == '/proxy_':
        statuscode, headers, body = proxy(environ)
        
    else:    
        statuscode, headers, body = handle_combiz_platform(environ)
    headers = CORS_header(headers)
    for k in headers:
        headerslist.append((k, headers[k]))
    #print(headerslist)
    start_response(statuscode, headerslist)
    return [body]

def application_authorize_platform(environ, start_response):
    global STATICRESOURCE_DIR
    global gConfig, gRequest, gSessionStore

        
    headers = {}
    headerslist = []
    cookie_header = None
    body = ''
    statuscode = '200 OK'
    if not ip_check(environ, start_response):
        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
        body = json.dumps({'result':u'your_ip_access_deny'}, ensure_ascii=True, indent=4)
        start_response(statuscode, headerslist)
        return [body]
    
    path_info = environ['PATH_INFO']
    if gSessionStore is None:
        gSessionStore = MongodbSessionStore(host=gConfig['authorize_platform']['mongodb']['host'], 
                                            port=int(gConfig['authorize_platform']['mongodb']['port']), 
                                            replicaset=gConfig['authorize_platform']['mongodb']['replicaset'],
                                            db = gConfig['authorize_platform']['mongodb']['database'],
                                            collection = gConfig['authorize_platform']['mongodb']['collection_session'],
                                            )
    is_expire = False
    
    statuscode = '200 OK'
    if path_info[-1:] == '/':
        #path_info += gConfig['web']['indexpage']
        #statuscode, headers, body =  handle_static(environ, path_info)
        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
        body = json.dumps({'result':u'access_deny'}, ensure_ascii=True, indent=4)
    elif check_is_static(path_info):
        statuscode, headers, body =  handle_static(environ, path_info)
    else:    
        with session_manager(environ):
            sess, cookie_header, is_expire = check_session(environ, gRequest, gSessionStore)
            if is_expire:
                headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
                statuscode = '200 OK'
                body = json.dumps({'result':u'session_expired'}, ensure_ascii=True, indent=4)
                if sess:
                    if  not sess.has_key('ip'):
                        sess['ip'] = environ['REMOTE_ADDR']
                    gSessionStore.save_if_modified(sess)
                    
            else:
                statuscode, headers, body = handle_authorize_platform(environ, sess)
                    
    headers = CORS_header(headers)
    if cookie_header:
        headerslist.append(cookie_header)
    for k in headers:
        headerslist.append((k, headers[k]))
    #print(headerslist)
    start_response(statuscode, headerslist)
    return [body]

def application_chat_platform(environ, start_response):
    global STATICRESOURCE_DIR
    global gConfig, gRequest, gSessionStore
    headers = {}
    headerslist = []
    cookie_header = None
    body = ''
    statuscode = '200 OK'
    if not ip_check(environ, start_response):
        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
        body = json.dumps({'result':u'your_ip_access_deny'}, ensure_ascii=True, indent=4)
        start_response(statuscode, headerslist)
        return [body]
    
    path_info = environ['PATH_INFO']
    #if gSessionStore is None:
        #gSessionStore = MongodbSessionStore(host=gConfig['chat_platform']['mongodb']['host'], 
                                            #port=int(gConfig['chat_platform']['mongodb']['port']), 
                                            #replicaset=gConfig['chat_platform']['mongodb']['replicaset'],
                                            #db = gConfig['chat_platform']['mongodb']['database'],
                                            #collection = gConfig['chat_platform']['mongodb']['collection_session'],
                                            #)
    #is_expire = False
    
    statuscode = '200 OK'
    if path_info[-1:] == '/':
        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
        body = json.dumps({'result':u'access_deny'}, ensure_ascii=True, indent=4)
    elif check_is_static(path_info):
        statuscode, headers, body =  handle_static(environ, path_info)
    else:    
        #with session_manager(environ):
            #sess, cookie_header, is_expire = check_session(environ, gRequest, gSessionStore)
            #if is_expire:
                #headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
                #statuscode = '200 OK'
                #body = json.dumps({'result':u'session_expired'}, ensure_ascii=True, indent=4)
                #if sess:
                    #if  not sess.has_key('ip'):
                        #sess['ip'] = environ['REMOTE_ADDR']
                    #gSessionStore.save_if_modified(sess)
                    
            #else:
        statuscode, headers, body = handle_chat_platform(environ, None)
                    
    headers = CORS_header(headers)            
    if cookie_header:
        headerslist.append(cookie_header)
    for k in headers:
        headerslist.append((k, headers[k]))
    #print(headerslist)
    start_response(statuscode, headerslist)
    return [body]

def sign_and_send(thirdpay, method, href, data, need_sign=True):
    ret = None
    if thirdpay == 'alipay':
        ret = sign_and_send_alipay(method, href, data, need_sign)
    return ret

def sign_and_send_alipay(method, href, data, need_sign=True):
    global gConfig
    qs = build_query_string(data)
    if need_sign:
        signed = get_sign_alipay(qs)
        qs += '&sign=%s' %  signed
        qs += '&sign_type=%s' %  gConfig['pay_platform']['alipay']['sign_type']
    
    text = qs
    text = enc_by_code(gConfig['pay_platform']['alipay']['input_charset'], text)
    connection_timeout, network_timeout = float(gConfig['pay_platform']['alipay']['connection_timeout']), float(gConfig['pay_platform']['alipay']['network_timeout'])
    client = HTTPClient.from_url(href, concurrency=1, connection_timeout=connection_timeout, network_timeout=network_timeout, )
    g = None
    if method == 'get':
        if not href[-1:] == '?':
            href += '?'
        href += urllib.quote(text)
        g = gevent.spawn(client.get, href)
    if method == 'post':
        postdata = urllib.quote(text)
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded; text/html; charset=%s' % str(gConfig['pay_platform']['alipay']['input_charset'])
        g = gevent.spawn(client.post, href, body=postdata, headers=headers)
    return g
    
    

def fake_gateway_alipay_return(querydict):
    global gConfig
    sign_data = {}
    if querydict['service'] == 'refund_fastpay_by_platform_pwd':
        sign_data['is_success'] = 'T'
        #sign_data['refund_result'] = 'TRADE_PENDING'
    elif querydict['service'] == 'create_direct_pay_by_user':
        if querydict.has_key('out_trade_no'):
            sign_data['is_success'] = 'T'
            sign_data['notify_id']  = str(ObjectId())
            sign_data['notify_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sign_data['notify_type'] = 'trade_status_sync'
            sign_data['out_trade_no'] = querydict['out_trade_no']
            sign_data['partner'] = gConfig['fake_gateway_alipay']['alipay']['partner_id']
            if querydict.has_key('seller_email'):
                sign_data['seller_email'] = querydict['seller_email']
            if querydict.has_key('subject'):
                sign_data['subject'] = querydict['subject']
            if querydict.has_key('buyer_email'):
                sign_data['buyer_email'] = querydict['buyer_email']
            if querydict.has_key('total_fee'):
                sign_data['total_fee'] = querydict['total_fee']
            
            #sign_data['trade_no'] =  ''
            sign_data['trade_status'] = 'TRADE_PENDING'
            
            
            href = str(gConfig['pay_platform']['alipay']['return_url'])
            if querydict.has_key('return_url'):
                href = querydict['return_url']
            sign_and_send_alipay('get', href, sign_data)
        else:
            print('fake_gateway_alipay_return out_trade_no required')

def fake_gateway_alipay_notify(querydict):
    global gConfig
    
    def get_pay_log_rec_by_trade_no(trade_no):
        ret = None
        db_util.mongo_init_client('pay_platform')
        client = db_util.gClientMongo['pay_platform']
        db = client['pay']
        if 'pay_log' in db.collection_names(False):
            collection = db['pay_log']
            ret = collection.find_one({"trade_no":trade_no})
        return ret
        
    
    data = {}
    if querydict['service'] == 'refund_fastpay_by_platform_pwd':
        data['notify_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['notify_type'] = 'batch_refund_notify'
        data['notify_id']  = str(ObjectId())
        data['batch_no']  = querydict['batch_no'] 
        data['success_num']  = '1'
        detail_data = querydict['detail_data']
        arr = detail_data.split('^')
        trade_no = arr[0]
        refund_fee = float(arr[1])
        result_details = '%s^%s^%s' % (arr[0], arr[1], 'SUCCESS')
        data['result_details'] = result_details
        href = str(gConfig['pay_platform']['alipay']['notify_url'])
        sign_and_send_alipay('post', href, data)
        rec = get_pay_log_rec_by_trade_no(trade_no)
        if rec:
            data = {}
            data['notify_type'] = 'trade_status_sync'
            data['out_trade_no'] = rec['out_trade_no']
            data['refund_status'] = 'REFUND_SUCCESS'
            if refund_fee < rec['total_fee']:
                data['trade_status'] = 'TRADE_SUCCESS'
            else:
                data['trade_status'] = 'TRADE_CLOSED'
            sign_and_send_alipay('post', href, data)
        
    elif querydict['service'] == 'create_direct_pay_by_user':
        if querydict.has_key('out_trade_no'):
            data['out_trade_no'] = querydict['out_trade_no']
            data['notify_id'] = str(ObjectId())
            data['notify_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data['notify_type'] = 'trade_status_sync'
            data['partner'] = gConfig['fake_gateway_alipay']['alipay']['partner_id']
            if querydict.has_key('buyer_email'):
                data['buyer_email' ] = querydict['buyer_email']
            if querydict.has_key('seller_email'):
                data['seller_email'] = querydict['seller_email']
            if querydict.has_key('subject'):
                data['subject'] = querydict['subject']
            if querydict.has_key('total_fee'):
                data['total_fee'] = querydict['total_fee']
                
            if querydict.has_key('paymethod') and querydict['paymethod'] == 'bankPay':
                data['bank_seq_no'] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            
            data['trade_no'] = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(ObjectId())
            data['trade_status'] = 'TRADE_SUCCESS'
            href = str(gConfig['pay_platform']['alipay']['notify_url'])
            sign_and_send_alipay('post', href, data)
        else:
            print('fake_gateway_alipay_notify out_trade_no required')

def fake_gateway_alipay_error_notify(querydict, error_code):
    global gConfig
    data = {}
    if querydict['service'] == 'refund_fastpay_by_platform_pwd':
        data['notify_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['notify_type'] = 'batch_refund_notify'
        data['notify_id']  = str(ObjectId())
        data['batch_no']  = querydict['batch_no'] 
        data['success_num']  = '0'
        detail_data = querydict['detail_data']
        arr = detail_data.split('^')
        result_details = '%s^%s^%s' % (arr[0], arr[1], error_code)
        data['result_details'] = result_details
        href = str(gConfig['pay_platform']['alipay']['notify_url'])
        if querydict.has_key('notify_url'):
            href = str(querydict['notify_url'])
        sign_and_send_alipay('post', href, data)
        
    elif querydict['service'] == 'create_direct_pay_by_user':    
        data['partner'] = gConfig['fake_gateway_alipay']['alipay']['partner_id']
        if querydict.has_key('out_trade_no'):
            data['out_trade_no'] = querydict['out_trade_no']
            data['error_code'] = error_code
            if querydict.has_key('buyer_email'):
                data['buyer_email'] = querydict['buyer_email']
            if querydict.has_key('seller_email'):
                data['seller_email'] = querydict['seller_email']
                
            href = str(gConfig['pay_platform']['alipay']['error_notify_url'])
            sign_and_send_alipay('post', href, data, need_sign=False)
        else:
            print('fake_gateway_alipay_error_notify out_trade_no required')
    
    
def dec_by_code(code, string):
    encode, decode, reader, writer =  codecs.lookup(str(code))
    text = string
    text, length = decode(text, 'replace')
    return text

def enc_by_code(code, string):
    encode, decode, reader, writer =  codecs.lookup(str(code))
    text = string
    text, length = encode(text, 'replace')
    return text

def handle_fake_gateway_alipay(environ, error_code_pay=None, error_code_refund=None):
    global ENCODING
    global gConfig
    headers = {}
    headers['Content-Type'] = 'text/json;charset=' + ENCODING
    statuscode = '200 OK'
    body = ''
    d = {}
    querydict = {}
    querystring = ''
    querystring1 = ''
    if environ.has_key('QUERY_STRING'):
        querystring = environ['QUERY_STRING']
        querydict = urlparse.parse_qs(querystring)
        for key in querydict.keys():
            d[key] = querydict[key][0]
        querydict = d
    if not environ.has_key('QUERY_STRING') or len(environ['QUERY_STRING'])==0:
        buf = environ['wsgi.input'].read()
        querystring = urllib.unquote_plus(buf)
        querystring = dec_by_code(gConfig['pay_platform']['alipay']['input_charset'], querystring)
        querydict = urlparse.parse_qs(querystring)
        d = {}
        for key in querydict.keys():
            d[key] = querydict[key][0]
        querydict = d
        
    
    try:
        querystring1 = querystring[:querystring.index('&sign=')]
    except:
        pass
    try:
        querystring1 = querystring1[:querystring1.index('&sign_type=')]
    except:
        pass
    signed1 = None
    if querydict['service'] == 'create_direct_pay_by_user':
        fake_gateway_alipay_return(querydict)
        
    if querydict['service'] == 'refund_fastpay_by_platform_pwd':
        headers['Content-Type'] = 'text/xml;charset=' + ENCODING
        body = '<?xml version="1.0" encoding="UTF-8"?><IS_SUCCESS>T</IS_SUCCESS>'
        
    gevent.sleep(float(gConfig['fake_gateway_alipay']['alipay']['process_second']))
    #print(querydict)
    if querydict.has_key('sign') and  querydict.has_key('sign_type') and querydict.has_key('_input_charset'):
        ok = check_sign_alipay(querydict['_input_charset'], querydict['sign'], querydict['sign_type'],  querystring1)
        if ok:
            error_code = error_code_pay
            if error_code is None:
                error_code = error_code_refund
            if error_code:
                fake_gateway_alipay_error_notify(querydict, error_code)
            else:
                fake_gateway_alipay_notify(querydict)
        else:
            print('signature check error')
            fake_gateway_alipay_error_notify(querydict, 'ILLEGAL_SIGN')
    else:
        print('need sign or sign_type or _input_charset')
    
    return statuscode, headers, body


def application_fake_gateway_alipay(environ, start_response):
    global STATICRESOURCE_DIR
    global gConfig, gSecurityConfig
    
    headers = {}
    headerslist = []
    body = ''
    statuscode = '200 OK'
    path_info = environ['PATH_INFO']
    
    statuscode = '200 OK'
    if path_info[-1:] == '/':
        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
        body = json.dumps({'result':u'access_deny'}, ensure_ascii=True, indent=4)
    elif check_is_static(path_info):
        statuscode, headers, body =  handle_static(environ, path_info)
    elif path_info == '/gateway.do':
        error_code_pay = gConfig['fake_gateway_alipay']['alipay']['error_code_pay']
        error_code_refund = gConfig['fake_gateway_alipay']['alipay']['error_code_refund']
        if len(error_code_pay) == 0:
            error_code_pay = None
        if error_code_pay and not gSecurityConfig['alipay']['error_code'].has_key(error_code_pay):
            error_code_pay = None
        if len(error_code_refund) == 0:
            error_code_refund = None
        if error_code_refund and not gSecurityConfig['alipay']['error_code'].has_key(error_code_refund):
            error_code_refund = None
        statuscode, headers, body = handle_fake_gateway_alipay(environ, error_code_pay, error_code_refund)
    
    headers = CORS_header(headers)            
    for k in headers:
        headerslist.append((k, headers[k]))
    
    start_response(statuscode, headerslist)
    return [body]

    
def application_pay_platform(environ, start_response):
    global STATICRESOURCE_DIR
    global gConfig, gWebSocketsMap, gJoinableQueue
    
    def check_is_static(aUrl):
        ret = False
        surl = dec(aUrl)
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
        if len(ext)>0 and  gConfig['mime_type'].has_key(ext):
            ret = True
        return ret
    
    
    def handle_websocket(environ):
        ws = get_websocket(environ)
        app = gConfig['wsgi']['application']
        interval = 1.0
        try:
            interval = float(gConfig[app]['websocket']['interval_poll'])
        except:
            interval = 1.0
        while ws and not ws.closed:
            obj = ws_recv(environ)
            if obj and isinstance(obj, dict) and obj.has_key('op'):
                if obj['op'] == 'queue_size':
                    qsize = 0
                    if gJoinableQueue:
                        qsize = gJoinableQueue.qsize()
                    ws.send(json.dumps({'queue_size':qsize}, ensure_ascii=True, indent=4))
            else:
                try:
                    ws.send('')
                except:
                    for k in gWebSocketsMap.keys():
                        if gWebSocketsMap[k] is ws:
                            gWebSocketsMap[k].close()
                            del gWebSocketsMap[k]
                            break
            gevent.sleep(interval)
        if ws and ws.closed:
            del ws
            
            
    
    headers = {}
    headerslist = []
    body = ''
    statuscode = '200 OK'
    
    if not ip_check(environ, start_response):
        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
        body = json.dumps({'result':u'your_ip_access_deny'}, ensure_ascii=True, indent=4)
        start_response(statuscode, headerslist)
        return [body]
    
    
    
    
    path_info = environ['PATH_INFO']
    
    headerslist = []
    statuscode = '200 OK'
    #print('path_info=%s' % path_info)
    if path_info[-1:] == '/':
        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
        body = json.dumps({'result':u'access_deny'}, ensure_ascii=True, indent=4)
    elif check_is_static(path_info):
        statuscode, headers, body =  handle_static(environ, path_info)
    elif path_info == '/pay':   
        statuscode, headers, body = handle_pay(environ)
    elif path_info == '/refund':   
        statuscode, headers, body = handle_refund(environ)
    elif path_info == '/query':   
        statuscode, headers, body = handle_pay_getinfo(environ)
    elif path_info == '/alipay_return_url':   
        headerslist.append(('Content-Type', 'text/plain;charset=' + ENCODING))
        handle_alipay_return_url(environ)
    elif path_info == '/alipay_notify_url':
        headerslist.append(('Content-Type', 'text/plain;charset=' + ENCODING))
        handle_alipay_notify_url(environ)
        body = 'success'
    elif path_info == '/alipay_error_notify_url':   
        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
        handle_alipay_error_notify_url(environ)
    
    headers = CORS_header(headers)            
    for k in headers:
        headerslist.append((k, headers[k]))
    #print(headerslist)
    start_response(statuscode, headerslist)
    if path_info == '/websocket':
        handle_websocket(environ)
    return [body]
    

def handle_http_proxy(environ, proxy_placeholder='proxy', real_protocol='http', real_host='localhost', real_port='80',  token='', connection_timeout=5.0, network_timeout=10.0, request_headers={}):
    global ENCODING, gHttpClient, gRequest, gProxyRequest
    path_info = environ['PATH_INFO']
    if environ.has_key('QUERY_STRING') and len(environ['QUERY_STRING'])>0:
        path_info += '?' + environ['QUERY_STRING']
    request = None

    if gProxyRequest is None:
        request = Request(environ)
    else:
        request = gProxyRequest
    method = request.method.lower()
    data = request.get_data()
    headers = {}
    for i in request.headers:
        headers[i[0]] = enc(i[1])
    for k in request_headers.keys():
        headers[k] = request_headers[k]
    headers['Host'] = real_host
    #for k in headers.keys():
        #print('%s=%s' % (k, headers[k]))
    href = '%s://%s:%s%s' % (real_protocol, real_host, real_port, path_info.replace('/%s/' % proxy_placeholder, '/'))
    if '?' in href:
        href += '&'
    else:
        href += '?';
    href += 'token=%s&random=%d' % ( token, random.randint(0,100000) )
    print('proxy to %s' % href)
    header = {'Content-Type': 'application/json;charset=' + ENCODING, 'Cache-Control': 'no-cache'}
    ret = ''
    url = URL(href)
    if not gHttpClient.has_key('http_proxy'):
        gHttpClient['http_proxy'] = HTTPClient(url.host, port=url.port, connection_timeout=connection_timeout, network_timeout=network_timeout, concurrency=200)
    client = gHttpClient['http_proxy']
    response = None
    try:
        if method == 'get':
            response = client.get(url.request_uri, headers)
        elif method == 'put':
            response = client.put(url.request_uri, data, headers)
        elif method == 'delete':
            response = client.delete(url.request_uri, data, headers)
        elif method == 'post':
            response = client.post(url.request_uri, data, headers)
    except Exception,e:
        idx = 0
        e1 = e
        while (e1.errno == 10053 or e1.errno == 10054 ) and idx < 4:
            idx += 1
            print('encounter 10053 error, trying %d reconnecting...' % idx)
            try:
                if method == 'get':
                    response = client.get(url.request_uri, headers)
                elif method == 'put':
                    response = client.put(url.request_uri, data, headers)
                elif method == 'delete':
                    response = client.delete(url.request_uri, data, headers)
                elif method == 'post':
                    response = client.post(url.request_uri, data, headers)
                break
            except Exception,e2:
                e1 = e2
            gevent.sleep(1.0)
        if idx >= 4:
            raise e1
    if response:
        if hasattr(response, 'status_code'):
            if response.status_code == 200 or response.status_code == 304:
                ret = response.read()
                # print(ret)
                header = {}
                for k in response._headers_index.keys():
                    if  not k in ['transfer-encoding', ]:
                        v = response._headers_index[k]
                        if '-' in k:
                            k = '-'.join([i.capitalize() for i in k.split('-')])
                        else:
                            k = k.capitalize()
                        header[k] = v

            else:
                msg = 'handle_http_proxy response error:%d' % response.status_code
                ret = json.dumps({'result':msg}, ensure_ascii=True, indent=4)
                #raise Exception(msg)
        else:
            raise Exception('handle_http_proxy error: response has no status_code')
    else:
        raise Exception('handle_http_proxy error')
    return  '200 OK', header, ret



    
def application_webgis(environ, start_response):
    global ENCODING
    global gConfig, gRequest, gSessionStore, gWebSocketsMap
    
    def handle_websocket(environ):
        key = str(gevent.getcurrent().__hash__())
        ws = get_websocket(environ)
        if not gWebSocketsMap.has_key(key):
            gWebSocketsMap[key] = ws
            app = gConfig['wsgi']['application']
            interval = 1.0
            try:
                interval = float(gConfig[app]['websocket']['interval_poll'])
            except:
                interval = 1.0
            while ws and not ws.closed:
                obj = ws_recv(environ)
                if obj and isinstance(obj, dict) and obj.has_key('op'):
                    if obj['op'] == 'queue_size':
                        qsize = 0
                        if gJoinableQueue:
                            qsize = gJoinableQueue.qsize()
                        ws.send(json.dumps({'queue_size':qsize}, ensure_ascii=True, indent=4))
                    if obj['op'] == 'turn_on_sound':
                        ws.send('')
                else:
                    try:
                        ws.send('')
                    except:
                        for k in gWebSocketsMap.keys():
                            if gWebSocketsMap[k] is ws:
                                gWebSocketsMap[k].close()
                                del gWebSocketsMap[k]
                                break
                gevent.sleep(interval)
            if ws and ws.closed:
                del ws
        return  '200 OK', {}, ''

    def proxy(environ, request_headers={}):
        global gConfig
        connection_timeout, network_timeout = 5.0, 10.0
        try:
            connection_timeout = float(gConfig['webgis']['anti_bird']['www_connection_timeout'])
        except:
            pass
        try:
            network_timeout = float(gConfig['webgis']['anti_bird']['www_network_timeout'])
        except:
            pass
        token = md5.new('bird%s' % time.strftime('%Y%m%d')).hexdigest()
        path_info = environ['PATH_INFO']
        if '/hasBird' in path_info:
            request_headers['Content-Type'] = 'application/json'
        return handle_http_proxy(environ, 'proxy', 'http', gConfig['webgis']['anti_bird']['tcp_host'], gConfig['webgis']['anti_bird']['http_port'], token, connection_timeout, network_timeout, request_headers)

    # def get_anti_bird_list_from_cache():
    #     ret = '{"result":"get_anti_bird_list_from_cache_error:cannot connect to db"}'
    #     arr = []
    #     if gConfig['webgis'].has_key('anti_bird') and gConfig['webgis']['anti_bird'].has_key('mongodb'):
    #         db_util.mongo_init_client('anti_bird')
    #         db = db_util.gClientMongo['anti_bird'][gConfig['webgis']['anti_bird']['mongodb']['database']]
    #         collection = db[gConfig['webgis']['anti_bird']['mongodb']['detector_collection']]
    #         arr = db_util.remove_mongo_id(list(collection.find({})))
    #         ret = json.dumps(arr, ensure_ascii=True, indent=4)
    #     return ret
    #
    # def get_latest_records_from_cache():
    #     ret = '{"result":"get_latest_records_from_cache_error:cannot connect to db"}'
    #     arr = []
    #     if gConfig['webgis'].has_key('anti_bird') and gConfig['webgis']['anti_bird'].has_key('mongodb'):
    #         db_util.mongo_init_client('anti_bird')
    #         db = db_util.gClientMongo['anti_bird'][gConfig['webgis']['anti_bird']['mongodb']['database']]
    #         collection = db[gConfig['webgis']['anti_bird']['mongodb']['detector_collection']]
    #         arr = db_util.remove_mongo_id(list(collection.find({})))
    #         ret = json.dumps(arr, ensure_ascii=True, indent=4)
    #     return ret




    def set_cookie(key, value):
        secure = False
        if gConfig['listen_port']['enable_ssl'].lower() == 'true':
            secure = True
        max_age = 60
        try:
            session_age = int(gConfig['webgis']['session']['session_age'])
        except:
            pass
        # cookie = ('Set-Cookie', dump_cookie(key, value, domain=str(gConfig['webgis']['session']['session_domain']), max_age=session_age, secure=secure))
        cookie = ('Set-Cookie', dump_cookie(key, value,  max_age=session_age, secure=secure))
        return cookie

    def get_cookie_data(request, key=None):
        string = '{}'
        if request:
            string = request.cookies.get('session_data')
        ret = None
        if string and len(string)>0:
            try:
                ret = json.loads(string)
                if key and ret.has_key(key):
                    ret = ret[key]
                else:
                    ret = None
            except:
                pass
        return ret

    def set_cookie_data(request, data):
        string = '{}'
        ret = None
        if request:
            string = request.cookies.get('session_data')
        if string and len(string)>0:
            try:
                obj = json.loads(string)
                if isinstance(obj, dict) and isinstance(data, dict):
                    for key in data.keys():
                        obj[key] = data[key]
                    string = json.dumps(obj)
                    ret = set_cookie('session_data', string)
            except:
                pass
        return ret

    def session_handle(environ, request, session_store):
        sid = get_cookie_data(request, 'session_id')
        sess = None
        cookie = None
        is_expire = False
        if sid is None or len(sid)==0:
            request.session = session_store.new()
            # session_store.save(request.session)
            sess = request.session
            cookie = set_cookie_data(None, {'session_id': request.session.sid})
            is_expire = True
        else:
            request.session = session_store.get(sid)
            if request.session:
                o = {'session_id': request.session.sid}
                for k in request.session.keys():
                    if not k in [u'password',]:
                        o[k] = request.session[k]
                cookie = set_cookie_data(request, o)
                session_store.save_if_modified(request.session)
            else:
                cookie = set_cookie('session_data', '{}')
                is_expire = True
        # if request.session.should_save:
        #     session_store.save(request.session)
            sess = request.session
        return sess, cookie, is_expire
    def handle_login(environ):
        ret = None
        querydict, buf = get_querydict_by_GET_POST(environ)
        if querydict.has_key('db') and querydict.has_key('collection') and querydict.has_key('username') and querydict.has_key('password'):
            ret = db_util.mongo_find_one(querydict['db'],
                                         querydict['collection'],
                                         {'username':querydict['username'],
                                          'password':querydict['password']})
        return ret

    def handle_state_examination(environ):
        def get_collection(collection):
            ret = None
            db_util.mongo_init_client('webgis')
            db = db_util.gClientMongo['webgis'][gConfig['webgis']['mongodb']['database']]
            if not collection in db.collection_names(False):
                ret = db.create_collection(collection)
            else:
                ret = db[collection]
            return ret

        def save_bayesian_nodes(adict, check_is_2014):
            def get_occur_p(line_name, name, value=None):
                ret = 0.0
                collection = get_collection('state_examination')
                l = list(collection.find({'line_name':line_name}))
                totalcnt = len(l)
                cnt = 0
                if totalcnt>0:
                    for i in l:
                        if len(name)>4 and name[:5] == 'unit_':
                            if i.has_key(name) and i[name] == value:
                                cnt += 1
                        if len(name)>8 and name[:8] == 'unitsub_':
                            id = name[8:]
                            if i.has_key('unitsub'):
                                for j in i['unitsub']:
                                    if j['id'] == id:
                                        cnt += 1
                    ret = float(cnt)/float(totalcnt)
                return ret
            def get_template_v(alist, unit, id, key):
                ret = None
                children = _.result(_.find(alist, {'unit':unit}), 'children')
                if children:
                    p0 = _.result(_.find(children, {'id':id}), key)
                    if p0:
                        ret = p0
                return ret
            def check_has_subunit(alist, line_name, unit):
                ret = []
                children = _.result(_.find(alist, {'unit':unit}), 'children')
                ids = _.pluck(children, 'id')
                # print(ids)
                for id in ids:
                    p = get_occur_p(line_name, 'unitsub_' + id)
                    if p>0:
                        ret.append(id)
                return ret
            standard_template = []
            pp = 'standard_template2009.json'
            if check_is_2014:
                pp = 'standard_template2014.json'
            with codecs.open(os.path.join(STATICRESOURCE_DIR, pp), 'r', 'utf-8-sig') as f:
                standard_template = json.loads(f.read())
            unitnames = ['unit_1','unit_2','unit_3','unit_4','unit_5','unit_6','unit_7','unit_8',]
            collection = get_collection('bayesian_nodes')
            # nodes = collection.find({'line_name':adict['line_name']})
            collection.remove({'line_name':adict['line_name'], 'name':{'$nin':unitnames}})
            nodes = collection.find({'line_name':adict['line_name'], 'name':{'$in':unitnames}})
            for node in nodes:
                subunits = check_has_subunit(standard_template, adict['line_name'], node['name'])
                if len(subunits) > 0:
                    node['conditions'] = []
                    list1 = []
                    for id in subunits:
                        un_p = get_template_v(standard_template, node['name'], id, 'p0')
                        if un_p is None:
                            un_p = {'I':0.0, 'II':0.0, 'III':0.0, 'IV':0.0}
                        for i in ['I', 'II', 'III', 'IV']:
                            un_p[i] += get_occur_p(adict['line_name'], node['name'], i)
                            if un_p[i] > 1.0:
                                un_p[i] = 1.0
                        #20151105bug
                        # node['conditions'].append([[['unitsub_' +  id, 'true']], un_p])
                    #20151105update
                        list1.append(['unitsub_' +  id, 'true'])
                    node['conditions'].append([list1, un_p])
                else:
                    node['conditions'] = [[[], {
                        'I':get_occur_p(adict['line_name'], node['name'], 'I'),
                        'II':get_occur_p(adict['line_name'], node['name'], 'II'),
                        'III':get_occur_p(adict['line_name'], node['name'], 'III'),
                        'IV':get_occur_p(adict['line_name'], node['name'], 'IV'),
                                                }]]
                collection.save(node)
            nodes = collection.find({'line_name':adict['line_name'], 'name':{'$in':unitnames}})
            for node in nodes:
                subunits = check_has_subunit(standard_template, adict['line_name'], node['name'])
                for id in subunits:
                    o = {}
                    o['name'] = 'unitsub_' + id
                    o['display_name'] = get_template_v(standard_template, node['name'], id, 'name')
                    o['description'] = get_template_v(standard_template, node['name'], id, 'according')
                    if o['description'] is None:
                        o['description'] = ''
                    o['line_name'] = adict['line_name']
                    o['domains'] = ['true',]
                    o['conditions'] = [[[], {'true':get_occur_p(adict['line_name'], 'unitsub_' + id, )}]]
                    collection.insert(o)
            # if adict.has_key('unitsub') and isinstance(adict['unitsub'], list):
            #     for i in adict['unitsub']:
            #         o = {}
            #         o['name'] = 'unitsub_' + i['id']
            #         o['display_name'] = i['name']
            #         o['description'] = get_template_v(standard_template, i['unit'], i['id'], 'according')
            #         if o['description'] is None:
            #             o['description'] = ''
            #         o['line_name'] = adict['line_name']
            #         o['domains'] = ['true',]
            #         o['conditions'] = [[[], {'true':get_occur_p(adict['line_name'], 'unitsub_' + i['id'], )}]]
            #         collection.insert(o)
                # unitset = set()
                # for i in  adict['unitsub']:
                #     node = collection.find_one({'line_name': adict['line_name'], 'name': i['unit']})
                #     un_p = get_template_v(standard_template, i['unit'], i['id'], 'p0')
                #     if un_p is None:
                #         un_p = {'I':0.0, 'II':0.0, 'III':0.0, 'IV':0.0}
                #     if node:
                #         if not i['unit'] in unitset:
                #             unitset.add(i['unit'])
                #             node['conditions'] = [[[['unitsub_' + i['id'], 'true']], un_p]]
                #         else:
                #             node['conditions'].append([[['unitsub_' + i['id'], 'true']], un_p])
                #         collection.save(node)



        def state_examination_save(querydict):
            def modifier(adict = {}):
                for k in adict.keys():
                    if not k in ['_id', 'check_year']:
                        if isinstance(adict[k], str) or  isinstance(adict[k], unicode):
                            adict[k] = adict[k].strip()
                    if k == 'line_name':
                        if '500kV' in adict[k]:
                            adict['voltage'] = '500kV'
                        if '220kV' in adict[k]:
                            adict['voltage'] = '220kV'
                        if '110kV' in adict[k]:
                            adict['voltage'] = '110kV'
                        if '35kV' in adict[k]:
                            adict['voltage'] = '35kV'
                        adict[k] = adict[k]\
                            .replace('-', '')\
                            .replace('500kV', '')\
                            .replace('220kV', '')\
                            .replace('110kV', '')\
                            .replace('35kV', '')\
                            .replace('10kV', '')\
                            .replace(u'Ⅱ', 'II')\
                            .replace(u'Ⅰ', 'I')
                        if adict[k][-1] == u'回':
                            adict[k] = adict[k].replace( u'回', u'回线')
                        if not adict[k][-1] == u'线':
                            adict[k] = adict[k] + u'线'
                    if k == 'line_state' or 'unit_' in k:
                        adict[k] = adict[k].replace(u'正常', 'I').replace(u'注意', 'II').replace(u'异常', 'III').replace(u'严重', 'IV')
                return adict


            def save_dict(querydict):
                ret = None
                collection = get_collection('state_examination')
                querydict['line_name'] = querydict['line_name'].strip()
                existone = collection.find_one({'line_name':querydict['line_name'].strip(), 'check_year':querydict['check_year']})
                if existone:
                    querydict['_id'] = str(existone['_id'])
                check_is_2014 = False
                if querydict.has_key('check_is_2014'):
                    check_is_2014 = querydict['check_is_2014']
                    del querydict['check_is_2014']
                querydict = modifier(querydict)
                _id = collection.save(db_util.add_mongo_id(querydict))
                ret = collection.find_one({'_id':_id})
                if ret:
                    ret = db_util.remove_mongo_id(ret)
                save_bayesian_nodes(querydict, check_is_2014)
                return ret


            ret = []
            if isinstance(querydict, dict) and querydict.has_key('line_name') and querydict.has_key('check_year'):
                ret = save_dict(querydict)
            if isinstance(querydict, list):
                collection = get_collection('state_examination')
                for i in querydict:
                    i = modifier(i)
                    existone = collection.find_one({'line_name':i['line_name'], 'check_year':i['check_year']})
                    if existone:
                        i['_id'] = str(existone['_id'])
                    o = save_dict(i)
                    if o:
                        ret.append(o)

            return json.dumps(ret, ensure_ascii=True, indent=4)

        def state_examination_query_line_names(querydict):
            ret = []
            collection = get_collection('state_examination')
            pipeline = [
                # {'$unwind':'$line_name'},
                {"$group": {"_id": "$line_name", "count": {"$sum": 1}}},
            ]
            ret = list(collection.aggregate(pipeline))
            ret = map(lambda x:x['_id'], ret)
            return json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)

        def state_examination_query(querydict):
            ret = []
            collection = get_collection('state_examination')
            if isinstance(querydict, dict):
                # print(querydict)
                ret = list(collection.find(db_util.add_mongo_id(querydict)))
            return json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
        def state_examination_delete(querydict):
            ret = []
            collection = get_collection('state_examination')
            if isinstance(querydict, dict):
                if querydict.has_key('_id'):
                    if isinstance(querydict['_id'], str) or isinstance(querydict['_id'], unicode):
                        existone = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
                        if existone:
                            collection.remove({'_id':existone['_id']})
                            save_bayesian_nodes(existone)
                            ret = json.dumps(db_util.remove_mongo_id(existone), ensure_ascii=True, indent=4)
                        else:
                            ret = json.dumps({'result':u'record_not_exist' }, ensure_ascii=True, indent=4)
                    if isinstance(querydict['_id'], list):
                        ids = db_util.add_mongo_id(querydict['_id'])
                        cond = {'_id':{'$in':ids}}
                        collection.remove(cond)
                        ret = json.dumps(db_util.remove_mongo_id(querydict['_id']), ensure_ascii=True, indent=4)
            return json.dumps(ret, ensure_ascii=True, indent=4)
        def state_examination_save_strategy_2009(querydict):
            ret = []
            if isinstance(querydict, list):
                with codecs.open(os.path.join(STATICRESOURCE_DIR, 'standard_template2009.json'), 'w', 'utf-8-sig') as f:
                    f.write(json.dumps(querydict, ensure_ascii=False, indent=4))
                with codecs.open(os.path.join(STATICRESOURCE_DIR, 'standard_template2009.json'), 'r', 'utf-8-sig') as f:
                    ret = json.loads(f.read())
            return json.dumps(ret, ensure_ascii=True, indent=4)
        def state_examination_save_strategy_2014(querydict):
            ret = []
            if isinstance(querydict, list):
                with codecs.open(os.path.join(STATICRESOURCE_DIR, 'standard_template2014.json'), 'w', 'utf-8-sig') as f:
                    f.write(json.dumps(querydict, ensure_ascii=False, indent=4))
                with codecs.open(os.path.join(STATICRESOURCE_DIR, 'standard_template2014.json'), 'r', 'utf-8-sig') as f:
                    ret = json.loads(f.read())
            return json.dumps(ret, ensure_ascii=True, indent=4)

        statuscode, headers, body =  '200 OK', {}, ''
        urls = gUrlMap.bind_to_environ(environ)
        querydict, buf = get_querydict_by_GET_POST(environ)
        endpoint, args = urls.match()
        if args.has_key('_id') and isinstance(querydict, dict):
            querydict['_id'] = args['_id']
        if endpoint == 'state_examination_save':
            body = state_examination_save(querydict)
        elif endpoint == 'state_examination_query':
            body = state_examination_query(querydict)
        elif endpoint == 'state_examination_delete':
            body = state_examination_delete(querydict)
        elif endpoint == 'state_examination_query_line_names':
            body = state_examination_query_line_names(querydict)
        elif endpoint == 'state_examination_save_strategy':
            body = state_examination_save_strategy(querydict)
        return statuscode, headers, body

    def handle_antibird(environ):
        global gConfig, gUrlMap, ENCODING
        def init_list(environ):
            ret = []
            s = '{"result":"unknown how to get anti bird list"}'
            # if gConfig['webgis'].has_key('anti_bird') and gConfig['webgis']['anti_bird'].has_key('fetch_from_www') and gConfig['webgis']['anti_bird']['fetch_from_www'].lower() == 'true':
            if True:
                environ['PATH_INFO'] = '/proxy/api/detector'
                environ['QUERY_STRING'] = ''
                code, header, s = proxy(environ)
            # if gConfig['webgis'].has_key('anti_bird') and gConfig['webgis']['anti_bird'].has_key('fetch_from_www') and gConfig['webgis']['anti_bird']['fetch_from_www'].lower() == 'false':
            # if False:
            #     s = get_anti_bird_list_from_cache()
            try:
                if len(s)>0:
                    obj = json.loads(s)
                    if isinstance(obj, dict) :
                        if obj.has_key('result'):
                            print('antibird/init_list error:%s' % obj['result'])
                        else:
                            if obj.has_key('_id'):
                                if obj.has_key('imei'):
                                    obj['label'] = obj['imei']
                                    obj['value'] = obj['imei']
                                ret = [obj, ]
                            else:
                                print('antibird/init_list error: unknown error')
                                ret = []
                    elif isinstance(obj, list) :
                        for i in obj:
                            idx = obj.index(i)
                            if i.has_key('imei'):
                                i['label'] = i['imei']
                                i['value'] = i['imei']
                            obj[idx] = i
                        ret = obj
            except Exception,e:
                raise
            return ret

        def get_latest_records(environ, querydict):
            ret = []
            objstr = ''
            if querydict.has_key('imei') and len(querydict['imei'])>0:
                records_num = 1
                if querydict.has_key('records_num') and len(querydict['records_num'])>0:
                    records_num = int(querydict['records_num'])
                href = '/proxy/api/detector/%s/log/%d' % (querydict['imei'], records_num)
                environ['PATH_INFO'] = href
                environ['QUERY_STRING'] = ''
                status, header, objstr = proxy(environ)
            if len(objstr)>0:
                try:
                    obj = json.loads(objstr)
                    if isinstance(obj, dict) :
                        if obj.has_key('result'):
                            print('antibird/get_latest_records error:%s' % obj['result'])
                        else:
                            if obj.has_key('_id'):
                                ret = [obj, ]
                            else:
                                print('antibird/get_latest_records error: unknown error')
                                ret = []
                    elif isinstance(obj, list) :
                        ret = obj
                except:
                    e = sys.exc_info()[1]
                    if hasattr(e, 'message'):
                        print('antibird/get_latest_records error:%s' % e.message)
                    else:
                        print('antibird/get_latest_records error:%s' % str(e))
            for item in ret:
                idx = ret.index(item)
                if item.has_key('picture') and isinstance(item['picture'], list):
                    for i in item['picture']:
                        idx1 = item['picture'].index(i)
                        item['picture'][idx1] = '/proxy/api/image/%s' % i
                ret[idx] = item
            return ret


        def get_latest_records_by_imei(environ, querydict):
            ret = get_latest_records(environ, querydict)
            return json.dumps(ret, ensure_ascii=True, indent=4)


        def get_equip_list(environ, querydict):
            ret = ''
            is_filter_used=False
            if querydict.has_key('is_filter_used') and querydict['is_filter_used'] is True:
                is_filter_used = True
            equip_list = init_list(environ)
            if not is_filter_used:
                ret = json.dumps(equip_list, ensure_ascii=True, indent=4)
            else:
                exist = []
                l = db_util.mongo_find(
                    gConfig['webgis']['mongodb']['database'],
                    'features',
                    {
                        "properties.webgis_type":"point_tower",
                        "properties.metals":{
                            "$elemMatch":{
                                "type":u"多功能驱鸟装置"
                            }
                        }
                    },
                    0,
                    'webgis'
                    )
                for i in l:
                    for j in i['properties']['metals']:
                        if isinstance(j, dict) and j.has_key('imei'):
                            if not j['imei'] in exist:
                                exist.append(j['imei'])
                while len(exist)>0:
                    i0 = exist[0]
                    for i in equip_list:
                        if i['imei'] == i0:
                            equip_list.remove(i)
                            exist.remove(i0)
                            break
                ret = json.dumps(equip_list, ensure_ascii=True, indent=4)
            return  ret

        def equip_tower_mapping(querydict):
            ret = {}
            if querydict.has_key('imei'):
                l = db_util.mongo_find(
                    gConfig['webgis']['mongodb']['database'],
                    'features',
                    {
                        "properties.webgis_type":"point_tower",
                        "properties.metals":{
                            "$elemMatch":{
                                "type":u"多功能驱鸟装置",
                                "imei":querydict['imei']
                            }
                        }
                    },
                    0,
                    'webgis'
                    )
                if len(l)>0:
                    obj = {}
                    obj['tower_id'] = l[0]['_id']
                    obj['name'] = l[0]['properties']['name']
                    obj['lng'] = l[0]['geometry']['coordinates'][0]
                    obj['lat'] = l[0]['geometry']['coordinates'][1]
                    obj['alt'] = l[0]['geometry']['coordinates'][2]
                    ret[querydict['imei']] = obj
            else:
                l = db_util.mongo_find(
                    gConfig['webgis']['mongodb']['database'],
                    'features',
                    {
                        "properties.webgis_type":"point_tower",
                        "properties.metals":{
                            "$elemMatch":{
                                "type":u"多功能驱鸟装置",
                            }
                        }
                    },
                    0,
                    'webgis'
                    )
                for i in l:
                    for j in i['properties']['metals']:
                        if j.has_key('type') and j['type'] == u'多功能驱鸟装置' and j.has_key('imei') and len(j['imei'])>0:
                            obj = {}
                            obj['tower_id'] = i['_id']
                            obj['name'] = i['properties']['name']
                            obj['lng'] = i['geometry']['coordinates'][0]
                            obj['lat'] = i['geometry']['coordinates'][1]
                            obj['alt'] = i['geometry']['coordinates'][2]
                            ret[j['imei']] = obj

            ret = json.dumps(ret, ensure_ascii=True, indent=4)
            return  ret

        statuscode, headers, body =  '200 OK', {}, ''
        urls = gUrlMap.bind_to_environ(environ)
        querydict, buf = get_querydict_by_GET_POST(environ)
        endpoint, args = urls.match()
        if args.has_key('_id') and isinstance(querydict, dict):
            querydict['_id'] = args['_id']
        if args.has_key('imei') and isinstance(querydict, dict):
            querydict['imei'] = args['imei']
        if args.has_key('records_num') and isinstance(querydict, dict):
            querydict['records_num'] = args['records_num']
        if endpoint == 'get_equip_list':
            body = get_equip_list(environ, querydict)
        elif endpoint == 'get_latest_records_by_imei':
            body = get_latest_records_by_imei(environ, querydict)
        elif endpoint == 'equip_tower_mapping':
            body = equip_tower_mapping(querydict)
        return statuscode, headers, body

    def handle_bayesian(environ):
        def get_collection(collection):
            ret = None
            db_util.mongo_init_client('webgis')
            db = db_util.gClientMongo['webgis'][gConfig['webgis']['mongodb']['database']]
            if not collection in db.collection_names(False):
                ret = db.create_collection(collection)
            else:
                ret = db[collection]
            return ret
        # def convert_strkey_to_bool(obj):
        #     if isinstance(obj, list):
        #         for i in range(0, len(obj)):
        #             obj[i] = convert_strkey_to_bool(obj[i])
        #     if isinstance(obj, dict):
        #         for k in obj.keys():
        #             if k in ['true', u'true']:
        #                 obj[True] = obj[k]
        #                 del obj['true']
        #                 del obj[u'true']
        #             elif k in ['false', u'false']:
        #                 obj[False] = obj[k]
        #                 del obj['false']
        #                 del obj[u'false']
        #             obj[k] = convert_strkey_to_bool(obj[k])
        #
        #     return obj
        def save_by_id(querydict, collection_name):
            ret = []
            collection = get_collection(collection_name)
            if isinstance(querydict, list):
                ids = []
                for i in querydict:
                    if i['_id'] is None:
                        del i['_id']
                    id = collection.save(db_util.add_mongo_id(i))
                    if id:
                        ids.append(id)
                ret = list(collection.find({'_id':{'$in':ids}}))
            elif isinstance(querydict, dict):
                id = collection.save(db_util.add_mongo_id(querydict))
                ret = collection.find_one({'_id':id})
            ret = json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
            return ret
        def delete_by_id(querydict, collection_name):
            ret = ''
            collection = get_collection(collection_name)
            if querydict.has_key('_id'):
                if isinstance(querydict['_id'], str) or isinstance(querydict['_id'], unicode):
                    existone = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
                    if existone:
                        collection.remove({'_id':existone['_id']})
                        ret = json.dumps(db_util.remove_mongo_id(existone), ensure_ascii=True, indent=4)
                    else:
                        ret = json.dumps({'result':u'record_not_exist' }, ensure_ascii=True, indent=4)
                if isinstance(querydict['_id'], list):
                    ids = db_util.add_mongo_id(querydict['_id'])
                    cond = {'_id':{'$in':ids}}
                    collection.remove(cond)
                    ret = json.dumps(db_util.remove_mongo_id(querydict['_id']), ensure_ascii=True, indent=4)
            return ret

        def bayesian_query_domains_range(querydict):
            ret = []
            collection = get_collection('bayesian_domains_range')
            ret = list(collection.find({}))
            ret = json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
            return ret
        def bayesian_save_domains_range(querydict):
            return save_by_id(querydict, 'bayesian_domains_range')
        def bayesian_delete_domains_range(querydict):
            return delete_by_id(querydict, 'bayesian_domains_range')


        def bayesian_query_node(querydict):
            ret = []
            if querydict.has_key('line_name') and len(querydict['line_name']):
                collection = get_collection('bayesian_nodes')
                ret = list(collection.find({'line_name':querydict['line_name']}))
            ret = json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
            return ret
        def bayesian_query_graphiz(querydict):
            ret = ''
            if querydict.has_key('line_name') and len(querydict['line_name']):
                g = create_bbn_by_line_name(querydict['line_name'])
                dpi = 100
                rankdir = 'LL'
                if querydict.has_key('dpi') and len(querydict['dpi']):
                    dpi = int(querydict['dpi'])
                if querydict.has_key('rankdir') and len(querydict['rankdir']):
                    rankdir = querydict['rankdir']
                ret = g.get_graphviz_source(dpi, rankdir)
            return enc(ret)
        def bayesian_save_node(querydict):
            return save_by_id(querydict, 'bayesian_nodes')
        def bayesian_delete_node(querydict):
            ret = '[]'
            delete_by_id(querydict, 'bayesian_nodes')
            collection = get_collection('bayesian_nodes')
            if querydict.has_key('names'):
                if isinstance(querydict['names'], list):
                    # names = [str(i) for i in querydict['names']]
                    names = querydict['names']
                    l = list(collection.find({'conditions': {'$elemMatch': {'$elemMatch': {'$elemMatch': {'$elemMatch':{'$in': names}}}}}}))
                    for i in l:
                        existlist = []
                        conditions = []
                        for ii in i['conditions']:
                            idx = i['conditions'].index(ii)
                            tmp = []
                            for iii in ii[0]:
                                # idx1 = ii[0].index(iii)
                                if not iii[0] in names:
                                    tmp.append(iii)
                            ii[0] = tmp
                            i['conditions'][idx] = ii
                        for ii in i['conditions']:
                            key = ''
                            for iii in ii[0]:
                                key += iii[0] + ':' + iii[1] + '|'
                            if not key in existlist:
                                existlist.append(key)
                                conditions.append(ii)
                        i['conditions'] = conditions
                        collection.save(i)
            if querydict.has_key('line_name') and len(querydict['line_name'])>0:
                ret = bayesian_query_node(querydict)
            return ret

        def get_occur_p(line_name, name, value=None):
            ret = 0.0
            collection = get_collection('state_examination')
            l = list(collection.find({'line_name':line_name}))
            totalcnt = len(l)
            cnt = 0
            if totalcnt>0:
                for i in l:
                    if len(name)>4 and name[:5] == 'unit_':
                        if i.has_key(name) and i[name] == value:
                            cnt += 1
                    if len(name)>8 and name[:8] == 'unitsub_':
                        id = name[8:]
                        if i.has_key('unitsub'):
                            for j in i['unitsub']:
                                if j['id'] == id:
                                    cnt += 1
                ret = float(cnt)/float(totalcnt)
            return ret
        def get_template_v(alist, unit, id, key):
            ret = None
            children = _.result(_.find(alist, {'unit':unit}), 'children')
            if children:
                p0 = _.result(_.find(children, {'id':id}), key)
                if p0:
                    ret = p0
            return ret
        def modifier(line_name, alist):
            standard_template_2009 = []
            standard_template_2014 = []
            with codecs.open(os.path.join(STATICRESOURCE_DIR, 'standard_template2009.json'), 'r', 'utf-8-sig') as f:
                standard_template_2009 = json.loads(f.read())
            with codecs.open(os.path.join(STATICRESOURCE_DIR, 'standard_template2014.json'), 'r', 'utf-8-sig') as f:
                standard_template_2014 = json.loads(f.read())
            ret = alist
            for linestate in ret:
                idx0 = ret.index(linestate)
                line_state = linestate['line_state']
                for res in linestate['result']:
                    idx = linestate['result'].index(res)
                    if res['name'][:8] == 'unitsub_':
                        id = res['name'][8:]
                        unit = res['name'][8:14]
                        p0 = get_template_v(standard_template_2009, unit, id, 'p0')
                        if p0 is None:
                            p0 = get_template_v(standard_template_2014, unit, id, 'p0')
                        # total_score = get_template_v(standard_template_2009, unit, id, 'total_score')
                        # if total_score is None:
                        #     total_score = get_template_v(standard_template_2014, unit, id, 'total_score')
                        # total_score = int(total_score)
                        if p0:
                            # res['p'] = p0[getlvl(unit, total_score)] * get_occur_p(line_name, res['name']) * 10.0
                            res['p'] = p0[line_state] * get_occur_p(line_name, res['name']) * 10.0
                            if res['p'] > 1.0:
                                res['p'] = 1.0
                        linestate['result'][idx] = res
                ret[idx0] = linestate
            return ret

        def bayesian_query_predict(querydict):
            ret = []
            year_num = 0
            line_name = None
            if querydict.has_key('line_name') and len(querydict['line_name']):
                line_name = querydict['line_name']
                g = create_bbn_by_line_name(querydict['line_name'])
                del querydict['line_name']
                if querydict.has_key('year_num') and len(querydict['year_num']):
                    year_num = int(querydict['year_num'])
                    del querydict['year_num']
                qd = {}
                querymulti = False
                for k in querydict.keys():
                    if isinstance(querydict[k], unicode):
                        qd[str(k)] = str(querydict[k])
                    elif isinstance(querydict[k], list) and k == u'line_state':
                        querymulti = True
                    else:
                        qd[str(k)] = querydict[k]
                if querymulti:
                    for i in querydict['line_state']:
                        qd['line_state'] = str(i)
                        ret.append({'line_state':i, 'result':bayes_util.query_bbn_condition(g,  **qd)})
                else:
                    ret = bayes_util.query_bbn_condition(g,  **qd)
            ret = modifier(line_name, ret)
            ret = json.dumps(ret, ensure_ascii=True, indent=4)
            return ret
        def reset_unit_by_line_name(line_name):
            collection = get_collection('bayesian_nodes')
            units = list(collection.find({'line_name':line_name, 'name':{'$regex':'^unit_[0-9]$'}}))
            data = bayes_util.get_state_examination_data_by_line_name(line_name)
            o = bayes_util.calc_probability_unit(data)
            for unit in units:
                if o.has_key(unit['name']):
                    unit['conditions'] = o[unit['name']]
                    # print(unit['name'])
                    # print(unit['conditions'])
                    collection.save(unit)
            ret = list(collection.find({'line_name':line_name}).sort('name', pymongo.ASCENDING))
            return ret
        def bayesian_reset_unit(querydict):
            ret = []
            if querydict.has_key('line_name') and len(querydict['line_name']):
                ret = reset_unit_by_line_name(querydict['line_name'])
            ret = json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
            return ret
        def build_additional_condition(line_name, cond):
            ret = cond
            collection = get_collection('bayesian_nodes')
            l = list(collection.find({'line_name':line_name}))
            for node in l:
                ret[node['name']] = node['conditions']
            return ret
        def create_bbn_by_line_name(line_name):
            cond = bayes_util.build_state_examination_condition(line_name)
            cond = build_additional_condition(line_name, cond)
            g = None
            if bayes_util.USE_C_MODULE:
                print('using c-accelerate module...')
                g = bayes_util.build_bbn_from_conditionals(cond)
            else:
                print('using pure-python module...')
                g = bayes_util.build_bbn_from_conditionals_plus(cond)
            return g


        statuscode, headers, body =  '200 OK', {}, ''
        urls = gUrlMap.bind_to_environ(environ)
        querydict, buf = get_querydict_by_GET_POST(environ)
        endpoint, args = urls.match()
        if args.has_key('_id') and isinstance(querydict, dict):
            querydict['_id'] = args['_id']
        if endpoint == 'bayesian_query_node':
            body = bayesian_query_node(querydict)
        elif endpoint == 'bayesian_save_node':
            body = bayesian_save_node(querydict)
        elif endpoint == 'bayesian_query_predict':
            body = bayesian_query_predict(querydict)
        elif endpoint == 'bayesian_reset_unit':
            body = bayesian_reset_unit(querydict)
        elif endpoint == 'bayesian_query_graphiz':
            body = bayesian_query_graphiz(querydict)
            headers['Content-Type'] = 'text/plain'
        elif endpoint == 'bayesian_delete_node':
            body = bayesian_delete_node(querydict)
        elif endpoint == 'bayesian_save_domains_range':
            body = bayesian_save_domains_range(querydict)
        elif endpoint == 'bayesian_delete_domains_range':
            body = bayesian_delete_domains_range(querydict)
        elif endpoint == 'bayesian_query_domains_range':
            body = bayesian_query_domains_range(querydict)
        return statuscode, headers, body

    def handle_distribute_network(environ):
        def get_collection(collection):
            ret = None
            db_util.mongo_init_client('webgis')
            db = db_util.gClientMongo['webgis'][gConfig['webgis']['mongodb']['database']]
            if not collection in db.collection_names(False):
                ret = db.create_collection(collection)
            else:
                ret = db[collection]
            return ret
        def query_network_nodes(querydict):
            ret = []
            collection = get_collection('network')
            network = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
            if network and network.has_key('properties') and network['properties'].has_key('nodes'):
                nodes = network['properties']['nodes']
                if len(nodes)>0:
                    collection = get_collection('features')
                    ret = list(collection.find({'_id':{'$in':nodes}}))
            return json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
        def query_network_names(querydict):
            ret = []
            collection = get_collection('network')
            ret = list(collection.find({'properties.webgis_type':'polyline_dn'}))
            return json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
        def query_edges(querydict):
            ret = []
            collection = get_collection('network')
            if querydict.has_key('_id'):
                network = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
                if network and network.has_key('properties') and network['properties'].has_key('nodes'):
                    nodes = network['properties']['nodes']
                    if len(nodes)>0:
                        collection = get_collection('edges')
                        ret = list(collection.find({'$or':[
                                                        {'properties.webgis_type':'edge_dn'},
                                                        {'properties.webgis_type':'edge_tower'},
                                                    ],
                                                    '$or':[
                                                        {'properties.start':{'$in':nodes}},
                                                        {'properties.end':{'$in':nodes}}
                                                    ]
                                                    }))
            else:
                collection = get_collection('edges')
                ret = list(collection.find({'properties.webgis_type':'edge_dn',
                                            }))

            return json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
        def remove_network(querydict):
            ret = []
            collection = get_collection('network')
            # if querydict.has_key('remove_node') and querydict['remove_node']:
            #     network = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
            #     if network and network.has_key('properties') and network['properties'].has_key('nodes'):
            #         nodes = network['properties']['nodes']
            #         if len(nodes)>0:
            #             c1 = get_collection('features')

            collection.remove({'_id':db_util.add_mongo_id(querydict['_id'])})
            ret = list(collection.find({'properties.webgis_type':'polyline_dn'}))
            return json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)
        def save_network(querydict):
            collection = get_collection('network')
            if querydict.has_key('properties') \
            and querydict['properties'].has_key('name') \
            and querydict['properties']['name'] \
            and len(querydict['properties']['name']):
                piny = db_util.get_pinyin_data()
                querydict['properties']['py'] = piny.hanzi2pinyin_first_letter(querydict['properties']['name'].replace('#','').replace('II',u'二').replace('I',u'一').replace(u'Ⅱ',u'二').replace(u'Ⅰ',u'一'))


            if querydict.has_key('_id') :
                if querydict['_id'] is not None:
                    existone = collection.find_one({'_id':db_util.add_mongo_id(querydict['_id'])})
                    if existone:
                        if querydict.has_key('properties'):
                            del querydict['_id']
                            for k in querydict['properties'].keys():
                                existone['properties'][k] = querydict['properties']['k']
                            collection.save(existone)
                else:
                    del querydict['_id']
                    collection.insert(querydict)

            ret = list(collection.find({'properties.webgis_type':'polyline_dn'}))
            return json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)

        def sort_dict(adict):
            if isinstance(adict, list):
                for idx in range(len(adict)):
                    adict[idx] = sort_dict(adict[idx])
            elif isinstance(adict, dict):
                keys = sorted(adict.keys())
                d = OrderedDict()
                for k in keys:
                    if isinstance(adict[k], list):
                        d[k] = sort_dict(adict[k])
                    else:
                        d[k] = adict[k]
                adict = d
            return adict
        def fault_position(querydict):
            def getlastline(s):
                ret = ''
                if os.sys.platform == 'win32':
                    s = dec1(s)
                    arr = s.split('\n')
                    ret = arr[-1].strip()
                    if len(ret) == 0:
                        ret = arr[-2].strip()
                elif os.sys.platform == 'linux2':
                    s = ''
                    with codecs.open(gConfig['webgis']['distribute_network']['mcr_path']['temp_file'], 'r', 'utf-8-sig') as f:
                        s = f.read()
                    arr = s.split('\n')
                    ret = arr[-1].strip()
                    ret = ret[ret.index('{'):]
                return ret
            def write_output(cmd):
                output = ''
                if os.sys.platform == 'win32':
                    output = gevent.subprocess.check_output(cmd)
                elif os.sys.platform == 'linux2':
                    output = gevent.subprocess.check_output(cmd, env={"LD_LIBRARY_PATH": exe['LD_LIBRARY_PATH']})
                    with codecs.open(gConfig['webgis']['distribute_network']['mcr_path']['temp_file'], 'w', 'utf-8-sig') as f:
                        f.write(enc(output))
                return output

            ret = []
            querydict = sort_dict(querydict)
            print(json.dumps(db_util.remove_mongo_id(querydict), ensure_ascii=True, indent=4))
            app = gConfig['wsgi']['application']
            exe = {}
            exe['common'] = {}
            if os.sys.platform == 'linux2':
                exe['LD_LIBRARY_PATH'] = gConfig[app]['distribute_network']['mcr_path']['LD_LIBRARY_PATH']
            exe['common']['rset_exe'] = gConfig[app]['distribute_network']['mcr_path']['common']['rset_exe']
            exe['common']['gis_exe'] = gConfig[app]['distribute_network']['mcr_path']['common']['gis_exe']
            exe['common']['ants_exe'] = gConfig[app]['distribute_network']['mcr_path']['common']['ants_exe']
            exe['common']['bayes_exe'] = gConfig[app]['distribute_network']['mcr_path']['common']['bayes_exe']
            exe['common']['power_resume_exe'] = gConfig[app]['distribute_network']['mcr_path']['common']['power_resume_exe']
            exe['common']['line_5'] = {}
            exe['common']['line_5']['data_bus_path'] = gConfig[app]['distribute_network']['mcr_path']['common']['line_5']['data_bus_path']
            exe['common']['line_5']['data_gen_path'] = gConfig[app]['distribute_network']['mcr_path']['common']['line_5']['data_gen_path']
            exe['common']['line_5']['data_lnbr_path'] = gConfig[app]['distribute_network']['mcr_path']['common']['line_5']['data_lnbr_path']
            exe['common']['line_5']['data_lnbr_0_path'] = gConfig[app]['distribute_network']['mcr_path']['common']['line_5']['data_lnbr_0_path']
            exe['common']['line_5']['data_conlnbr_path'] = gConfig[app]['distribute_network']['mcr_path']['common']['line_5']['data_conlnbr_path']
            exe['common']['line_5']['rset_bus_load_vector_path'] = gConfig[app]['distribute_network']['mcr_path']['common']['line_5']['rset_bus_load_vector_path']
            exe['common']['line_5']['g_state_path'] = gConfig[app]['distribute_network']['mcr_path']['common']['line_5']['g_state_path']
            exe['common']['line_5']['fault_vec_path'] = gConfig[app]['distribute_network']['mcr_path']['common']['line_5']['fault_vec_path']
            exe['common']['line_5']['ftu1_path'] = gConfig[app]['distribute_network']['mcr_path']['common']['line_5']['ftu1_path']
            exe['common']['line_5']['ftu2_path'] = gConfig[app]['distribute_network']['mcr_path']['common']['line_5']['ftu2_path']
            exe['common']['line_5']['ftu3_path'] = gConfig[app]['distribute_network']['mcr_path']['common']['line_5']['ftu3_path']
            exe['yx'] = {}
            exe['yx']['rset_exe'] = gConfig[app]['distribute_network']['mcr_path']['yx']['rset_exe']
            exe['yx']['gis_exe'] = gConfig[app]['distribute_network']['mcr_path']['yx']['gis_exe']
            exe['yx']['ants_exe'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ants_exe']
            exe['yx']['bayes_exe'] = gConfig[app]['distribute_network']['mcr_path']['yx']['bayes_exe']
            exe['yx']['power_resume_exe'] = gConfig[app]['distribute_network']['mcr_path']['yx']['power_resume_exe']
            exe['yx']['ftu10_2'] = {}
            exe['yx']['ftu10_2']['data_bus_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu10_2']['data_bus_path']
            exe['yx']['ftu10_2']['data_gen_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu10_2']['data_gen_path']
            exe['yx']['ftu10_2']['data_lnbr_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu10_2']['data_lnbr_path']
            exe['yx']['ftu10_2']['ftu1_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu10_2']['ftu1_path']
            exe['yx']['ftu10_1'] = {}
            exe['yx']['ftu10_1']['data_bus_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu10_1']['data_bus_path']
            exe['yx']['ftu10_1']['data_gen_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu10_1']['data_gen_path']
            exe['yx']['ftu10_1']['data_lnbr_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu10_1']['data_lnbr_path']
            exe['yx']['ftu10_1']['ftu1_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu10_1']['ftu1_path']
            exe['yx']['ftu5'] = {}
            exe['yx']['ftu5']['data_bus_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu5']['data_bus_path']
            exe['yx']['ftu5']['data_gen_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu5']['data_gen_path']
            exe['yx']['ftu5']['data_lnbr_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu5']['data_lnbr_path']
            exe['yx']['ftu5']['ftu1_path'] = gConfig[app]['distribute_network']['mcr_path']['yx']['ftu5']['ftu1_path']


            if querydict.has_key('algorithm'):
                if querydict['algorithm'] == 'gis':
                    cmd = ''
                    if querydict.has_key('dn_id') :
                        if querydict['dn_id'] in [u'5643ea96d8b95a164008f49d']:#测试配网1
                            # cmd = '%s "%s" "%s" "%s" "%s" "%s"' % (
                            #     exe['common']['gis_exe'],
                            #     exe['common']['line_5']['data_bus_path'],
                            #     exe['common']['line_5']['data_gen_path'],
                            #     exe['common']['line_5']['data_lnbr_path'],
                            #     exe['common']['line_5']['data_conlnbr_path'],
                            #     exe['common']['line_5']['fault_vec_path']
                            # )
                            # if os.sys.platform == 'win32':
                            cmd = [
                                exe['common']['gis_exe'],
                                exe['common']['line_5']['data_bus_path'],
                                exe['common']['line_5']['data_gen_path'],
                                exe['common']['line_5']['data_lnbr_path'],
                                exe['common']['line_5']['data_conlnbr_path'],
                                exe['common']['line_5']['fault_vec_path']
                            ]
                        elif querydict['dn_id'] in [u'564ea4cad8b95a08ece92582']:#10kV州城Ⅴ回线
                            line_type = ''
                            if querydict.has_key('line_type') and len(querydict['line_type'])>0:
                                line_type = querydict['line_type']
                                # cmd = '%s "%s" "%s" "%s" "%s"' % (
                                #     exe['yx']['gis_exe'],
                                #     exe['yx'][line_type]['data_bus_path'],
                                #     exe['yx'][line_type]['data_gen_path'],
                                #     exe['yx'][line_type]['data_lnbr_path'],
                                #     exe['yx'][line_type]['ftu1_path'],
                                # )
                                cmd = [
                                    exe['yx']['gis_exe'],
                                    exe['yx'][line_type]['data_bus_path'],
                                    exe['yx'][line_type]['data_gen_path'],
                                    exe['yx'][line_type]['data_lnbr_path'],
                                    exe['yx'][line_type]['ftu1_path'],
                                ]

                    if len(cmd) > 0:
                        # if os.sys.platform == 'linux2':
                        #     cmd.insert(0, '/usr/bin/env')
                        #     cmd.insert(1, 'LD_LIBRARY_PATH=%s' % exe['LD_LIBRARY_PATH'])
                        print(cmd)
                        output = write_output(cmd)
                        try:
                            s = getlastline(output)
                            print('s=%s' % s)
                            ret = json.loads(s)
                        except Exception,e:
                            ret = []
                    else:
                        ret = {'result':u'不存在该条线路的运行数据，无法进行计算.'}

                elif querydict['algorithm'] == 'ants':
                    cmd = ''
                    ants_NC_max = 100
                    ants_m = 20
                    ants_Alpha = 1
                    ants_Beta = 1
                    ants_Rho = 0.95
                    ants_Q = 1
                    if querydict.has_key('ants_NC_max'):
                        ants_NC_max = querydict['ants_NC_max']
                    if querydict.has_key('ants_m'):
                        ants_m = querydict['ants_m']
                    if querydict.has_key('ants_Alpha'):
                        ants_Alpha = querydict['ants_Alpha']
                    if querydict.has_key('ants_Beta'):
                        ants_Beta = querydict['ants_Beta']
                    if querydict.has_key('ants_Rho'):
                        ants_Rho = querydict['ants_Rho']
                    if querydict.has_key('ants_Q'):
                        ants_Q = querydict['ants_Q']
                    if querydict.has_key('dn_id') :
                        if querydict['dn_id'] in [u'5643ea96d8b95a164008f49d']:#测试配网1
                            # cmd = '%s "%s" "%s" "%s" "%s" "%s" "%s" "%s" %d %d %d %d %f %d' % (
                            #     exe['common']['ants_exe'],
                            #     exe['common']['line_5']['data_bus_path'],
                            #     exe['common']['line_5']['data_gen_path'],
                            #     exe['common']['line_5']['data_lnbr_path'],
                            #     exe['common']['line_5']['data_conlnbr_path'],
                            #     exe['common']['line_5']['ftu1_path'],
                            #     exe['common']['line_5']['ftu2_path'],
                            #     exe['common']['line_5']['ftu3_path'],
                            #     ants_NC_max,
                            #     ants_m,
                            #     ants_Alpha,
                            #     ants_Beta,
                            #     ants_Rho,
                            #     ants_Q
                            #      )
                            cmd = [
                                exe['common']['ants_exe'],
                                exe['common']['line_5']['data_bus_path'],
                                exe['common']['line_5']['data_gen_path'],
                                exe['common']['line_5']['data_lnbr_path'],
                                exe['common']['line_5']['data_conlnbr_path'],
                                exe['common']['line_5']['ftu1_path'],
                                exe['common']['line_5']['ftu2_path'],
                                exe['common']['line_5']['ftu3_path'],
                                str(ants_NC_max),
                                str(ants_m),
                                str(ants_Alpha),
                                str(ants_Beta),
                                str(ants_Rho),
                                str(ants_Q)
                            ]
                        elif querydict['dn_id'] in [u'564ea4cad8b95a08ece92582']:#10kV州城Ⅴ回线
                            line_type = ''
                            if querydict.has_key('line_type') and len(querydict['line_type'])>0:
                                line_type = querydict['line_type']
                                # cmd = '%s "%s" "%s" "%s" "%s" %d %d %d %d %f %d' % (
                                #     exe['yx']['ants_exe'],
                                #     exe['yx'][line_type]['data_bus_path'],
                                #     exe['yx'][line_type]['data_gen_path'],
                                #     exe['yx'][line_type]['data_lnbr_path'],
                                #     exe['yx'][line_type]['ftu1_path'],
                                #     ants_NC_max,
                                #     ants_m,
                                #     ants_Alpha,
                                #     ants_Beta,
                                #     ants_Rho,
                                #     ants_Q
                                #      )
                                cmd = [
                                    exe['yx']['ants_exe'],
                                    exe['yx'][line_type]['data_bus_path'],
                                    exe['yx'][line_type]['data_gen_path'],
                                    exe['yx'][line_type]['data_lnbr_path'],
                                    exe['yx'][line_type]['ftu1_path'],
                                    str(ants_NC_max),
                                    str(ants_m),
                                    str(ants_Alpha),
                                    str(ants_Beta),
                                    str(ants_Rho),
                                    str(ants_Q)
                                ]
                    if len(cmd) > 0:
                        print(cmd)
                        output = write_output(cmd)
                        try:
                            s = getlastline(output)
                            print(s)
                            ret = json.loads(s)
                        except:
                            ret = []
                    else:
                        ret = {'result':u'不存在该条线路的运行数据，无法进行计算.'}


                elif querydict['algorithm'] == 'bayes':
                    cmd = ''
                    bayes_q = 0.3
                    if querydict.has_key('bayes_q'):
                        bayes_q = querydict['bayes_q']
                    if querydict.has_key('dn_id') :
                        if querydict['dn_id'] in [u'5643ea96d8b95a164008f49d']:#测试配网1
                            # cmd = '%s "%s" "%s" "%s" "%s" "%s"  %f ' % (
                            #     exe['common']['bayes_exe'],
                            #     exe['common']['line_5']['data_bus_path'],
                            #     exe['common']['line_5']['data_gen_path'],
                            #     exe['common']['line_5']['data_lnbr_path'],
                            #     exe['common']['line_5']['data_conlnbr_path'],
                            #     exe['common']['line_5']['fault_vec_path'],
                            #     bayes_q
                            #      )
                            cmd = [
                                exe['common']['bayes_exe'],
                                exe['common']['line_5']['data_bus_path'],
                                exe['common']['line_5']['data_gen_path'],
                                exe['common']['line_5']['data_lnbr_path'],
                                exe['common']['line_5']['data_conlnbr_path'],
                                exe['common']['line_5']['fault_vec_path'],
                                str(bayes_q)
                            ]
                        elif querydict['dn_id'] in [u'564ea4cad8b95a08ece92582']:#10kV州城Ⅴ回线
                            line_type = ''
                            if querydict.has_key('line_type') and len(querydict['line_type'])>0:
                                line_type = querydict['line_type']
                                # cmd = '%s "%s" "%s" "%s" "%s"  %f' % (
                                #     exe['yx']['bayes_exe'],
                                #     exe['yx'][line_type]['data_bus_path'],
                                #     exe['yx'][line_type]['data_gen_path'],
                                #     exe['yx'][line_type]['data_lnbr_path'],
                                #     exe['yx'][line_type]['ftu1_path'],
                                #     bayes_q
                                #      )
                                cmd = [
                                    exe['yx']['bayes_exe'],
                                    exe['yx'][line_type]['data_bus_path'],
                                    exe['yx'][line_type]['data_gen_path'],
                                    exe['yx'][line_type]['data_lnbr_path'],
                                    exe['yx'][line_type]['ftu1_path'],
                                    str(bayes_q)
                                ]
                    if len(cmd) > 0:
                        print(cmd)
                        output = write_output(cmd)
                        try:
                            s = getlastline(output)
                            print(s)
                            ret = json.loads(s)
                        except:
                            ret = []
                    else:
                        ret = {'result':u'不存在该条线路的运行数据，无法进行计算.'}


                elif querydict['algorithm'] == 'power_resume':
                    cmd = ''
                    if querydict.has_key('dn_id') :
                        if querydict['dn_id'] in [u'565e87f9d8b95a1cec89cd01']:#测试配网3
                            # cmd = '%s "%s" "%s" "%s" "%s"  ' % (
                            #     exe['common']['power_resume_exe'],
                            #     exe['common']['line_5']['data_bus_path'],
                            #     exe['common']['line_5']['data_gen_path'],
                            #     exe['common']['line_5']['data_lnbr_0_path'],
                            #     exe['common']['line_5']['data_conlnbr_path']
                            #      )
                            cmd = [
                                exe['common']['power_resume_exe'],
                                exe['common']['line_5']['data_bus_path'],
                                exe['common']['line_5']['data_gen_path'],
                                exe['common']['line_5']['data_lnbr_0_path'],
                                exe['common']['line_5']['data_conlnbr_path']
                            ]
                    if len(cmd) > 0:
                        print(cmd)
                        output = write_output(cmd)
                        try:
                            s = getlastline(output)
                            print(s)
                            ret = json.loads(s)
                        except:
                            ret = []
                    else:
                        ret = {'result':u'不存在该条线路的运行数据，无法进行计算.'}

            return json.dumps(db_util.remove_mongo_id(ret), ensure_ascii=True, indent=4)

        statuscode, headers, body =  '200 OK', {}, ''
        urls = gUrlMap.bind_to_environ(environ)
        querydict, buf = get_querydict_by_GET_POST(environ)
        endpoint, args = urls.match()
        if args.has_key('_id') and isinstance(querydict, dict):
            querydict['_id'] = args['_id']
        if endpoint == 'distribute_network_query_network_nodes':
            body = query_network_nodes(querydict)
        if endpoint == 'distribute_network_query_edges':
            body = query_edges(querydict)
        if endpoint == 'distribute_network_query_network_names':
            body = query_network_names(querydict)
        if endpoint == 'distribute_network_remove_network':
            body = remove_network(querydict)
        if endpoint == 'distribute_network_save_network':
            body = save_network(querydict)
        if endpoint == 'distribute_network_fault_position':
            body = fault_position(querydict)
        return statuscode, headers, body

    headers = {}
    headerslist = []
    cookie_header = None
    statuscode = '200 OK'
    body = ''
        
    path_info = environ['PATH_INFO']
    if 'proxy.cgi' in path_info:
        statuscode, headers, body = handle_proxy_cgi(environ)
    elif path_info == '/test':
        statuscode, headers, body = handle_test(environ)
    elif path_info == '/get':
        statuscode, headers, body = handle_get_method(environ)
    elif path_info == '/post':
        statuscode, headers, body = handle_post_method(environ)
    elif path_info == '/wmts':
        statuscode, headers, body = handle_wmts(environ)
    elif path_info == '/tiles':
        statuscode, headers, body = handle_tiles(environ)
    elif '/arcgistile' in path_info:
        statuscode, headers, body = handle_arcgistile(environ)
    elif path_info == '/terrain/layer.json' or path_info[-8:] == '.terrain':
        statuscode, headers, body = handle_terrain(environ)
    #elif path_info[-8:] == '.terrain':
        #return handle_terrain1(environ)
    # elif path_info == '/wfs':
    #     statuscode, headers, body = handle_wfs(environ)
    elif path_info =='/create_cluster' or  path_info =='/kill_cluster':
        statuscode, headers, body = handle_cluster(environ)
    elif path_info == '/websocket':
        statuscode, headers, body = handle_websocket(environ)
    elif len(path_info)>6 and path_info[:6] == '/proxy':
        statuscode, headers, body = proxy(environ)
        headers['Cache-Control'] = 'no-cache'
    # elif path_info == '/anti_bird_equip_list':
    #     statuscode, headers, body = anti_bird_equip_list(environ)
    # elif path_info == '/anti_bird_equip_tower_mapping':
    #     statuscode, headers, body = anti_bird_equip_tower_mapping(environ)
    # elif path_info == '/anti_bird_get_latest_records_by_imei':
    #     statuscode, headers, body = anti_bird_get_latest_records_by_imei(environ)
    else:
        if path_info[-1:] == '/':
            path_info = gConfig['web']['indexpage']
        if str(gConfig['webgis']['session']['enable_session'].lower()) == 'true' :
            # and path_info in ['/login', '/logout', gConfig['web']['loginpage'], gConfig['web']['indexpage'], gConfig['web']['mainpage']]:
            if gSessionStore is None:
                gSessionStore = FilesystemSessionStore()
            is_expire = False
            with session_manager(environ):
                sess, cookie_header, is_expire = session_handle(environ, gRequest, gSessionStore)
                if path_info == str(gConfig['web']['unauthorizedpage']):
                    if  not sess.has_key('ip'):
                        sess['ip'] = environ['REMOTE_ADDR']

                    gSessionStore.save_if_modified(sess)
                    headerslist.append(('Content-Type', str(gConfig['mime_type']['.html'])))
                    headerslist.append(cookie_header)
                    statuscode, headers, body =  handle_static(environ, gConfig['web']['unauthorizedpage'])
                    start_response('401 Unauthorized', headerslist)
                    return [body]

                if path_info == '/logout':
                    gSessionStore.delete(sess)
                    sess, cookie_header, is_expire = session_handle(environ, gRequest, gSessionStore)
                    headerslist.append(cookie_header)
                    headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
                    start_response('200 OK', headerslist)
                    return [json.dumps({'result':u'ok'}, ensure_ascii=True, indent=4)]

                if is_expire:
                    if  not sess.has_key('ip'):
                        sess['ip'] = environ['REMOTE_ADDR']
                    gSessionStore.save_if_modified(sess)
                    headerslist.append(('Content-Type', str(gConfig['mime_type']['.html'])))
                    headerslist.append(cookie_header)
                    statuscode, headers, body =  handle_static(environ, gConfig['web']['unauthorizedpage'])
                    start_response('401 Unauthorized', headerslist)
                    return [body]
                    # headerslist.append(('Location', str(gConfig['web']['expirepage'])))
                    # start_response('302 Redirect', headerslist)
                    # return ['']
                    # headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
                    # statuscode = '200 OK'
                    # body = json.dumps({'result':u'session_expired'}, ensure_ascii=True, indent=4)
                if path_info == '/login':
                    user = handle_login(environ)
                    if user:
                        sess = gSessionStore.session_class(user, sess.sid, False)
                        sess['username'] = user['username']
                        cookie_header = set_cookie_data(gRequest, {'_id':user['_id'], 'username': user['username'], 'displayname': user['displayname']})
                        gSessionStore.save_if_modified(sess)
                        headerslist.append(cookie_header)
                        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
                        start_response('200 OK', headerslist)
                        return [json.dumps(sess, ensure_ascii=True, indent=4)]
                    else:
                        headerslist.append(cookie_header)
                        headerslist.append(('Content-Type', 'text/json;charset=' + ENCODING))
                        start_response('200 OK', headerslist)        
                        return [json.dumps({'result':u'用户名或密码错误'}, ensure_ascii=True, indent=4)]

                if path_info == str(gConfig['web']['mainpage']):
                    #401 Unauthorized
                    #if session_id is None or token is None:
                    headerslist.append(('Content-Type', str(gConfig['mime_type']['.html'])))
                    headerslist.append(cookie_header)
                    if sess is None or len(sess.keys())==0 or len(sess.sid)==0 or not sess.has_key('username'):
                        statuscode, headers, body =  handle_static(environ, gConfig['web']['unauthorizedpage'])
                        statuscode = '401 Unauthorized'
                        start_response(statuscode, headerslist) 
                        return [body]
                if not is_expire and len(sess.sid)>0:
                    if 'state_examination' in path_info:
                        statuscode, headers, body = handle_state_examination(environ)
                    elif 'bayesian/' in path_info:
                        statuscode, headers, body = handle_bayesian(environ)
                    elif 'antibird/' in path_info:
                        statuscode, headers, body = handle_antibird(environ)
                    elif 'distribute_network/' in path_info:
                        statuscode, headers, body = handle_distribute_network(environ)
                    else:
                        statuscode, headers, body = handle_static(environ, path_info)

        else:
            if path_info == '/login' and str(gConfig['webgis']['session']['enable_session'].lower()) != 'true':
                path_info = gConfig['web']['mainpage']
            if 'state_examination/' in path_info:
                statuscode, headers, body = handle_state_examination(environ)
            elif 'antibird/' in path_info:
                statuscode, headers, body = handle_antibird(environ)
            elif 'bayesian/' in path_info:
                statuscode, headers, body = handle_bayesian(environ)
            else:
                statuscode, headers, body =  handle_static(environ, path_info)
        
    #headkeys = set([i[0] for i in headerslist])
    headers = CORS_header(headers)
    if cookie_header:
        headerslist.append(cookie_header)
    for k in headers:
        headerslist.append((k, headers[k]))
    #print(headerslist)

    # headerslist = add_to_headerlist(headerslist, 'Cache-Control', 'no-cache')
    # print(headerslist)
    start_response(statuscode, headerslist)
    return [body]

def add_to_headerlist(headerslist, key, value):
    ret = headerslist
    existidx = -1
    for i in ret:
        if i[0] == key:
            existidx = ret.index(i)
            break
    if existidx < 0:
        ret.append((key, value))
    else:
        ret[existidx] = (key, value)
    return ret

def application_markdown(environ, start_response):
    global gConfig, gRequest, gSessionStore
    headers = {}
    headerslist = []
        
    path_info = environ['PATH_INFO']
    if path_info == '/get':
        statuscode, headers, body = handle_get_method(environ)
    elif path_info == '/post':
        statuscode, headers, body = handle_post_method(environ)
    else:
        if path_info[-1:] == '/':
            path_info += gConfig['web']['indexpage']
        statuscode, headers, body =  handle_static(environ, path_info)
    headers = CORS_header(headers)    
    for k in headers:
        headerslist.append((k, headers[k]))
    start_response(statuscode, headerslist)
    return [body]
    
    
    
    
def handle_proxy_cgi(environ):
    global gConfig, gHttpClient
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
    headers = {'Content-Type': 'text/plain;charset=' + ENCODING}
    try:
        if url.startswith("http://") or url.startswith("https://"):
            request = None
            response = None
            http = None
            urlobj = URL(url)
            
            if not gHttpClient.has_key('proxy_cgi'):
                gHttpClient['proxy_cgi'] = HTTPClient(urlobj.host, port=urlobj.port, concurrency=100)
            client = gHttpClient['proxy_cgi']
            
            if method == "POST":
                #length = int(environ["CONTENT_LENGTH"])
                headers["Content-Type"] = environ["CONTENT_TYPE"]
                response = client.post(urlobj.request_uri, post_data, headers)
            else:
                response = client.get(urlobj.request_uri)
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
                client.close()
                headers['Content-Length'] = str(len(s))
        else:
            s += "Illegal request."
    
    except Exception, E:
        s += "Status: 500 Unexpected Error"
        s += "Content-Type: text/plain"
        s += "Some unexpected error occurred. Error text was:%s" % E.message
    return '200 OK', headers, s
    
            


def get_host_ip():
    ret = []
    if sys.platform == 'win32':
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
    elif 'linux' in sys.platform:
        import commands
        ips = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | grep -iv \"inet6\" |  awk {'print $2'} | sed -ne 's/addr\:/ /p'")
        arr = ips.split('\n')
        for i in arr:
            ret.append(i.strip())
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
        if obj.has_key('odbc'):
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
    else:
        print('unknown area')
        ret['result'] = []
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


def delete_expired_session(interval):
    global gSessionStore
    while 1:
        gevent.sleep(interval)
        if gSessionStore:
            #print('session recycle checking')
            gSessionStore.delete_expired_list()
            ws_send('session_list', ws_session_query())
            
    
def joinedqueue_consumer_pay():
    global gConfig, gJoinableQueue
    interval = float(gConfig['pay_platform']['queue']['queue_consume_interval'])
    while 1:
        gevent.sleep(interval)
        item = None
        try:
            item = gJoinableQueue.get()
        except:
            item = None
        if item:
            try:
                sign_and_send(item['thirdpay'], item['method'], item['url'], item['data'])
            finally:
                gJoinableQueue.task_done()

def chat_offline_save_log(obj):
    global gConfig, gClientMongo
    def get_collection(collection):
        ret = None
        db_util.mongo_init_client('chat_platform')
        db = db_util.gClientMongo['chat_platform'][gConfig['chat_platform']['mongodb']['database']]
        if not collection in db.collection_names(False):
            ret = db.create_collection(collection)
        else:
            ret = db[collection]
        return ret
    id = None
    if obj['op'] not in ['chat/online', 'chat/offline', 'chat/info/online', 'chat/info/offline', 'chat/request/contact/remove', 'chat/request/group/quit'] and obj.has_key('to'):
        offlinecol = 'chat_log_offline'
        if gConfig['chat_platform']['mongodb'].has_key('collection_chat_log_offline'):
            offlinecol = gConfig['chat_platform']['mongodb']['collection_chat_log_offline']
        collection = get_collection(offlinecol)
        id = collection.save(db_util.add_mongo_id(obj))
    return id

def chat_save_log(obj):
    global gConfig, gClientMongo
    def get_collection(collection):
        ret = None
        db_util.mongo_init_client('chat_platform')
        db = db_util.gClientMongo['chat_platform'][gConfig['chat_platform']['mongodb']['database']]
        if not collection in db.collection_names(False):
            ret = db.create_collection(collection)
        else:
            ret = db[collection]
        return ret
    id = None
    if obj.has_key('op') and  obj['op'] in ['chat/chat', 'chat/online', 'chat/offline']:
        collection = get_collection(gConfig['chat_platform']['mongodb']['collection_chat_log'])
        # if obj.has_key('timestamp'):
        #     obj['timestamp'] = datetime.datetime.fromtimestamp(obj['timestamp']/1000).strftime('%Y-%m-%d %H:%M:%S')
        if obj['op'] in ['chat/online', 'chat/offline']:
            obj1 = copy.deepcopy(obj)
            for k in obj1.keys():
                if not k in ['from', 'timestamp', 'op', 'to']:
                    del obj1[k]
            if obj1.has_key('_id'):
                del obj1['_id']
            id = collection.save(db_util.add_mongo_id(obj1))
        else:
            id = collection.save(db_util.add_mongo_id(obj))
    return id

               
def joinedqueue_consumer_chat():
    global gConfig, gJoinableQueue, gWebSocketsMap

    interval = float(gConfig['chat_platform']['queue']['queue_consume_interval'])
    while 1:
        gevent.sleep(interval)
        item = None
        try:
            item = gJoinableQueue.get()
        except:
            item = None
        if item:
            try:
                g = gevent.spawn(chat_save_log, item)
                k = item['to']
                if gWebSocketsMap.has_key(k):
                    for ws in gWebSocketsMap[k]:
                        if not ws.closed:
                            ws.send(json.dumps(item, ensure_ascii=True, indent=4))
                else:
                    gevent.spawn(chat_offline_save_log, item)

            finally:
                gJoinableQueue.task_done()    
    

def tcp_reconnect_check(interval=1):
    global gConfig, gTcpReconnectCounter, gTcpSock
    tcp_reconnect_threshold = int(gConfig['webgis']['anti_bird']['tcp_reconnect_threshold'])
    gTcpReconnectCounter = tcp_reconnect_threshold
    while 1:
        gTcpReconnectCounter += interval
        #print(gTcpReconnectCounter)
        if gTcpReconnectCounter > tcp_reconnect_threshold:
            gTcpReconnectCounter = 0
            print('[%s]Trying to reconnect to anti-bird tcpserver [%s:%s]...' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  gConfig['webgis']['anti_bird']['tcp_host'], gConfig['webgis']['anti_bird']['tcp_port']))
            if gTcpSock:
                if not gTcpSock.closed:
                    gTcpSock.close()
                del gTcpSock
            gTcpSock = None
        gevent.sleep(interval)

def tcp_print_exception():
    e = sys.exc_info()[1]
    message = ''
    if hasattr(e, 'strerror'):
        message = e.strerror
        if message is None and hasattr(e, 'message'):
            message = e.message
    elif hasattr(e, 'message'):
        message = e.message
    else:
        message = str(e)
    print('connecting anti-bird server fail:%s' %  message)
        
def tcp_connect():
    global gConfig
    tcp_host = gConfig['webgis']['anti_bird']['tcp_host']
    tcp_port = int(gConfig['webgis']['anti_bird']['tcp_port'])
    timeout = 5.0
    try:
        timeout = float(gConfig['webgis']['anti_bird']['tcp_timeout'])
    except:
        timeout = 5.0
    sock = socket.create_connection((tcp_host, tcp_port), timeout=timeout)
    sock.settimeout(None)
    #sock = socket.create_connection((tcp_host, tcp_port))
    sock.send("bird")
    return sock    

    
def tcp_recv(sock=None):
    global gConfig, gWebSocketsMap, gTcpReconnectCounter, gTcpSock
    def get_packet(astr):
        ret = ''
        rest = astr
        if '###' in astr:
            idx0 =  astr.index('###') + 3
            astr = astr[idx0:]
            if '###' in astr:
                idx1 = astr.index('###')
                ret = astr[:idx1]
                rest = astr[idx1+3:]
        return ret, rest
    
    def get_packets(astr):
        ret = []
        p, rest = get_packet(astr)
        while len(p)>0:
            ret.append(p)
            p, rest = get_packet(rest)
        return ret, rest
        
    def send_to_client(packets):
        for imei in packets:
            try:
                obj = {'imei':imei}
                for k in gWebSocketsMap.keys():
                    ws = gWebSocketsMap[k]
                    if not ws.closed:
                        ws.send(json.dumps(obj, ensure_ascii=True, indent=4))
            except:
                e = sys.exc_info()[1]
                if hasattr(e, 'message'):
                    print('send_to_client error:%s' % e.message)
                else:
                    print('send_to_client error:%s' % str(e))
    def save_to_cache(astr):
        pass

    MAX_MSGLEN = int(gConfig['webgis']['anti_bird']['max_msg_len'])
    tcp_reconnect_threshold = int(gConfig['webgis']['anti_bird']['tcp_reconnect_threshold'])
    recvstr = ''
    while 1:
        try:
            if gTcpSock is None:
                gTcpSock = tcp_connect()
            
            if gTcpSock and not gTcpSock.closed:
                buf = bytearray(b"\n" * MAX_MSGLEN)
                gTcpSock.recv_into(buf)
                recvstr += buf.strip().decode("utf-8")
                if len(recvstr)>0:
                    gTcpReconnectCounter = 0;
                    print('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), recvstr))
                    packets, recvstr = get_packets(recvstr)
                    if gConfig['webgis'].has_key('anti_bird') and gConfig['webgis']['anti_bird'].has_key('update_to_cache') and gConfig['webgis']['anti_bird']['update_to_cache'].lower() == 'true':
                        save_to_cache(packets)
                    send_to_client(packets)
        except:
            recvstr = ''
            tcp_print_exception()
            if gTcpSock:
                if not gTcpSock.closed:
                    gTcpSock.close()
                del gTcpSock
            gTcpSock = None
        gevent.sleep(0.01)

    
def cycles_task():
    global gConfig, gJoinableQueue
    if gConfig['wsgi']['application'].lower() == 'authorize_platform':
        gevent.spawn(delete_expired_session, int(gConfig['authorize_platform']['session']['session_cycle_check_interval']))
    elif gConfig['wsgi']['application'].lower() == 'pay_platform' and gJoinableQueue:
        gevent.spawn(joinedqueue_consumer_pay)
    elif gConfig['wsgi']['application'].lower() == 'chat_platform' and gJoinableQueue:
        gevent.spawn(joinedqueue_consumer_chat)
    elif gConfig['wsgi']['application'].lower() == 'webgis':
        if gConfig['webgis']['anti_bird'].has_key('enable_fetch') and gConfig['webgis']['anti_bird']['enable_fetch'].lower() == 'true':
            interval = 1
            if gConfig['webgis']['anti_bird'].has_key('cycle_interval'):
                interval = int(gConfig['webgis']['anti_bird']['cycle_interval'])
            gevent.spawn(tcp_recv, None)
            gevent.spawn(tcp_reconnect_check, interval)
    
    
def mainloop_single( port=None, enable_cluster=False, enable_ssl=False):
    global gConfig
    gen_model_app_cache()
    server = None
    app = None
    
    
    key = 'application_' + gConfig['wsgi']['application']
    if globals().has_key(key):
        print('application ready to start:%s' % gConfig['wsgi']['application'])
        app = globals()[key]
    else:
        print('unknown application:%s' % gConfig['wsgi']['application'])
        return
    
    
    cycles_task()
    if port and not enable_cluster:
        if enable_ssl:
            print('listening at host 127.0.0.1, port %d with ssl crypted' % port)
            server = pywsgi.WSGIServer(('127.0.0.1', port), app, handler_class = WebSocketHandler, keyfile = gConfig['listen_port']['keyfile'], certfile = gConfig['listen_port']['certfile'])
        else:    
            print('listening at host 127.0.0.1, port %d' % port)
            server = pywsgi.WSGIServer(('127.0.0.1', port), app, handler_class = WebSocketHandler)
            
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
                        server = pywsgi.WSGIServer((i, pport), app, handler_class = WebSocketHandler, keyfile = gConfig['listen_port']['keyfile'], certfile = gConfig['listen_port']['certfile'])
                    else:
                        server = pywsgi.WSGIServer((i, pport), app, handler_class = WebSocketHandler)
                    servers.append(server)
                        
                    if idx < len(host_list)-1:
                        server.start()
    
                    idx += 1
                servers[-1].serve_forever()
            elif isinstance(pport, unicode):
                for i in host_list:
                    if enable_ssl:
                        server = pywsgi.WSGIServer((i, int(pport)), app, handler_class = WebSocketHandler, keyfile = gConfig['listen_port']['keyfile'], certfile = gConfig['listen_port']['certfile'])
                    else:
                        server = pywsgi.WSGIServer((i, int(pport)), app, handler_class = WebSocketHandler)
                    servers.append(server)
                    if idx < len(host_list)-1:
                        server.start()
    
                    idx += 1
                servers[-1].serve_forever()
            elif isinstance(pport, list):
                for i in host_list:
                    for j in pport:
                        if enable_ssl:
                            server = pywsgi.WSGIServer((i, int(j)), app, handler_class = WebSocketHandler, keyfile = gConfig['listen_port']['keyfile'], certfile = gConfig['listen_port']['certfile'])
                        else:    
                            server = pywsgi.WSGIServer((i, int(j)), app, handler_class = WebSocketHandler)
                        servers.append(server)
                        if idx < len(host_list) * len(pport)-1:
                            server.start()
                        
                        idx += 1
                servers[-1].serve_forever()
        else:
            print('wrong host or port in %s' % db_util.CONFIGFILE)
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
    if not gConfig.has_key('web_cache'):
        return
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
   


if __name__=="__main1__":
    freeze_support()
    options = db_util.init_global()
    #print(options)
    init_global()
    s = get_sign_alipay(u'dsadsadsadsadsadsa')
    print(s)
    print(len(s))
    #print(gSecurityConfig)
    #key = 'application_' + gConfig['wsgi']['application']
    #if globals().has_key(key):
        #app = globals()[key]
    #else:
        #print('unknown application:%s' % gConfig['wsgi']['application'])


if __name__=="__main__":
    freeze_support()
    options = db_util.init_global()
    
    init_global()
    if options.signcert_enable:
        create_self_signed_cert( options.signcert_directory,  options.signcert_year)
    elif options.batch_download_tile_enable:
        db_util.command_batch_tile_download(options)
    else:
        if options.cluster_enable:
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
    
    
    
    
    
    