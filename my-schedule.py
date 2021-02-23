# 通过schedule来执行
import time
import schedule

from jwc import job as job1
from weifuwu import job as job2

schedule.every(10).minutes.do(job1) # 每10分钟监控教务处新闻
schedule.every().day.at("06:30").do(job2) # 每天6：30打卡

while True:
    schedule.run_pending() # 运行所有可运行的任务
    time.sleep(1)