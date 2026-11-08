from datetime import datetime, timezone
from models import db


class Document(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    original_name = db.Column(
        db.String(255),
        nullable=False
    )

    storage_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False,
        default="General"
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    owner = db.relationship(
        "User",
        backref="documents"
    )