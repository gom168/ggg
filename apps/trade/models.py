from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model  # from users.models import UserProfile

from goods.models import Goods

User = get_user_model()


# Create your models here.

class ShoppingCart(models.Model):
    '''购物车'''
    user = models.ForeignKey(User, verbose_name='用户', null=True, on_delete=models.SET_NULL)
    goods = models.ForeignKey(Goods, verbose_name='商品', null=True, on_delete=models.SET_NULL)
    goods_num = models.IntegerField(default=0, verbose_name='商品数量')
    is_choosen = models.BooleanField(default=True,verbose_name='是否购买')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        #unique_together = ('user', 'goods')

    def __str__(self):
        return '%s(%d)'.format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    '''订单信息'''
    ORDER_STATUS = (
        ('success', '成功'),
        ('cancel', '取消'),
        ('paying', '待支付'),
    )
    user = models.ForeignKey(User, verbose_name='用户', null=True, on_delete=models.SET_NULL)
    order_sn = models.CharField(max_length=30, unique=True, verbose_name='订单号')
    trade_no = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='交易号')
    pay_status = models.CharField(max_length=100, choices=ORDER_STATUS, verbose_name='订单状态')
    pay_script = models.CharField(max_length=11, verbose_name='订单留言')
    order_mount = models.FloatField(default=0.0, verbose_name='订单金额')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    # 用户基本信息
    address = models.CharField(max_length=100, default='', verbose_name='收货地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, verbose_name='联系电话')

    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    '''订单商品详情'''
    order = models.ForeignKey(OrderInfo, verbose_name='订单信息', null=True, on_delete=models.SET_NULL)
    goods = models.ForeignKey(Goods, verbose_name='商品', null=True, on_delete=models.SET_NULL)
    goods_num = models.IntegerField(default=0, verbose_name='商品数量')

    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.order_sn


