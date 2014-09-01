import os,sys
import shutil

from cx_Freeze import setup, Executable




#def copying_additional():
    #approot = os.path.join('build', 'exe.win32-2.7')
    #path = os.path.abspath(os.path.join(approot, 'static'))
    #if not os.path.exists(path):
        #os.mkdir(path)
    ##for root, dirs, files  in os.walk('static', topdown=False):
        ##for name in dirs:
    #for name in os.listdir('static'):
        #if os.path.isdir(os.path.join('static', name)) and  name in ['img','geojson','photos']:
            #pdest = os.path.join(path, name)
            #psrc =  os.path.abspath(os.path.join('static', name))
            #if os.path.exists(pdest):
                #shutil.rmtree(pdest)
            #shutil.copytree(psrc, pdest)
            
        


def build(is_include_web=False):
    base = None
    base_gui = None
    base_services = None
    if sys.platform == 'win32':
        base = 'Console'
        base_gui = 'Win32GUI'
        base_services = 'Win32Service'
    
    include_files = [
                    'ogc-config.ini', 
                    'ogc_service_install.bat', 
                    'ogc_service_uninstall.bat', 
                    #'ogc_service2_install.bat', 
                    #'ogc_service2_uninstall.bat', 
                    'ogc_server_task_schedule.xml', 
                    'pinyin_word.data',
                    'static/img',
                    #'static/geojson',
                    'gdal-bin',
                    ]
    
    if is_include_web:
        include_files.extend(
            [
                #'static/api',
                'static/css',
                #'static/gltf',
                'static/img',
                'static/js',
                #'static/lab',
                #'static/lib',
                #'static/demos',
                #'static/theme',
                'static/threejs',
                #'static/indexdata.js',
                'static/webgis_index.html',
                'static/webgis_login.html',
                'static/webgis_bootstrap.html',
                'static/webgis_expire.html',
                'static/webgis_unauthorized.html',
            ]
        )
    
    setup(
            name = "ogc_server",
            version = "1.0",
            description = u"OGC Server服务器端应用程序",
            options = {"build_exe" : {
                'packages': ['win32serviceutil','win32service','win32event','servicemanager','socket','win32timezone','cx_Logging',],
                'includes': ['lxml._elementpath', 'greenlet','gevent', 'cx_Logging', 'ogc_server'],
                'include_files' : include_files,
                'include_msvcr': True,
            }
                    },
            executables = [
                Executable("ogc_server.py",
                                      base = base,
                                      targetName = "ogc_server.exe",
                                      #icon ='res/nfdw_gui.ico'
                                      ),
                Executable("ogc_server_services_config.py",
                                      base = base_services,
                                      targetName = "ogc_server_services.exe",
                                      #icon ='res/nfdw_gui.ico'
                                      ),
                #Executable("ogc_server_services_win32.py",
                                      #base = base,
                                      #targetName = "ogc_server_services_win32.exe",
                                      ##icon ='res/nfdw_gui.ico'
                                      #),
                #Executable("download.py",
                         #base = base,
                         #targetName = "download.exe",
                         ##icon ='res/nfdw.ico'
                         #),                       
            ]
    )
    

if __name__ == '__main__':
    build(False)
    
    