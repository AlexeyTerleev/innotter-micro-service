from uuid import uuid4

import pytest

from innotter.models import Follower, Like, Page, Post, Tag


@pytest.fixture
def tag():
    return Tag.objects.create(
        name="tag_name",
    )


@pytest.fixture
def page():
    return Page.objects.create(
        name="page_name",
        user_id=uuid4(),
    )


@pytest.fixture
def post(page):
    return Post.objects.create(page=page, content={"content": "content"})


@pytest.fixture
def follower(page):
    return Follower.objects.create(page=page, user_id=uuid4())


@pytest.fixture
def like(post):
    return Like.objects.create(post=post, user_id=uuid4())


@pytest.fixture
def user_id():
    return uuid4()
