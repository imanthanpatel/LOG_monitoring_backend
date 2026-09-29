# SentinelSIEM Backend API Documentation

This project is a Django REST API for a security monitoring and investigation platform. It supports log ingestion, alert management, rule-based detection, MITRE ATT&CK mapping, investigations, evidence handling, audits, and notifications.

## 1. Base URL

- Local development: http://127.0.0.1:8000
- API root: http://127.0.0.1:8000/api/

## 2. Authentication

Most endpoints require JWT authentication.

- Login returns: access token and refresh token
- Send the token in the request header:

```http
Authorization: Bearer <access_token>
```

Public endpoints:
- POST /api/auth/register/
- POST /api/auth/login/

Protected endpoints require valid authentication.

## 3. Authentication APIs

### Register user

- Method: POST
- URL: /api/auth/register/
- Description: Create a new user account.
- Body example:

```json
{
  "username": "analyst1",
  "email": "analyst1@example.com",
  "password": "StrongPass123!",
  "role": "SOC"
}
```

### Login

- Method: POST
- URL: /api/auth/login/
- Description: Authenticate a user and receive JWT tokens.
- Response example:

```json
{
  "message": "Login Successful",
  "username": "analyst1",
  "access": "<jwt_access_token>",
  "refresh": "<jwt_refresh_token>",
  "role": "SOC"
}
```

### Logout

- Method: POST
- URL: /api/auth/logout/
- Description: Blacklist the refresh token.
- Body:

```json
{
  "refresh": "<refresh_token>"
}
```

### Current user

- Method: GET
- URL: /api/auth/me/
- Description: Returns information about the logged-in user.

## 4. User Management APIs

### Get all users

- Method: GET
- URL: /api/user-list/
- Description: Returns all users.
- Requires: Authentication

### Update user profile/role

- Method: PATCH
- URL: /api/users/<id>/
- Description: Updates a user's profile information or assigned role.
- Requires: Authentication + Admin permission

### Delete user

- Method: DELETE
- URL: /api/users/<id>/delete
- Description: Deletes a user account.
- Requires: Authentication + Admin permission
- Note: A user cannot delete their own account.

## 5. Dashboard and Alert Summary APIs

### Dashboard statistics

- Method: GET
- URL: /api/dashboard/
- Description: Returns general SOC dashboard totals.
- Response includes:
  - total_logs
  - total_alerts
  - active_rules
  - critical_alerts
  - high_alerts
  - medium_alerts
  - low_alerts
  - total_users
  - failed_logins

### Alert summary stats

- Method: GET
- URL: /api/stats/
- Description: Returns aggregate counts for alert severities.

### List alerts

- Method: GET
- URL: /api/alerts/
- Description: Returns all alert records.

### Alert detail

- Method: GET
- URL: /api/alerts/<id>/
- Description: Returns one specific alert.
- Requires: Authentication

### Update alert status

- Method: PUT
- URL: /api/alerts/status/
- Description: Updates the status of an alert.
- Body example:

```json
{
  "id": 12,
  "status": "OPEN"
}
```

### Assign alert to investigator

- Method: POST
- URL: /api/alerts/<id>/assign/
- Description: Assigns an alert to an investigator and creates an investigation record.
- Requires: Authentication
- Body example:

```json
{
  "investigator": 7
}
```

## 6. Log Ingestion APIs

### Ingest log

- Method: POST
- URL: /api/ingest/
- Description: Creates a log record from a JSON payload.
- Body example:

```json
{
  "event_id": 4625,
  "source": "windows",
  "log_type": "authentication",
  "message": "Failed login attempt",
  "computer": "DC01",
  "ip_address": "10.0.0.22",
  "username": "admin",
  "time_generated": "2026-09-23T10:30:00Z"
}
```

### List logs

- Method: GET
- URL: /api/logs/
- Description: Returns log records with optional filters.
- Query params:
  - ordering=
  - event_id=
  - source=
  - log_type=
  - username=
  - computer=
  - ip_address=
- Example:

```http
GET /api/logs/?event_id=4625&ordering=-time_generated
```

## 7. Detection and Rule APIs

These endpoints are served via a DRF router.

### Rules collection

- GET /api/rules/
- POST /api/rules/
- GET /api/rules/<id>/
- PUT /api/rules/<id>/
- PATCH /api/rules/<id>/
- DELETE /api/rules/<id>/

### Rule statistics

