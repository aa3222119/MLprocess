import json,time,random
from urllib.request import urlopen, quote
import requests,csv
import pandas as pd 
import sys,os
import difflib
import warnings
warnings.filterwarnings("ignore")
 
 
def levenshtein1(s1,s2): 
    m=[[0 for i in range(len(s2)+1)] for j in range(len(s1)+1)]
    for i in range(len(s1)+1):
        for j in range(len(s2)+1):
            if i==0 or j==0:
                m[i][j]=max(i,j)
            else:
                m[i][j]=min(m[i][j-1]+1,m[i-1][j]+1,m[i-1][j-1]+(1 if s1[i-1] != s2[j-1] else 0))
        #print(m[i])
    return m[len(s1)][len(s2)]


def levenshtein(lst1,lst2,i,j):  
    if min(i,j) == -1:  
        return max(i,j)+1  
    return min(  
        levenshtein(lst1,lst2,i-1,j)+1,  
        levenshtein(lst1,lst2,i,j-1)+1,  
        levenshtein(lst1,lst2,i-1,j-1)+(1 if lst1[i] != lst2[j] else 0))


def get_gaode_lnglat(address,name):#高德api取经纬度
    ak='1c56354f2ee9098742333b3b3c6893b6'#'608d75903d29ad471362f8c58c550'#'7ec25a9c6716bb26f0d25e9fdfa012b8'#1c56354f2ee9098742333b3b3c6893b6'  
    url = 'http://restapi.amap.com/v3/geocode/geo'
    uri = url + '?' + 'key='+ak+'&address='+address+name
    try:
        req=requests.get(uri)
        temp=req.json() 
        #print(temp)
        location= temp['geocodes'][0]['location'].split(',')
        return location[0],location[1]
    except Exception:
        print(uri+'   高德错啦')
        return '', ''

def get_baidu_lnglat(name, address):#百度api取经纬度
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'BhMsRoY3GgWHvINnpdw1WfD4'#'uSa21BRDeqeoLBLmvwt1YBpzGMcfnA3G'#'afVRYRDraiBW7TCe5YwCDdTjym88DYeI'#'7Kn4ozd5ZZWujbggtPRtaL0XrwaEqC8L'#'HTkDeHAw2OVWUU5sf2aGA4xG'#'uSa21BRDeqeoLBLmvwt1YBpzGMcfnA3G',7Kn4ozd5ZZWujbggtPRtaL0XrwaEqC8L
    address_name = (address if address else '')+(name if name else '')
    add = quote(str(address_name[:40]).encode('utf-8')) #由于本文城市变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
    try:
        req = urlopen(uri)
        res = req.read().decode()  # 将其他编码的字符串解码成unicode
        temp = json.loads(res)  # 对json数据进行解析
        lng = temp['result']['location']['lng']
        lat = temp['result']['location']['lat']
        confidence = temp['result']['confidence']
        precise = temp['result']['precise']
        return lng,lat,confidence,precise
    except Exception as err :
        print(uri+'   百度错啦',err)
        return 0,0,0,0

def get_baidu_location(lat, lng):
    url = "http://api.map.baidu.com/geocoder/v2/?location="
    uri = url + str(lat) + "," + str(lng) + "&output=json&pois=1&ak=" + "BhMsRoY3GgWHvINnpdw1WfD4"
    req = urlopen(uri)
    res = req.read().decode()  # 将其他编码的字符串解码成unicode
    # res = re.findall('{[\w\W]*}', res)[-1]
    temp = eval(res)  # 对json数据进行解析
    province = temp['result']['addressComponent']['province']
    city = temp['result']['addressComponent']['city']
    district = temp['result']['addressComponent']['district']
    return province, city, district


tag_weight = {'写字楼':3, '住宅区':4, '房屋中介,物流公司,政府机构':0.3, '综合医院,专科医院':2, '高等院校':1.5, '中学,小学,幼儿园':0.6, '运动健身,休闲娱乐,购物':0.6}
aks = ['BhMsRoY3GgWHvINnpdw1WfD4', 'uSa21BRDeqeoLBLmvwt1YBpzGMcfnA3G', 'HTkDeHAw2OVWUU5sf2aGA4xG', 'afVRYRDraiBW7TCe5YwCDdTjym88DYeI'] + \
      ['7Kn4ozd5ZZWujbggtPRtaL0XrwaEqC8L']

def get_num_from_url(url):
    res = {'status': 401, 'message': '当前..'}
    try:
        res = eval(requests.get(url).text)
        return res['results'].__len__()
    except:
        print(res,end='>> ')
        if res['status'] == 401:
            time.sleep(1)
            return get_num_from_url(url)


