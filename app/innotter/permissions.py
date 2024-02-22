import os
from uuid import UUID

import jwt
import requests
from jwt.exceptions import InvalidTokenError
from rest_framework.permissions import BasePermission

from innotter.models import Page, Post
from innotter.utils import get_user_info


class JWTAuthentication(BasePermission):
    def has_access(self, request, view):
        return True

    def get_page(self, request, view):
        view_type = view.__class__.__name__
        if view_type == "PageViewSet":
            page_id = view.kwargs.get("pk")
            return Page.objects.filter(id=page_id).first()
        elif view_type == "PostViewSet":
            post_id = view.kwargs.get("pk")
            post = Post.objects.filter(id=post_id).first()
            if post:
                return post.page
        return None

    def has_permission(self, request, view):
        try:
            token = request.headers.get("Authorization", "").replace("Bearer ", "")
            decoded = jwt.decode(token, "JWT_SECRET_KEY", algorithms=["HS256"])
            access = self.has_access(request, view)
        except (InvalidTokenError, jwt.ExpiredSignatureError) as e:
            print(e)
            access = False
        return access


class IsAdmin(JWTAuthentication):
    def has_access(self, request, view):
        page = self.get_page(request, view)
        if not page:
            return False
        user = get_user_info(request)
        return admin(user)


class IsModeratorOfPageOwnerGroup(JWTAuthentication):
    def has_access(self, request, view):
        page = self.get_page(request, view)
        bearer = request.headers.get("Authorization", "")
        if not page:
            return False
        user = get_user_info(request)
        return moderator_of_page_owner_group(user, page, bearer)


class IsPageOwner(JWTAuthentication):
    def has_access(self, request, view):
        page = self.get_page(request, view)
        if not page:
            return False
        user = get_user_info(request)
        return page_owner(user, page)


def admin(user) -> bool:
    return user["role"] == "Role.admin"


def page_owner(user, page) -> bool:
    return UUID(user["id"]) == page.user_id


def moderator_of_page_owner_group(user, page, user_bearer) -> bool:
    return user["role"] == "Role.moderator" and page_owner_belongs_to_moderator_group(
        page, user_bearer
    )


def page_owner_belongs_to_moderator_group(page, moderator_bearer) -> bool:
    url = os.environ.get("USERS_URL", "")
    response = requests.get(
        url,
        headers={"Content-Type": "application/json", "Authorization": moderator_bearer},
    )
    response_users_ids = [UUID(user["id"]) for user in response.json()]
    return page.user_id in response_users_ids
