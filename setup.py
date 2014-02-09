import os,sys
import shutil

from cx_Freeze import setup, Executable




def copying_additional():
    #lib = os.path.dirname(sys.executable)
    #lib = os.path.join(lib, 'Lib', 'site-packages')
    #include_files = [os.path.join(lib, 'zmq', 'libzmq.pyd'),os.path.join(lib,'greenlet.pyd')]
    #dest = os.path.join('build', 'exe.win32-2.7')
    
    #for i in include_files:
        #if not os.path.exists(os.path.join(dest, os.path.basename(i))):
            #shutil.copy(i, dest)
    approot = os.path.join('build', 'exe.win32-2.7')
    path = os.path.abspath(os.path.join(approot, 'static'))
    if not os.path.exists(path):
        os.mkdir(path)
    #for root, dirs, files  in os.walk('static', topdown=False):
        #for name in dirs:
    for name in os.listdir('static'):
        if os.path.isdir(os.path.join('static', name)) and  name in ['img','geojson','photos']:
            pdest = os.path.join(path, name)
            psrc =  os.path.abspath(os.path.join('static', name))
            if os.path.exists(pdest):
                shutil.rmtree(pdest)
            shutil.copytree(psrc, pdest)
            
        


def build():
    base = None
    base_gui = None
    if sys.platform == "win32":
        base = "Console"
        base_gui = "Win32GUI"
    
    setup(
            name = "ogc_server",
            version = "1.0",
            description = "昭通供电局服务器端应用程序",
            options = {"build_exe" : {
                "packages": ["lxml._elementpath", "greenlet"],
                "include_files" : ['ogc-config.ini', 'pinyin_word.data'],
                "include_msvcr": True
            }
                    },
            executables = [
                Executable("ogc_server.py",
                                      base = base,
                                      targetName = "ogc_server.exe",
                                      #icon ='res/nfdw_gui.ico'
                                      ),
                #Executable("proc.py",
                         #base = base,
                         #targetName = "sync.exe",
                         #icon ='res/nfdw.ico'
                         #),                       
            ]
    )
    

if __name__ == '__main__':
    build()
    copying_additional()
    
    