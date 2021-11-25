import re
from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model

from Fresh_Ecommerce.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()

class SmsSerializer(serializers.Serializer):
    '''短信发送序列化'''

    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        '''验证手机号码'''


        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号格式有误，请重新输入')

        # 验证手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('手机号已经被注册过，请更换手机号重新注册或直接使用该手机号登录')

        # 验证短信发送频率
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError('验证码发送频率过快，请稍后再试')

        return mobile