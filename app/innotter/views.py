from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from innotter.models import Page, Post, Follower, Tag, Like
from innotter.serializers import PageSerializer, PostSerializer, FollowerSerializer, TagSerializer
from innotter.permissions import JWTAuthentication
from innotter.paginations import CustomPageNumberPagination
from innotter.utils import get_user_info

# TODO permissions and pagination with tags

class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [JWTAuthentication]
    serializer_class = PostSerializer
    
    def get_queryset(self):
        user_id = get_user_info(self.request).get("id")
        following_pages = Follower.objects.filter(user_id=user_id).values_list("page_id", flat=True)
        return Post.objects.filter(page__in=following_pages).order_by("-created_at")
    

class PageViewSet(viewsets.ModelViewSet):
    permission_classes = [JWTAuthentication]

    queryset = Page.objects.all()
    serializer_class = PageSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user_id=get_user_info(self.request).get("id"))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        page = self.paginate_queryset(instance.post_set.all())
        serializer = PostSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    @action(detail=True, methods=["patch"])
    def follow(self, request, pk=None):
        page = self.get_object()
        user_id = get_user_info(self.request).get("id")
        response = None
        if Follower.objects.follow_page(page, user_id):
            response = Response({"message": f"You are now following page {page.id}."})
        else:
            response = Response({"message": f"You are already following page {page.id}."})
        return response

    @action(detail=True, methods=["patch"])
    def unfollow(self, request, pk=None):
        page = self.get_object()
        user_id = get_user_info(self.request).get("id")
        response = None
        if Follower.objects.unfollow_page(page, user_id):
            response = Response({"message": f"You no longer following page {page.id}."})
        else:
            response = Response({"message": f"You are not following page {page.id}."})
        return response
    
    @action(detail=True, methods=["get"])
    def followers(self, request, pk=None):
        page = self.get_object()
        followers = Follower.objects.filter(page=page)
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["patch"])
    def block(self, request, pk=None):
        page = self.get_object()
        page.blocked = True
        page.save()
        return Response({"message": f"Page {pk} has been blocked."})
    

    @action(detail=True, methods=["post"])
    def post(self, request, pk=None):
        page = self.get_object()
        data = request.data.copy()
        data["page"] = page.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    


class PostViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [JWTAuthentication]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=["patch"])
    def like(self, request, pk=None):
        post = self.get_object()
        user_id = get_user_info(self.request).get("id")
        response = None
        if Like.objects.like_post(post, user_id):
            response = Response({"message": f"You like post {post.id}."})
        else:
            response = Response({"message": f"You are already liked post {post.id}."})
        return response
    
    @action(detail=True, methods=["patch"])
    def remove_like(self, request, pk=None):
        post = self.get_object()
        user_id = get_user_info(self.request).get("id")
        response = None
        if Like.objects.remove_like_post(post, user_id):
            response = Response({"message": f"You removed like from post {post.id}."})
        else:
            response = Response({"message": f"You are didn't liked post {post.id}."})
        return response
    

class TagViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [JWTAuthentication]

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [JWTAuthentication]

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPageNumberPagination
