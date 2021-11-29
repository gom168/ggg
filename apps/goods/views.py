import django_filters.rest_framework
from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory, GoodsImage, Banner, Settings
from .serializers import GoodsSerializer, CategorySerializer, GoodsImageSerializer, BannerSerializer, SettingsSerializer
from .filters import GoodsFilter,SettingsFilter, CategoryOfgoodsFilter

from rest_framework.views import APIView
from rest_framework.response import Response



from rest_framework.filters import BaseFilterBackend

from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

import json

# Create your views here.


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class BannerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class GoodsImageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''商品轮播图数据'''
    queryset = GoodsImage.objects.all()
    serializer_class = GoodsImageSerializer


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''商品列表页，并实现分页、搜索、过滤、排序'''

    queryset = Goods.objects.filter(is_delete=True).order_by('id')
    lookup_field = 'goods_sn'
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = GoodsFilter
    search_fields = ['name', 'goods_brief', 'goods_desc']
    ordering_fields = ['sold_num', 'price']


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''商品分类列表数据'''
    queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer


class SettingsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = SettingsFilter


class GoodsOfCategory(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()

    serializer_class = GoodsSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = CategoryOfgoodsFilter




