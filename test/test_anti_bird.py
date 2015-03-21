import os, sys
import time
import json
import md5
import random
from geventhttpclient import HTTPClient, URL

def handle_http_proxy(path_info, real_host, connection_timeout, network_timeout):
    token = md5.new('bird%s' % time.strftime('%Y%m%d')).hexdigest()
    href = 'http://%s%s?token=%s&random=%d' % (real_host, path_info.replace('/proxy/', '/'), token, random.randint(0,100000))
    #print(href)
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


if __name__ == '__main__':
    path_info = '/proxy/api/detector/%s/log/%d' % ('861001005546268', 10)
    real_host = 'bird.yncft.com'
    code, header, s = handle_http_proxy(path_info, real_host, 5.0, 10.0)
    print(s)
    

