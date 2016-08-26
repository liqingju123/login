# -*- coding: utf-8 -*-
from urllib import urlopen
import urllib2 
import re
import gzip, StringIO
import zlib
import sys
from dome1 import  dome1
import huoqu_haodaifu_yisheng_xiangqing
from pip._vendor import requests


def search_haodaifu(search_txt):
    search_html = get_html('http://so.haodf.com/index/search?type=doctor&kw=' + urllib2.quote(search_txt.decode(sys.stdin.encoding).encode('gbk')))
    search_all_doctor = re.findall('<a target="_blank" href="(.*?)" class="blue1_link">详细介绍</a>', search_html)
    huoqu_haodaifu_yisheng_xiangqing.print_doctor_infor(search_all_doctor[0])

def get_html(site):
    print site
    try:
        a = dome1()
        print a.printTxtLine("111=====")
        hdr = {'User-Agent': 'Mozilla/6.0', 'Content-Type':'text/html; charset=gbk', 'Content-Encoding':'gzip'}
        req11 = urllib2.Request(site, headers=hdr)
        data = urllib2.urlopen(req11, timeout=40)
        page = data.read()
        page1 = page.decode('gbk','ignore').encode('utf-8')
        return page1
    except Exception, e:
        print e
        return '错误'
    
search_haodaifu('郑朝光')


