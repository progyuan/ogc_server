# -*- coding: utf-8 -*-

import urllib,urllib2  
import base64

url = 'http://localhost/post'
ba = None
with open('testpic.jpg', 'rb') as f:
    ba =base64.b64encode(f.read())
parameters = {'int':123,'float':2.345678, 'str' : 'Hello world', 'list':[1,2,3], 'dict':{'key1':'value1'}, '中文':'你好'}#,'file':"{'filename':'aaa.jpg', 'data':'%s'}" % ba}  
#parameters = {'str' : 'Gimp'}  
data = urllib.urlencode(parameters)    # Use urllib to encode the parameters  
request = urllib2.Request(url, data) 
response = urllib2.urlopen(request)
page = response.read(2000)
