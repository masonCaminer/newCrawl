# coding:utf-8
import re
import urllib.request
import requests
import chardet
from bs4 import BeautifulSoup
import datetime
from db.MySQLCommand_blog import MySQLCommand_blog
import random
import time
import os
#有图片
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
    content = soup.findAll("div", "content-detail markdown-body")
    contentauthor = soup.find("a","b-author").renderContents().decode('utf-8', 'ignore') .strip()
    create_time = soup.find("span","b-time icon-shijian1").renderContents().decode('utf-8', 'ignore') .strip()
    return content,contentauthor,create_time


# 抓取阿里博客搜索结果:url：key=关键词
def search():
    mysqlComment.connectionMysql()
    search_url = 'https://yq.aliyun.com/articles/?spm=a2c4e.11153940.minheadermenu.3.32eb4190413y0Q'
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(dt + " " + search_url)
    req = requests.get(search_url)
    req.raise_for_status()
    req.encoding = req.apparent_encoding
    html = req.text
    soup = BeautifulSoup(html, "lxml")
    content = soup.findAll("div","item-box normal-item")  # resultset object
    num = len(content)
    for i in range(num):
        # 先解析出来所有新闻的标题、来源、时间、url
        p_img = content[i].find('img')
        if p_img == None:
            continue
        contenttitle = content[i].find('h3').renderContents().decode('utf-8', 'ignore') .strip()
        contentlink = "https://yq.aliyun.com"+content[i].find('a',"alllink").get("href").strip()
        img_link = str(p_img.get("src")).strip()
        # contentauthor = content[i].find("p","source").find("a").renderContents().decode('utf-8', 'ignore') .strip()
        contents, contentauthor, create_time = extract_news_content(contentlink)
        # create_time = content[i].find('span', 'b-time icon-shijian1').renderContents().decode('utf-8', 'ignore')  # 创作时间
        if len(contents) == 0:
            continue
        else:
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            news_dict = {
                "content_title": contenttitle,
                "content_author": contentauthor,
                "content_link": contentlink,
                "content_details": str(contents[0]).strip(),
                "insert_time": dt,
                "create_time": create_time,
                "image_link": img_link
            }
            id = mysqlComment.insertData(news_dict)
            if id != None:
                #path = "D:/文件夹/"+str(id)+".jpg"
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
                    path = "/opt/wwwroot/ailab.d.kingnet.com/static/main/static/blogsimg/" + str(nn) + "/"
                    path1 = "static/blogsimg/" + str(nn) + "/"
                    isExists = os.path.exists(path)
                    if not isExists:
                        os.makedirs(path)
                    path = path + str(id) + ".jpg"
                    path1 = path1 + str(id) + ".jpg"
                mysqlComment.updateData(id, path1)
                # 保存图片
                data = urllib.request.urlopen(img_link)
                # print(data)
                f = open(path, "wb")
                f.write(data.read())
                f.close()
                time.sleep(2)
    mysqlComment.closeMysql()

if __name__ == '__main__':
    search()  # coding:utf-8
