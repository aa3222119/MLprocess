#encoding=utf-8
import sys, urllib, urllib2, json
reload(sys)
sys.setdefaultencoding('utf-8')
import httplib

class juhe_oil:
    def __init__(self, apikey):
        self.url = 'http://apis.juhe.cn/oil/region' #数据API请求URL
        self.addr = 'apis.juhe.cn' #数据API请求URL
        self.appkey = apikey #您申请到的数据的APPKEY
        self.index = 0

    def run(self, city):
        print city + ' start...'
        self.output = open('station_list_171111.txt', 'a+')
        self.error_log = open('error_city_171111.txt', 'a+')
        page = 0
        while page < 200:
            page += 1
            print page
            paramsData = {'city': city, 'page': page, 'key': self.appkey} #需要传递的参数
            params = urllib.urlencode(paramsData)

            try:
                conn = httplib.HTTPConnection(self.addr, timeout=7)
                conn.request('GET','/oil/region' + '?%s' % params)
                resp = conn.getresponse()
                content = resp.read()
            except Exception, e:
                page-=1
                print 'exception: ' + str(page)
                continue

            #req = urllib2.Request(self.url, params)
            #req.add_header('Content-Type', "application/x-www-form-urlencoded")
            #resp = urllib2.urlopen(req)
            #content = resp.read()
            if(content):
                result = json.loads(content, 'utf-8')
                error_code = result['error_code']
                if(error_code == 0):
                    if(result['resultcode'] == '200'):
                        data = result['result']['data'] #接口返回结果数据
                        self.deal(data)
                    else:
                        if page == 1:
                            self.error_log.write(city)
                            self.error_log.write('\n')
                        break
                else:
                    errorinfo = str(error_code)+":"+result['reason'] #返回不成功，错误码:原因
                    print(errorinfo)
                    if page == 1:
                        self.error_log.write(city)
                        self.error_log.write('\n')
                    break
        self.output.close()
        self.error_log.close()
        print 'end...'

    def deal(self, data):
        for result in data:
            self.write_in(result, 'id')
            self.write_in(result, 'name')
            self.write_in(result, 'areaname')
            self.write_in(result, 'address')
            self.write_in(result, 'brandname')
            self.write_in(result, 'type')
            self.write_in(result, 'discount')
            self.write_in(result, 'exhaust')
            self.write_in(result, 'lat')
            self.write_in(result, 'lon')
            self.write_in(result['price'], 'E0')
            self.write_in(result['price'], 'E90')
            self.write_in(result['price'], 'E93')
            self.write_in(result['price'], 'E97')
            self.write_in(result['gastprice'], '0#')
            self.write_in(result['gastprice'], '90#')
            self.write_in(result['gastprice'], '92#')
            self.write_in(result['gastprice'], '93#')
            self.write_in(result['gastprice'], '95#')
            self.write_in(result['gastprice'], '97#')
            self.write_in(result['gastprice'], '98#')
            self.write_in(result, 'fwlsmc')
            self.write_in(result, 'position')
            
            self.output.write('\n')
            self.index+=1
            print self.index

    def write_in(self, result, key):
        if result == None:
            self.output.write('\t')
        elif len(result)==0:
            self.output.write('\t')
        elif result.has_key(key):
            self.output.write(str(result[key]) + '\t')
        else:
            self.output.write('\t')

def get_city_list(city_file):
    city_list = []
    f = open(city_file, 'r')
    while True: 
        line=f.readline().strip() 
        if len(line)==0:
            break
        city_list.append(line)
    f.close()
    return city_list
    

if __name__ == "__main__":
    crawler = juhe_oil('b17d61a3d33c0cf5b38dc04f51d6ad5d')
    city_list = get_city_list('city_new.txt')
    for city in city_list:
        print city
        crawler.run(city)
