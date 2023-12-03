from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from innotter.models import Follower, Page, Post, Tag
from innotter.utils import get_user_info


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def setup_feed(user_request, faker):
    page = Page.objects.create(name=faker.word(), user_id=uuid4())
    post1 = Post.objects.create(page=page, content=faker.json())
    post2 = Post.objects.create(page=page, content=faker.json())
    follower = Follower.objects.create(
        page=page, user_id=get_user_info(user_request)["id"]
    )
    return page, post1, post2, follower


@pytest.fixture
def setup_page(user_request, faker):
    page = Page.objects.create(
        name=faker.word(), user_id=get_user_info(user_request)["id"]
    )
    return page


@pytest.fixture
def setup_post(user_request):
    page = Page.objects.create(
        name="Test Page", user_id=get_user_info(user_request)["id"]
    )
    post = Post.objects.create(page=page, content={"text": "Post"})
    return page, post


@pytest.fixture
def setup_tag(user_request, faker):
    tag = Tag.objects.create(name=faker.word())
    page = Page.objects.create(
        name=faker.word(), user_id=get_user_info(user_request)["id"]
    )
    page.tags.add(tag)
    return page, tag
