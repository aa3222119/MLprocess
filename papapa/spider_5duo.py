from buildings.comm_across import *
from bs4 import BeautifulSoup
import requests


def do_grab__(st=10848, ed=10869):
    for page in range(st, ed):
        res = requests.get(f'https://www.555duo.net/a/html/{page}.html')
        soup = BeautifulSoup(res.text)
        down_soup = soup.find_all('a', class_='down')
        if down_soup and len(down_soup)>6:
            href = down_soup[6].get('href')
            print(href)


# do_grab__(4900, 4930)


headers_ = {'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'text/plain;charset=UTF-8'}

sess = requests.session()


def download_url(url, save_path, chunk_size=512):
    r = sess.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


for page in range(1, 599):
    sess = requests.session()
    data_dir = 'Z:\\pics\\data'
    res = sess.get(f'https://www.ku137.net/b/1/list_1_{page}.html', headers=headers_)
    res.encoding = 'GBK'
    soup = BeautifulSoup(res.text)
    ul_a = soup.find_all('ul', class_='cl')[-1].find_all('a')
    print(f'{page} len={len(ul_a)} ')
    for a_link in ul_a:
        title = a_link.get('title')
        e_li = findall_in_dir(title, data_dir)
        if e_li:
            print(f'{page} {title}  {e_li}')
            continue
        zip_page = a_link.get('href')
        res_1 = sess.get(zip_page, headers=headers_)
        soup_1 = BeautifulSoup(res_1.text)
        title111 = soup_1.find_all('div', class_='Title111')
        zip_link = title111[0].find_all('a')[1].get('href')
        print(f'{page} {title} {zip_link} {e_li}')
        try:
            download_url(zip_link, f'{data_dir}\\{title}.zip')
        except Exception as err:
            print(err)


for page in range(1, 2):
    sess = requests.session()
    data_dir = 'Z:\\pics\\data'
    res = sess.post(f'https://www.bthy.xyz/list.php?class=riben&page={page}', headers={})
    soup = BeautifulSoup(res.text)
    a_li = soup.find_all('ul', class_='list')[-1].find_all('a')
    for a_link in a_li[:2]:
        link_ = a_link.get('href')
        res_1 = sess.get(f'https://www.bthy.xyz{link_}', headers={})
        soup_1 = BeautifulSoup(res_1.text)

