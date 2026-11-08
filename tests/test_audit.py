
from app import app
from models import db
from models.audit import AuditLog


def test_audit_log_is_saved_in_database():
    with app.app_context():
        log = AuditLog(
            actor_id=None,
            document_id=None,
            action="TEST_AUDIT",
            details="Testing audit database storage"
        )

        try:
            db.session.add(log)
            db.session.flush()

            saved_log = db.session.get(AuditLog, log.id)

            assert saved_log is not None
            assert saved_log.action == "TEST_AUDIT"
            assert saved_log.details == "Testing audit database storage"

        finally:
            db.session.rollback()
