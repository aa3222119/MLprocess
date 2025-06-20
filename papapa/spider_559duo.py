# import os
# import re
from papapa.spider_5duo import *
# from buildings.comm_across import *
# from bs4 import BeautifulSoup
# import requests


headers_ = {'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'text/plain;charset=UTF-8'}
ser_patt = re.compile(r'\[.*?]')
data_dir = 'C:\\data\\5duo'


for i in range(1, 2):
    p1_url = f'https://www.559duo.cc/a/1/list_1_{i}.html'
    res = requests.get(p1_url, headers=headers_)
    res.encoding = 'GBK'
    soup = BeautifulSoup(res.text)
    m_soup = soup.find('div', class_='lleft')
    if m_soup:
        down_soup = m_soup.select('li a')
        for l_soup in down_soup:
            file_name = l_soup.get('title')
            ser_name = re.findall(ser_patt, file_name)[0]
            url_ = l_soup.get('href')
            print(f'> {i=} {file_name=} {ser_name=} {url_=}')
            res_v = requests.get(url_)
            soup_1 = BeautifulSoup(res_v.text)
            # title111 = soup_1.find_all('div', class_='Title111')
            a_down_li = soup_1.find_all('a', class_='down')
            if len(a_down_li) > 4:
                zip_link = a_down_li[6].get('href')
                full_file_name = os.sep.join([data_dir, ser_name, f'{file_name}.zip'])
                print(f' >> {zip_link} {full_file_name=}')
                if os.path.isfile(full_file_name):  # os.path.exists
                    print(f' < {full_file_name} exists')
                    continue
                try:
                    iter_mkdir(full_file_name)
                    download_url(zip_link, f'{full_file_name}')
                except Exception as err:
                    print(err)
