from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.audit import AuditLog

admin = Blueprint("admin", __name__)

@admin.route("/admin/audit-logs")
@login_required
def audit_logs():

    # Only admin users can view audit logs
    if current_user.role != "admin":
        return "Access Denied", 403

    logs = AuditLog.query.order_by(
        AuditLog.timestamp.desc()
    ).all()

    return render_template(
        "audit_logs.html",
        logs=logs
    )