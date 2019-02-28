
import urllib
import requests, random
import threading
import sys
sys.path.append('../DBbase')
from db_func import *
from hcomponents import *
import re
import os
import threading 
 
import bs4 
import datetime
from datetime import datetime

import pymysql
import warnings
warnings.filterwarnings("ignore")
pymysql.install_as_MySQLdb()
from bs4 import BeautifulSoup
#from multiprocessing.dummy import Pool as ThreadPool

def connectdb():
    db = pymysql.connect(host=HOST2,user=USER2,passwd=PASSWORD2,db=DATABASE2,charset='utf8')
    db.autocommit(True)
    cursor = db.cursor()
    return (db,cursor)
def read_mysql_get_ip():
    db1,cursor1=connectdb()
    today=datetime.now().strftime('%Y-%m-%d')  
    cmd1 = "select * from ips"
    original_data=cursor1.execute(cmd1)
    db1.commit()
    original_data1=cursor1.fetchmany(original_data)
    db1.close()
    cursor1.close()
    ip_data=pd.DataFrame(list(original_data1),columns=["ip","port","anonymous_degree","degree_delta","agent_type","response_time","response_time_delta","location","Verify_time","updata_time","test_times","success_times","fit","origin","reversed"])              
    return ip_data
def replace_ip_sql(oil_data):
    db2,cursor2=connectdb()
    cursor2 = db2.cursor()
    cmd2 = "REPLACE INTO ips VALUES ('%s','%s' ,'%s', '%s' ,'%s', '%s','%s', '%s' ,'%s','%s', '%s' , '%s','%s','%s','%s');" % (oil_data["ip"],oil_data["port"],oil_data["anonymous_degree"],oil_data["degree_delta"],oil_data["agent_type"],oil_data["response_time"],oil_data["response_time_delta"],oil_data["location"],oil_data["Verify_time"],oil_data["updata_time"],oil_data["test_times"],oil_data["success_times"],oil_data["fit"],oil_data["origin"],oil_data["reversed"])       
    cursor2.execute(cmd2)
    db2.commit()
    db2.close()
    cursor2.close()
def Replace_mysql(oil_data):    
    db2,cursor2=connectdb()
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

def judge_proxie(ip,return_ip):
    if return_ip == []:
        return 0
        pass
    print('return_host_ip:'+str(return_host()[0]))
    if return_ip == return_host():
        return 0
    else:
        if ip['ip'] == return_ip[0]:
            return 1
        else:
            return 2
            
def return_host(proxies):
    return_ip = ''
    timer0 = Timer_(0)
    try:
        url = "http://2018.ip138.com/ic.asp"
        web_data = requests.get(url, proxies=proxies, timeout=6)
        # return_ip=re.findall(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])', web_data.text)
        return_ip = re.findall(r'\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]', web_data.text)
    except Exception as err:
        # print(err)
        pass
    timer0.toc()
    return timer0.tictoc[-1], return_ip


# bdtable_name = 'bi_papapa.ips'


def runtime_get_tododf():
    my = my_(config.MYSQL_BI_RW_ENV)
    sqls = """select * from bi_papapa.ips
           where UNIX_TIMESTAMP(Verify_time) < UNIX_TIMESTAMP(now()) - 999
           order by test_times-success_times-anonymous_degree+UNIX_TIMESTAMP(Verify_time)/3600 limit 100"""
    df = my.to_dataframe(sqls)
    return df


def ipsdic_upd(re_dict,type='update'):
    my = my_(config.MYSQL_BI_RW_ENV)
    ip = re_dict.pop('ip')
    port = re_dict.pop('port')

    if type == 'delete':
        my.sql_engine("delete from bi_papapa.ips where where ip='%s' and port=%d" %(ip, port))
    else:
        upd_sqlsf = "update bi_papapa.ips set %s where ip='%s' and port=%d"
        ss = ','.join(['%s=%s' % (k, v) for k, v in re_dict.items()])
        upd_sqls = upd_sqlsf % (ss, ip, port)
        # print(upd_sqls)
        my.sql_engine(upd_sqls)

veryupd_dict = {'anonymous_degree': '(anonymous_degree + 0)/2',
                'degree_delta':'degree_delta-1',
                    'response_time': '(response_time+6)/2',
                    'response_time_delta': 'response_time_delta+1',
                    'Verify_time': 'now()',
                    'test_times': 'test_times+1'}
GLO_sta = {}
delta_t, local_ip = return_host('')
print(local_ip)
GLO_sta['delta_t'] = delta_t
GLO_sta['local_ip'] = local_ip[0]
print(GLO_sta)


