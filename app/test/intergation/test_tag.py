import pytest
from rest_framework import status


@pytest.mark.django_db
class TestTagViewSet:
    def test_post(api_client, user_headers, faker):
        url = "/tag/"
        data = {"name": faker.word()}
        response = api_client.post(url, data=data, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_get(api_client, user_headers, setup_tag):
        page, tag = setup_tag
        url = f"/tags/?filter_by_name={tag.name}"
        response = api_client.delete(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK
