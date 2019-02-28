import os
PRO_PATH = 'F:\python_pro\papapa'
os.chdir(PRO_PATH + '\console')
import sys
sys.path.append('..\DBbase')
sys.path.append('..\console')
from db_func import *
from hcomponents import *
import requests,time,re,random,os
from bs4 import BeautifulSoup
from Createandsqls import *
from get_station_func import *

# funct: df 存数据库前的字符串加标点 #
def df_add_singlequotemark(df):
    for co in df.columns:
        if df[co].dtype.char == 'M' or df[co].dtype.char == 'O':
            df[co] = df[co].map(lambda x: re.sub(re.compile('\s'), '', str(x)))   # 去掉\s
            if len(df[co]) and type(df[co][0]) is str and len(df[co][0])>1 and df[co][0][0] + df[co][0][-1] == "''":   # 避免重复加
                continue
            df[co] = df[co].apply(lambda x: ("'%s'" %str(x).strip().replace("'", "").replace('%', '%%').replace('\\', '')) if x else None)
    return df


def save_human_record():
    database = 'bi_papapa'
    tablename = 'pa_stations_human_record_enc'
    df_human_record = pd.read_excel(PRO_PATH+'\加油站\全本修订后.xlsx').fillna('')
    df_human_record.columns = ['name', 'st_human', 'address', 'province']
    df_human_record_s = df_add_singlequotemark(df_human_record)
    df_human_record_s['create_time'] = 'now()'

    dw_in = my_(config.MYSQL_BI_RW_ENV)
    dw_in.getdata(create_sqls[tablename])
    dw_in.df_upd_tosql(df_human_record_s, 1000, '%s.%s' % (database,tablename))


def save_tianyancha_output():
    cmd_win = 'dir %s\\tianyancha /b /s | find ".xls"' % PRO_PATH
    filepath_list = os.popen(cmd_win).read().strip().split()
    df_stations = []
    for filepath in filepath_list:
        print(filepath)
        df_stations = df_stations.append(pd.read_excel(filepath,skiprows=1)) if len(df_stations) else pd.read_excel(filepath,skiprows=1)
        print(df_stations.columns)
    df_stations = df_stations.reset_index().fillna('')
    df_stations.columns = ['stid', 'name', 'st_human', 'registered_capital', 'establish_date', 'phone', 'address',
                           'home_page', 'email', 'operation_Scope']
    df_stations_s = df_add_singlequotemark(df_stations)
    df_stations_s['create_time'] = 'now()'
    df_stations_s = df_stations_s.drop(['stid'], 1)    # df_stations_s.stid = df_stations_s.index

    database = 'bi_papapa'
    tablename = 'pa_stations_muchcols_enc'
    dw_in = my_(config.MYSQL_BI_RW_ENV)
    dw_in.getdata(create_sqls[tablename])
    dw_in.df_upd_tosql(df_stations_s, 1000, '%s.%s' % (database, tablename))



def save_juhe_output():
    df_juhe = pd.read_excel(PRO_PATH + '/station_list_20171111.xlsx')
    df_juhe = df_juhe[['name', 'areaname', 'address', 'brandname', 'type', 'lat', 'lon', 'fwlsmc']]
    df_juhe.columns = ['name', 'fullregion', 'address', 'brandname', 'shoptype', 'latitude', 'longitude', 'fwlsmc']
    df_juhe_s = df_add_singlequotemark(df_juhe)
    df_juhe_s['create_time'] = 'now()'

    database = 'bi_papapa'
    tablename = 'pa_stations_juhe_enc'
    dw_in = my_(config.MYSQL_BI_RW_ENV)
    dw_in.getdata(create_sqls[tablename])
    dw_in.df_upd_tosql(df_juhe_s, 1000, '%s.%s' % (database, tablename))


def get_latlngfrom_baidu():
    time.sleep(0.02)
    if random.random() > 0.5:
        limit = random.randint(1, 2000)
    else:
        limit = 0
    database = 'bi_papapa'
    tablename = 'pa_stations_muchcols_enc'
    db_table = '%s.%s' %(database, tablename)
    sqls = 'select * from %s where update_time is null limit %s,1' %(db_table,limit)
    upd_sql = 'update %s set longitude = %s,latitude=%s,confidence=%s,precise=%s,update_time=now() where stid = %s'
    dw_in = my_(config.MYSQL_BI_RW_ENV)
    df = dw_in.to_dataframe(sqls)
    if df.__len__() ==1:
        stid = df.stid[0]
        longitude, latitude, confidence, precise = get_baidu_lnglat(df.name[0], df.address[0])
        print(longitude, latitude, confidence, precise)
        if longitude and latitude:
            upd_sql_s = upd_sql % (db_table,longitude,latitude,confidence, precise,stid)
            print(upd_sql_s)
            dw_in.getdata(upd_sql_s)
        else:
            dw_in.getdata('update %s set update_time=now() where stid = %s' % (db_table, stid))


