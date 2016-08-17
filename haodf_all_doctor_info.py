# encoding:utf-8
from bs4 import BeautifulSoup
from urllib import urlopen
import urllib2
import time
import sys     



add_url = 'http://www.haodf.com'
def rm_all_pasce(text):
    return text.replace("\n", "").replace("\t", "").replace(' ', '').replace('\r', '').replace('<<收起', '')

def get_html(site):
    hdr = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(site, headers=hdr)
    try:
        data = urllib2.urlopen(req, timeout=4)
        page = data.read()
        print '===请求到了==='
    except:
        return '1错误'
    try:
#         page1 = page.decode('gbk')
        return BeautifulSoup(page);
    except:
        return BeautifulSoup(page);

# 获取医院大名and小名    
def get_yiyuan_name(one_url):
    context = get_html(one_url)
    if context == '错误':
        return '错误'
    get_yinyuan_list = context.find_all('div', {"id":"ltb"})
    get_yinyuan_list_2 = context.find_all('div', {"class":"panelA_blue"})
    if len(get_yinyuan_list) == 0 or len(get_yinyuan_list_2) == 0:
        return '错误'

    daming_yiyuan = str(get_yinyuan_list[0].span.a.get_text().encode('utf-8'))

    yiyuan = str(get_yinyuan_list_2[0].p.get_text().encode('utf-8')).replace('(', '__').replace(')', '').replace(' ', '')
    return  daming_yiyuan + '__' + yiyuan  

# 获取 地址 医院 科室信息    
def  get_yiyuan_keshi(context_text):
#     print context_text
#     base_text = context_text.find_element_by_class_name('container').get_attribute('innerHTML')
    context_all_dev = BeautifulSoup(str(context_text), "html.parser")
#     print context_all_dev

    all_a = context_all_dev.find_all("div", {"class":"luj"});
    if len(all_a) == 0:
        return '错误'
    content_a_html = BeautifulSoup(str(all_a[0]), "html.parser")
    content_a_list = content_a_html.find_all("a", {"target":"_blank"});
    if len(content_a_list) < 4:
        return '错误'
    content_a_list = content_a_list[2:]
    one_a_all = str(content_a_list[0].get_text().encode('utf-8')) + '__' + get_yiyuan_name(add_url + str(content_a_list[1]['href'].encode('utf-8')))  # + '__' + str(content_a_list[1].get_text().encode('utf-8'))
    return one_a_all

def get_hist(host):
    context = get_html(host)
    if '错误' == context:
        return '错误'
    
    javas = context.find_all('script', {'type':'text/javascript'});
    if len(javas) < 2:
        return '错误'

    content_all = str(javas[2].get_text().encode('utf8')).replace('BigPipe.onPageletArrive({"id":"bp_doctor_about","content":"', '').replace('\n","cssList":[],"jsList":{"http:\/\/www.haodf.com\/api\/get_activetime.php?d=[0-9]+":0}});', '');
    content_all = content_all.decode("unicode-escape").encode("utf-8").replace('\\', '')

    get_hist = str(javas[1]).replace('<script type="text/javascript">BigPipe.onPageletArrive({"id":"bp_top","content":"', '').decode("unicode-escape").encode("utf-8").replace('\\', '')

    return get_doctor_info(content_all, get_hist, host) 

#read_doctor_log_err = open('/Users/imac/Downloads/liqingju_好大夫所有的医生/log/存储已请求医生信息_log_err_06_26.txt', 'wr');  # 没有请求到 擅长的
def get_doctor_info(base_text, context_text, host):
    context_all_dev = BeautifulSoup(base_text, "html.parser")
    all_text = str(get_yiyuan_keshi(context_text))
#     print 'all_text1==   '+all_text
    
    all_jianjie_zhicheng = context_all_dev.find_all("td", {"valign":"top"})
    if len(all_jianjie_zhicheng) < 6:
        return '错误'
#     print "=====   "+all_jianjie_zhicheng[7].get_text()
    zhicheng = rm_all_pasce(str(all_jianjie_zhicheng[6].get_text().encode('utf-8')))
    if '师' not in zhicheng:
        zhicheng = rm_all_pasce(str(all_jianjie_zhicheng[7].get_text().encode('utf-8')))
    all_text = str(all_text) + '__' + zhicheng.replace('师', '师__1')
   
    
    all_jianjie_name = context_all_dev.find_all("div", {"class":"nav"})
    all_text = all_text + '__' + rm_all_pasce(str(all_jianjie_name[0].h1.a.get_text().encode('utf-8')))
   
    # nav
    all_jianjie = context_all_dev.find_all("div", {"id":"full"})
#     print context_all_dev
    all_jianjie_shanchang = context_all_dev.find_all("div", {"id":"full_DoctorSpecialize"})
    if len(all_jianjie_shanchang) == 0:
        all_jianjie_shanchang = context_all_dev.find_all("div", {"id":"truncate_DoctorSpecialize"})
    if len(all_jianjie_shanchang) == 0:
        print '错误'
       # read_doctor_log_err.write(host + '\n')
    else:
        all_text = all_text + '__' + rm_all_pasce(str(all_jianjie_shanchang[0].get_text().encode('utf-8')))
     
   
    if len(all_jianjie) == 0:
        one_zhijiye = context_all_dev.find_all('td', {'colspan':'3', 'valign':'top'})
        all_text = all_text + '__' + rm_all_pasce(str(one_zhijiye[1].get_text().encode('utf-8')))
      
    else:
        for one_div in all_jianjie:
            text_str = str(one_div.get_text().encode('utf-8'));
            all_text = all_text + '__' + rm_all_pasce(text_str)
         
   
    return all_text



def input_txt(index, start_index, start_end):
    all_doctor_txt = open('/Users/imac/Downloads/liqingju_好大夫所有的医生/详细信息/错误.txt', 'r');
    all_doctor_txt_input = open('/Users/imac/Downloads/liqingju_好大夫所有的医生/详细信息/好大夫所有的医生信息_全部信息_10_2.txt', 'wr');
    read_doctor_log_06_26 = open('/Users/imac/Downloads/liqingju_好大夫所有的医生/log/存储已请求医生信息_log__07_2_%d.txt' % index, 'a');

    all_doctor_list = all_doctor_txt.readlines();
#     all_doctor_list = all_doctor_list[start_index:start_end]
    for doctor_url in all_doctor_list:
        doctor_url_list = doctor_url.split('__')
        doctor_url =doctor_url_list[len(doctor_url_list)-1].replace("\n", "")
        print doctor_url  # http://www.haodf.com/doctor/DE4r08xQdKSLBD0VWyqZSnk6w5sT.htm
        print str(get_hist(doctor_url))
        input_str = str(get_hist(doctor_url)) + '__' + str(doctor_url.encode('utf8')) + '\n'
        print input_str,
        all_doctor_txt_input.write(input_str)
        read_doctor_log_06_26.write(doctor_url + '\n')

    all_doctor_txt.close()
    all_doctor_txt_input.close()
    read_doctor_log_06_26.close()
input_txt(1,1,1)    
  #  read_doctor_log_err.close()
   #http://www.haodf.com/doctor/DE4r0eJWGqZNhlZWGOlzbFG6uJ8FLja7.htm 
# print get_hist('http://www.haodf.com/doctor/DE4r0eJWGqZNhlZWGOlzbFG6uJ8FLja7.htm')  


