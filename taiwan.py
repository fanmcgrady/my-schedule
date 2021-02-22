import openpyxl
import requests
from bs4 import BeautifulSoup
import re

file = openpyxl.load_workbook("Taiwan.xlsx")
sheet1 = file.active
baseurl = 'https://giving.ntu.edu.tw/HeroList.aspx?pn='
for i in range(1, 2216):
    url = baseurl + str(i)
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'lxml')
    info = bs.find_all('td')
    excel = []
    for j in range(len(info)):
        txt = re.sub(u"<.*?>", "", str(info[j])).replace(' ', '').replace('\n', '')
        excel.append(txt)
        if (j + 1) % 5 == 0:
            sheet1.append(excel)
            excel = []
    print("已爬取第%d个网页" % i)
    file.save('Taiwan.xlsx')
