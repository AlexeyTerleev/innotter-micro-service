import pytest
from rest_framework import status

from innotter.models import Like, Page, Post
from innotter.utils import get_user_info


@pytest.fixture
def setup_data(user_request):
    page = Page.objects.create(name='Test Page', user_id=get_user_info(user_request)["id"])
    post = Post.objects.create(page=page, content={'text': 'Post'})
    return page, post


@pytest.mark.django_db
class TestPostViewSet:
    def test_patch(api_client, user_headers, setup_data):
        page, post = setup_data
        url = f"/post/{post.id}/"
        data = {"content": "{'text': 'new_content'}"}
        response = api_client.patch(url, data=data, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_delete(api_client, user_headers, setup_data):
        page, post = setup_data
        url = f"/post/{post.id}/"
        response = api_client.delete(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_like(api_client, user_headers, setup_data):
        page, post = setup_data
        url = f"/post/{post.id}/like/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK

    def test_remove_like(api_client, user_headers, setup_data):
        page, post = setup_data
        Like.objects.like_post(post=post, user_id=page.user_id)

        url = f"/post/{post.id}/remove_like/"
        response = api_client.patch(url, headers=user_headers)
        assert response.status_code == status.HTTP_200_OK


