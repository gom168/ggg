from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

#from utils.permissions import IsOwnerOrReadOnly
from .Serializers import ShoppingCartSerializer,ShoppingCartDetailSerializer,OrderSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods

from datetime import datetime


from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication



# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    '''
    list:
        购物车列表
    create:
        加入购物车
    update:
        购物车修改
    delete:
        删除购物车
    '''

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = ShoppingCartSerializer
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user, is_delete=False)

    def perform_create(self, serializer):
        '''创建购物车更新库存量'''
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        '''删除购物车更新库存量'''
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        '''修改购物车更新库存量'''
        existed_record = ShoppingCart.objects.filter(is_delete=False).get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    订单管理
    list:
        订单列表
    delete:
        删除订单
    create:
        新增订单
    '''

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user, is_delete=False)

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user, is_delete=False)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order