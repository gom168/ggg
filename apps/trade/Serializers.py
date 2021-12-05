from rest_framework import serializers
from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer
import time
from djangoProject.settings import app_private_key_path, alipay_public_key_path, ali_app_id, return_url, notify_url
import random
from utils.alipay import AliPay


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=ali_app_id,
            app_notify_url="http://47.93.198.159:8000/alipay/return/",
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.93.198.159:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    is_delete = serializers.BooleanField(read_only=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=ali_app_id,
            app_notify_url="http://47.93.198.159:8000/alipay/return/",
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.93.198.159:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    def generate_order_sn(self):
        # 生成订单编号
        return '%s%d%d' % (time.strftime('%Y%m%d%H%M%S'), self.context['request'].user.id, random.randint(1000, 9999))

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goods_num = serializers.IntegerField(required=True, min_value=1, label='数量',
                                    error_messages={
                                        'required': '请选择商品数量',
                                        'min_value': '商品数量至少为1'
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.filter(is_delete=False))

    def create(self, validated_data):
        '''新增数据'''
        user = self.context['request'].user
        goods_num = validated_data['goods_num']
        goods = validated_data['goods']
        existed = ShoppingCart.objects.filter(is_delete=False, user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.goods_num += 1
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改购物车商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance

