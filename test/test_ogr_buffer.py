# -*- coding: utf-8 -*-
import os, sys, json

import shapely
import shapely.wkt
import pyproj
import geojson

import db_util
from db_util import enc, dec
from bson.objectid import ObjectId


def build_line_geojson():
    linename = u'永发I回线'
    line = db_util.mongo_find_one('ztgd', 'lines', {'properties.line_name':linename})
    geojson = db_util.get_line_geojson('ztgd', line)
    return geojson


    
    
    
#def calc_buffer_shapely(geojsonobj, dist):
    #obj = geojsonobj
    #if obj.has_key('geometry'):
        #obj = obj['geometry']
    #geojson = json.dumps(obj, ensure_ascii=False, indent=4)
    
    #source = osr.SpatialReference()
    #source.ImportFromEPSG(4326)
    #target = osr.SpatialReference()
    #target.ImportFromEPSG(3857) 
    #transform = osr.CoordinateTransformation(source, target)    
    #transform1 = osr.CoordinateTransformation(target, source)    
    #pts = ogr.CreateGeometryFromJson(enc(geojson))
    #pts.Transform(transform)
    ##poly = pts.Buffer(dist)
    #gj = json.loads(pts.ExportToJson())
    #shp = asShape(gj)
    #b = shp.buffer(dist)
    #b = b.boundary
    #poly = ogr.CreateGeometryFromWkt(b.wkt)
    ##print(b)
    #poly.Transform(transform1)
    #g = json.loads(poly.ExportToJson())
    #return g
    
    
if __name__ == "__main__":
    g = db_util.calc_buffer(build_line_geojson(), 5000)
    print(g)
    print(len(g['coordinates'][0]))
    #calc_buffer_shapely(build_line_geojson(), 500)
    l = db_util.mongo_geowithin('ztgd', g)
    print(len(l))
    #for i in l:
        #print(i['properties']['tower_name'])
    