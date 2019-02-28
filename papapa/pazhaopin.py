from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
import html5lib
import time
import urllib.request,urllib.parse,http.cookiejar
import pandas as pd
import random


def ZhiPin():
    user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                   'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                   ]
    Res = []
    for i in range(1,300):
        print(i)
        time.sleep(2)
        url="http://www.zhipin.com/c101110100/s_302_303_304_305_306-h_101110100-t_802_803_804_805_806_807/?ka=sel-stage-807&page="+str(i) #翻页使用循环实现
        headers = {'User-Agent': random.choice(user_agents)}
        data=urllib.request.urlopen(url).read()
        page_data=data.decode('UTF-8')
        soup=BeautifulSoup(page_data, "html5lib")
        li_all=soup.find_all('a', href=re.compile("/gongsi/(\S+)"))
        company_link=soup.find_all('a',href=re.compile("/job_detail/(\S+).html"))
        #print(soup)
        for li in company_link:
            #print(li)
            html_ss=str(li)
            #print(re.findall('/gongsi/\d+\.html',html_ss))
            gongsi_html='http://www.zhipin.com'+re.findall('/job_detail/\d+\.html',html_ss)[0]
            Res.append(gongsi_html)
        if len(li_all)<4:
            print("nothing else on this page,the last page=%s, len=%s" %(i,len(li_all)))
            break
    Res_Unique = list(set(Res))
    print(len(Res),len(Res_Unique))

    Comany=[]
    for job in Res_Unique:
        print(job)
        time.sleep(3)
        try:
            headers = {'User-Agent': random.choice(user_agents)}
            Content = urllib.request.urlopen(job).read()
            Content_page_data = Content.decode('UTF-8')
            Content_soup = BeautifulSoup(Content_page_data, "html5lib")
            # li_all = soup.find_all('h3', href=re.compile("/gongsi/(\S+)"))
            li_title = Content_soup.find('div', class_='info-company', attrs={"class": "name"}).get_text("|", strip=True)
            li_location = Content_soup.find(attrs={"class": "location-address"}).get_text()
            Res_Dict = {'company': li_title, 'location': li_location, 'url': job}
            Comany.append(Res_Dict)
        except Exception as err:
            print(err)
            break


    pd.DataFrame(Comany).to_csv('zhipin.csv')
    # f1 = open('C:\\Users\\admin\\Desktop\\gongsi.txt', 'w')
    #for i in Res_Unique:
        #f1.write(str(i))
        #f1.write('\n')
    #f1.close()

ZhiPin()