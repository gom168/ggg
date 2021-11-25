from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.


class GoodsCategory(models.Model):
    '''商品分类'''
    CATEGORY_TYPE = (
        (1, '一级类目'),
        (2, '二级类目'),
        (3, '三级类目'),
    )
    name = models.CharField(default='', max_length=30, verbose_name='类别名', help_text='类别名')
    code = models.CharField(default='', max_length=30, verbose_name='类别code', help_text='类别code')
    desc = models.TextField(default='', verbose_name='类别描述', help_text='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类目级别', help_text='类目级别')
    parent_category = models.ForeignKey('self', null=True, blank=True, verbose_name='父类别', related_name='sub_cat', on_delete=models.SET_NULL)
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    '''品牌名'''
    name = models.CharField(default='', max_length=30, verbose_name='品牌名', help_text='品牌名')
    desc = models.TextField(default='', max_length=200, verbose_name='品牌描述', help_text='品牌描述')
    image = models.ImageField(max_length=200, upload_to='brand/images/')
    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    '''商品'''
    category = models.ForeignKey(GoodsCategory, verbose_name='商品类目', null=True, on_delete=models.SET_NULL)
    goods_sn = models.CharField(max_length=50, default='', verbose_name='商品唯一货号')
    name = models.CharField(max_length=300, verbose_name='商品名')
    click_num = models.IntegerField(default=0, verbose_name='点击量')
    sold_num = models.IntegerField(default=0, verbose_name='销售量')
    fav_num = models.IntegerField(default=0, verbose_name='收藏量')
    goods_num = models.IntegerField(default=0, verbose_name='库存量')
    price = models.FloatField(default=0, verbose_name='价格')
    goods_brief = models.TextField(max_length=500, verbose_name='商品简介')
    goods_desc = UEditorField(verbose_name=u'内容', imagePath='goods/images/', width=1000, height=300, filePath='goods/files/', default='')
    ship_free = models.BooleanField(default=True, verbose_name='是否承担运费')
    goods_front_image = models.ImageField(upload_to='goods/images/', null=True, blank=True, verbose_name='封面图')
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    is_hot = models.BooleanField(default=False, verbose_name='是否热销')
    detail_image = models.ImageField(upload_to='goods/images/', null=True, blank=True, verbose_name='商品介绍图')

    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    '''商品轮播图'''
    goods = models.ForeignKey(Goods, verbose_name='', related_name='商品', null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='', null=True, blank=True, verbose_name='图片')
    image_url = models.CharField(max_length=300, null=True, blank=True, verbose_name='图片链接')

    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '商品轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    '''轮播商品'''
    goods = models.ForeignKey(Goods, verbose_name='商品', null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='banner', verbose_name='轮播图片')
    index = models.IntegerField(default=0, verbose_name='轮播顺序')

    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Settings(models.Model):
    '''参数设置'''
    setting_id = models.CharField(max_length=20, verbose_name="配置id")
    name = models.CharField(max_length=20, verbose_name="配置名称")
    info = models.CharField(max_length=100, verbose_name="配置信息")
    goods_sn = models.CharField(max_length=50, verbose_name='商品唯一货号')

    add_time = models.DateField(default=datetime.now, verbose_name='添加时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '参数设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name