def get_around_carnum_bybaidu(lat, lng):
    carnumk = 0.1
    ak = random.choice(aks)
    try:
        for k,v in tag_weight.items():
            print(v,k,end='>> ')
            # if random.random() > 1:
            #     ak = aks[1]
            # else:
            #     ak = aks[0]
            # ak = aks[3]
            latlng = str(lat) + "," + str(lng)
            url2 = "http://api.map.baidu.com/place/v2/search?query=%s&location=%s&radius=1500&output=json&page_size=10&ak=%s" %(k, latlng, ak)
            encodedStr2 = quote(url2, safe="/:=&?#+!$,;'@()*[]")
            num = get_num_from_url(encodedStr2)
            print(num,end='>> ')
            carnumk += v*num * 0.2
            time.sleep(0.2)
            url8 = "http://api.map.baidu.com/place/v2/search?query=%s&location=%s&radius=5000&output=json&page_size=10&ak=%s" % (k, latlng, ak)
            encodedStr8 = quote(url8, safe="/:=&?#+!$,;'@()*[]")
            num = get_num_from_url(encodedStr8)
            print(num)
            carnumk += v * num * 0.08
            time.sleep(0.2)
    except:

        aks.pop(aks.index(ak))
        print('some mistake',len(aks))
        carnumk = 0
        time.sleep(2)
    return carnumk


def check_match(data_org,data_tyc):  # 找到书上的数据和天眼查数据的区别，并使用天眼查的数据补全书上的信息。

    data_org['company_']=''
    data_org['human_']=''
    data_org['min_sim']=-1
    data_org['min_sim_num']=0

    for i,row in data_org.iterrows():

        name_org = row['企业名称']
        data_tyc['sim'] = data_tyc['公司名称'].map(lambda x : levenshtein1(x,name_org))
        data_org.loc[i,'min_sim'] = data_tyc['sim'].min()
        data_tyc_min = data_tyc[data_tyc['sim']==data_org.loc[i,'min_sim']].reset_index()
        data_org.loc[i,'min_sim_num'] = len(data_tyc_min)
        data_org.loc[i,'company_'] = data_tyc_min['公司名称'][0]
        data_org.loc[i,'human_'] = data_tyc_min['法定代表人'][0]
        data_org.loc[i,'reg_capital_'] = data_tyc_min['注册资本'][0]
        data_org.loc[i,'Est_time_'] = data_tyc_min['成立日期'][0]
        data_org.loc[i,'tel_'] = data_tyc_min['联系电话'][0]
        data_org.loc[i,'address_'] = data_tyc_min['地址'][0]
        data_org.loc[i,'website_'] = data_tyc_min['企业网址'][0]
        data_org.loc[i,'email_'] = data_tyc_min['邮箱'][0]
        data_org.loc[i,'Bus_scope_'] = data_tyc_min['经营范围'][0]

def get_latlng(df_stations):#对天眼查的数据，找到每个企业的经纬度，并把经纬度补充到原数据上。
    data=df_stations.reset_index()
    num=0
    print('共',len(data),'条数据')
    for i,row in data.iterrows():
        name=data.loc[i,'公司名称']
        address=data.loc[i,'地址']

        baidu_lng,baidu_lat=get_baidu_lnglat(str(name),str(address)) 
        data.loc[i,"baidu_lat"]=baidu_lat
        data.loc[i,"baidu_lng"]=baidu_lng
        gaode_lng,gaode_lat=get_gaode_lnglat(str(address),str(name))
        data.loc[i,"gaode_lat"]=gaode_lat
        data.loc[i,"gaode_lng"]=gaode_lng

        num=num+1
        if num%50==0:
            print(num,'条数据成功')
        else:
            continue
    data.to_excel('D:\python\W河北邯郸-加油站-全(1)_经纬度.xlsx')    
if __name__ == "__main__":
    PRO_PATH = 'D:\python\map'
    cmd_win = 'dir %s\加油站 /b /s | find ".xls"' % PRO_PATH
    filepath_list = os.popen(cmd_win).read().strip().split()
    df_stations = []
    for filepath in filepath_list:
        df_stations = df_stations.append(pd.read_excel(filepath,skiprows=1)) if len(df_stations) else pd.read_excel(filepath,skiprows=1)		
    #data=pd.read_csv('D:/python/map/oil.csv',encoding='gbk',sep ='\t',header=None)
    data=df_stations.reset_index()
    num=0
    print('共',len(data),'条数据')
    for i,row in data.iterrows():
        name=data.loc[i,'公司名称']
        address=data.loc[i,'地址']

        baidu_lng,baidu_lat=get_baidu_lnglat(str(name),str(address)) 
        data.loc[i,"baidu_lat"]=baidu_lat
        data.loc[i,"baidu_lng"]=baidu_lng
        gaode_lng,gaode_lat=get_gaode_lnglat(str(address),str(name))
        data.loc[i,"gaode_lat"]=gaode_lat
        data.loc[i,"gaode_lng"]=gaode_lng

        num=num+1
        if num%50==0:
            print(num,'条数据成功')
        else:
            continue
    data.to_excel('D:\python\W河北邯郸-加油站-全(1)_经纬度.xlsx')