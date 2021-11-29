from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class NotesConfig(models.Model):
    '''用户发帖'''

    user = models.ForeignKey(User, verbose_name='用户', null=True, on_delete=models.SET_NULL)
    subject = models.CharField(max_length=80, verbose_name='主题')
    message = models.TextField(default='', verbose_name='内容', help_text='内容')
    message_id = models.CharField(max_length=20, verbose_name="帖子id", help_text="帖子id")
    read_num = models.IntegerField(default=0, verbose_name="浏览量")
    post_time = models.DateTimeField(default=datetime.now, verbose_name="发帖日期")

    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '用户帖子'

        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserComment(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', null=True, on_delete=models.SET_NULL)
    comment_id = models.CharField(max_length=20, verbose_name="评论id")
    message = models.TextField(default='', verbose_name='留言内容', help_text='评论内容')
    comment_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")
    note_id = models.CharField(default=' ', max_length=20, verbose_name="帖子的唯一标识符")

    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name = '回帖评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment_id
