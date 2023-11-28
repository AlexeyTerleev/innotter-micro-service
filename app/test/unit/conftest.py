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


@pytest.fixture
def admin_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE3NzUwODksInN1YiI6eyJpZCI6ImI3MzVhMjA2LTQ1YzMtNDE0ZS04MzBlLTNjMzgwNDhiYjI4MSIsImdyb3VwX2lkIjoiNmM4OGRkMzctMWIxNS00M2ViLWJkNWItNzAzNjI0M2ZmZTY0Iiwicm9sZSI6IlJvbGUuYWRtaW4ifX0.zt2c6G_lqkU_Tcl_WABwP41_1GzNf4E5ooRZ0lH6A1M"


@pytest.fixture
def moderator_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE3NzUxMTgsInN1YiI6eyJpZCI6ImM3ZTI0NGYyLWJhZTktNGRiOC1hNzk2LWYwOTM2NzliZTQ2NyIsImdyb3VwX2lkIjoiODEwZTg4N2QtNDhmZC00NDNiLWIxMTYtNmM0NzFmMzc0MTc4Iiwicm9sZSI6IlJvbGUubW9kZXJhdG9yIn19.dyk4F2ke_Bw-XbvOMm_39-RU7cOhL00i84uHevlYuWE"


@pytest.fixture
def user_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE3NzUxNTUsInN1YiI6eyJpZCI6ImRiMDQ3OGRjLWY2MzYtNDJmNS05ZjkxLTlhNzljODI3NzQ4NiIsImdyb3VwX2lkIjoiODEwZTg4N2QtNDhmZC00NDNiLWIxMTYtNmM0NzFmMzc0MTc4Iiwicm9sZSI6IlJvbGUudXNlciJ9fQ.YJEyYMRAH31z5hGdloZDui8xumkYBfHWDPdoCXryjFw"


@pytest.fixture
def admin_request(mocker, admin_token):
    return mocker.Mock(headers={"Authorization": f"Bearer {admin_token}"})


@pytest.fixture
def moderator_request(mocker, moderator_token):
    return mocker.Mock(headers={"Authorization": f"Bearer {moderator_token}"})


@pytest.fixture
def user_request(mocker, user_token):
    return mocker.Mock(headers={"Authorization": f"Bearer {user_token}"})
