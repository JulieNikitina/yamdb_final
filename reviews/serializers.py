from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    text = serializers.SlugField(
        max_length=100,
        validators=[UniqueValidator(queryset=Review.objects.all())]
    )

    class Meta:
        fields = '__all__'
        model = Review
        extra_kwargs = {'title': {'required': False}}


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        extra_kwargs = {
            'title': {'required': False},
            'review': {'required': False}
        }
