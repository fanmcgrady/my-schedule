import requests
from bs4 import BeautifulSoup

from news import News
from connect import insertJwcNews
import schedule
import time

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


schedule.every(10).minutes.do(job) # 每10分钟执行一次

while True:
    schedule.run_pending() # 运行所有可运行的任务
    time.sleep(1)
