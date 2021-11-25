import django_filters.rest_framework
from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import UserFav, UserLeavingMessage
from .serializer import UserFavSerializer, UserLeavingMessageSerializer
from .models import UserLeavingMessage

from django_filters.rest_framework import DjangoFilterBackend

#from utils.permissions import IsOwnerOrReadOnly


from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

# Create your views here.


# @csrf_exempt
# def post_comment(request):
#     if request.method == "POST":
#         req = json.loads(request.body)
#         print(req)
#         key_flag = req.get("subject") and len(req) == 1
#
#         if key_flag:
#             message = UserLeavingMessage(subject=req["subject"])
#             message.save()
#             return JsonResponse({"status": "BS.202", "msg": "publish article sucess."})
#         else:
#             return JsonResponse({"status": "BS.400", "message": "please check param."})


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''用户收藏'''
    permission_classes = [IsAuthenticated] #permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = UserFavSerializer
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user, is_delete=False)


class UserLeavingMessageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = 'good_sn'
    serializer_class = UserLeavingMessageSerializer
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user, is_delete=False)

    # queryset = UserLeavingMessage.objects.all()
    #
    # serializer_class = UserLeavingMessageSerializer
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # #filter_class = CategoryOfgoodsFilter
