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
headers = [('Host', 'img0.imgtn.bdimg.com'),
           ('Connection', 'keep-alive'),
           ('Cache-Control', 'max-age=0'),
           ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
           ('User-Agent',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'),
           ('Accept-Encoding', 'gzip,deflate,sdch'),
           ('Accept-Language', 'zh-CN,zh;q=0.8'),
           ('If-None-Match', '90101f995236651aa74454922de2ad74'),
           ('Referer',
            'http://image.baidu.com/i?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&word=%E4%BA%A4%E9%80%9A&ie=utf-8'),
           ('If-Modified-Since', 'Thu, 01 Jan 1970 00:00:00 GMT')]


# 输入url，将其新闻页的正文输入txt
def extract_news_content(web_url):
    request = urllib.request.Request(web_url)

    # 在请求加上头信息，伪装成浏览器访问
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    opener = urllib.request.build_opener()
    html = opener.open(request).read()
    soup = BeautifulSoup(html, "lxml")
    content = soup.findAll("div", "content")
    contentauthor = soup.find("a", "b-author").renderContents().decode('utf-8', 'ignore').strip()
    create_time = soup.find("span", "b-time icon-shijian1").renderContents().decode('utf-8', 'ignore').strip()
    return content, contentauthor, create_time


# 抓取阿里博客搜索结果:url：key=关键词
def search():
    mysqlComment.connectionMysql()
    # htmlf = open('/opt/developer/maoyl/ai_news_get_python/专利-排位系统.htm', 'r',encoding="gbk")
    htmlf =open('C:\\Users\\Administrator\\Desktop\\专利-排位系统.htm','r')
    htmlpage = htmlf.read()
    soup = BeautifulSoup(htmlpage, "html.parser")  # 实例化一个BeautifulSoup对象
    content = soup.findAll("html")  # resultset object
    num = len(content)
    for i in range(num):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        news_dict = {
            "content_title": "专利-排位系统",
            "content_author": "",
            "content_link": "",
            "content_details": str(content[0]).strip(),
            "insert_time": dt,
            "create_time": "",
            "image_link": ""
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
                path = path + str(id) + ".jpg"
                path1 = path1 + str(id) + ".jpg"
            else:
                nn = int(id / 100) * 100
                path = "/opt/wwwroot/intelligence/static/blogsimg/" + str(nn) + "/"
                path1 = "static/blogsimg/" + str(nn) + "/"
                isExists = os.path.exists(path)
                if not isExists:
                    os.makedirs(path)
                path = path + str(id) + ".jpg"
                path1 = path1 + str(id) + ".jpg"
            mysqlComment.updateData(id, path1)
            # 保存图片
            img = Image.open("/opt/developer/maoyl/ai_news_get_python/1.jpg")
            img.save(path)
            time.sleep(2)
    mysqlComment.closeMysql()


if __name__ == '__main__':
    search()  # coding:utf-8
