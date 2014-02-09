import os, sys
import subprocess

GDALGEM_BIN = r'E:\Program Files (x86)\gdal\apps\gdaldem.exe'
INPUT_DEM = r'D:\gis\demdata\ASTGTM2_N23E101_dem.tif'
OUTPUT_DEM = r'D:\gis\demdata\ASTGTM2_N23E101_dem_color.png'
COLOR_TEXT_FILE = r'G:\work\python\ogc_server\data\color_terrain_text.txt'

if __name__ == '__main__':
    subprocess.check_output([GDALGEM_BIN, 'color-relief', INPUT_DEM, COLOR_TEXT_FILE, OUTPUT_DEM, '-of', 'png'])
    
    
    
