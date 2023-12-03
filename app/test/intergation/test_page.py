import pytest
import json
from rest_framework import status

from innotter.models import Follower


@pytest.mark.django_db
class TestPageViewSet:
    def test_post(self, api_client, user_headers, faker):
        url = "/page/"
        data = {"name": faker.word()}
        response = api_client.get(url, data=data, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, api_client, user_headers, setup_page):
        url = f"/page/{setup_page.id}/"
        response = api_client.delete(url, headers=user_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get(self, api_client, user_headers, setup_page):
        url = f"/page/{setup_page.id}/"
        response = api_client.get(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_patch(self, api_client, user_headers, setup_page, faker):
        url = f"/page/{setup_page.id}/"
        data = {"description": faker.text()[:100]}
        response = api_client.patch(url, data=json.dumps(data), content_type="application/json", headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_follow(self, api_client, user_headers, setup_page):
        url = f"/page/{setup_page.id}/follow/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_unfollow(self, api_client, user_headers, setup_page):
        Follower.objects.follow_page(page=setup_page, user_id=setup_page.user_id)

        url = f"/page/{setup_page.id}/unfollow/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_followers(self, api_client, user_headers, setup_page):
        url = f"/page/{setup_page.id}/followers/"
        response = api_client.get(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_block(self, api_client, admin_headers, setup_page):
        url = f"/page/{setup_page.id}/block/"
        response = api_client.patch(url, headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_post_create(self, api_client, user_headers, setup_page, faker):
        url = f"/page/{setup_page.id}/post/"
        data = {"content": faker.json()}
        response = api_client.post(url, data=json.dumps(data), content_type="application/json", headers=user_headers)
        assert response.status_code == status.HTTP_201_CREATED
