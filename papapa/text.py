from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
import html5lib
import time
import urllib.request,urllib.parse,http.cookiejar
import numpy
import pandas as pd

goods=[]
name=[]
price=[]
for j in range(1,17):
    time.sleep(3)
    url="http://np.ule.com/item/------%E6%89%B6%E8%B4%AB---5om26LSr----"+str(j)+".html"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    headers = {'User-Agent': user_agent}
    data = urllib.request.urlopen(url).read()
    page_data = data.decode('utf-8')
    soup = BeautifulSoup(page_data, "html5lib")
    goods_name=soup.find_all('p',"name")

    for l_name in goods_name:
        z_name=l_name.get_text("|", strip=True)
        name.append(z_name)
    goods_price=soup.find_all('p',"price")
    for l_price in goods_price:
        z_price=l_price.get_text("|", strip=True)
        price.append(z_price)
    for i,j in zip(name,price):
        Res_Dict = {'name':i,'price':j}
        goods.append(Res_Dict)
    #print(soup)
    #print(z_name)
    #print(z_price)
print(goods)
pd.DataFrame(goods).to_csv('ule1.csv')


