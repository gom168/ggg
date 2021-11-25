import xadmin
from .models import NotesConfig, UserComment


class NotesConfigAdmin(object):
    list_display = ["user", "subject", "message_id", "read_num", "comment_num", "post_time"]
    list_filter = ["user", "subject", "message_id", "read_num", "comment_num", "post_time"]
    search_fields = ["subject",]
    list_per_page = 10
    show_detail_fields = ["subject",]


class UserCommentAdmin(object):
    list_display = ["user", "note", "comment_time", "comment_id", "message"]
    list_filter = ["user", "note", "comment_time", "comment_id", "message"]
    list_per_page = 10


xadmin.site.register(NotesConfig, NotesConfigAdmin)
xadmin.site.register(UserComment,UserCommentAdmin)
