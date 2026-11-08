
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, login_required, current_user
from flask_wtf.csrf import CSRFProtect

from config import Config
from models import db
from models.user import User
from models.document import Document
from models.audit import AuditLog
from models.permission import DocumentPermission

from routes.auth import auth
from routes.documents import documents
from routes.permissions import permissions
from routes.admin import admin


app = Flask(__name__)

# Load application configuration
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Enable CSRF protection
csrf = CSRFProtect(app)

# Configure Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Register application blueprints
app.register_blueprint(auth)
app.register_blueprint(documents)
app.register_blueprint(permissions)
app.register_blueprint(admin)


# Home page
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    return redirect(url_for("auth.login"))


# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# Create database tables
with app.app_context():
    db.create_all()


# Run application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
