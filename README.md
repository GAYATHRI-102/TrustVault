
# TrustVault – Secure Document Sharing System

## 1. Project Overview

TrustVault is a secure document management and sharing web application developed using Python Flask.

It allows registered users to upload and manage documents, share documents with other registered users, and control access through read and edit permissions.

The application includes authentication, server-side authorization, file validation, audit logging and document search.

## 2. Features

- User registration and login.
- Secure password hashing.
- Protected dashboard.
- Document upload and download.
- Document ownership management.
- Read-only and edit permissions.
- Granting and revoking document access.
- Owner-only document deletion.
- Document category editing.
- Search documents by name, owner, category and upload date.
- Audit logging of document activities.
- Admin-restricted audit-log viewing.
- File-extension and MIME-type validation.
- Maximum upload size of 10 MB.
- CSRF protection.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Flask-SQLAlchemy | Database integration |
| SQLite | Database |
| Flask-Login | User authentication |
| Flask-WTF | CSRF protection |
| Werkzeug | Password hashing and secure filenames |
| Python Magic | File content detection |
| HTML/CSS | Frontend |
| Bootstrap | User interface styling |
| Pytest | Automated testing |

## 4. Project Structure

```text
TrustVault/
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── document.py
│   ├── audit.py
│   └── permission.py
├── routes/
│   ├── auth.py
│   ├── documents.py
│   ├── permissions.py
│   └── admin.py
├── security/
│   └── authorization.py
├── templates/
├── tests/
├── instance/
└── THREATS.md
```

## 5. Installation and Setup

### Prerequisites

- Python 3.10 or later.
- pip.
- Git.

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TrustVault
```

Replace the placeholder with the actual repository URL.

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

On Linux systems, Python Magic may also require the `libmagic` system library.

### Step 3: Configure environment variables

Create a `.env` file in the project root directory.

Add:

```text
SECRET_KEY=replace-with-a-strong-random-secret
```

Do not commit `.env` or expose the secret key publicly.

### Step 4: Run the application

```bash
python3 app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

## 6. How to Use the Application

1. Register a new user account.
2. Log in using the registered credentials.
3. Upload a document.
4. View uploaded documents on the documents page.
5. Search documents using available filters.
6. Open Manage Permissions for an owned document.
7. Grant read or edit access to another registered user.
8. Revoke permissions when access is no longer required.
9. View audit logs using an authorized admin account.

## 7. Security Implementation

TrustVault includes the following security measures:

- Password hashing instead of plain-text password storage.
- Server-side document authorization.
- Separate read and edit permissions.
- Owner-only permission management and deletion.
- CSRF protection for forms.
- File-extension and MIME-type validation.
- Unique filenames for uploaded files.
- Maximum upload size restriction.
- Environment-based application secret key.
- Admin-restricted audit-log access.

For detailed security analysis, refer to `THREATS.md`.

## 8. Running Automated Tests

Run:

```bash
pytest -v
```

### Latest test results

**11 tests passed, 0 failed.**

Tests cover authentication pages, document permissions, unauthorized document access, audit-log storage, file validation and upload-size restrictions.

## 9. Limitations and Future Improvements

- Add login rate limiting.
- Integrate malware scanning for uploaded documents.
- Improve audit-log tamper resistance.
- Configure secure cookies and HTTPS for production.
- Use persistent production database and file storage.
- Add automated backups.
- Improve scalability for larger document collections.

## 10. AI Development Assistance

ChatGPT was used as a development assistant for understanding Flask concepts, implementation guidance, debugging, testing and documentation.

Refer to `PROMPTS.md` for the AI development log.

## 11. Project Status

TrustVault has implemented its core authentication, document management, permission-sharing, audit logging and upload-validation functionality.

The application has passed 11 automated tests in the development environment.

Production deployment and additional security hardening remain necessary before using the application for sensitive real-world documents.

### Demo Login Instructions

TrustVault supports role-based access control with separate Admin and Viewer accounts.

- **Admin:** The account registered using the configured `ADMIN_EMAIL` environment variable. The admin can access the audit logs at `/admin/audit-logs`.
- **Viewer:** A normal registered account with document access based on permissions granted by the document owner.

To evaluate the audit logging functionality, please log in using the Admin account and visit:

https://trustvault-3-kbf2.onrender.com/admin/audit-logs