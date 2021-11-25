from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

User = get_user_model()


# Create your models here.

class UserFav(models.Model):
    '''用户收藏'''
    user = models.ForeignKey(User, verbose_name='用户', null=True, on_delete=models.SET_NULL)
    goods = models.ForeignKey(Goods, verbose_name='商品', null=True, on_delete=models.SET_NULL)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        # 联合唯一验证
        unique_together = ('user', 'goods')

    def __str__(self):
        return self.user.name


class UserLeavingMessage(models.Model):
    '''用户留言'''
    MESSAGE_CHOICES = (
        (1, '留言'),
        (2, '投诉'),
        (3, '询问'),
        (4, '售后'),
        (5, '求购'),
    )
    user = models.ForeignKey(User, verbose_name='用户', null=True, on_delete=models.SET_NULL)
    goods_sn = models.CharField(max_length=50, verbose_name='商品唯一货号')
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name='留言类型',
                                help_text='留言类型: 1(留言), 2(投诉), 3(询问),4(售后), 5(求购)')
    subject = models.CharField(max_length=80, default='', verbose_name='主题')
    message = models.TextField(default='', verbose_name='留言内容', help_text='留言内容')

    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(models.Model):
    '''用户收货地址'''
    user = models.ForeignKey(User, verbose_name='用户', null=True, on_delete=models.SET_NULL)
    district = models.CharField(max_length=50, default='', verbose_name='区域')
    address = models.CharField(max_length=100, default='', verbose_name='详细地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, default='', verbose_name='联系电话')

    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address