# from email import message
import datetime
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText

import requests
from pyquery import PyQuery as pq
from selenium import webdriver
# from emails import Email
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from readconfig import ReadConfig

profile = webdriver.FirefoxOptions()
# profile.add_argument('-headless')  # 设置无头模式
# 设置代理服务器
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.http', "127.0.0.1")  # IP为你的代理服务器地址:如‘127.0.0.0’，字符串类型
profile.set_preference('network.proxy.http_port', "7777")  # PORT为代理服务器端口号:如，9999，整数类型
browser = webdriver.Firefox(options=profile)

config = ReadConfig()
username = config.get_key("username")
passwd = config.get_key("passwd")
receiver = config.get_key("receiver")

def sendEmail(message_body, receiver="43471492@qq.com"):
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "43471492@qq.com"  # 用户名
    mail_pass = "ndzvzbybgsbrbgjd"  # 口令
    sender = '43471492@qq.com'
    message = MIMEText(message_body, 'plain', 'utf-8')
    message['From'] = Header("微服务自动打卡小助手", 'utf-8')
    message['To'] = Header(username, 'utf-8')
    subject = '微服务自助打卡邮件通知'
    message['Subject'] = Header(subject, 'utf-8')
    # print(message)
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        # smtpObj.connect()    # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功")
        smtpObj.quit()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def Login_To_Get_Session(username, password):
    url = "https://ua.scu.edu.cn/login?service=https%3A%2F%2Fwfw.scu.edu.cn%2Fa_scu%2Fapi%2Fsso%2Fcas-index%3Fredirect%3Dhttps%253A%252F%252Fwfw.scu.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex"
    browser.get(url)
    # WebDriverWait(browser,10).until(EC.presence_of_all_elements_located)
    # time.sleep(2)
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    # 定位到iframe
    iframe = browser.find_element_by_id("loginIframe")
    # 切换到iframe
    browser.switch_to_frame(iframe)
    # 选中“密码登录”
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'van-tabs__nav--line')))
    type_username_password = browser.find_element_by_css_selector("div.van-tabs__nav--line>div:nth-child(3)")
    type_username_password.click()

    # 输入工号密码
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'van-field__value')))
    current_box = browser.find_elements_by_css_selector('.van-tabs__content>div')[2]
    div_input_username = current_box.find_elements_by_css_selector('.van-field__body')[0]
    div_input_password = current_box.find_elements_by_css_selector('.van-field__body')[1]
    input_username = div_input_username.find_element_by_css_selector('input')
    input_password = div_input_password.find_element_by_css_selector('input')
    input_username.send_keys(username)
    input_password.send_keys(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'van-button--block')))
    submit_button = browser.find_element_by_css_selector(
        "button.van-button.van-button--default.van-button--normal.van-button--block")
    submit_button.click()
    # time.sleep(5)
    browser.switch_to.default_content()
    html = browser.page_source  # 获取页面的源代码
    doc = pq(html)
    html_scripts = doc('body>script:nth-child(4)').text()
    # the_script_that_we_want = html_scripts[2]
    # data_old_Info = browser.find_element_by_css_selector("body>script:nth-child(3)").get_attribute('textContent')
    # reObj1 = re.compile(r'/oldInfo(.*?})*/')
    the_script_that_we_want = re.findall(r'oldInfo:\s(.*?),\stipMsg', html_scripts)
    # print(html_scripts)
    # print(script_text[0])
    data_tmp = the_script_that_we_want[0]
    data = eval(data_tmp)
    cookies = browser.get_cookies()
    browser.quit()
    session = requests.Session()
    re_cookies = requests.cookies.RequestsCookieJar()
    # 获取cookie中的name和value,转化成requests可以使用的形式
    for cookie in cookies:
        re_cookies.set(cookie['name'], cookie['value'])
    # print(re_cookies)
    headers = {
        'Host': 'wfw.scu.edu.cn',
        'Accept': 'application/json,text/javascript,*/*;q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate,br',
        'Content-Type': 'application/x-www-form-urlencoded;',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '2082',
        'Origin': 'https://wfw.scu.edu.cn',
        'Connection': 'keep-alive',
        'Referer': 'https://wfw.scu.edu.cn/ncov/wap/default/index',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.52'
    }
    now_time = datetime.datetime.now().strftime('%Y%m%d')
    data["date"] = now_time
    print(data)
    session.cookies.update(re_cookies)
    r = session.post(url="https://wfw.scu.edu.cn/ncov/wap/default/save", headers=headers, data=data).json()
    if ("今天已经填报了" in r["m"]):
        print("今天已经填报了")
        message_body = "今天已经填报过了,请不要重复使用我哦！"
        sendEmail(message_body, receiver)
    elif ("操作成功" in r["m"]):
        print("填报成功")
        message_body = '今日打卡成功！专心做其他事情吧！'
        sendEmail(message_body, receiver)


Login_To_Get_Session(username, passwd)
