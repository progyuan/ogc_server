import os, sys
import subprocess


OSM2PGSQL = r'F:\work\python\ogc_server\3rdparty\osm2pgsql\x64\osm2pgsql.exe'
OSMDATA = r'F:\work\python\ogc_server\data\osm\map.osm'
DEFAULTSTYLE = r'F:\work\python\ogc_server\3rdparty\osm2pgsql\default.style'

if __name__=="__main__":
    #r = subprocess.check_output([ OSM2PGSQL, '-h'] )
    #r = subprocess.check_output([ OSM2PGSQL, '-d', 'osmdb',  '-l', '-s', '-U', 'postgres', '-P', '5432', '-E','4326', '-S', DEFAULTSTYLE,  OSMDATA ] )
    #r = subprocess.check_output([ OSM2PGSQL, '-d', 'osmdb',   '-s', '-U', 'postgres', '-P', '5432', '-E','4326', '-S', DEFAULTSTYLE,  OSMDATA ] )
    r = subprocess.check_output([ OSM2PGSQL, '-d', 'osmdb', '-l',  '-s', '-U', 'postgres', '-P', '5432',  '-S', DEFAULTSTYLE,  OSMDATA ] )
    #r = subprocess.check_output([ OSM2PGSQL, '-d', 'osmdb',  '-l',  '-U', 'postgres', '-P', '5432', '-E','4326', '-S', DEFAULTSTYLE,  OSMDATA ] )
    print(r)
    