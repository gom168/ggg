from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import django_filters.rest_framework
from .models import NotesConfig, UserComment
from .serializers import NotesSerializer, UserCommentSerializer
from rest_framework.filters import BaseFilterBackend
from .filters import NoteCommentFilter

from utils.permissions import IsOwnerOrReadOnly


class NotesViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = NotesSerializer

    def get_queryset(self):
        return NotesConfig.objects.filter(user=self.request.user, is_delete=False)


class CommentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    serializer_class = UserCommentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = NoteCommentFilter

    def get_queryset(self):
        return UserComment.objects.filter(user=self.request.user, is_delete=False)
