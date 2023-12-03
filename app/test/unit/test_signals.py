import pytest

from innotter.models import Follower, Like


@pytest.mark.django_db
class TestPageSignals:
    def test_follow(self, page, user_id):
        Follower.objects.follow_page(page, user_id)
        assert page.followers == 1

    def test_unfollow(self, page, user_id):
        Follower.objects.follow_page(page, user_id)

        Follower.objects.unfollow_page(page, user_id)
        page.refresh_from_db()
        assert page.followers == 0


@pytest.mark.django_db
class TestPostSignals:
    def test_like(self, post, user_id):
        Like.objects.like_post(post, user_id)
        assert post.likes == 1

    def test_remove_like(self, post, user_id):
        Like.objects.like_post(post, user_id)
        Like.objects.remove_like_post(post, user_id)
        post.refresh_from_db()
        assert post.likes == 0
