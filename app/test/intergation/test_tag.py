import pytest
import json
from rest_framework import status


@pytest.mark.django_db
class TestTagViewSet:
    def test_post(self, api_client, user_headers, faker):
        url = "/tag/"
        data = {"name": faker.word()}
        response = api_client.post(url, data=json.dumps(data), content_type="application/json", headers=user_headers)
        assert response.status_code == status.HTTP_201_CREATED

    def test_get(self, api_client, user_headers, setup_tag):
        page, tag = setup_tag
        url = f"/tags/?filter_by_name={tag.name}/"
        response = api_client.get(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK
