"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import requests

r = requests.get("http://lawyee.hnadl.cn/PubPage/CaseInterface")
print(r.status_code)
print(r.text)