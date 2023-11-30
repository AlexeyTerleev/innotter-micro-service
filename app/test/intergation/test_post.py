import pytest
import json
from rest_framework import status

from innotter.models import Like


@pytest.mark.django_db
class TestPostViewSet:
    def test_patch(self, api_client, user_headers, setup_post, faker):
        page, post = setup_post
        url = f"/post/{post.id}/"
        data = {"content": faker.json()}
        response = api_client.patch(url, data=json.dumps(data), content_type="application/json", headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, api_client, user_headers, setup_post):
        page, post = setup_post
        url = f"/post/{post.id}/"
        response = api_client.delete(url, headers=user_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_like(self, api_client, user_headers, setup_post):
        page, post = setup_post
        url = f"/post/{post.id}/like/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_remove_like(self, api_client, user_headers, setup_post):
        page, post = setup_post
        Like.objects.like_post(post=post, user_id=page.user_id)

        url = f"/post/{post.id}/remove_like/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK
