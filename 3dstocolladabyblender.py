import os, sys
import bpy
import shutil
import time

def select_by_name( name = "", extend = True ):
    if not extend :
        bpy.ops.object.select_all(action='DESELECT')
    ob = bpy.data.objects.get(name)
    if ob:
        ob.select = True
        bpy.context.scene.objects.active = ob

def reduce_one(src, dst, ratio, angle, exportformat = '3ds'):
    print('delete existing object...')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    #print('import %s...' % src)
    bpy.ops.import_scene.autodesk_3ds(filepath=src, constrain_size=0)
    select_by_name(name = "Camera", extend = False)
    bpy.ops.object.delete()
    select_by_name(name = "Lamp", extend = False)
    bpy.ops.object.delete()
    select_by_name(name = "Model", extend = False)
    bpy.ops.object.select_by_type(extend=True, type='MESH')
    bpy.ops.object.join()
            
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].decimate_type = 'COLLAPSE'
    bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
    bpy.context.object.modifiers["Decimate"].ratio = ratio
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].decimate_type = 'DISSOLVE'
    bpy.context.object.modifiers["Decimate"].angle_limit = angle * 3.14159/180.0
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")
    
    if exportformat == '3ds':    
        print('export to 3ds %s...' % dst)
        bpy.ops.export_scene.autodesk_3ds(filepath=dst, check_existing=False,  use_selection=True)
    if exportformat == 'dae':    
        print('export to dae %s...' % dst)
        bpy.ops.wm.collada_export(filepath=dst, check_existing=False,  selected=False)
    bpy.ops.object.delete()
    #time.sleep(2)


def reduce_one_recusive(src, dst, ratio, angle,  recursive, exportformat = '3ds'):
    d = os.path.dirname(dst) 
    tmp = '_tmp_%s' % os.path.basename(dst)
    tmp = os.path.join(d, tmp)
    s = src
    d = tmp
    for i in range(recursive):
        print('recursive %s: ratio=%s, angle=%s, format=%s...' % (str(i), str(ratio), str(angle), exportformat))
        if i == 0:
            s = src
        if i == recursive-1:
            d = dst
        else:
            s = tmp
        reduce_one(s, d, ratio, angle, exportformat)
    if os.path.exists(tmp):
        os.remove(tmp)
        
    
    
def reduce_many(src_dir, dst_dir, ratio=0.1, angle=90,  recursive=5, exportformat='3ds'):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    needdelete = []
    filelist = []
    for root, dirs, files  in os.walk(src_dir, topdown=False):
        findsvn = False
        for dirname in dirs:
            #print(dirname)
            #if '.svn' in os.path.join(root, dirname):
                #findsvn = True
                #break
            if dirname.endswith('_' + str(ratio)):
                needdelete.append(os.path.join(root, dirname))
        #if findsvn:
            #continue
        
    for d in needdelete:
        print('deleting %s...' % d)
        shutil.rmtree(d)
        
        
    for root, dirs, files  in os.walk(src_dir, topdown=False):
        for name in files:
            src = os.path.abspath(os.path.join(root, name))
            if src[-4:] == '.3ds':
                #src_dir = os.path.dirname(src)
                #arr = os.path.basename(src_dir).split('_')
                #if len(arr)>2:
                    #continue
                #dst_dir = src_dir + '_' + str(ratio)
                #if not os.path.exists(dst_dir):
                    #os.mkdir(dst_dir)
                dst = os.path.join(dst_dir, name)
                if exportformat=='dae':
                    dst = dst.replace('.3ds', '.dae')
                filelist.append((src, dst))
                    
        
                
    for i in  filelist:
        src, dst = i[0] , i[1]
        #print(src + ' ' + dst)          
        reduce_one_recusive(src, dst, ratio, angle, recursive, exportformat)

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()        

def test():
    src = r'F:\work\csharp\kmgdmodel_xly\YF_SNF241A\SNF241A_33.3ds'
    print('delete existing object...')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    print('import %s...' % src)
    bpy.ops.import_scene.autodesk_3ds(filepath=src, constrain_size=10)
    select_by_name(name = "Camera", extend = False)
    bpy.ops.object.delete()
    
    select_by_name(name = "Model", extend = False)
    bpy.ops.object.select_by_type(extend=True, type='MESH')
    #bpy.ops.mesh.select_all(action='SELECT')
    abpy.ops.object.join()

def export_to_obj(src, dst, ratio=1.0, scale=0.001):
    print('delete existing object...')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    #print('import %s...' % src)
    bpy.ops.import_scene.autodesk_3ds(filepath=src, constrain_size=0)
    select_by_name(name = "Camera", extend = False)
    bpy.ops.object.delete()
    select_by_name(name = "Lamp", extend = False)
    bpy.ops.object.delete()
    select_by_name(name = "Model", extend = False)
    bpy.ops.object.select_by_type(extend=True, type='MESH')
    bpy.ops.object.join()
    
    
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].decimate_type = 'COLLAPSE'
    bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
    bpy.context.object.modifiers["Decimate"].ratio = ratio
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")
    
    print('export to obj %s...' % dst)
    bpy.ops.export_scene.obj(filepath=dst, check_existing=False,  use_selection=True, global_scale=scale)
    
def export_to_dae(src, dst, ratio=1.0, scale=0.001):
    print('delete existing object...')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    #print('import %s...' % src)
    bpy.ops.import_scene.autodesk_3ds(filepath=src, constrain_size=0)
    select_by_name(name = "Camera", extend = False)
    bpy.ops.object.delete()
    select_by_name(name = "Lamp", extend = False)
    bpy.ops.object.delete()
    select_by_name(name = "Model", extend = False)
    bpy.ops.object.select_by_type(extend=True, type='MESH')
    bpy.ops.object.join()
    
    
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].decimate_type = 'COLLAPSE'
    bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
    bpy.context.object.modifiers["Decimate"].ratio = ratio
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")
    
    print('export to obj %s...' % dst)
    bpy.ops.export_scene.obj(filepath=dst, check_existing=False,  use_selection=True, global_scale=scale)
    
    
    
    
def batch_export_obj(srcdir, dstdir, ratio=1.0, scale=0.001):
    if not os.path.exists(dstdir):
        os.mkdir(dstdir)
    for root, dirs, files  in os.walk(srcdir, topdown=False):
        for name in files:
            src = os.path.abspath(os.path.join(root, name))
            if src[-4:] == '.3ds':
                dst = os.path.abspath(os.path.join(dstdir, name))
                dst = dst.replace('.3ds', '.obj')
                export_to_obj(src, dst)
            
if __name__=="__main__":
    reduce_many(r'F:\work\csharp\kmgdmodel_xly',u'F:\work\csharp\kmgdmodel_dae', 0.1, 90, 1, 'dae')
    #reduce_one_recusive(r'F:\work\csharp\kmgdmodel_xly\YF_SZF241A\SZF241A_18.3ds', r'F:\work\csharp\kmgdmodel_xly\YF_SZF241A\SZF241A_18_0.1_90.dae', 0.1, 90, 1, 'dae')
    #batch_export_obj(r'F:\work\csharp\kmgdmodel_xly', r'F:\work\csharp\obj')
    #test()
    #pass