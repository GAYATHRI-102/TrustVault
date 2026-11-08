
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from models import db
from models.user import User
from models.document import Document
from models.permission import DocumentPermission
from models.audit import AuditLog

permissions = Blueprint("permissions", __name__)


def get_owned_document(document_id):
    document = db.session.get(Document, document_id)

    if document is None or document.owner_id != current_user.id:
        abort(404)

    return document


def record_permission_audit(action, document, recipient):
    log = AuditLog(
        actor_id=current_user.id,
        document_id=document.id,
        action=action,
        details=f"Access permission for {recipient.email}"
    )
    db.session.add(log)


@permissions.route("/documents/<int:document_id>/permissions")
@login_required
def manage_permissions(document_id):
    document = get_owned_document(document_id)

    shared_permissions = DocumentPermission.query.filter_by(
        document_id=document.id
    ).all()

    return render_template(
        "permissions.html",
        document=document,
        shared_permissions=shared_permissions
    )


@permissions.route(
    "/documents/<int:document_id>/permissions/grant",
    methods=["POST"]
)
@login_required
def grant_permission(document_id):
    document = get_owned_document(document_id)

    email = request.form.get("email", "").strip().lower()
    access_type = request.form.get("access_type", "")

    if access_type not in ("read", "edit"):
        flash("Please select valid access permission.")
        return redirect(url_for(
            "permissions.manage_permissions",
            document_id=document.id
        ))

    recipient = User.query.filter_by(email=email).first()

    if recipient is None:
        flash("No registered user found with that email.")
        return redirect(url_for(
            "permissions.manage_permissions",
            document_id=document.id
        ))

    if recipient.id == current_user.id:
        flash("You already own this document.")
        return redirect(url_for(
            "permissions.manage_permissions",
            document_id=document.id
        ))

    permission = DocumentPermission.query.filter_by(
        document_id=document.id,
        user_id=recipient.id
    ).first()

    if permission is None:
        permission = DocumentPermission(
            document_id=document.id,
            user_id=recipient.id
        )
        db.session.add(permission)

    permission.can_read = access_type == "read"
    permission.can_edit = access_type == "edit"

    record_permission_audit(
        "PERMISSION_GRANTED",
        document,
        recipient
    )

    db.session.commit()

    flash(f"{access_type.capitalize()} access granted successfully.")

    return redirect(url_for(
        "permissions.manage_permissions",
        document_id=document.id
    ))


@permissions.route(
    "/documents/<int:document_id>/permissions/<int:permission_id>/revoke",
    methods=["POST"]
)
@login_required
def revoke_permission(document_id, permission_id):
    document = get_owned_document(document_id)

    permission = db.session.get(DocumentPermission, permission_id)

    if permission is None or permission.document_id != document.id:
        abort(404)

    recipient = db.session.get(User, permission.user_id)

    record_permission_audit(
        "PERMISSION_REVOKED",
        document,
        recipient
    )

    db.session.delete(permission)
    db.session.commit()

    flash("Document access revoked successfully.")

    return redirect(url_for(
        "permissions.manage_permissions",
        document_id=document.id
    ))
