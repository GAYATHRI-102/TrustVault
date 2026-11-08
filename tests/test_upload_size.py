
from io import BytesIO
import uuid

from app import app
from models import db
from models.user import User


def test_oversized_upload_is_rejected(tmp_path, monkeypatch):

    monkeypatch.setitem(app.config, "TESTING", True)
    monkeypatch.setitem(app.config, "WTF_CSRF_ENABLED", False)
    monkeypatch.setitem(app.config, "MAX_CONTENT_LENGTH", 10)
    monkeypatch.setitem(app.config, "UPLOAD_FOLDER", str(tmp_path))

    with app.app_context():

        unique_id = uuid.uuid4().hex

        user = User(
            name="Upload Tester",
            email=f"upload_{unique_id}@test.com",
            role="viewer"
        )
        user.set_password("TestPassword123")

        db.session.add(user)
        db.session.commit()

        user_id = user.id

        try:
            with app.test_client() as client:

                with client.session_transaction() as session:
                    session["_user_id"] = str(user_id)
                    session["_fresh"] = True

                response = client.post(
                    "/documents/upload",
                    data={
                        "file": (
                            BytesIO(b"This file is too large"),
                            "large.txt"
                        ),
                        "category": "Testing"
                    }
                )

                assert response.status_code == 413

        finally:
            db.session.delete(db.session.get(User, user_id))
            db.session.commit()
