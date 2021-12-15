import django_filters
from django.db.models import Q
from .models import OrderGoods


class OrderGoodsFilter(django_filters.rest_framework.FilterSet):

    order_id = django_filters.CharFilter(field_name="order__id", lookup_expr="iexact")

    class Meta:
        model = OrderGoods
        fields = ['order_id']