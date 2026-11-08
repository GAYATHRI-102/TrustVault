import uuid

from app import app
from models import db
from models.user import User
from models.document import Document


def test_user_without_permission_cannot_download_edit_or_delete(tmp_path):
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["UPLOAD_FOLDER"] = str(tmp_path)

    with app.app_context():
        unique_id = uuid.uuid4().hex

        owner = User(
            name="Document Owner",
            email=f"owner_{unique_id}@test.com",
            role="viewer"
        )
        owner.set_password("OwnerPassword123")

        viewer = User(
            name="Unauthorized Viewer",
            email=f"viewer_{unique_id}@test.com",
            role="viewer"
        )
        viewer.set_password("ViewerPassword123")

        db.session.add_all([owner, viewer])
        db.session.flush()

        document = Document(
            original_name="private_test.txt",
            storage_name=f"{unique_id}.txt",
            category="Testing",
            owner_id=owner.id
        )

        db.session.add(document)
        db.session.commit()

        document_id = document.id
        storage_name = document.storage_name
        document_path = tmp_path / storage_name
        document_path.write_text("Private test document")

        try:
            with app.test_client() as client:

                # Log in as the user who has no permission.
                with client.session_transaction() as session:
                    session["_user_id"] = str(viewer.id)
                    session["_fresh"] = True

                # Attempt to download the private document.
                download_response = client.get(
                    f"/documents/download/{document_id}"
                )

                # Attempt to edit the private document.
                edit_response = client.get(
                    f"/documents/edit/{document_id}"
                )

                # Attempt to delete the private document.
                delete_response = client.post(
                    f"/documents/delete/{document_id}"
                )

                assert download_response.status_code == 404
                assert edit_response.status_code == 404
                assert delete_response.status_code == 404

            # Confirm the document still exists.
            assert db.session.get(Document, document_id) is not None
            assert document_path.exists()

        finally:
            db.session.delete(
                db.session.get(Document, document_id)
            )
            db.session.delete(
                db.session.get(User, viewer.id)
            )
            db.session.delete(
                db.session.get(User, owner.id)
            )
            db.session.commit()