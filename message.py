from news import News
from readconfig import ReadConfig
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

class Message:
    def __init__(self):
        self.config = ReadConfig()
        self.client = AcsClient(self.config.get_key("key"), self.config.get_key("secret"), 'cn-hangzhou')

    def send(self, news=News("", "", "")):
        contents = ", 'newsName': '{}', url: '{}'{}".format(
            news.title[:17] + "..." if len(news.title) > 20 else news.title,
            news.url.replace("http://jwc.scu.edu.cn/", ""), "}"
        )

        for key, value in self.config.get_users():
            self.sendTo(key, value, contents)

    def sendTo(self, name, phone, contents):
        contents = "{}'name': '{}'".format("{", name) + contents

        # 模版内容:
        # ${name}您好，教务处网站${content}发布了新通知公告，标题为："${newsName}"。（地址：http://jwc.scu.edu.cn/${url}）
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', "四川大学网络空间安全学院")
        request.add_query_param('TemplateCode', "SMS_183760754")
        request.add_query_param('TemplateParam', contents)

        response = self.client.do_action(request)
        print(str(response, encoding='utf-8'))


