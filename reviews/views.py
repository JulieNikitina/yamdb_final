from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from objects.models import Title
from reviews.models import Review
from reviews.permissions import CustomPermission
from reviews.serializers import CommentSerializer, ReviewSerializer
from users.models import User


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user)
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CustomPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )
        return review.comments.all().order_by('id')

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )
        user = get_object_or_404(User, username=self.request.user)
        serializer.save(author=user, review=review)
