
# AI Development Log – TrustVault

This document records the AI assistance used during TrustVault development. The task descriptions summarize the assistance received and are not necessarily verbatim prompts.

## Entry 1 – 7 November 2026

### Task
Create the initial TrustVault authentication system.

### AI assistance
Used ChatGPT to understand Flask, SQLAlchemy, Flask-Login and password hashing.

### Implementation
- Created the user model.
- Implemented user registration, login and logout.
- Added a protected dashboard.
- Used Werkzeug password hashing.

### Validation
Tested registration, login and logout manually.

### Corrections
Moved environment loading before configuration initialization to ensure the secret key is loaded.

### Commit
Add the actual GitHub commit link after committing.

---

## Entry 2 – 7 November 2026

### Task
Implement document ownership and permission-based sharing.

### AI assistance
Used ChatGPT to understand how to create document permissions and implement separate read and edit access.

### Implementation
- Created the DocumentPermission model.
- Added permission management routes.
- Implemented permission granting and revocation.
- Restricted permission management to document owners.
- Added authorization helper functions.

### Validation
Tested owner access, read-only access, edit access and revoked permissions.

### Corrections
Ensured that edit permission also allows reading, while read-only permission does not allow editing.

### Commit
Add the actual GitHub commit link after committing.

---

## Entry 3 – 7 November 2026

### Task
Secure document operations using server-side authorization.

### AI assistance
Used ChatGPT to understand authorization checks for document downloading, editing and deletion.

### Implementation
- Added document ownership checks.
- Restricted downloading to users with read or edit access.
- Restricted editing to owners and users with edit permission.
- Restricted document deletion to owners.
- Returned HTTP 404 for unauthorized document operations.

### Validation
Created an automated test to verify that a user without permission cannot download, edit or delete another user's document.

### Corrections
Ensured authorization is checked in backend routes rather than relying only on hiding buttons in HTML templates.

### Commit
Add the actual GitHub commit link after committing.

---

## Entry 4 – 8 November 2026

### Task
Implement audit logging and restrict audit-log access.

### AI assistance
Used ChatGPT to understand database-based audit logging and admin-only access restrictions.

### Implementation
- Created the AuditLog model.
- Recorded document-related activities.
- Recorded permission granting and revocation.
- Created an audit-log viewing page.
- Restricted audit-log access to admin users.

### Validation
Verified that audit records are saved in the database and that non-admin users receive HTTP 403 when accessing the audit-log page.

### Corrections
Ensured that ordinary users cannot access the audit-log page by directly entering its URL.

### Commit
Add the actual GitHub commit link after committing.

---

## Entry 5 – 8 November 2026

### Task
Improve document upload security.

### AI assistance
Used ChatGPT to understand file-extension validation, MIME-type detection and upload-size restrictions.

### Implementation
- Added an allowed file-extension list.
- Integrated Python Magic for MIME-type detection.
- Rejected files whose detected content does not match the expected file type.
- Used UUID-based storage filenames.
- Configured a maximum upload size of 10 MB.

### Validation
Created tests to verify that fake PDF files are rejected, genuine PDF files are accepted and oversized uploads receive HTTP 413.

### Corrections
Added content-based file validation instead of relying only on the filename extension.

### Commit
Add the actual GitHub commit link after committing.

---

## Entry 6 – 8 November 2026

### Task
Implement document search and filtering.

### AI assistance
Used ChatGPT to understand how to filter documents using Flask request parameters and SQLAlchemy model data.

### Implementation
Added document filtering by:
- Document name.
- Document owner.
- Document category.
- Upload date.

### Validation
Manually tested document category filtering and verified that the search interface displays matching documents.

### Corrections
Ensured that search results include both owned documents and documents shared with the current user.

### Commit
Add the actual GitHub commit link after committing.

---

## Entry 7 – 8 November 2026

### Task
Create automated tests and security documentation.

### AI assistance
Used ChatGPT to understand pytest, authorization testing, upload-validation testing and threat modelling.

### Implementation
- Created automated tests for authentication pages.
- Tested document authorization rules.
- Tested unauthorized document operations.
- Tested audit-log database storage.
- Tested file-content validation.
- Tested oversized file rejection.
- Created THREATS.md to document security risks, mitigations and remaining limitations.

### Validation
Executed `pytest -v`.

**Latest test result: 11 passed, 0 failed.**

### Corrections
Added a separate oversized-upload test by temporarily lowering the upload limit during the test without changing the actual application limit.

### Commit
Add the actual GitHub commit link after committing.

---

## AI Usage Transparency

ChatGPT was used as a development assistant to explain concepts, suggest implementation approaches, help debug errors, review code and prepare automated tests and documentation.

The application was implemented and tested in the development environment. AI assistance does not replace the need for manual verification, security review or understanding the implementation.

All GitHub commit links should be added after the corresponding changes are actually committed.
