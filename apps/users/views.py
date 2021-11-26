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

from .models import VerifyCode
from .serializer import UserDetailSerializer,UserRegSerializer
from utils.yunpian import yunpian


class CustomBackend(ModelBackend):
    '''自定义用户验证'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
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
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def get_permissions(self):
        '''动态设置权限'''
        if self.action == 'retrieve':
            return [IsAuthenticated]
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