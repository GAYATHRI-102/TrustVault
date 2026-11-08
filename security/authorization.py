
from models.permission import DocumentPermission


def can_read_document(user, document):
    # The document owner always has access.
    if document.owner_id == user.id:
        return True

    # Check whether the user has explicit read or edit permission.
    permission = DocumentPermission.query.filter_by(
        document_id=document.id,
        user_id=user.id
    ).first()

    if permission and (permission.can_read or permission.can_edit):
        return True

    return False


def can_edit_document(user, document):
    # Only the owner or a user with explicit edit permission.
    if document.owner_id == user.id:
        return True

    permission = DocumentPermission.query.filter_by(
        document_id=document.id,
        user_id=user.id
    ).first()

    return bool(permission and permission.can_edit)
