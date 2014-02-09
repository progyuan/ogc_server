import os, sys



if __name__ == '__main__':
    d = os.path.dirname(os.path.dirname(__file__))
    d = os.path.join(d, 'static')
    d = os.path.join(d, 'threejs')
    d = os.path.join(d, 'examples')
    
    l = os.listdir( d)
    for i in l:
        if '.html' in i:
            s = '''<p><a href="threejs/examples/%s" target="_blank">%s</a></p>''' % (i, i)
            print(s)

