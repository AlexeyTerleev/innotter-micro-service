from rest_framework import serializers

from innotter.models import Page, Post


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = [
            'id', 'name', 'description', 'user_id', 
            'tags', 'followers', 'created_at', 'modified_at'
        ]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'page', 'content', 'reply_to_post_id', 
            'likes', 'created_at', 'modified_at'
        ]