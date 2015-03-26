import os, sys
import time
import json
import md5
import random
from geventhttpclient import HTTPClient, URL

IMAGE_ROOT = ur'd:\bird'

def handle_http_proxy(path_info, real_host, connection_timeout, network_timeout):
    token = md5.new('bird%s' % time.strftime('%Y%m%d')).hexdigest()
    href = 'http://%s%s?token=%s&random=%d' % (real_host, path_info.replace('/proxy/', '/'), token, random.randint(0,100000))
    print(href)
    ret = ''
    try:
        client = HTTPClient.from_url(href, concurrency=1, connection_timeout=connection_timeout, network_timeout=network_timeout, )
        url = URL(href) 
        response = client.get(url.request_uri)
        if response and (response.status_code == 200 or response.status_code == 304):
            ret = response.read()
        else:
            msg = 'handle_http_proxy response error:%d' % response.status_code
            ret = json.dumps({'result':msg}, ensure_ascii=True, indent=4)
    except:
        e = sys.exc_info()[1]
        msg = ''
        if hasattr(e, 'message'):
            msg = 'handle_http_proxy error:%s' % e.message
        else:
            msg = 'handle_http_proxy error:%s' % str(e)
        ret = json.dumps({'result':msg}, ensure_ascii=True, indent=4)
    return  '200 OK', {}, ret


def save_to_image(imei, num=50):
    if '*' in imei:
        path_info = '/proxy/api/detector'
        real_host = 'bird.yncft.com'
        code, header, s = handle_http_proxy(path_info, real_host, 5.0, 10.0)
        equiplist = json.loads(s)
        imei = imei.replace('*', '')
        for obj in equiplist:
            if imei in obj['imei']:
                imei = obj['imei']
                break
    
    path_info = '/proxy/api/detector/%s/log/%d' % (imei, num)
    real_host = 'bird.yncft.com'
    code, header, s = handle_http_proxy(path_info, real_host, 5.0, 10.0)
    pics = []
    logarr = json.loads(s)
    for  i in logarr:
        if len(i['picture']) > 0:
            for j in i['picture']:
                pics.append( '/proxy/api/image/%s' % j)
    
    if not os.path.exists(IMAGE_ROOT):
        os.mkdir(IMAGE_ROOT)
    p = os.path.join(IMAGE_ROOT, imei)
    if not os.path.exists(p):
        os.mkdir(p)
    real_host = 'bird.yncft.com'
    for url in pics:
        code, header, s = handle_http_proxy(url, real_host, 5.0, 10.0)
        p1 = os.path.join(p, '%d_%s.jpg' % (pics.index(url), imei ))
        print('saving %s...' % p1)
        with open(p1, 'wb') as f:
            f.write(s)
    return pics
    
    
def test():
    #path_info = '/proxy/api/detector'
    #real_host = 'bird.yncft.com'
    #code, header, s = handle_http_proxy(path_info, real_host, 5.0, 10.0)
    #print(s)
    path_info = '/proxy/api/detector/%s/log/%d' % ('861001005535428', 50)
    real_host = 'bird.yncft.com'
    code, header, s = handle_http_proxy(path_info, real_host, 5.0, 10.0)
    #print(s)
    logarr = json.loads(s)
    #print(logarr)
    for  i in logarr:
        if len(i['picture'])>1:
            print(i['picture'])
    oid = logarr[0]['picture'][0]
    print(oid)
    path_info = '/proxy/api/image/%s' % oid
    code, header, s = handle_http_proxy(path_info, real_host, 5.0, 10.0)
    print(s)
    
def test1():
    path_info = '/proxy/api/statistics/heatmap/%s/%s/%d/%d' % ('20150301', '20150326', 3, 12)
    real_host = 'bird.yncft.com'
    code, header, s = handle_http_proxy(path_info, real_host, 5.0, 10.0)
    #print(s)
    arr = json.loads(s)
    #print(s)
    for i in arr:
        print(i)

if __name__ == '__main__':
    #pics = save_to_image('*5428', 100)
    #print(pics)
    test1()
    
    
    
    
    
    