def get_loc_from_baidu():
    time.sleep(0.02)
    if random.random() > 0.5:
        limit = random.randint(1, 2000)
    else:
        limit = 0
    database = 'bi_papapa'
    tablename = 'pa_stations_muchcols_enc'
    db_table = '%s.%s' % (database, tablename)
    sqls = "select * from %s where province='' and latitude>0 and longitude>0 and update_time<FROM_UNIXTIME(UNIX_TIMESTAMP(now()) - 60) limit %s,1" % (db_table, limit)
    upd_sql = "update %s set province = '%s',city='%s',region='%s',update_time=now() where stid = %s"
    dw_in = my_(config.MYSQL_BI_RW_ENV)
    df = dw_in.to_dataframe(sqls)
    if df.__len__() == 1:
        stid = df.stid[0]
        province, city, region = get_baidu_location(df.latitude[0], df.longitude[0])
        print(df.name[0],df.address[0],province, city, region)
        if province:
            upd_sql_s = upd_sql % (db_table, province, city, region, stid)
            print(upd_sql_s)
            dw_in.getdata(upd_sql_s)
        else:
            dw_in.getdata('update %s set update_time=now() where stid = %s' % (db_table, stid))

# for i in range(10000):
#     get_latlngfrom_baidu()
# for j in range(10000):
#     get_loc_from_baidu()


def devide_by_name(name):
    forg = ['碧辟', '壳牌', '美孚', 'BP', '道达尔']
    party = ["中石化", "中石油", "中化石油", "中国石油", "中国石化", "中海油"]
    company_category = "民营/其他"
    for x in forg:
        if x in name:
            company_category = '外资'
    for x in party:
        if x in name:
            company_category = '国资'
    return company_category


