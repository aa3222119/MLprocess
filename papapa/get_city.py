# -*- coding: utf-8 -*-
import os
PRO_PATH = 'F:\python_pro\papapa'
os.chdir(PRO_PATH + '\console')
import sys
sys.path.append('..\DBbase')
sys.path.append('..\console')
from db_func import *
from urllib.request import urlopen, quote
import requests,csv
import difflib
from math import *
import warnings
warnings.filterwarnings("ignore")
from bs4 import  BeautifulSoup


def get_lng_lat(address):
    lng=''
    lat=''
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'afVRYRDraiBW7TCe5YwCDdTjym88DYeI'
    add = quote(str(address).encode('utf-8')) 
    uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak    
    try:
        req = urlopen(uri)
        res = req.read().decode() #将其他编码的字符串解码成unicode
        temp = json.loads(res) #对json数据进行解析
        lng = temp['result']['location']['lng']
        lat = temp['result']['location']['lat']
    except Exception as e:
        print(e)
    return lng, lat  # 对json数据进行解析


def get_province(lng,lat):
    url='http://api.map.baidu.com/geocoder/v2/?'
    location=str(lat)+','+str(lng)
    output='json'
    ak='afVRYRDraiBW7TCe5YwCDdTjym88DYeI'
    uri=url+'&location='+location+'&output='+output+'&pois=1'+'&ak='+ak
    try:
        req = urlopen(uri)
        res = req.read().decode()  # 将其他编码的字符串解码成unicode
        temp = json.loads(res)  # 对json数据进行解析
        province = temp['result']['addressComponent']['province']
        province = province.split('省')[0]
        province = province.split('市')[0]
    except Exception as e:
        print(e)
        province = ''
    return "'%s'" % province


def init_city_2():
    # 初始化城市数据以及前两个维度，沿海以及一二三线
    database = 'bi_papapa'
    city_property_tablename ='pa_city_property'
    city_pro_table = '%s.%s' % (database, city_property_tablename)
    dw_in = my_(config.MYSQL_BI_RW_ENV)

    city_info=pd.DataFrame()
    url='http://www.sohu.com/a/215950130_120507'
    req = urlopen(url)
    html_doc=req.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    article=soup.find('article',class_='article')
    soup_div = BeautifulSoup(str(article), 'html.parser')
    ps=soup_div.find_all('p')
    # city_range=['一','二','三','四','五','六']
    sea_citys = ['上海', '天津', '大连', '秦皇岛', '青岛', '烟台', '威海', '连云港', '南通', '宁波', '温州', '福州', '广州', '湛江', '北海', '深圳', '珠海', '汕头', '厦门']
    number=0
    for i,p in enumerate(ps):
        if i<5 or i %2==1:
            continue
        if i>16:
            break
        citys=p.get_text()
        citys=citys.split('、')
        citys_name=[x.strip().split('市')[0] for x in citys]
        #citys_name=[x.strip().split('自治')[0] for x in citys_name]
        for j in citys_name:
            city_info.loc[number,'cityname'] = "'%s'" %j
            lng,lat=get_lng_lat(j)
            city_info.loc[number,'province']=get_province(lng,lat)
            city_info.loc[number,'longitude'],city_info.loc[number,'latitude']=lng,lat
            if j in sea_citys:
                sea_flat='0'
            else:
                sea_flat='1'
            if  int((i-6)/2)<2:  # 一线
                city_range_flat='00'
            elif int((i-6)/2)==2:  # 二线
                city_range_flat='01'
            elif  int((i-6)/2)==3:  # 三线
                city_range_flat='10'
            else:
                city_range_flat='11'
            city_info.loc[number,'property']=int(city_range_flat+sea_flat, 2)
            #print(city_info.loc[number,'property'])
            # city_info.loc[number,'create_time']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            number+=1
        #print(city_range[int((i-6)/2)],'线城市有：',citys_name)
    city_info.loc[:,'create_time'] = 'now()'

    print(city_info)
    dw_in.df_upd_tosql(city_info, 1000, city_pro_table)

def update_carnum():
    # 更新汽车保有量数据 http://www.chyxx.com/industry/201707/544427.html
    database = 'bi_papapa'
    city_property_tablename = 'pa_city_property'
    city_pro_table = '%s.%s' % (database, city_property_tablename)
    cars_citys = ['北京', '成都', '重庆', '上海', '苏州', '深圳', '天津', '郑州', '西安', '东莞', '武汉', '杭州', '石家庄', '广州', '青岛', '南京', '宁波', '佛山', '保定', '长沙', '昆明', '潍坊', '临沂']
    dw_in = my_(config.MYSQL_BI_RW_ENV)

    bit_w = 8
    sqls = f"update {city_pro_table} set property=property|{bit_w} "
    dw_in.sql_engine(sqls)
    for c in cars_citys:
        sqls = f"update {city_pro_table} set property=property^{bit_w} where cityname='{c}' and property&{bit_w}>0"
        dw_in.sql_engine(sqls)



