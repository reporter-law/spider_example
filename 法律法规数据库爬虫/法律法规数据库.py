"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import requests
from lxml import etree
import json


def url_get():
    url = "http://search.chinalaw.gov.cn/SearchLawTitle?effectLevel=&SiteID=124&Sort=PublishTime&Type=1"
    data = {"Query": "权利告知"}
    r = requests.get(url,params=data)
    print(r.status_code)
    soup = etree.HTML(r.text)
    number = soup.xpath('//*[@id="pagecount"]/text()')
    print(number)
    for i in range(1,int(number[0])+1):
        data = {"Query": "权利告知","PageIndex":i}
        r = requests.post(url, params=data)
        #print(r.status_code)
        yield r.url

#url_get()

#静态页面

def parse_url():
    content = {}
    for url in url_get():
        r = requests.get(url)
        print(r.status_code)
        soup = etree.HTML(r.text)
        for i in range(1,11):
            print(soup.xpath('/html/body/div[2]/div[2]/div/div/div[2]/div[1]//td[@class="listLef"]/h3[@style="width: 100%;"]/a//text()'))
            content["title"] = "".join(soup.xpath('/html/body/div[2]/div[2]/div/div/div[2]/div[%d]//td[@class="listLef"]/h3/a//text()'%i))
            content["release"] = "".join(soup.xpath('/html/body/div[2]/div[2]/div/div/div[2]/div[%d]//div[@class="searInfo"]//text()'%i))
            content["subject_note"] = "".join(soup.xpath('/html/body/div[2]/div[2]/div/div/div[2]/div[%d]//div[@class="searContent"]//text()'%i))
            print(content)
            with open('J:\PyCharm项目\常用设置\爬虫工具\检索的相关法律条文.txt',"a+",encoding='gbk')as f:
                f.write(str(content) + "\n")
parse_url()
