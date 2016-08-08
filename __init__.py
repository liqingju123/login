# encoding:utf-8
from pip._vendor import requests
from Cookie import Cookie
from pip._vendor.requests import cookies
import re
import urllib2
import datetime
from time import sleep
import time
from threading import Thread
from distutils.tests.setuptools_build_ext import if_dl

host ='http://www.guahao.com'

def rm_all_pasce(text):
    return text.replace("\n", "").replace("\t", "").replace(' ', '').replace('\r', '').replace('<<收起', '')
def get_html(site):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36','Referer':site}
        req = urllib2.Request(site, headers=hdr)
        page = urllib2.urlopen(req,timeout= 10000)  
        print page.getcode()
        html_1 =page.read() 
        return html_1
    except:
        print  '走的错误'
        return '错误'


# 获取所有医生的链接
def get_doctor_all_url():
    get_urls = 'http://www.guahao.com/search/expert?dt=all&phone=&sort=haoyuan&ht=all&diagnosis=&hospitalId=&hk=all&hl=all&imagetext=&activityId=&fhc=&standardDepartmentId=&hydate=all&fg=1&ipIsShanghai=false&mf=true&iSq=1&consult=all&c=%E4%B8%8D%E9%99%90&dty=all&volunteerDoctor=&o=all&searchAll=Y&q=+&p=%E5%85%A8%E5%9B%BD&ci=all&pi=all&es=all&hdi=&pageNo='
    input_txt =open('/Users/imac/Downloads/好大夫所有医生/唯一集团/医生链接.txt','a')

    for index in range(515,32017):  
        html_txt=get_html(get_urls+str(index))
        print index
        list_img =re.findall(r'<a target="_blank" href="(.*)" onmousedown="return _smartlog\(this,\'TJZJ\'\)" class="cover-bg"></a>', html_txt)#获取医生个人链接
        for one_img in list_img:
            input_txt.write(rm_all_pasce(one_img)+'\n')
            print one_img
    input_txt.close()
    print '完毕'

def get_more_text(text_doctor_info):
    return re.findall(r'<a href="javascript:;" data-description="([\s\S]*?)">更多</a>',text_doctor_info)  

def name_zhuzhiyis_guanxian(all_info):
    return rm_all_pasce(all_info).replace('<strong>','').replace('</strong>','__').replace('<span>/</span>','__').replace('<span>','').replace('</span>','')



#获取简介
def get_jianjie(text_doctor_info):
    text_all_shanchang_txt = re.findall(r'<div class="about">[\S\s]*?</div>',text_doctor_info) # 获取所有的简介  
    if len(text_all_shanchang_txt)==0:
        return '错误'
    get_more_text_list = get_more_text(text_all_shanchang_txt[0])
    if len(get_more_text_list)>0:
        return get_more_text_list[0]# 长简介
    else:
        text_all_shanchang =  re.findall(r'<b>简介：</b>[\s\S]*?<span>([\s\S]*?)</span>',text_all_shanchang_txt[0]) #，没有长擅长那就获取短擅长
        if len(text_all_shanchang)>0:
            return text_all_shanchang[0]#短简介
        else:
            return '暂无'
#获取擅长
def get_shanchang(text_doctor_info):
    text_all_shanchang_txt = re.findall(r'<div class="goodat">[\S\s]*?</div>',text_doctor_info) # 获取所有的擅长
    if len(text_all_shanchang_txt)==0:
        return '错误'
    get_more_text_list = get_more_text(text_all_shanchang_txt[0])
    if len(get_more_text_list)>0:
        return get_more_text_list[0]# 擅长
    else:
        text_all_shanchang =  re.findall(r'<b>擅长：</b>[\s\S]*?<span>([\s\S]*?)</span>',text_all_shanchang_txt[0]) #，没有长擅长那就获取短擅长
        if len(text_all_shanchang)>0:
            return text_all_shanchang[0]#短简介
        else:
            return '暂无'

#姓名——科室——职务
def get_doctor_name_keshi(text_doctor_info):
    text_all =re.findall(r'<h1>([\s\S]*?)</h1>',text_doctor_info)
    if len(text_all)==0:
        return '错误'
    zhiwu= name_zhuzhiyis_guanxian(text_all[0])# 获取医生 姓名——科室——职务
    all_text =zhiwu.split('__')
    if len(all_text)==3:
        return zhiwu
    else:
        return zhiwu+'__1'
    
def not_have_doctor(text_doctor_info):
    if(re.findall(r'<div class="msg">[\s\S]*</div>', text_doctor_info)):
        return False
    return True
    
    

# 医院科室
def get_yiyuan_keshi(text_doctor_info):
    text_all =  re.findall(r'<a title=[\s\S]*?href=[\s\S]*?target=\"_blank\"[\s\S]*?onmousedown=\"return _smartlog\(this,\'YIYUAN\'\)\">([\s\S]*?)</a>',text_doctor_info) 
    text_all_keshi =  re.findall(r'<a href="http://www.guahao.com/department/.*?" target="_blank" onmousedown="return _smartlog\(this,\'KESHI\'\)\S\s]*?>([\S\s]*?)</a>',text_doctor_info) 
    yiyuankeshi=''
    for index in range(0,len(text_all)):
        yiyuankeshi =yiyuankeshi+ rm_all_pasce(text_all[index]+','+text_all_keshi[index])+','# 医院--科室
    return yiyuankeshi

