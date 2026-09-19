from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Follow, Group, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """Возвращает публикации и управляет публикациями автора запроса."""

    queryset = Post.objects.select_related('author', 'group')
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: PostSerializer) -> None:
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Возвращает комментарии выбранной публикации и управляет ими."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_post(self) -> Post:
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self) -> QuerySet[Comment]:
        return self.get_post().comments.select_related('author')

    def perform_create(self, serializer: CommentSerializer) -> None:
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращает список сообществ или выбранное сообщество."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Возвращает и создаёт подписки текущего пользователя."""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self) -> QuerySet[Follow]:
        return self.request.user.follower.select_related(
            'user', 'following'
        )

    def perform_create(self, serializer: FollowSerializer) -> None:
        serializer.save(user=self.request.user)
