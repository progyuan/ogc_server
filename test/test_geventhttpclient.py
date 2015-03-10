# -*- coding: utf-8 -*-
import time
import random
import os
import sys
import datetime
import urllib
import gevent
from geventhttpclient import HTTPClient, URL

ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
HREF = u'http://afgrtbb.tk/code/mess.asp'

def make_random_phone():
    return random.choice(['139','188','185','136','158','151'])+"".join(random.choice("0123456789") for i in range(8))
    

def make_random_password():
    ret = ''
    for i in range(6):
        ret += str(random.randint(0, 9))
    return ret
    
def make_random_card():
    s = '62'
    length = random.randint(14, 17)
    for i in range(length):
        s += str(random.randint(0, 9))
    ret = ''
    idx = 0
    for i in s:
        if idx>0 and idx % 4 == 0:
            ret += ' '
        ret += i
        idx += 1
    return ret


def chinese_charactor():
    head = random.randint(0xB0, 0xCF)
    body = random.randint(0xA, 0xF)
    tail = random.randint(0, 0xF)
    val = ( head << 8 ) | (body << 4) | tail
    str = "%x" % val
    return str.decode('hex').decode('gb2312')  

def make_random_name():
    i = random.randint(2, 3)
    ret = ''
    for i in range(i):
        ret += chinese_charactor()
    return ret

def make_random_id():
    u''' 随机生成新的18为身份证号码 '''
    t = time.localtime()[0]
    x = '%02d%02d%02d%04d%02d%02d%03d' %(random.randint(10,99),
                                        random.randint(01,99),
                                        random.randint(01,99),
                                        random.randint(t - 80, t - 18),
                                        random.randint(1,12),
                                        random.randint(1,28),
                                        random.randint(1,999))
    y = 0
    for i in range(17):
        y += int(x[i]) * ARR[i]

    return '%s%s' %(x, LAST[y % 11])    

def build_random_param():
    iden = make_random_id()
    name = make_random_name()
    card = make_random_card()
    drawpassword = make_random_password()
    loginpass = make_random_password()
    mobile = make_random_phone()
    ret = HREF + '?action=account&iden=%s&name=%s&card=%s&drawpassword=%s&loginpass=%s&mobile=%s' % (iden, urllib.quote_plus(name.encode('utf-8')), urllib.quote(card), drawpassword, loginpass, mobile)
    ret = HREF + '?action=account&iden=%s&name=%s&card=%s&drawpassword=%s&loginpass=%s&mobile=%s' % (iden, name, urllib.quote(card), drawpassword, loginpass, mobile)
    return ret
    

def one_request():
    try:
        href = build_random_param()
        print(href)
        url = URL(href)    
        http = HTTPClient.from_url(url, concurrency=1, connection_timeout=50, network_timeout=60, )
        #response = None
        #g = gevent.spawn(http.get, url.request_uri)
        #g.join()
        #response = g.value
        response = http.get(url.request_uri)
        print(response)
        if response and response.status_code == 200:
            print('200 OK')
    except Exception,e:
        print(e)


def run():
    while 1:
        one_request()
        gevent.sleep(1)

if __name__ == '__main__':
    #print(build_random_param())
    run()
    
    
    
    