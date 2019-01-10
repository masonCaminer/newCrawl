# coding:utf-8
import re
import urllib.request
import requests
import chardet
from bs4 import BeautifulSoup
import datetime
from db.MySQLCommand import MySQLCommand
import random
import time
import os

mysqlComment = MySQLCommand()
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
        content = soup.findAll("article", {"class": "article"})  # resultset object
        if len(content) == 0:
            content = soup.find_all("div", {"class": "content"})
        if len(content) == 0:
            content = soup.find_all("div", {"class": "show_content"})
        return content
    return ""

# 抓取百度新闻搜索结果:中文搜索，前10页，url：key=关键词
def search(key_word):
    for i in range(2):
        mysqlComment.connectionMysql()
        search_url = 'http://news.baidu.com/ns?word=key_word&pn=pn_s&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0&rsv_page=1'
        search_url = search_url.replace('key_word', key_word)
        search_url = search_url.replace('pn_s', str((i+1)*20))
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(dt+" "+search_url)
        req = requests.get(search_url)
        i += 20
        req.raise_for_status()
        req.encoding = req.apparent_encoding
        # req = urllib.request.urlopen(search_url.replace('key_word', key_word))
        real_visited = 0
        html = req.text
        soup = BeautifulSoup(html, "lxml")
        content = soup.findAll("div", {"class": "result"})  # resultset object
        num = len(content)
        for i in range(num):
            # 先解析出来所有新闻的标题、来源、时间、url
            p_str = content[i].find('a')  # if no result then nontype object
            p_img = content[i].find('img')
            if p_img==None:
                continue
            contenttitle = p_str.renderContents()
            contenttitle = contenttitle.decode('utf-8', 'ignore')  # need it
            contenttitle = re.sub("<[^>]+>", "", contenttitle).strip()
            contentlink = str(p_str.get("href")).strip()
            img_link = str(p_img.get("src")).strip()
            p_str2 = content[i].find('p').renderContents()
            contentauthor = p_str2[:p_str2.find(str.encode('&nbsp;&nbsp'))]  # 来源
            contentauthor = contentauthor.decode('utf-8', 'ignore')  # 时
            contentauthor = contentauthor.split('\t')[0].strip()
            real_visited += 1
            # file_name = r"D:\Python27\newscn\%d.txt" % (real_visited)
            contents = extract_news_content(contentlink)  # 还写入文件

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
                    "image_link":img_link
                }
                id = mysqlComment.insertData(news_dict)
                if id !=None:

                    # path = "D:/文件夹/"+str(id)+".jpg"
                    # path = "/opt/developer/maoyl/ai_news_get_python/tupian/"+str(id)+".jpg"

                    if id%100==0:
                        path = "/opt/wwwroot/ailab.d.kingnet.com/static/main/static/newsimg/"+str(id)+"/"
                        path1 = "static/newsimg/"+str(id)+"/"
                        isExists = os.path.exists(path)
                        if not isExists:
                            os.makedirs(path)
                        path = path+str(id)+".jpg"
                        path1=path1+str(id)+".jpg"
                    else:
                        nn = int(id/100)*100
                        path = "/opt/wwwroot/ailab.d.kingnet.com/static/main/static/newsimg/"+str(nn)+"/"
                        path1 = "static/newsimg/"+str(nn)+"/"
                        isExists = os.path.exists(path)
                        if not isExists:
                            os.makedirs(path)
                        path = path+str(id)+".jpg"
                        path1=path1+str(id)+".jpg"

                    mysqlComment.updateData(id,path1)
                    #保存图片
                    opener = urllib.request.build_opener()
                    opener.addheaders = headers
                    data = opener.open(img_link)
                    # print(data)
                    f = open(path, "wb")
                    f.write(data.read())
                    f.close()
                    time.sleep(2)
        mysqlComment.closeMysql()


if __name__ == '__main__':
    # key_word = raw_input('input key word:')
    search("ai")  # coding:utf-8
    # testMysql()
