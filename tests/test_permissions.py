
from app import app
from types import SimpleNamespace
from unittest.mock import patch

from security.authorization import can_read_document, can_edit_document


def create_user(user_id):
    return SimpleNamespace(id=user_id)


def create_document(owner_id=1):
    return SimpleNamespace(id=100, owner_id=owner_id)


def test_owner_can_read_and_edit():
    with app.app_context():
        owner = create_user(1)
        document = create_document(1)

        assert can_read_document(owner, document) is True
        assert can_edit_document(owner, document) is True


def test_read_permission_cannot_edit():
    with app.app_context():
        user = create_user(2)
        document = create_document()

        permission = SimpleNamespace(
            can_read=True,
            can_edit=False
        )

        with patch("security.authorization.DocumentPermission.query") as mock_query:
            mock_query.filter_by.return_value.first.return_value = permission

            assert can_read_document(user, document) is True
            assert can_edit_document(user, document) is False


def test_edit_permission_allows_read_and_edit():
    with app.app_context():
        user = create_user(2)
        document = create_document()

        permission = SimpleNamespace(
            can_read=False,
            can_edit=True
        )

        with patch("security.authorization.DocumentPermission.query") as mock_query:
            mock_query.filter_by.return_value.first.return_value = permission

            assert can_read_document(user, document) is True
            assert can_edit_document(user, document) is True


def test_revoked_permission_blocks_access():
    with app.app_context():
        user = create_user(2)
        document = create_document()

        with patch("security.authorization.DocumentPermission.query") as mock_query:
            mock_query.filter_by.return_value.first.return_value = None

            assert can_read_document(user, document) is False
            assert can_edit_document(user, document) is False
