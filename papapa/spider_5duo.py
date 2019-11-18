import requests
from bs4 import BeautifulSoup


def do_grab__(st=10848, ed=10869):
    for page in range(st, ed):
        res = requests.get(f'https://www.555duo.net/a/html/{page}.html')
        soup = BeautifulSoup(res.text)
        down_soup = soup.find_all('a', class_='down')
        if down_soup and len(down_soup)>6:
            href = down_soup[6].get('href')
            print(href)


do_grab__(4900, 4930)
