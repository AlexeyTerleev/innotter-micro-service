import pytest
from uuid import uuid4
from django.urls import reverse
from rest_framework import status

from innotter.models import Follower, Post, Page
from innotter.serializers import PostSerializer
from innotter.utils import get_user_info


@pytest.fixture
def setup_data(user_request):
    page = Page.objects.create(name='Test Page', user_id=uuid4())
    post1 = Post.objects.create(page=page, content={'text': 'Post 1'})
    post2 = Post.objects.create(page=page, content={'text': 'Post 2'})
    follower = Follower.objects.create(page=page, user_id=get_user_info(user_request)["id"])
    return page, post1, post2, follower


@pytest.mark.django_db
class TestFeedViewSet:
    def test_get(api_client, user_headers):
        page, post1, post2, follower = setup_data
        url = "/feed/"
        response = api_client.get(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

        expected_data = PostSerializer([post1, post2], many=True).data
        assert response.data == expected_data