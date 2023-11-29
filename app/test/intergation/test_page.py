import pytest
from rest_framework import status

from innotter.models import Follower, Page
from innotter.utils import get_user_info


@pytest.fixture
def setup_data(user_request):
    page = Page.objects.create(name='Test Page', user_id=get_user_info(user_request)["id"])
    return page


@pytest.mark.django_db
class TestPageViewSet:
    def test_post(api_client, user_headers):
        url = "/page/"
        data = {"name": "Test Page"}
        response = api_client.get(url, data=data, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_delete(api_client, user_headers, setup_data):
        url = f"/page/{setup_data.id}"
        response = api_client.delete(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_get(api_client, user_headers, setup_data):
        url = f"/page/{setup_data.id}"
        response = api_client.get(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_patch(api_client, user_headers, setup_data):
        url = f"/page/{setup_data.id}"
        data = {"description": "description"}
        response = api_client.patch(url, data=data, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_follow(api_client, user_headers, setup_data):
        url = f"/page/{setup_data.id}/follow/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_unfollow(api_client, user_headers, setup_data):
        Follower.objects.follow_page(page=setup_data, user_id=setup_data.user_id)

        url = f"/page/{setup_data.id}/unfollow/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_followers(api_client, user_headers, setup_data):
        url = f"/page/{setup_data.id}/followers/"
        response = api_client.get(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK
    
    def test_block(api_client, admin_headers, setup_data):
        url = f"/page/{setup_data.id}/block/"
        response = api_client.patch(url, headers=admin_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_post_create(api_client, user_headers, setup_data):
        url = f"/page/{setup_data.id}/post/"
        data = {"content": "{'text': 'Post'}"}
        response = api_client.post(url, data=data, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK