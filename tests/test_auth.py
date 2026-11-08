from app import app
from models import db
from models.user import User


def test_login_page_loads():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/login")
        assert response.status_code == 200


def test_registration_page_loads():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/register")
        assert response.status_code == 200