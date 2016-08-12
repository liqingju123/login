# encoding:utf-8
from urllib import urlopen
import urllib2 
import re
from pip._vendor import requests


# 淘宝使用的是 https 使用HTTPS 请求
def _ssl_get_images_(ssl_host):
    requ = requests.get('https:%s' % ssl_host, verify=False)
    return requ.text
# 根据 网页详情获取 真正的 请求页面详情图片的JS
def _taobao_itmes_all_all_(itmes_url):
    text_url = get_html(itmes_url)
    one_url_list = re.findall(r'"descUrl":"(.*?)","fetchDcUrl"', text_url)
    for one_url in one_url_list:
        _write_local_(one_url)
    print '写入完成'

#获取JS 中的图片路径 存储到本地
def _write_local_(one_url):
    text_all_txt = _ssl_get_images_(one_url)
    print text_all_txt
    image_all = re.findall(r'<img align="absmiddle" src="(.*?)".*?>', str(text_all_txt))
    print len(image_all)
    path_url = r'/Users/imac/Downloads/金刚/%d.jpg'# 修改成自己的硬盘地址
    index = 0
    for one_url in image_all:
        write_image(one_url, path_url % index)
        index = index + 1
        print one_url
# 获取http 页面的请求
def get_html(site):
    print site
    try:
        #这里可改成自己的header
        hdr = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36','Referer':site}
        req11 = urllib2.Request(site, headers=hdr)
        data = urllib2.urlopen(req11, timeout=40)
        page = data.read()
        page = page.decode('gbk')# 淘宝使用的是 GBK 的编码
        return page
    except Exception,e:
        print e
        return '错误'
#将图片写入本地
def write_image(url,path):
    data = urllib2.urlopen(url).read()  
    f = file(path,"wb")  
    f.write(data)



# 测试保存图片
_taobao_itmes_all_all_('https://detail.tmall.com/item.htm?spm=a1z10.3-b.w4011-14225354334.29.3uTI47&id=520792741995&rn=55bf8b2bec12a5d850f2907ec9b85826&abbucket=9&skuId=3103701958589')












