import psycopg2

from message import Message


def insertJwcNews(newslist):
    if len(newslist) == 0:
        return

    conn = psycopg2.connect(database="student", user="fangzhiyang", password="123", host="localhost", port="5432")
    cur = conn.cursor()

    for news in newslist:
        cur.execute("select * from t_jwc_news where url = '%s'" % news.url)
        result = cur.fetchall()

        if len(result) == 0:
            cur.execute("insert into t_jwc_news(title, url, date) values(%s, %s, %s)",
                        (news.title, news.url, news.date))
            print("插入：{}".format(news.title))
            Message().send(news)

    conn.commit()
    cur.close()
    conn.close()