def human_merge():

    database = 'bi_papapa'
    muchcols_tablename = 'pa_stations_muchcols_enc'
    hum_tablename = 'pa_stations_human_record_enc'
    muchcols_table = '%s.%s' % (database, muchcols_tablename)
    hum_table = '%s.%s' % (database, hum_tablename)
    dw_in = my_(config.MYSQL_BI_RW_ENV)
    df_much = dw_in.to_dataframe('select * from %s' % muchcols_table)
    df_human = dw_in.to_dataframe('select stid,name book_name,st_human book_human,address book_address,province from %s' % hum_table)

    print('统计字频······')
    word_dict = {}
    for index in df_much.index:
        for word in df_much.loc[index, 'name']:
            if word in word_dict:
                word_dict[word] = word_dict[word] + 1
            else:
                word_dict[word] = 1
    words = list(word_dict.items())
    word_df = pd.DataFrame(words, columns=['rindex', 'count'])
    word_list_sort = word_df.sort_index(axis=0, ascending=False, by='count')
    # word_list = np.array(word_list_sort).tolist()

    print('基于字频的倒排索引。。。。。')
    rev_word_data = []
    rev_word = word_list_sort[:1200].reset_index()

    for i,row in rev_word.iterrows():
        data = list(df_much['name'].map(lambda x:1 if row['rindex'] in x else 0))
        rev_word_data.append(data)
    print('转换成矩阵，牺牲内存，换取速度.....')
    rev_word_data = np.matrix(rev_word_data)

    cool = ['name', 'st_human', 'address','province', 'city', 'region', 'phone', 'email', 'establish_date', 'registered_capital', 'home_page',
            'company_category', 'operation_Scope', 'latitude', 'longitude', 'p_carnum']
    df_much = df_much.drop(['create_time','update_time', 'obligate'], 1)
    for i, row in df_human.iterrows():
        print(i,row['book_name'], end='>>')
        # if i > 10:
        #     break

        # gindexs = []     # 匹配到的索引
        # for ii in word_data:
        #     if ii[0] in row['book_name']:
        #         gindexs.append(ii[2])
        #
        # mul_in = np.matrix(gindexs).sum(0)

        indx = rev_word.rindex.map(lambda x: x in row['book_name'])
        gindexs = rev_word_data[rev_word[indx].index]
        mul_in = gindexs.sum(0)
        ind = (mul_in >= mul_in.max() - 1).tolist()[0]
        df_much_tmp = df_much[ind]
        if df_much_tmp.__len__() == 0:
            print('没有，那么全匹配', i, row['book_name'])
            df_much_tmp = df_much

        # mul_index = 0
        # for xx in gindexs:
        #     if len(xx) > 1:
        #         # print('one',xx[1])
        #         tmp_array = np.array([1 if xxx else 0 for xxx in xx])
        #         if type(mul_index) == int:
        #             mul_index = tmp_array
        #         else:
        #             mul_index += tmp_array
        # df_much_tmp = df_much[mul_index >= mul_index.max() - 1]

        df_much_tmp['sim'] = df_much_tmp['name'].map(lambda x: levenshtein1(x, row['book_name']))
        # if df_much_tmp['sim'].min()>2:
        #    continue
        # else:
        df_human.loc[i, 'min_sim'] = df_much_tmp['sim'].min()
        df_much_min = df_much_tmp[df_much_tmp['sim'] == df_human.loc[i, 'min_sim']].reset_index()
        df_human.loc[i, 'min_sim_num'] = len(df_much_min)
        df_human.loc[i, 'muchcols_id'] = df_much_min.loc[0, 'stid']
        df_human.loc[i, 'obligate'] = '''"{'min_sim':%s, 'min_sim_num':%s}"''' %(df_human.loc[i, 'min_sim'], df_human.loc[i, 'min_sim_num'])
        for col in cool:
            df_human.loc[i, col] = df_much_min[col][0]
        print(df_much_min['name'][0])

    df_human['company_category'] = df_human['name'].map(devide_by_name)
    for x in ['外资','国资','民营/其他']:
        df_human[df_human.company_category == x].to_excel(x.replace('/', '')+'.xlsx')

    # 保存检索的关联到 pa_stations_human_record_enc.muchcols_name
    df_human['muchcols_name'] = df_human['name']
    df_human['name'] = df_human['book_name']
    df_human['update_time'] = 'now()'
    df_stations_s = df_add_singlequotemark(df_human.loc[:, ['name', 'muchcols_name',
                                                            # 'obligate',
                                                            'min_sim', 'muchcols_id']])
    dw_in.df_upd_tosql(df_stations_s, 1000, hum_table)


def update_estation():
    database = 'bi_papapa'
    muchcols_tablename = 'pa_stations_muchcols_enc'
    muchcols_table = '%s.%s' % (database, muchcols_tablename)
    hum_tablename = 'pa_stations_human_record_enc'
    hum_table = '%s.%s' % (database, hum_tablename)
    dw_in = my_(config.MYSQL_BI_RW_ENV)
    df_much = dw_in.to_dataframe('select * from %s where p_carnum = 0 or p_carnum is null and name in (select distinct muchcols_name from %s)' % (muchcols_table,hum_table))
    df_much['p_carnum'] = 0.0
    for i, row in df_much.iterrows():
        if len(aks) == 0:
            print('全部aks已经用完')
            break
        if devide_by_name(row['name']) != '民营/其他':
            print(row['name'],devide_by_name(row['name']),)

        row['p_carnum'] = get_around_carnum_bybaidu(row['latitude'], row['longitude'])
        sqld = 'update %s set p_carnum=%s,update_time=now() where stid = %s' %(muchcols_table,row['p_carnum'],row['stid'])
        print(sqld)
        dw_in.sql_engine(sqld)


pa_columns =['company_url','company_name','email','address','phone','home_page','human','human_page','have_company',
          'register_num','organization_code','Tax_identification','company_category','operation_Scope']
for x in pa_columns:
    df_stations[x] = ''

cookie={}
header = {'Accept': '*/*',
 'Connection': 'keep-alive',
 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
 'Accept-Encoding': 'gzip, deflate, br',
 'Referer': 'https://gd.tianyancha.com/login',
 'Origin': 'https://gd.tianyancha.com',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
 'X-Requested-With': 'XMLHttpRequest',
 'cookie':'aliyungf_tc=AQAAAAyFEW7MjAUAl0CNPUDTkg0D/kZE; csrfToken=lyYZ0ebsTLbJ6DFtIF689fEg; TYCID=642938e0e53511e7ad070f122e1a65c3; undefined=642938e0e53511e7ad070f122e1a65c3; ssuid=7444004751; _csrf=yUV0+UdggVYxYm+EhPvFNA==; OA=/0Y0ayEr0VZ3PnTEUdp6qjEUtruEuC35RompPb5uT3s=; _csrf_bk=20d1a092a85051b74242c176ef589207; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1513740313; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1513741169',
 'homeFilterExpand': 'true'}

