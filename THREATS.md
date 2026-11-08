
# TrustVault – Threat Model and Security Analysis

## 1. Project Overview

TrustVault is a Flask-based secure document-sharing application. Users can upload documents, download documents they are authorized to access, edit document categories, and share documents with other registered users.

The application uses Flask, Flask-Login, Flask-SQLAlchemy, SQLite, Flask-WTF, and Python Magic for file-type validation.

## 2. Assets to Protect

The important assets in TrustVault are:

- User account details and password hashes.
- Uploaded documents and their contents.
- Document ownership information.
- Read and edit permissions.
- Audit logs containing user activities.
- Application secret key and session information.

## 3. Security Threats and Mitigations

### Threat 1: Unauthorized Document Access

**Risk:** A user may attempt to access another user's private documents by changing document IDs in the URL.

**Mitigation:**
- Document ownership is checked before allowing owner-only actions.
- Read and edit permissions are checked on the server.
- Users without permission receive an HTTP 404 response when attempting unauthorized document access.
- Document IDs alone do not grant access.

### Threat 2: Unauthorized Document Modification

**Risk:** A user with read-only access may attempt to edit or delete a document.

**Mitigation:**
- The `can_edit_document()` function checks whether the user owns the document or has edit permission.
- Read permission does not grant edit permission.
- Document deletion is restricted to the document owner.
- Authorization checks are performed in the backend routes, not just in the user interface.

### Threat 3: Password Theft

**Risk:** Storing passwords as plain text could expose user credentials if the database is compromised.

**Mitigation:**
- Passwords are stored as hashes using Werkzeug's password hashing functions.
- Password verification uses `check_password_hash()`.
- Passwords are not stored directly in the database.

### Threat 4: Malicious File Uploads

**Risk:** An attacker may upload a file with a misleading extension, such as an executable file renamed to `.pdf`.

**Mitigation:**
- The application allows only selected file extensions.
- Uploaded file content is checked using Python Magic MIME detection.
- Files whose detected MIME type does not match their extension are rejected.
- Uploaded files are stored using generated unique filenames instead of their original filenames.

**Remaining risk:** MIME detection is not a complete malware scanner. Malicious files may still require additional scanning.

### Threat 5: Oversized File Uploads

**Risk:** An attacker may upload extremely large files to consume server storage or resources.

**Mitigation:**
- Flask's `MAX_CONTENT_LENGTH` setting limits requests to 10 MB.
- Oversized upload requests are rejected with HTTP 413.
- A test verifies that oversized uploads are rejected.

### Threat 6: Cross-Site Request Forgery (CSRF)

**Risk:** An attacker may trick an authenticated user into submitting an unwanted action.

**Mitigation:**
- Flask-WTF CSRF protection is enabled.
- Forms that perform actions include CSRF tokens.
- Logout uses a POST request rather than a GET request.

### Threat 7: Unauthorized Permission Changes

**Risk:** A user may attempt to grant or revoke document permissions without being the document owner.

**Mitigation:**
- Permission management routes verify document ownership.
- Only document owners can grant or revoke access.
- Permission records are associated with a specific document and user.
- A unique database constraint prevents duplicate permission records for the same document and user.

### Threat 8: Audit Log Unauthorized Access

**Risk:** An unauthorized user may attempt to view activity records containing information about document operations.

**Mitigation:**
- Audit logs are available only to users with the admin role.
- Non-admin users receive HTTP 403 when accessing the audit-log page.
- The application records activities such as document uploads, downloads, edits, deletions, and permission changes.

**Remaining risk:** Audit logs are stored in the application database and are not protected against direct database modification by someone with database access.

### Threat 9: Session Theft

**Risk:** An attacker may try to steal or misuse an authenticated user's session.

**Mitigation:**
- Flask-Login manages authenticated sessions.
- Session cookies use the HttpOnly flag.
- SameSite is configured as Lax.
- The application secret key is loaded from an environment variable rather than committed to source control.
- The `.env` file is excluded using `.gitignore`.

**Remaining risk:** Secure cookie configuration over HTTPS must also be enabled for production deployment.

### Threat 10: Database Injection

**Risk:** An attacker may attempt to manipulate database queries through malicious input.

**Mitigation:**
- Flask-SQLAlchemy ORM is used for database operations.
- User input is handled through ORM filters rather than manually concatenated SQL queries.

## 4. Security Testing

The following automated tests have been implemented:

| Test | Expected result |
|---|---|
| Login page loads | HTTP 200 |
| Registration page loads | HTTP 200 |
| Document owner can read and edit | Allowed |
| Read permission cannot edit | Edit denied |
| Edit permission allows reading | Allowed |
| Revoked permission blocks access | Denied |
| Unauthorized download, edit and delete | HTTP 404 |
| Audit log is saved | Record exists |
| Fake PDF upload | Rejected |
| Genuine PDF upload | Accepted |
| Oversized upload | HTTP 413 |

All 11 automated tests passed during the latest test run.

## 5. Remaining Security Improvements

The following improvements should be considered before production deployment:

- Enable secure session cookies when running over HTTPS.
- Use a strong production secret key.
- Add rate limiting to login and registration endpoints.
- Consider malware scanning for uploaded files.
- Use persistent and appropriately secured database and file storage.
- Restrict direct access to uploaded files.
- Consider stronger protection against direct modification or deletion of audit records.
- Add regular database backups and appropriate retention policies.

## 6. Conclusion

TrustVault implements server-side authorization, password hashing, file validation, upload-size restrictions, CSRF protection, and activity logging.

Automated tests verify important access-control and upload-validation behavior. However, these tests do not prove that the application is completely secure. Additional security testing, production configuration, and deployment hardening are necessary before handling sensitive real-world documents.
