# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import urllib.request
import sys
import os
import bs4 
import datetime
from datetime import datetime
from config import *
import time
time.strftime('%Y%m%d')
import pymysql
import warnings
warnings.filterwarnings("ignore")
pymysql.install_as_MySQLdb()

from bs4 import BeautifulSoup
# 功能：爬取代理IP


def connectdb(host,user,passward,database):
    db = conn = pymysql.connect(host=host,user=user,passwd=passward,db=database,charset='utf8')
    db.autocommit(True)
    cursor = db.cursor()
    return (db,cursor)

def Replace_mysql(oil_data):    
    db2,cursor2=connectdb(HOST2,USER2,PASSWORD2,DATABASE2)
    cursor2 = db2.cursor()
    #print(len(oil_data))
    #print(oil_data)
    for i in range(0,len(oil_data)):
        #print(oil_data.get_value(i,"ip"),oil_data.get_value(i,"port"),oil_data.get_value(i,"anonymous_degree"),oil_data.get_value(i,"agent_type"),oil_data.get_value(i,"response_time"),oil_data.get_value(i,"location"),oil_data.get_value(i,"Verify_time"),oil_data.get_value(i,"updata_time"),oil_data.get_value(i,"test_time"),oil_data.get_value(i,"reversed"))
        cmd2 = "REPLACE INTO ips VALUES ('%s','%s' ,'%s', '%s' ,'%s', '%s','%s', '%s' ,'%s','%s', '%s' , '%s','%s','%s','%s');" % (oil_data.loc[i,"ip"],oil_data.loc[i,"port"],oil_data.loc[i,"anonymous_degree"],oil_data.loc[i,"degree_delta"],oil_data.loc[i,"agent_type"],oil_data.loc[i,"response_time"],oil_data.loc[i,"response_time_delta"],oil_data.loc[i,"location"],oil_data.loc[i,"Verify_time"],oil_data.loc[i,"updata_time"],oil_data.loc[i,"test_times"],oil_data.loc[i,"success_times"],oil_data.loc[i,"fit"],oil_data.loc[i,"origin"],oil_data.loc[i,"reversed"])       
        #print(cmd2)
        cursor2.execute(cmd2)
        db2.commit()
    db2.close()
    cursor2.close()
       
def  get_ip_list_2():
    uri="http://www.66ip.cn/areaindex_"
    #a="1/1.html"#---966.html
    ip_data=pd.DataFrame() 
    idx=0
    for city in range(1,35):
        try:
            url=uri+str(city)+"/1.html"
            response=urllib.request.urlopen(url)
            data=response.read()
            soup = BeautifulSoup(data, 'html.parser')
            tables = soup.find_all('table')
            table_soup = BeautifulSoup(str(tables[2]), 'html.parser')
            for i, tr in enumerate(table_soup.find_all('tr')):
                if i <1:   
                    continue
                else:
                    td=tr.find_all('td')
                    ip_data.loc[idx,'ip']=td[0].get_text()
                    ip_data.loc[idx,'port']=td[1].get_text()
                    ip_data.loc[idx,'anonymous_degree']=0 
                    ip_data.loc[idx,'agent_type']="http"
                    ip_data.loc[idx,'location']=td[2].get_text()
                    ip_data.loc[idx,'Verify_time']=datetime.now().strftime('%Y-%m-%d %H:%M:%S') #td[6].get_text()
                    ip_data.loc[idx,'updata_time']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    idx+=1
                if idx%500==0:    
                    print(str(idx)+"个ip处理了")
            #time.sleep(0.5)
            ip_data['test_times']=0
            ip_data['degree_delta']=0
            ip_data['response_time_delta']=0
            ip_data['success_times']=0
            ip_data['fit']=0
            ip_data['origin']=1
            ip_data['reversed']=''
            ip_data['response_time']=5
        except Exception:
            pass   
    return ip_data   
Replace_mysql(get_ip_list_2())  