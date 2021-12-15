from .Serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderSerializer, OrderDetailSerializer, \
    OrderGoodsSerializer, OrderGoods2Serializer, OrderGoodsDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods

from django.http import HttpResponseRedirect
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from datetime import datetime
from utils.alipay import AliPay
from rest_framework.views import APIView
from djangoProject.settings import ali_pub_key_path, private_key_path,notify_url,return_url
from rest_framework.response import Response
from utils.permissions import IsOwnerOrReadOnly
from djangoProject.settings import app_private_key_path, alipay_public_key_path, ali_app_id, return_url, notify_url
from django_filters.rest_framework import DjangoFilterBackend
import django_filters.rest_framework
from .filters import OrderGoodsFilter


class AlipayView(APIView):
    def get(self, request):
        print("hello")
        """
        处理支付宝的return_url返回
        """
        processed_dict = {}
        # 1. 获取GET中参数
        for key, value in request.GET.items():
            processed_dict[key] = value
        # 2. 取出sign
        sign = processed_dict.pop("sign", None)

        print("1111111111111111111111111111111")

        # 3. 生成ALipay对象
        alipay = AliPay(
            appid="2021000118658197",
            app_notify_url=notify_url,
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url=return_url
        )

        verify_re = alipay.verify(processed_dict, sign)

        # 这里可以不做操作。因为不管发不发return url。notify url都会修改订单状态。
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)


            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = True
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
        return HttpResponseRedirect('http://localhost:8080/#/helloHome')

    def post(self, request):
        """
        处理支付宝的notify_url
        """
        # 存放post里面所有的数据
        processed_dict = {}
        # 取出post里面的数据
        for key, value in request.POST.items():
            processed_dict[key] = value
        # 把signpop掉，文档有说明
        sign = processed_dict.pop("sign", None)

        # 生成一个Alipay对象
        alipay = AliPay(
            appid="2021000118658197",
            app_notify_url=notify_url,
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url=return_url
        )

        # 进行验证
        verify_re = alipay.verify(processed_dict, sign)

        # 如果验签成功
        if verify_re is True:
            # 商户网站唯一订单号
            order_sn = processed_dict.get('out_trade_no', None)
            # 支付宝系统交易流水号
            trade_no = processed_dict.get('trade_no', None)
            # 交易状态
            trade_status = processed_dict.get('trade_status', None)


            # 查询数据库中订单记录
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 订单商品项
                order_goods = existed_order.goods.all()
                # 商品销量增加订单中数值
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                # 更新订单状态
                existed_order.pay_status = True
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            # 需要返回一个'success'给支付宝，如果不返回，支付宝会一直发送订单支付成功的消息
            return Response("success")
        return HttpResponseRedirect('http://localhost:8080/#/helloHome')


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
        goods.goods_num -= shop_cart.goods_num
        goods.save()

    def perform_destroy(self, instance):
        '''删除购物车更新库存量'''
        goods = instance.goods
        goods.goods_num += instance.goods_num
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        '''修改购物车更新库存量'''
        existed_record = ShoppingCart.objects.filter(is_delete=False).get(id=serializer.instance.id)
        existed_goods_num = existed_record.goods_num
        saved_record = serializer.save()
        nums = saved_record.goods_num - existed_goods_num
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    '''
    订单管理
    list:
        订单列表
    delete:
        删除订单
    create:
        新增订单
    '''

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user, is_delete=False)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user, is_delete=False)
        if order.buy_only == False:
            for shop_cart in shop_carts:
                if shop_cart.is_choosen == False:
                    order_goods = OrderGoods()
                    order_goods.goods = shop_cart.goods
                    order_goods.goods_num = shop_cart.goods_num
                    order_goods.order = order
                    order_goods.save()
                    shop_cart.delete()
        return order


class OrderGoodsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderGoods2Serializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = OrderGoodsFilter

    def get_queryset(self):
        return OrderGoods.objects.filter(is_delete=False)

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderGoodsDetailSerializer
        else:
            return OrderGoods2Serializer

    def perform_create(self, serializer):
        order_goods = serializer.save()

        return order_goods

        # order = serializer.save()
        # shop_carts = ShoppingCart.objects.filter(user=self.request.user, is_delete=False)
        # for shop_cart in shop_carts:
        #     if shop_cart.is_choosen == False:
        #         order_goods = OrderGoods()
        #         order_goods.goods = shop_cart.goods
        #         order_goods.goods_num = shop_cart.goods_num
        #         order_goods.order = order
        #         order_goods.save()
        #         shop_cart.delete()
        # return order

# class AliPayView(APIView):
#
#     alipay = AliPay(
#         appid=ali_app_id,
#         app_notify_url=None,
#         app_private_key_string=open(app_private_key_path).read(),
#
#         alipay_public_key_string=open(alipay_public_key_path).read(),
#         sign_type="RSA2",
#         debug=True,
#     )
#
#     def get(self, request):
#
#         data = dict(request.GET.items())
#         signature = data.pop("sign", None)
#         print(data)
#         success = self.alipay.verify(data, signature)
#         order_sn = data.get('out_trade_no', None)
#         print(success)
#         trade_status = self.alipay.api_alipay_trade_query(out_trade_no=order_sn).get("trade_status", None)
#         print(trade_status)
#         if success and trade_status in ("TRADE_SUCCESS", "TRADE_FINISHED"):
#             trade_no = data.get('trade_no', None)
#             existed_orders = OrderInfo.objects.filter(order_sn=order_sn, is_delete=False)
#             if existed_orders:
#                 for order in existed_orders:
#                     order_goods = order.goods.all()
#                     for order_good in order_goods:
#                         goods = order_good.goods
#                         goods.sold_num += order_good.goods_num
#                         goods.save()
#                     order.pay_status = trade_status
#                     order.trade_no = trade_no
#                     order.pay_time = datetime.now()
#                     order.save()
#                 response = HttpResponseRedirect('http://127.0.0.1:8080/#/app/home/member/order')
#                 response.set_cookie('nextPath', 'pay', max_age=2)
#                 print('cookie', response.cookies)
#                 return response
#         return HttpResponseRedirect('http://127.0.0.1:8080/#/app/shoppingcart/cart')
#
#     def post(self, request):
#         data = dict(request.POST.items())
#         signature = data.pop("sign", None)
#         success = self.alipay.verify(data, signature)
#         order_sn = data.get('out_trade_no', None)
#         trade_status = self.alipay.api_alipay_trade_query(out_trade_no=order_sn).get("trade_status", None)
#         if success and trade_status in ("TRADE_SUCCESS", "TRADE_FINISHED"):
#             trade_no = data.get('trade_no', None)
#             existed_orders = OrderInfo.objects.filter(order_sn=order_sn, is_delete=False)
#             print(len(existed_orders))
#             if existed_orders:
#                 for order in existed_orders:
#                     order_goods = order.goods.all()
#                     for order_good in order_goods:
#                         goods = order_good.goods
#                         goods.sold_num += order_good.goods_num
#                         goods.save()
#                     order.pay_status = trade_status
#                     order.trade_no = trade_no
#                     order.pay_time = datetime.now()
#                     order.save()
#                 response = HttpResponseRedirect('http://127.0.0.1:8080/#/app/home/member/order')
#                 response.set_cookie('nextPath', 'pay', max_age=2)
#                 print('cookie', response.cookies)
#                 return response
#         return HttpResponseRedirect('http://127.0.0.1:8080/#/app/shoppingcart/cart')
