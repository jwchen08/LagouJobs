# coding=utf-8
import re
import requests
import MySQLdb
import time
from bs4 import BeautifulSoup
import json
import random
cityCN = ['北京', '上海', '广州', '深圳', '成都']
cityEN = ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Chengdu']
# 当前查询的城市
currentCity = cityCN[0]
keywords= ['Python', '数据挖掘', 'C++', '前端', 'java']
# 当前查询的关键词
currentKeyword = keywords[1]
start_url = 'http://www.lagou.com/jobs/positionAjax.json'
url = start_url+r'?city='+currentCity+r'&needAddtionalResult=false'
# 记录当前页面
currentPage = 1
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/50.0.2661.75 Safari/537.36',
           'Origin': 'https://www.lagou.com'}
params = {'pn': currentPage, 'kd': currentKeyword}
# 获取代理IP
iplist = []  # 初始化一个list用来存放我们获取到的IP
html = requests.get("http://haoip.cc/tiqu.htm")  # 不解释咯
iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S)  # 表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
for ip in iplistn:
    i = re.sub('\n', '', ip)  # re.sub 是re模块替换的方法，这儿表示将\n替换为空
    iplist.append(i.strip())  # 添加到我们上面初始化的list里面
IP = ''.join(str(random.choice(iplist)).strip())  # 将从self.iplist中获取的字符串处理成我们需要的格式（处理了些，什么自己看哦，这是基础呢）
# proxy = {'http': IP}  # 构造成一个代理
proxy = {'http': '110.73.141.147:8123'}
print proxy
resp = requests.post(url, data=params, headers=headers, proxies=proxy)
# r = requests.get('http://sou.zhaopin.com/jobs/searchresult.ashx',params=params,headers=headers)
print resp.url
# print resp.text
# resp.txt为json文件
jdict = json.loads(resp.text)
pageSize = jdict["content"]["pageSize"]
# 记录职位总数
totalCount = jdict["content"]["positionResult"]["totalCount"]
# 记录总工资，用来计算平均值
totalSalary = 0
# 记录有效工资条数
validCount = 0
# 网页页数，网站只显示30页，此处显示50页
pageNumber = totalCount/pageSize+1
if pageNumber > 5:
    pageNumber = 5
jcontent = jdict["content"]
jposresult = jcontent["positionResult"]
jresult = jposresult["result"]
for each in jresult:
    # print each['city']
    # print each['companyShortName']
    # print each['companySize']
    # print each['positionName']
    # print each['salary']
    # print each['workYear']
    # print ''
    oneSalary = re.search('(.*?)[kK]-(.*?)[kK]', each['salary'])
    if oneSalary:
        totalSalary += int(oneSalary.group(1)) + int(oneSalary.group(2))
        validCount += 1
while currentPage < pageNumber:
    # 防止请求过于频繁
    time.sleep(1)
    currentPage += 1
    params = {'pn': currentPage, 'kd': currentKeyword}
    resp = requests.post(url, data=params, headers=headers, proxies=proxy)
    jdict = json.loads(resp.text)
    jcontent = jdict["content"]
    jposresult = jcontent["positionResult"]
    jresult = jposresult["result"]
    for each in jresult:
        # print each['city']
        # print each['companyShortName']
        # print each['companySize']
        # print each['positionName']
        # print each['salary']
        # print each['workYear']
        # print ''
        oneSalary = re.search('(.*?)[kK]-(.*?)[kK]', each['salary'])
        if oneSalary:
            totalSalary += int(oneSalary.group(1)) + int(oneSalary.group(2))
            validCount += 1
print currentCity+'与'+currentKeyword+'相关的职位数量：'+str(totalCount)
print '其中有效条目数量：'+str(validCount)
print '平均工资为：'+str(totalSalary/(2*validCount))+'k'

        # soup = BeautifulSoup(r.text, 'html.parser')
# list1 = soup.find_all('table')
# resultlist=[]
# for li in list1:
#     jobname=li.find('td',class_='gsmc') #公司名称
#     jobsalary=li.find('td',class_='zwyx') #工资
#     joblocation=li.find('td',class_='gzdd') #地址
#     jobnameStr=''
#     jobsalaryStr=''
#     joblocationStr=''
#     if jobname:
#         jobnameStr= jobname.a.string
#         # print jobnameStr
#     if jobsalary:
#         jobsalaryStr= jobsalary.string
#         # print jobsalaryStr
#     if joblocation:
#         joblocationStr= joblocation.string
#         # print joblocationStr
#     resultlist.append([jobnameStr,jobsalaryStr,joblocationStr])
# # print resultlist[1][0]