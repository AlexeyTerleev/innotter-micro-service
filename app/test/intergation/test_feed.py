import pytest
from rest_framework import status

from innotter.serializers import PostSerializer


@pytest.mark.django_db
class TestFeedViewSet:
    def test_get(api_client, user_headers, setup_feed):
        page, post1, post2, follower = setup_feed
        url = "/feed/"
        response = api_client.get(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

        expected_data = PostSerializer([post1, post2], many=True).data
        assert response.data == expected_data
