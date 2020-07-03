# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import requests
from 常用设置 import user_agent as u
import random
from bs4 import BeautifulSoup
import lxml
from 常用设置.cookie_pool_simple import 获取cookies as cookies
import time
from concurrent.futures import  ThreadPoolExecutor as e
from threading import Thread as t
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
from 项目.项目一_法律家爬虫.代理模块 import url_ip as i
#from 项目.项目一_法律家爬虫.代理模块 import proxy_pool_jhao_getting as p
#from 项目.项目一_法律家爬虫.代理模块 import daili_cui as d


'''！！！！！！！！！！！！！！！！不用获取url，因为可以构造出来！！！！！！！！！！！！！！！！！！！！！！！！'''

#留待明天测试是否是固定1分钟ip的原因



class Requests_law_url():
    def __init__(self,index_):
        self.index = index_
        '''index_需要类来传递'''

    def get_page(self):
        '''提交url，获取url内容'''
        '''控制index来控制翻页'''
        s = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        s.mount('http://', adapter)
        s.mount('https://', adapter)
        s.keep_alive = False
        # number = str(1 + index)
        url = 'http://www.fae.cn/cp/kind.html'  # kind994导致重复？以及max_retryies?
            # params为formdata(host='42.242.10.162', port=36171)


        try:

            # time.sleep(1)
            headers = {
                'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3',
                'Accept - Encoding': 'gzip, deflate',
                'Accept - Language': 'zh - CN, zh;q = 0.9',
                'Cache - Control': 'max - age = 0',
                'Connection': 'close',
                'Content - Length': '25',
                'Content - Type': 'application / x - www - form - urlencoded',
                'Cookie': cookies.get_cookie(),
                # 'JSESSIONID=3ADA544719F80B1B369CE7A2AAC2186A; __51cke__=; __tins__17376415=%7B%22sid%22%3A%201586509337484%2C%20%22vd%22%3A%204%2C%20%22expires%22%3A%201586511172280%7D; __51laig__=' + str(4 +index),
                'Host': 'www.fae.cn',
                'Origin': 'http: // www.fae.cn',
                'Referer': 'http: // www.fae.cn / cp / kind.html',
                'Upgrade - Insecure - Requests': '1',
                'User - Agent': u.getheaders(),
            }
            params = {
                'kind_id': 994,
                'page_number': self.index,
            }
            r = s.post(url, headers=headers, data=params, stream=True)
            # d.check_proxy())#,proxies =random.choice([p.check_proxy(),d.check_proxy()]))
            '''循环中不停传递index'''

            '''内部变量可以被改变'''
            if r.status_code == 200:
                # time.sleep(sec)
                print(r.headers)
                print('这是分隔线............................第{number}页..............'.format(number=self.index) + '\n')
                self.index += 1
                r.encoding = r.apparent_encoding
                time.sleep(1)
                yield r.text
            else:
                print('出现错误....................错误代码： ' + str(r.status_code))
                print(time.strftime('%Y-%m-%d-%I-%M-%S', time.localtime()))
                time.sleep(6)

        except requests.exceptions.ConnectionError as c:
            print(c)
            print(time.strftime('%Y-%m-%d-%I-%M-%S', time.localtime()))
            for index in range(6, -1, -1):
                print('重来倒计时中..{sec}'.format(sec=index))
            self.get_page()

    def parse_url(self):
        '''解析内容，提取链接'''
        for htmls in self.get_page():
            soup = BeautifulSoup(htmls, 'lxml')
            time.sleep(1)
            '''太快了不全'''
            results = soup.find_all('td', attrs={'style': 'height: 33px;font-family:黑体;font-size:20px;'})
            time.sleep(1)
            if results is None:
                print('none')
            else:
                for result in results:
                    # find_all()回来的是一个列表！！！！！
                    urls = 'http://www.fae.cn' + result.a['href']
                    print(urls)

                    with open('../清洗模块/清洗前后文件/urls(多线程——).txt', 'a', encoding='utf-8')as f:
                        f.write(urls + '\n')
            # print('写入中。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。')
            # 只有一页之后就会爬取失败。用return怎么样？
#debugger:
# for i in get_page(1):
    #print(i)
#五线程组

threads = []#上次基本在450页

def third_page():
    index_ = 43702#40380 41380 43380不存在 41665不存在
    start_ = Requests_law_url(index_)
    while index_ <= 60000:
        start_.parse_url()
        index_ += 1

def fourth_page():
    index_ = 67965
    start_ = Requests_law_url(index_)
    while index_ <= 80000:
        index_ = index_
        start_.parse_url()
        index_ += 1


def fifth_page():
    index_ = 838292
    start_ = Requests_law_url(index_)
    while index_ <= 100000:
        start_.parse_url()
        index_ += 1


threads.append(t(target=third_page))
threads.append(t(target=fourth_page))
threads.append(t(target=fifth_page))

if __name__ == '__main__':
    try:
        for t in threads:
            t.start()
            time.sleep(3)
            # 防止过两秒重试造成的线程二无法启动
    except:
        print('出错。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。')