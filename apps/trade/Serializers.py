from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart

from goods.serializers import GoodsSerializer


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, min_value=1, label='数量',
                                    error_messages={
                                        'required': '请选择商品数量',
                                        'min_value': '商品数量至少为1'
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.filter(is_delete=False))

    def create(self, validated_data):
        '''新增数据'''
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']
        existed = ShoppingCart.objects.filter(is_delete=False, user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += 1
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改购物车商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance