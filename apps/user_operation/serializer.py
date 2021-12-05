from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress

from goods.serializers import GoodsSerializer


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ['id', 'user', 'province', 'city', 'district', 'address', 'signer_name', 'add_time', 'signer_mobile']


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserLeavingMessage
        fields = ['id', 'user', 'message_type', 'subject', 'message', 'add_time']


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ['id', 'goods']


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav
        fields = ['id', 'user', 'goods']
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.filter(is_delete=False),
                fields=['user', 'goods'],
                message='请勿重复收藏'
            )
        ]
