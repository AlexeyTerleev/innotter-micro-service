import pytest
from rest_framework import status

from innotter.models import Like, Page, Post, Tag
from innotter.utils import get_user_info


@pytest.fixture
def setup_data(user_request):
    tag = Tag.objects.create(name="tag_name")
    page = Page.objects.create(name='Test Page', tags = [tag], user_id=get_user_info(user_request)["id"])
    return page, tag


@pytest.mark.django_db
class TestTagViewSet:
    def test_post(api_client, user_headers):
        url = "/tag/"
        data = {"name": "tag_name"}
        response = api_client.post(url, data=data, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_get(api_client, user_headers, setup_data):
        page, tag = setup_data
        url = f"/tags/?filter_by_name={tag.name}"
        response = api_client.delete(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK
   