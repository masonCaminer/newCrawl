# coding:utf-8
import re
from urllib.request import Request
import urllib.request
import requests
import chardet
from bs4 import BeautifulSoup
import datetime
from db.MySQLCommand import MySQLCommand
import random
import time
import os
from urllib.parse import urlencode
import json
from urllib import request

mysqlComment = MySQLCommand()
headers = [
           ('Accept', 'image/webp,image/apng,image/*,*/*;q=0.8'),
           ('User-Agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'),
           ('Accept-Encoding', 'gzip, deflate, br'),
           ('Accept-Language', 'zh-CN,zh;q=0.9'),
           ('Referer',
            'https://www.toutiao.com/ch/news_hot/')
           ]

# 输入url，将其新闻页的正文输入txt
def extract_news_content(web_url):
    request = urllib.request.Request(web_url)
    # 在请求加上头信息，伪装成浏览器访问
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    opener = urllib.request.build_opener()
    html = opener.open(request).read()
    infoencode = chardet.detect(html)['encoding']  ##通过第3方模块来自动提取网页的编码
    if html != None and infoencode != None:  # 提取内容不为空，error.或者用else
        html = html.decode(infoencode, 'ignore')
        soup = BeautifulSoup(html, "lxml")
        return soup.renderContents().decode('utf-8', 'ignore')


# 抓取今日头条新闻搜索结果:中文搜索，前10页，url：key=关键词
def search(key_word):
    mysqlComment.connectionMysql()
    a_url = "https://www.toutiao.com/a6604819333707203075/"
    contents = extract_news_content(a_url)  # 还写入文件
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_link="http://p3.pstatp.com/large/pgc-image/15378043148850c425321e9"
    news_dict = {
        "content_title": "小米小爱火了，Siri也很受欢迎，但这个AI几乎人人都有却没人使用",
        "content_author": "狐说IT",
        "content_link": a_url,
        "content_details": str(contents).strip(),
        "insert_time": dt,
        "image_link": image_link
    }
    id = mysqlComment.insertData(news_dict)
    if id != None:
        if id % 100 == 0:
            path = "/opt/wwwroot/ailab.d.kingnet.com/static/main/static/newsimg/" + str(id) + "/"
            path1 = "static/newsimg/" + str(id) + "/"
            isExists = os.path.exists(path)
            if not isExists:
                os.makedirs(path)
            path = path + str(id) + ".jpg"
            path1 = path1 + str(id) + ".jpg"
        else:
            nn = int(id / 100) * 100
            path = "/opt/wwwroot/ailab.d.kingnet.com/static/main/static/newsimg/" + str(nn) + "/"
            path1 = "static/newsimg/" + str(nn) + "/"
            isExists = os.path.exists(path)
            if not isExists:
                os.makedirs(path)
            path = path + str(id) + ".jpg"
            path1 = path1 + str(id) + ".jpg"

        mysqlComment.updateData(id, path1)
        # 保存图片
        opener = urllib.request.build_opener()
        opener.addheaders = headers
        data = opener.open(image_link)
        # print(data)
        f = open(path, "wb")
        f.write(data.read())
        f.close()


    mysqlComment.closeMysql()

if __name__ == '__main__':
    search("ai")  # coding:utf-8
