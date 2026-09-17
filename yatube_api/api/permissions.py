from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.views import APIView

from posts.models import Comment, Post


class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Разрешает изменять объект только его автору."""

    def has_object_permission(
        self, request: Request, view: APIView, obj: Post | Comment
    ) -> bool:
        return request.method in SAFE_METHODS or obj.author == request.user
