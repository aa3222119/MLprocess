import requests
from bs4 import BeautifulSoup


def do_grab__(st=13542, ed=13586):
    for page in range(st, ed+1):
        res = requests.get(f'https://www.558duo.cc/a/57/{page}.html')
        soup = BeautifulSoup(res.text)
        down_soup = soup.find_all('a', class_='down')
        if down_soup and len(down_soup) > 6:
            href = down_soup[6].get('href')
            print(href)


do_grab__(st=13431, ed=13462)