- Method: GET
- URL: /api/rules/stats/
- Description: Returns total enabled and disabled rules.

### MITRE techniques

- GET /api/mitre/
- GET /api/mitre/<id>/

### MITRE coverage

- Method: GET
- URL: /api/mitre/coverage/
- Description: Returns rule-to-MITRE mapping coverage percentage.

### MITRE statistics

- Method: GET
- URL: /api/mitre/stats/
- Description: Returns total technique and tactic counts.

## 8. Investigation APIs

### My investigations

- Method: GET
- URL: /api/investigations/me/
- Description: Returns all investigations assigned to the authenticated investigator.
- Requires: Authentication + Investigator role

### Completed investigation reports

- Method: GET
- URL: /api/investigations/completed/
- Description: Returns completed and closed investigation reports for the SOC dashboard.
- Requires: Authentication + ADMIN or SOC role
- Includes: summary, root cause, recommendations, conclusion, evidence, investigator, and completion time.

### Investigation detail

- Method: GET
- URL: /api/investigations/<id>/
- Description: Fetches one assigned investigation.
- ADMIN and SOC users can also view completed investigation reports.

### Update investigation

- Method: PATCH
- URL: /api/investigations/<id>/
- Description: Updates investigation fields such as summary, root cause, recommendations, or conclusion.

### Complete investigation

- Method: POST
- URL: /api/investigations/<id>/complete/
- Description: Marks the investigation as completed and closes the associated alert.
- Requires all required fields to be filled before submission.

### Investigation evidence

- Method: GET
- URL: /api/investigations/<id>/evidence/
- Description: Lists evidence related to an investigation.

- Method: POST
- URL: /api/investigations/<id>/evidence/
- Description: Uploads evidence for an investigation.

## 9. Evidence APIs

### Upload or list investigation evidence

- GET /api/investigations/<id>/evidence/
- POST /api/investigations/<id>/evidence/

Evidence is tied to an investigation and includes metadata such as the uploader and upload date.

## 10. Audit Log API

### Get audit logs

- Method: GET
- URL: /api/audit-logs/
- Description: Returns audit entries for system actions.
- Requires: Authentication

## 11. Notification APIs

### My notifications

- Method: GET
- URL: /api/notifications/
- Description: Returns notifications for the logged-in user.

### Mark notification as read

- Method: PATCH
- URL: /api/notifications/<id>/read/
- Description: Marks a user notification as read.

## 12. Typical API Flow

1. Register or log in via /api/auth/register/ or /api/auth/login/
2. Use the returned access token as a bearer token in the Authorization header
3. Submit logs to /api/ingest/
4. Read logs at /api/logs/
5. Review alert summaries at /api/dashboard/ or /api/stats/
6. Assign alerts to investigators via /api/alerts/<id>/assign/
7. Investigate assigned alerts through /api/investigations/me/
8. Upload evidence under /api/investigations/<id>/evidence/
9. Close an investigation using /api/investigations/<id>/complete/

## 13. Notes

- This backend uses Django REST Framework with JWT-based authentication.
- Authentication is required for most operational APIs.
- User roles such as ADMIN, SOC, INVESTIGATOR, and VIEWER are enforced by custom permissions.
- The detection engine and alerting layer are rule-driven and MITRE-mapped.

## 14. Quick Start

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requriment.txt
python manage.py migrate
python manage.py runserver
```

Then open:
- http://127.0.0.1:8000/api/

## 15. Summary

This API exposes the full workflow of a lightweight SIEM platform:
- ingest logs
- detect suspicious activity
- generate alerts
- assign incidents for investigation
- attach evidence
- audit every action
- notify users

If you want, I can also generate a separate Swagger-style OpenAPI document or a Postman collection for these endpoints.
🔴 Real-time streaming detection (Kafka/WebSockets)
🤖 AI-based anomaly detection engine
📊 SOC dashboard (React / Next.js)
🔗 Attack chain correlation (Kill-chain analysis)
🌐 Threat intelligence feed integration
📡 ELK stack integration

```
### 👨‍💻 Author
```
Manthan Patel

```
### ⭐ Support This Project
```
If you find this project useful:

⭐ Star the repository
🍴 Fork it
🧠 Contribute new detection rules
🚀 Improve MITRE coverage

```
### ⚠️ Disclaimer
```
This project is built for educational and research purposes only.

It is NOT intended for production enterprise security monitoring.
```












