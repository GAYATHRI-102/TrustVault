from dotenv import load_dotenv
load_dotenv()
from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

from config import Config
from models import db
from models.user import User
from routes.auth import auth

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


app.register_blueprint(auth)


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    return redirect(url_for("auth.login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)