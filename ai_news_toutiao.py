# 爬图片
from urllib import request
from urllib.parse import urlencode
import urllib.error
import os
from hashlib import md5
from multiprocessing.pool import Pool
import json as jn
import requests
from bs4 import BeautifulSoup
import chardet
import re
from lxml import etree
import time

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
        content = soup.renderContents().decode('utf-8', 'ignore')
        content = re.findall(r"content:\s?'(.+?)',\s+", content)
        if len(content) == 0:
            return ""
        content = content[0]
        q = etree.HTML('<cite>' + content + '</cite>')
        b = q.xpath('//cite/text()')[0]
        # soups = BeautifulSoup(b, "lxml").findAll("img")[0].get("src")
        # k = etree.HTML(b)
        # n = k.xpath('//p/text()')
        return b


# 抓取今日头条新闻搜索结果
def search(offset, key_word):
    json = get_page(offset, key_word)
    # str 转json
    json = jn.loads(json).get('data')
    # urls = [article.get('article_url') for article in json if article.get('article_url')]
    num = 0
    for article in json:
        if article.get('article_url'):
            a_url = article.get('article_url')
            title = article.get('title')
            if title.find('机') != -1 or title.find('安卓') != -1 or title.find('全面') != -1 or title.find('学') != -1 or title.find('教') != -1 or title.find('华为') != -1:
                continue
            if ('AI' not in title) and ('ai' not in title):
                continue
            if article.get('has_video')==True:
                continue
            author = article.get('source')
            timestamp = time.time()
            time_tuple = time.localtime(timestamp)
            time_now = datetime.datetime.now().strftime("%Y-%m-%d")
            time_content = time.strftime("%Y-%m-%d", time.localtime(float(article.get("display_time"))))
            image_link = article.get("large_image_url")
            if time_now != time_content:
                continue
            if image_link == '':
                continue
            contents = extract_news_content(a_url)  # 还写入文件
            if contents == "":
                continue
            num += 1
            if num == 3:
                break
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            news_dict = {
                "content_title": title,
                "content_author": author,
                "content_link": a_url,
                "content_details": str(contents).strip(),
                "insert_time": dt,
                "image_link": image_link
            }
            mysqlComment.connectionMysql()
            id = mysqlComment.insertData(news_dict)
            if id != None:
                if id % 100 == 0:
                    # path + "D:/文件夹/" + str(id) + "/"
                    path = "/opt/wwwroot/ailab.d.kingnet.com/static/main/static/newsimg/" + str(id) + "/"
                    path1 = "static/newsimg/" + str(id) + "/"
                    isExists = os.path.exists(path)
                    if not isExists:
                        os.makedirs(path)
                    path = path + str(id) + ".jpg"
                    path1 = path1 + str(id) + ".jpg"
                else:
                    nn = int(id / 100) * 100
                    # path = "D:/文件夹/" + str(nn) + "/"
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


def get_page(offset, key_word):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': key_word,
        'autoload': 'true',
        'count': 20,  # 每次返回 20 篇文章
        'cur_tab': 1
    }
    url = "https://www.toutiao.com/search_content/?" + urlencode(params)
    try:
        response = request.urlopen(url=url)
        if response.status == 200:
            return response.read().decode('utf-8')
    except urllib.error.URLError:
        return None


if __name__ == '__main__':
    search('0', 'AI')  # coding:utf-8
