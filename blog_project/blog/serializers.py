from django.contrib import auth
from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User
from django.utils.text import slugify


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author", read_only=True)
    class Meta:
        model = Post
        fields = ('id', "author_name", "title", "text", "author", "published_date", "create_date")
        kwargs = {
            "published_date": {'read_only':True},
            "create_date": {'read_only':True}
        }

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.slug = slugify(instance.title)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source="post", read_only=True)
    class Meta:
        model = Post
        fields = ('id', "post_title", "text", "author")
        read_only_fields = ("create_date", "published_date")

    def to_representation(self, instance):
        data = super(CommentSerializer, self).to_representation(instance)
        return data
