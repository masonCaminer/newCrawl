
# coding=utf-8

# 提交word
import re
import urllib.request
import requests
import chardet
from bs4 import BeautifulSoup
from db.MySQLCommand_blog import MySQLCommand_blog
# 有图片
mysqlComment = MySQLCommand_blog()
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
    # htmlf = open('/opt/developer/maoyl/ai_news_get_python/看最新进展深入了解深度学习.htm', 'r',encoding="utf-8")
    htmlf = open('C:\\Users\\Administrator\\Desktop\\博客\\看最新进展深入了解深度学习.htm', 'r',encoding="utf-8")
    htmlpage = htmlf.read()
    news_dict = {
        "content_details": str(htmlpage).strip(),
    }
    mysqlComment.updateDatas(85,str(content[0]).strip())

    mysqlComment.closeMysql()


if __name__ == '__main__':
    search()  # coding:utf-8
