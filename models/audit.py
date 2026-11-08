from datetime import datetime, timezone
from models import db


class AuditLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    actor_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("document.id"),
        nullable=True
    )

    action = db.Column(
        db.String(100),
        nullable=False
    )

    details = db.Column(
        db.String(500)
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )