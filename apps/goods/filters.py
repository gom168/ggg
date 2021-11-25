import django_filters
from django.db.models import Q

from .models import Goods, Settings
from rest_framework.filters import BaseFilterBackend


class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''商品过滤类'''
    name = django_filters.CharFilter(field_name="name", lookup_expr='contains')
    pricemin = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        '''自定义过滤'''
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['name', 'pricemin', 'pricemax', 'is_hot', 'is_new']


class SettingsFilter(django_filters.rest_framework.FilterSet):
    '''配置信息过滤类'''
    goods_sn = django_filters.CharFilter(field_name="goods_sn", lookup_expr="iexact")

    class Meta:
        model = Settings
        fields = ['goods_sn']


class CategoryOfgoodsFilter(django_filters.rest_framework.FilterSet):

    category_name = django_filters.CharFilter(field_name="category__name", lookup_expr="iexact")

    class Meta:
        model = Goods
        fields = ['category_name']