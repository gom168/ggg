import requests
import json

from djangoProject.settings import APIKEY

class YunPian(object):
    def __init__(self):
        self.api_key = APIKEY
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【Lenovo购物商城】欢迎您注册联想购物商城账号 ，验证码：{}（5分钟内有效，如非本人操作，请忽略）'.format(code)
        }
        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        return re_dict


yunpian = YunPian()


if __name__ == '__main__':
    yunpian.send_sms('1234', '18563985032')  # 改为你自己的手机号