# 获取医生挂号信息    
def guahao(text_doctor_info):
    guahaoinfo =''
    text_all_shanchang =  re.findall(r'<a href="javascript:;" class="guahao active" data-scroll-top="service-guahao" title="预约挂号" onmousedown="return _smartlog\(this,\'GUAHAO_KJ\'\)">挂号</a>',text_doctor_info)
    if len(text_all_shanchang)>0:
        text_all_shanchang =  re.findall(r'<p style="font-size: 14px;">([\s\S]*?)</p>',text_doctor_info)    
        if len(text_all_shanchang)>0:
            for one_zhuyishixiang in text_all_shanchang: #注意事项
                guahaoinfo= one_zhuyishixiang  #有就返回
        else:
            guahaoinfo ='医生已开通挂号服务'  #已开通 没有注意事项        
    else:
        guahaoinfo ='医生未开通挂号服务'    #医生未 没有注意事项  

    return guahaoinfo


# 图文咨询
def tuwen_zixun(text_doctor_info):
    text_all =  re.findall(r'<div class="item animation-hover-flash tuwen active" data-href="http://www.guahao.com/expert/consult/ask.*?" onmousedown="return _smartlog\(this,\'TWWZ\'\)">[\s\S]*?</div>',text_doctor_info) 
    if len(text_all)>0:
        tuwen_list =re.findall(r'<strong>(.*?)</strong>',text_all[0])
        return '图文咨询价格:' +str(len(tuwen_list)>0 and tuwen_list[0] or '错误')
    else:
        return '暂未开通图文咨询'

#电话问诊
def _dianhua(text_doctor_info):
    text_shipinzixun =re.findall(r'<div class="item animation-hover-flash dianhua active">([\s\S]*?)</div>', text_doctor_info)

    if len(text_shipinzixun)>0:
        shipinjiage = re.findall('strong>(.*?)</strong>', text_shipinzixun[0]) 
        return '电话咨询价格:'+str(len(shipinjiage)>0 and shipinjiage[0] or '错误')
    else:
        return '暂无开通电话预约'

#视频问诊
def shipinwenzhen(text_doctor_info):
    text_all_jiage =re.findall(r'<div class="service-popup-shipin J_PopupShipin J_Remind" style="width:400px;padding:0;left:603px;top:100px;" data-load=\'([\s\S]*?)\'>',text_doctor_info)
    if len(text_all_jiage)==0:
        return '错误'
    url_shipin =host+text_all_jiage[0]
 
    if url_shipin.endswith('='):
        return '暂无开通视频问诊'
    else:
        jiage =re.findall('"originalFee":"(.*?)"', get_html(url_shipin))
        if len(jiage)>0:
            return '视频问诊价格：'+jiage[0]+'__'+url_shipin
        else:
            return '暂无开通视频问诊'

def get_all_txt(text_doctor_info):
    print '多线程时间开始== '+str(datetime.datetime.now())
#     thread.start_new_thread(get_doctor_name_keshi, (text_doctor_info,))
#     thread.start_new_thread(get_yiyuan_keshi, (text_doctor_info,)) 
#     thread.start_new_thread(get_shanchang, (text_doctor_info,)) 
#     thread.start_new_thread(get_jianjie, (text_doctor_info,)) 
#     thread.start_new_thread(guahao, (text_doctor_info,)) 
#     thread.start_new_thread(tuwen_zixun, (text_doctor_info,)) 
#     thread.start_new_thread(_dianhua, (text_doctor_info,)) 
#     thread.start_new_thread(shipinwenzhen, (text_doctor_info,)) 
#     print '多线程时间结束== '+str(datetime.datetime.now())

# text_doctor_info = get_html('http://www.guahao.com/expert/138181403422390000?hospDeptId=138181401423383000')
# text_doctor_info = get_html('http://www.guahao.com/expert/138181403984930000?hospDeptId=138181401643702000')

doctor_all_txt =open('/Users/imac/Downloads/好大夫所有医生/唯一集团/遗漏错误请求.txt','r')
write_input =open('/Users/imac/Downloads/好大夫所有医生/唯一集团/遗漏错误请求_详情.txt','a')
doctor_all_list =doctor_all_txt.readlines()
doctor_all_list =doctor_all_list[1240:]
for one_doctor in doctor_all_list:
    doctor_list_all_info=one_doctor.split('__')
    one_doctor =rm_all_pasce(doctor_list_all_info[len(doctor_list_all_info)-1])
    print '=====  '+one_doctor
    text_doctor_info = get_html(one_doctor)
#     text_doctor_info = get_html(rm_all_pasce(text_doctor_info))
    if text_doctor_info=='错误':
        write_input.write('错误__'+one_doctor+'\n')
    else:
        if(not_have_doctor(text_doctor_info)):
            doctor_info = get_doctor_name_keshi(text_doctor_info)+'__'+get_yiyuan_keshi(text_doctor_info)+'__'+get_shanchang(text_doctor_info)+'__'+get_jianjie(text_doctor_info)+'__'+rm_all_pasce(guahao(text_doctor_info))+'__'+tuwen_zixun(text_doctor_info)+'__'+_dianhua(text_doctor_info)+'__'+shipinwenzhen(text_doctor_info)
            print doctor_info
            write_input.write(rm_all_pasce(doctor_info+'__'+doctor_list_all_info[len(doctor_list_all_info)-1])+'\n')
#             write_input.write(rm_all_pasce(doctor_info+'__'+one_doctor)+'\n')
        else:
            print '该医生不存在'
            write_input.write(rm_all_pasce('没有该医生'+'__'+doctor_list_all_info[len(doctor_list_all_info)-1])+'\n') 
    
    sleep(2)   
        
write_input.close()
doctor_all_txt.close()

         


 


