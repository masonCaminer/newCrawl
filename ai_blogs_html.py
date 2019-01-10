# coding=utf-8

# 提交word
import re
import urllib.request
import requests
import chardet
from bs4 import BeautifulSoup
import datetime
from db.MySQLCommand_blog import MySQLCommand_blog
import random
import time
from PIL import Image
import os
from PIL import Image

# 有图片
mysqlComment = MySQLCommand_blog()
headers = [('Host','img0.imgtn.bdimg.com'),
('Connection', 'keep-alive'),
('Cache-Control', 'max-age=0'),
('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'),
('Accept-Encoding','gzip,deflate,sdch'),
('Accept-Language', 'zh-CN,zh;q=0.8'),
('If-None-Match', '90101f995236651aa74454922de2ad74'),
('Referer','http://image.baidu.com/i?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&word=%E4%BA%A4%E9%80%9A&ie=utf-8'),
('If-Modified-Since', 'Thu, 01 Jan 1970 00:00:00 GMT')]

# 抓取阿里博客搜索结果:url：key=关键词
def search():
    mysqlComment.connectionMysql()
    htmlf = open('/opt/developer/maoyl/ai_news_get_python/blogs/数据科学实践中常犯的十二种错误.htm', 'r', encoding="utf-8")
    # htmlf = open('C:\\Users\\Administrator\\Desktop\\1.htm', 'r', encoding="utf-8")
    htmlpage = htmlf.read()
    soup = BeautifulSoup(htmlpage, "html.parser")  # 实例化一个BeautifulSoup对象
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content_link="https://yq.aliyun.com/articles/639003?spm=a2c4e.11163080.searchblog.59.15442ec1oQC1NC"
    content_author="技术小能手"
    content_title="数据科学实践中常犯的十二种错误"
    content_details=str(soup.renderContents().decode('utf-8', 'ignore')).strip()
    create_time="2018-09-13 13:43:06"
    image_link="https://yqfile.alicdn.com/059216539fc80b8fab33c1d9b521f80a5eea65f0.png"
    news_dict = {
        "content_title": content_title,
        "content_author": content_author,
        "content_link": content_link,
        "content_details": content_details,
        "insert_time": dt,
        "create_time": create_time,
        "image_link": image_link
    }
    id = mysqlComment.insertData(news_dict)
    if id != None:
        # path = "D:/文件夹/"+str(id)+".jpg"
        # path = "/opt/developer/maoyl/ai_news_get_python/tupian/"+str(id)+".jpg"
        if id % 100 == 0:
            path = "/opt/wwwroot/ailab.d.kingnet.com/static/main/static/blogsimg/" + str(id) + "/"
            path1 = "static/blogsimg/" + str(id) + "/"
            isExists = os.path.exists(path)
            if not isExists:
                os.makedirs(path)
            path = path + str(id) + ".jpeg"
            path1 = path1 + str(id) + ".jpeg"
        else:
            nn = int(id / 100) * 100
            print(nn)
            path = "/opt/wwwroot/ailab.d.kingnet.com/static/main/static/blogsimg/" + str(nn) + "/"
            path1 = "static/blogsimg/" + str(nn) + "/"
            isExists = os.path.exists(path)
            if not isExists:
                os.makedirs(path)
            path = path + str(id) + ".png"
            path1 = path1 + str(id) + ".png"
        mysqlComment.updateData(id, path1)
        # 保存图片
        response = requests.get(image_link)
        # print(data)
        f = open(path, "wb")
        f.write(response.content)
        f.close()

    mysqlComment.closeMysql()


if __name__ == '__main__':
    search()  # coding:utf-8
    # response = requests.get("https://yqfile.alicdn.com/8d41fb55f53268260d43407fddd3943173e6af3d.png")
    # # print(data)
    # f = open("C:\\Users\\Administrator\\Desktop\\4.jpg", "wb")
    # f.write(response.content)
    # f.close()
    # with open("C:\\Users\\Administrator\\Desktop\\3.jpg", 'wb') as f:
    #     f.write(response.content)
