import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
from readconfig import ReadConfig

config = ReadConfig()

import base64


def ocr_captcha(imgurl):
    try:
        cred = credential.Credential(config.get_key("qkey"), config.get_key("qsecret"))
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

        req = models.EnglishOCRRequest()

        # with open("captcha.png", "rb") as f:  # 转为二进制格式
        #     base64_data = base64.b64encode(f.read())  # 使用base64进行加密
        #     print(base64_data)

        params = {
            # "ImageBase64" : base64_data.decode()
            # "ImageUrl" : "https://ua.scu.edu.cn/captcha?captchaId=7988765407"
            "ImageBase64": imgurl
        }
        req.from_json_string(json.dumps(params))

        resp = client.EnglishOCR(req)
        # print(resp.to_json_string())
        return resp.TextDetections[0].DetectedText

    except TencentCloudSDKException as err:
        # print(err)

        return "fail"

def get_captcha(imgurl):
    limit = 10
    while True and limit > 0:
        res = ocr_captcha(imgurl)
        if len(res) != 6:
            limit -= 1
            print("识别失败，重试")
            continue
        else:
            return res

# if __name__ == '__main__':
    # result = get_captcha("https://ua.scu.edu.cn/captcha?captchaId=7988765407")
    # print(result)