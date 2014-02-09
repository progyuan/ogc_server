# -*- coding: utf-8 -*-
import os
import sys
import json
from lxml import etree
import configobj

from pysimplesoap.client import SoapClient, SoapFault


CONFIGFILE = 'ogc-config.ini'

gConfig = configobj.ConfigObj(CONFIGFILE, encoding='UTF8')


def soap_login():
    client = SoapClient(wsdl='%s?wsdl' % gConfig['webservice']['location'], namespace = gConfig['webservice']['namespace'], timeout=int(gConfig['webservice']['timeout']))
    response = client.login(username='yunnan', password='yunnan585372')
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




    
    
if __name__=="__main__":
    print(soap_login())
    #print(soap_GetFlashofDate('', ''))
    #print(soap_GetFlashofEnvelope('', '','', '','', ''))
    