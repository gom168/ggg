import django_filters
from django.db.models import Q

from .models import UserComment
from rest_framework.filters import BaseFilterBackend


class NoteCommentFilter(django_filters.rest_framework.FilterSet):

    note_id = django_filters.CharFilter(field_name="note_id", lookup_expr="iexact")

    class Meta:
        model = UserComment
        fields = ['note_id']