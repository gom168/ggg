from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import NotesConfig, UserComment

import time

import random


class NotesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_time = serializers.DateTimeField(read_only=True)

    def generate_message_id(self):
        # 生成notes编号
        return '%s%d%d' % (time.strftime('%Y%m%d%H%M%S'), self.context['request'].user.id, random.randint(1000, 9999))

    def validate(self, attrs):
        attrs['message_id'] = self.generate_message_id()
        return attrs

    class Meta:
        model = NotesConfig
        fields = ['id', 'user', 'message_id', 'subject', 'message', 'post_time', 'read_num']


class UserCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    comment_time = serializers.DateTimeField(read_only=True)

    def generate_comment_id(self):
        # 生成notes的评论编号
        return '%s%d%d' % (time.strftime('%Y%m%d%H%M%S'), self.context['request'].user.id, random.randint(1000, 9999))

    def validate(self, attrs):
        attrs['comment_id'] = self.generate_comment_id()
        return attrs

    class Meta:
        model = UserComment
        fields = ['id', 'user', 'comment_id', 'message', 'comment_time', 'note_id']