import base64

from django.core.mail import send_mail
from django.template import loader
from django.urls import reverse
from itsdangerous import URLSafeTimedSerializer as utsr
from django.conf import settings as django_settings
from djangoProject import settings


# 邮箱验证携带token值封装类
class Token:
    def __init__(self, secret_key):
        self.serializer = utsr(secret_key)
        self.salt = base64.encodebytes(secret_key.encode('utf8'))

    # 生成token
    def generate_validate_token(self, username):
        # 返回有两个点'.'组成三部分的token值
        return self.serializer.dumps(username, self.salt)

    # 验证token
    def confirm_validate_token(self, token, expiration=3600):
        """
            :param expiration: token值有效期，单位/秒
        """
        # 返回原生值，类型根据生产token值是传入的变量而定
        return self.serializer.loads(token, salt=self.salt, max_age=expiration)

    # 删除token
    def remove_validate_token(self, token):
        return self.serializer.loads(token, salt=self.salt)

# 创建token对象
token_confirm = Token(django_settings.SECRET_KEY)


# 发送邮件验证
#@celery_app.task
def send_email(u_id,host,eml):
    token = token_confirm.generate_validate_token(u_id)

    # 构造邮箱激活路由
    eml_url = "http://" + host + reverse("App:active",kwargs= {'token':token})

    # 加载模板
    html = loader.get_template('active.html').render({'eml_url': eml_url})
    send_mail(settings.SUBJECT, '', settings.EMAIL_FROM, [eml], html_message=html)
    # return token