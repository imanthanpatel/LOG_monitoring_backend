# SentinelSIEM Backend

SentinelSIEM is a Django REST API for a lightweight security information and event management (SIEM) platform. It ingests security logs, evaluates detection rules, creates alerts, and supports investigations with MITRE ATT&CK mapping, evidence, audit logs, and notifications.

## Features

- JWT authentication
- Security log ingestion and filtering
- Rule-based detection and alert generation
- Alert assignment and investigation management
- MITRE ATT&CK mapping and coverage statistics
- Investigation evidence upload and retrieval
- Audit logging
- User notifications
- Role-based access control

## Technology Stack

- Python
- Django 5
- Django REST Framework
- Simple JWT
- MySQL
- Django Channels
- Celery
- django-cors-headers

## Prerequisites

- Python 3.11 or later
- MySQL 8 or later
- Git

Create the MySQL database:

```sql
CREATE DATABASE logmonitor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

The development settings expect MySQL at `localhost:3306` with database `logmonitor`. Update `backend/settings.py` before deployment.

## Installation

From the repository root:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies and initialize the database:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

API URL: `http://127.0.0.1:8000/api/`

Admin URL: `http://127.0.0.1:8000/admin/`

## Security Configuration

The current settings contain development-only defaults. Before production deployment:

- Set `DEBUG = False`.
- Move `SECRET_KEY` to an environment variable.
- Move database credentials to environment variables.
- Restrict `ALLOWED_HOSTS`.
- Restrict CORS origins.
- Use a dedicated MySQL user.
- Serve the API over HTTPS.
- Rotate credentials exposed in source control.

## Authentication

Register or log in:

```http
POST /api/auth/register/
POST /api/auth/login/
```

Send the access token with protected requests:

```http
Authorization: Bearer <access_token>
```

Other authentication endpoints:

```http
POST /api/auth/logout/
GET  /api/auth/me/
```

Example login request:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"analyst1","password":"your-password"}'
```

## API Overview

All routes below are relative to `http://127.0.0.1:8000`.

| Area | Routes |
| --- | --- |
| Authentication | `/api/auth/register/`, `/api/auth/login/`, `/api/auth/logout/`, `/api/auth/me/` |
| Users | `/api/user-list/`, `/api/users/<id>/`, `/api/users/<id>/delete` |
| Alerts | `/api/dashboard/`, `/api/stats/`, `/api/alerts/`, `/api/alerts/<id>/`, `/api/alerts/status/`, `/api/alerts/<id>/assign/` |
| Logs | `/api/ingest/`, `/api/logs/` |
| Detection | `/api/rules/`, `/api/mitre/`, `/api/mitre/coverage/`, `/api/mitre/stats/` |
| Investigations | `/api/investigations/me/`, `/api/investigations/completed/`, `/api/investigations/<id>/`, `/api/investigations/<id>/complete/` |
| Evidence | `/api/investigations/<id>/evidence/` |
| Audit | `/api/audit-logs/` |
| Notifications | `/api/notifications/`, `/api/notifications/<id>/read/` |

Rules and MITRE collections use Django REST Framework routers and support standard collection and detail operations where applicable.

## Ingesting Logs

```bash
curl -X POST http://127.0.0.1:8000/api/ingest/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "event_id": 4625,
    "source": "windows",
    "log_type": "authentication",
    "message": "Failed login attempt",
    "computer": "DC01",
    "ip_address": "10.0.0.22",
    "username": "admin",
    "time_generated": "2026-09-23T10:30:00Z"
  }'
```

Filter logs using:

```http
GET /api/logs/?event_id=4625&ordering=-time_generated
```

Supported filters include `event_id`, `source`, `log_type`, `username`, `computer`, `ip_address`, and `ordering`.

## Typical Workflow

1. Register or log in.
2. Include the JWT access token in requests.
3. Ingest security logs.
4. Review alerts and dashboard statistics.
5. Assign alerts to investigators.
6. Update investigations and attach evidence.
7. Complete investigations and review the audit trail.

## Testing

Run Django tests from the backend directory:

```bash
python manage.py test
```

The repository also includes `tests/test_siem.py`, which sends representative security events to a running local server.

## Project Structure

```text
backend/
├── accounts/          Authentication, users, roles, and permissions
├── alerts/            Alerts and dashboard endpoints
├── audit/             Audit logs
├── detection/         Detection engine and MITRE mappings
├── evidence/          Investigation evidence
├── ingestion/         Log ingestion and search
├── investigations/    Investigation lifecycle
├── notifications/     User notifications
├── api/               Shared API functionality
├── backend/           Django settings and URL configuration
├── tests/             SIEM request scenarios
├── manage.py
└── requirements.txt
```

## License and Disclaimer

No license has been specified for this repository yet. Add a license before accepting external contributions or publishing the project for reuse.

This project is intended for educational and research use. Review and harden the configuration before using it for production security monitoring.
