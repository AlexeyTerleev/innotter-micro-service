from datetime import date, timedelta

import pytest

from innotter.tasks import unblock_pages


@pytest.mark.django_db
class TestTasks:
    def test_unblock_page(self, page):
        page.blocked = True
        page.unblock_date = date.today()
        page.save()

        unblock_pages()
        page.refresh_from_db()

        assert page.blocked is False
        assert page.unblock_date is None

    def test_dont_unblock_page(self, page):
        page.blocked = True
        page.unblock_date = date.today() + timedelta(days=1)
        page.save()

        unblock_pages()
        page.refresh_from_db()

        assert page.blocked is True
        assert page.unblock_date == date.today() + timedelta(days=1)
