import requests
from bs4 import BeautifulSoup

from connect import insertJwcNews
from news import News


# import schedule

def job():
    print("I'm working...")
    url = 'http://jwc.scu.edu.cn'
    html = requests.get(url)
    html.encoding = 'utf-8'
    bs = BeautifulSoup(html.text, 'html.parser')
    info = bs.select('.list-llb-list')

    # 爬虫网页，获取首页通知公告
    newslist = []
    for li in info:
        a = li.find('a')
        title = a['title']
        url = a['href']
        date = a.select('.list-date-a')[0].get_text()
        newslist.append(News(title, url, date))

    # 数据库操作
    insertJwcNews(newslist)


