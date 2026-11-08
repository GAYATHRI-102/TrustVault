
from models import db


class DocumentPermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("document.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    can_read = db.Column(db.Boolean, default=False, nullable=False)
    can_edit = db.Column(db.Boolean, default=False, nullable=False)
    user = db.relationship("User")

    __table_args__ = (
        db.UniqueConstraint(
            "document_id",
            "user_id",
            name="unique_document_user_permission"
        ),
    )
    document = db.relationship(
    "Document",
    backref="shared_permissions"
)