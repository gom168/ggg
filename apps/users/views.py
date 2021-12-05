from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import django_filters.rest_framework
from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializer import UserDetailSerializer
from .models import UserProfile
from django.core.mail import EmailMultiAlternatives

User = get_user_model()

# Create your views here.


from random import choice

from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from djangoProject import settings

from .models import VerifyCode
from .serializer import UserDetailSerializer, UserRegSerializer, SmsSerializer
from utils.yunpian import yunpian


class CustomBackend(ModelBackend):
    '''自定义用户验证'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password) and user.is_delete != True:
                return user
        except Exception as e:
            return None


class UserViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    用户
    create:
        新增用户
    '''

    serializer_class = UserRegSerializer
    queryset = User.objects.filter(is_delete=False)
    # lookup_field = 'username'
    authentication_classes = [JSONWebTokenAuthentication]

    def get_permissions(self):
        '''动态设置权限'''
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def get_serializer_class(self):
        '''动态设置序列化'''
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username
        headers = self.get_success_headers(re_dict)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_object(self):
        return self.request.user


def send_email(email, code):
    subject = '来自联想官方商城的注册确认邮件'

    text_content = '''感谢注册联想官方商城，验证码为{},有效期为{}天'''.format(code, settings.CONFIRM_DAYS)

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是联想官方商城</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    # msg.attach_alternative(html_content, "text/html")
    msg.send()
    return 1


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    '''发送邮件验证码'''

    serializer_class = SmsSerializer

    def generate_code(self):
        '''生成4位数验证码'''
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        print(email)
        code = self.generate_code()

        send_email(email, code)
        # sms_status = send_email(email, code)
        # if sms_status['code'] != 0:
        #     return Response({
        #         'email': sms_status['msg']
        #     }, status=status.HTTP_400_BAD_REQUEST)
        # else:
        code_record = VerifyCode(code=code, email=email)
        code_record.save()
        return Response({
            'email': email,
            'code': code
        }, status=status.HTTP_201_CREATED)
