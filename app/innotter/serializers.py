from rest_framework import serializers

from innotter.models import Page, Post, Tag, Follower


class PageSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Page
        fields = [
            'id', 'name', 'description', 
            'tags', 'followers', 'created_at', 'modified_at'
        ]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'page', 'content', 'reply_to_post_id', 
            'likes', 'created_at', 'modified_at'
        ]


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = [
            'user_id',
        ]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id', 'name',
        ]