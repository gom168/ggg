import django_filters
from django.db.models import Q

from .models import UserLeavingMessage
from rest_framework.filters import BaseFilterBackend


# class UserLeavingMessageFilter(django_filters.rest_framework.FilterSet):
#
#     goods_sn = django_filters.CharFilter(field_name="goods_sn", lookup_expr="iexact")
#
#     class Meta:
#         model = UserLeavingMessage
#         fields = ['goods_sn']