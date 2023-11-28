from uuid import UUID

import pytest

from innotter.models import Page
from innotter.permissions import (
    IsAdmin,
    IsModeratorOfPageOwnerGroup,
    IsPageOwner,
    JWTAuthentication,
)
from innotter.utils import get_user_info


@pytest.mark.django_db
class TestPermissions:
    def test_jwt_auth(self, mocker, admin_request, moderator_request, user_request):
        view = mocker.Mock()

        assert JWTAuthentication().has_permission(admin_request, view) is True
        assert JWTAuthentication().has_permission(moderator_request, view) is True
        assert JWTAuthentication().has_permission(user_request, view) is True

    def test_is_admin(self, mocker, admin_request, user_request, page):
        view = mocker.Mock()
        mocker.patch(
            f"innotter.permissions.JWTAuthentication.get_page", return_value=page
        )

        assert IsAdmin().has_permission(admin_request, view) is True
        assert IsAdmin().has_permission(user_request, view) is False

    def test_is_moderator_of_page_owner_group(
        self, mocker, admin_request, moderator_request, user_request
    ):
        page = Page.objects.create(
            name="page_name",
            user_id=UUID(get_user_info(user_request)["id"]),
        )
        view = mocker.Mock()
        mocker.patch(
            f"innotter.permissions.JWTAuthentication.get_page", return_value=page
        )
        mocker.patch(
            f"innotter.permissions.page_owner_belongs_to_moderator_group",
            return_value=True,
        )

        assert (
            IsModeratorOfPageOwnerGroup().has_permission(moderator_request, view)
            is True
        )
        assert (
            IsModeratorOfPageOwnerGroup().has_permission(admin_request, view) is False
        )
        assert IsModeratorOfPageOwnerGroup().has_permission(user_request, view) is False

    def test_is_page_owner(
        self, mocker, admin_request, moderator_request, user_request
    ):
        page = Page.objects.create(
            name="page_name",
            user_id=UUID(get_user_info(user_request)["id"]),
        )
        view = mocker.Mock()
        mocker.patch(
            f"innotter.permissions.JWTAuthentication.get_page", return_value=page
        )

        assert IsPageOwner().has_permission(user_request, view) is True
        assert IsPageOwner().has_permission(admin_request, view) is False
        assert IsPageOwner().has_permission(moderator_request, view) is False
