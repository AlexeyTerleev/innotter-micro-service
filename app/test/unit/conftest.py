from uuid import uuid4

import pytest

from innotter.models import Follower, Like, Page, Post, Tag


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def tag(faker):
    return Tag.objects.create(
        name=faker.word(),
    )


@pytest.fixture
def page(faker):
    return Page.objects.create(
        name=faker.word(),
        user_id=uuid4(),
    )


@pytest.fixture
def post(page, faker):
    return Post.objects.create(page=page, content=faker.json())


@pytest.fixture
def follower(page, user_id):
    return Follower.objects.create(page=page, user_id=user_id)


@pytest.fixture
def like(post, user_id):
    return Like.objects.create(post=post, user_id=user_id)