def verify_ips(row):

    ips_dict = veryupd_dict.copy()
    for v in ['ip', 'port']:
        ips_dict[v] = row[v]
    if 'http' in row['agent_type'] or 'HTTP' in row['agent_type']:
        agt_ss = 'http://%s:%s' % (row['ip'], row['port'])
        delta_t, pro_ip = return_host({'http': agt_ss})
        # print(agt_ss, delta_t, pro_ip)
        if pro_ip:
            anod = 0 + (0 if pro_ip[0] == GLO_sta['local_ip'] else 1) + (0 if pro_ip[0] in [row['ip'], GLO_sta['local_ip']] else 1)
            ips_dict['anonymous_degree'] = '(anonymous_degree + %s)/2' % anod
            ips_dict['response_time'] = '(response_time+%2.4s)/2' % delta_t
            ips_dict['success_times'] = 'success_times+1'
            ips_dict['response_time_delta'] = '%2.4s - response_time' % delta_t
            ips_dict['degree_delta'] = '%2.4s - anonymous_degree' % anod
            print(agt_ss, delta_t, pro_ip, anod)
            # elif random.random() > 0.8:
            #     ipsdic_upd(ips_dict, 'delete')
            #     continue
    ipsdic_upd(ips_dict)


def xx():
    df = runtime_get_tododf()
    task_list = []
    for i,row in df.iterrows():
        task = threading.Thread(target=verify_ips, args=(row,))
        task_list += [task]
        task.setDaemon(True)
        task.start()
        time.sleep(0.1)
    [t.join(12) for t in task_list]

def drop_smips():
    del_sqls1 = ['delete from bi_papapa.ips where origin < 0 and success_times = 0 and test_times > 2 order by Verify_time desc limit 200',
                 'delete from bi_papapa.ips where origin < 0 and success_times = 0 and test_times > 1 order by Verify_time desc limit 20',
                 'delete from bi_papapa.ips where success_times = 0 and test_times > 6 order by Verify_time desc limit 200',
                 'delete from bi_papapa.ips where success_times = 0 and test_times > 4 order by Verify_time desc limit 20',
                 'delete from bi_papapa.ips where degree_delta < -7 and anonymous_degree < 0.1 order by degree_delta-response_time limit 100',
                 'delete from bi_papapa.ips where degree_delta < -3 and anonymous_degree < 0.1 order by degree_delta-response_time limit 9',
                 'delete from bi_papapa.ips where anonymous_degree < 0.1 order by -test_times+success_times+anonymous_degree-UNIX_TIMESTAMP(Verify_time)/3600  limit %s' %random.randint(0, 30),]
    sqls = random.choice(del_sqls1)
    print(sqls,my_(config.MYSQL_BI_RW_ENV).sql_engine(sqls), end='>> ')

def do_():
    time_intval = 87
    while(1):
        if random.randint(0, 100) > 35:
            print('验证一波', end='>> ')
            xx()
        else:
            drop_smips()
            time.sleep(12)
        print('停留%ss' % time_intval)
        time.sleep(time_intval)

def updata_degree(degree,ip_data):
    ip_data['anonymous_degree']=degree #0.5*ip_data['anonymous_degree']+0.5*degree
    return ip_data
def ini_proxies(ip_data):#初始化
    #print(ip_data)
    url="http://2017.ip138.com/ic.asp"
    proxies={"http":"http://"+str(ip_data["ip"])+":"+str(ip_data["port"])}
    #print(ip_data['ip'])
    try:
        start1 = time.time()
        web_data = requests.get(url,proxies=proxies,timeout=5)
        end1 = time.time()
        html=web_data.text
        ip_data['agent_type']='http'
        ip_data['response_time']=(end1-start1)#0.5*ip_data['response_time']+0.5*(end1-start1)
        ip_data['success_times']+=1
        return_ip=re.findall(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])',html)
        print('return_ip:'+str(return_ip[0]))
        degree=judge_proxie(ip_data,return_ip)
        ip_data['degree_delta']=0
        ip_data['response_time_delta']=0
        ip_data=updata_degree(degree,ip_data)
        
    except Exception as err:
        #print(err)
        ip_data['anonymous_degree']=0
        ip_data['response_time']=5
    #print(ip_data)
    ip_data['test_times']+=1
    ip_data['updata_time']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
    ip_data['fit']=0
    ip_data['origin']=1
    replace_ip_sql(ip_data)

if __name__ == "__main__":
    do_()