cookie_list = [{'auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUyMDg2MDEzOSIsImlhdCI6MTUxMjk5NjE5NywiZXhwIjoxNTI4NTQ4MTk3fQ.ZoE-MXPgNX6e1XVB8wUlTmo5aZnSeySxIyp5C439_5_Kd6valWA0qV7GGOwAbw3o9oSghHLTDUjFQ_jS5zeTQA'},
         {'auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTg5MTc1ODU5NCIsImlhdCI6MTUxMzA2MzA0NCwiZXhwIjoxNTI4NjE1MDQ0fQ.l4Bfkb8InWY0cOPVUV8f3VpIg2XO0pMGf7vr249zprWeTZDFM12lqNl3xpLnPM7MJBWuKpm8z4cA_UhJ_CQKJQ'}]
user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                   'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36']

userpasswd_list = {'18520860139': '0ea98d8c4d4459be18a3182d8df62da3',
                   '18255172867': '0659c7992e268962384eb17fafe88364',
                   '13471288987': '0659c7992e268962384eb17fafe88364',
                   '15891758594': '0659c7992e268962384eb17fafe88364',
                   '15587944391': '0659c7992e268962384eb17fafe88364',
                   '13923858482': 'f66548ee7323c90f04db17d6cd12ffce'             #  this is vip
                   }

def do_login():
    session = requests.Session()
    data = {"mobile": "18520860139","cdpassword":"0ea98d8c4d4459be18a3182d8df62da3","loginway":"PL","autoLogin": True}
    header.update({'User-Agent': random.choice(user_agent_list)})
    login_step1 = session.post('https://gd.tianyancha.com/cd/login.json', data=data, headers=header, verify='123.cer')


# for i,row in df_stations.iterrows():
for i in df_stations[df_stations['company_url'] == ''].index:

    name = df_stations.loc[i, '企业名称']
    print(i,name)
    time.sleep(2)

    cookie.update(random.choice(cookie_list))
    header.update({'User-Agent':random.choice(user_agent_list)})
    res = requests.get('https://www.tianyancha.com/search?key=%s&checkFrom=searchBox' % name, cookies=cookie, headers=header)
    time.sleep(1)

    cookie.update(dict(res.cookies))
    with open('./html_/kan_%s.html' % name, 'wb') as f:
        f.write(res.content)

    company_urls = re.findall('https://www.tianyancha.com/company/\d+', res.text)
    if company_urls:
        company_url = company_urls[0]
        res_company = requests.get(company_url, cookies=cookie, headers=header)
        cookie.update(dict(res_company.cookies))
        with open('./html_/detail_%s.html' % name, 'wb') as f:
            f.write(res_company.content)

        body_soup = BeautifulSoup(res_company.text, "html5lib")

        company_header_soup = body_soup.find_all('div', class_='companyTitleBox55')
        if company_header_soup:
            pass
        else:
            print('no company_header_soup. wait....')
            time.sleep(20)
            continue

        company_name = company_header_soup[0].find_all('span', class_='f18')[0].get_text()
        email = company_header_soup[0].find_all('span', class_='emailWidth')[0].get_text()
        address = company_header_soup[0].find('span',class_='pr10').get_text()
        phone = company_header_soup[0].find_all('span', class_='')[0].get_text()
        home_page = company_header_soup[0].find_all('span', class_='')[1].get_text()

        human = body_soup.find_all('a', class_='', href=re.compile('.*human.*'))[0].get_text()
        human_page = body_soup.find_all('a', class_='', href=re.compile('.*human.*'))[0].get('href')
        have_company = body_soup.find_all('span', class_='new-err')[0].get_text()

        table2_soup = body_soup.find_all('tbody', class_='')[1]
        some_other = table2_soup.find_all('td', class_='')
        register_num = some_other[0].get_text()   # 工商注册号
        organization_code = some_other[1].get_text()  # 组织代码
        Tax_identification = some_other[2].get_text()  # 纳税识别号
        company_category = some_other[3].get_text()  # 公司类型
        operation_Scope = some_other[11].get_text()  # 经营范围

        for x in pa_columns:
            df_stations.loc[i,x] = eval(x)
    else:
        print('no company_urls. wait..10s..')
        time.sleep(10)


