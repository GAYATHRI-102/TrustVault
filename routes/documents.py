import os
import uuid
import magic

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, current_app, abort, send_file
)

from models.permission import DocumentPermission
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import db
from models.document import Document
from models.audit import AuditLog
from security.authorization import can_read_document, can_edit_document


documents = Blueprint("documents", __name__)

ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "txt", "png", "jpg", "jpeg"
}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def validate_file_content(file):
    file.seek(0)

    mime_type = magic.from_buffer(
        file.read(2048),
        mime=True
    )

    file.seek(0)

    allowed_mime_types = {
        "pdf": ["application/pdf"],
        "doc": ["application/msword"],
        "docx": [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ],
        "txt": ["text/plain"],
        "png": ["image/png"],
        "jpg": ["image/jpeg"],
        "jpeg": ["image/jpeg"]
    }

    extension = file.filename.rsplit(".", 1)[1].lower()

    return mime_type in allowed_mime_types.get(extension, [])

def record_audit(action, document_id, details):
    log = AuditLog(
        actor_id=current_user.id,
        document_id=document_id,
        action=action,
        details=details
    )

    db.session.add(log)




@documents.route("/documents")
@login_required
def document_list():

    # Get documents owned by the current user.
    owned_documents = Document.query.filter_by(
        owner_id=current_user.id
    ).all()

    # Get documents shared with the current user.
    shared_permissions = DocumentPermission.query.filter_by(
        user_id=current_user.id
    ).all()

    shared_documents = []

    for permission in shared_permissions:
        document = db.session.get(
            Document,
            permission.document_id
        )

        if document and can_read_document(current_user, document):
            shared_documents.append(document)

    # Combine documents without duplicates.
    all_documents = {
        document.id: document
        for document in owned_documents + shared_documents
    }

    user_documents = list(all_documents.values())

    # Get search values from the URL.
    search_name = request.args.get("name", "").strip().lower()
    search_owner = request.args.get("owner", "").strip().lower()
    search_category = request.args.get("category", "").strip().lower()
    search_date = request.args.get("date", "").strip()

    # Filter documents.
    filtered_documents = []

    for document in user_documents:

        if search_name and search_name not in document.original_name.lower():
            continue

        if search_owner and search_owner not in document.owner.name.lower():
            continue

        if search_category and search_category not in document.category.lower():
            continue

        if search_date:
            document_date = document.created_at.strftime("%Y-%m-%d")

            if document_date != search_date:
                continue

        filtered_documents.append(document)

    return render_template(
        "documents.html",
        documents=filtered_documents,
        search_name=search_name,
        search_owner=search_owner,
        search_category=search_category,
        search_date=search_date
    )


@documents.route("/documents/upload", methods=["GET", "POST"])
@login_required
def upload_document():

    if request.method == "POST":

        uploaded_file = request.files.get("file")
        category = request.form.get("category", "General").strip()

        if not uploaded_file or not uploaded_file.filename:
            flash("Please select a document.")
            return redirect(url_for("documents.upload_document"))

        safe_name = secure_filename(uploaded_file.filename)

        if not safe_name or not allowed_file(safe_name):
            flash("This file type is not allowed.")
            return redirect(url_for("documents.upload_document"))

        if not validate_file_content(uploaded_file):
            flash("File content does not match the allowed file type.")
            return redirect(url_for("documents.upload_document"))

        storage_name = uuid.uuid4().hex

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        document = Document(
            original_name=safe_name,
            storage_name=storage_name,
            category=category or "General",
            owner_id=current_user.id
        )

        try:
            uploaded_file.save(
                os.path.join(upload_folder, storage_name)
            )

            db.session.add(document)
            db.session.flush()

            record_audit(
                "DOCUMENT_UPLOADED",
                document.id,
                "Document uploaded successfully"
            )

            db.session.commit()

        except Exception:
            db.session.rollback()

            stored_path = os.path.join(upload_folder, storage_name)

            if os.path.exists(stored_path):
                os.remove(stored_path)

            current_app.logger.exception("Document upload failed")
            flash("Upload failed. Please try again.")
            return redirect(url_for("documents.upload_document"))

        flash("Document uploaded successfully.")
        return redirect(url_for("documents.document_list"))

    return render_template("upload.html")



@documents.route("/documents/download/<int:document_id>")
@login_required
def download_document(document_id):
    document = db.session.get(Document, document_id)

    if document is None or not can_read_document(current_user, document):
        abort(404)

    file_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        document.storage_name
    )

    if not os.path.isfile(file_path):
        abort(404)

    record_audit(
        "DOCUMENT_DOWNLOADED",
        document.id,
        "Document downloaded"
    )
    db.session.commit()

    return send_file(
        file_path,
        as_attachment=True,
        download_name=document.original_name
    )

@documents.route(
    "/documents/edit/<int:document_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_document(document_id):

    document = db.session.get(Document, document_id)

    if document is None or not can_edit_document(
        current_user,
        document
    ):
        abort(404)

    if request.method == "POST":

        category = request.form.get(
            "category",
            ""
        ).strip()

        if not category:
            flash("Category cannot be empty.")
            return redirect(url_for(
                "documents.edit_document",
                document_id=document.id
            ))

        document.category = category

        record_audit(
            "DOCUMENT_CATEGORY_UPDATED",
            document.id,
            "Document category updated"
        )

        db.session.commit()

        flash("Document category updated successfully.")

        return redirect(
            url_for("documents.document_list")
        )

    return render_template(
        "edit_document.html",
        document=document
    )

@documents.route("/documents/delete/<int:document_id>", methods=["POST"])
@login_required
def delete_document(document_id):
    document = db.session.get(Document, document_id)

    # Only the document owner can delete it.
    if document is None or document.owner_id != current_user.id:
        abort(404)

    file_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        document.storage_name
    )

    record_audit(
        "DOCUMENT_DELETED",
        document.id,
        "Document deleted by owner"
    )

    db.session.delete(document)
    db.session.commit()

    if os.path.isfile(file_path):
        os.remove(file_path)

    flash("Document deleted successfully.")

    return redirect(url_for("documents.document_list"))
