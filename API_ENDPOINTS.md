# Complete API Endpoints Reference

This document lists all available API endpoints in the Division Information Management System.

**Base URL:** `http://127.0.0.1:8000`

**Authentication:** All endpoints (except login) require JWT authentication. Include in headers:
```
Authorization: Bearer <your_access_token>
```

---

## Authentication Endpoints

### 1. Login (Get JWT Token)
```
POST /api/auth/login/
```
**Body (JSON):**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "STAFF"
  }
}
```

### 2. Refresh Token
```
POST /api/auth/refresh/
```
**Body (JSON):**
```json
{
  "refresh": "your_refresh_token_here"
}
```

### 3. Get Current User Info
```
GET /api/auth/me/
```
**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "STAFF",
  ...
}
```

---

## Document Management Endpoints

### Base: `/api/documents/`

### 1. List Documents
```
GET /api/documents/
```
**Query Parameters:**
- `search` - Search by name or description
- `type` - Filter by type (PUBLICATION, MEMOS, AWARDS)
- `access` - Filter by access level (PUBLIC, PERMITTED, RESTRICTED)

**Example:**
```
GET /api/documents/?search=research&type=PUBLICATION
```

### 2. Upload Document
```
POST /api/documents/
```
**Body (multipart/form-data):**
- `name` - Document name (required)
- `file` - File to upload (required)
- `document_type` - PUBLICATION, MEMOS, or AWARDS (required)
- `access_level` - PUBLIC, PERMITTED, or RESTRICTED (required)
- `description` - Optional description

### 3. Get Document Details
```
GET /api/documents/{id}/
```

### 4. Update Document
```
PATCH /api/documents/{id}/
PUT /api/documents/{id}/
```
**Body (JSON or form-data):**
```json
{
  "name": "Updated Name",
  "access_level": "PUBLIC"
}
```

### 5. Delete Document
```
DELETE /api/documents/{id}/
```

### 6. Download Document
```
GET /api/documents/{id}/download/
```

---

## Support Tickets Endpoints

### Base: `/api/tickets/`

### 1. List Tickets
```
GET /api/tickets/
```
**Query Parameters:**
- `search` - Search by title, description, or ticket_id
- `status` - Filter by status (OPEN, IN_PROGRESS, CLOSED)
- `priority` - Filter by priority (LOW, MEDIUM, HIGH, URGENT)
- `assigned_to` - Filter by assignee user ID

**Example:**
```
GET /api/tickets/?status=OPEN&priority=HIGH
```

### 2. Create Ticket
```
POST /api/tickets/
```
**Body (JSON):**
```json
{
  "title": "Printer not working",
  "description": "The printer in Room 101 is not responding",
  "priority": "HIGH"
}
```

### 3. Get Ticket Details
```
GET /api/tickets/{id}/
```

### 4. Update Ticket
```
PATCH /api/tickets/{id}/
PUT /api/tickets/{id}/
```
**Body (JSON):**
```json
{
  "status": "IN_PROGRESS",
  "assigned_to": 2
}
```

### 5. Delete Ticket
```
DELETE /api/tickets/{id}/
```

### 6. Assign Ticket
```
PATCH /api/tickets/{id}/assign/
```
**Body (JSON):**
```json
{
  "assigned_to": 2
}
```

### 7. Close Ticket
```
PATCH /api/tickets/{id}/close/
```

---

## Calendar/Events Endpoints

### Base: `/api/events/`

### 1. List Events
```
GET /api/events/
```
**Query Parameters:**
- `date` - Filter by specific date (YYYY-MM-DD or YYYY/MM/DD)
- `date_from` - Filter events from this date
- `date_to` - Filter events up to this date
- `type` - Filter by event type (MEETING, WORKSHOP, SEMINAR, MAINTENANCE)
- `search` - Search by title, description, or venue
- `upcoming` - Filter only upcoming events (true/false)

**Examples:**
```
GET /api/events/?date=2025-11-25
GET /api/events/?date_from=2025-01-01&date_to=2025-12-31
GET /api/events/?type=MEETING&upcoming=true
```

### 2. Create Event
```
POST /api/events/
```
**Body (JSON):**
```json
{
  "title": "Faculty Meeting",
  "description": "Monthly department meeting",
  "date": "2025-11-25",
  "start_time": "14:00:00",
  "end_time": "16:00:00",
  "event_type": "MEETING",
  "venue": "Conference Room A"
}
```

### 3. Get Event Details
```
GET /api/events/{id}/
```

### 4. Update Event
```
PATCH /api/events/{id}/
PUT /api/events/{id}/
```

### 5. Delete Event
```
DELETE /api/events/{id}/
```

---

## User Directory/Profile Endpoints

### Base: `/api/users/`

### 1. List Users (Directory)
```
GET /api/users/
```
**Query Parameters:**
- `search` - Search by email, name, department, or position
- `role` - Filter by role (ADMIN, STAFF, FACULTY)
- `status` - Filter by status (ACTIVE, INACTIVE, ON_LEAVE)
- `department` - Filter by department

**Example:**
```
GET /api/users/?role=FACULTY&status=ACTIVE
GET /api/users/?search=john&department=IT
```

### 2. Get User Profile
```
GET /api/users/{id}/
```

### 3. Update Profile
```
PATCH /api/users/{id}/
PUT /api/users/{id}/
```
**Body (JSON or form-data):**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1-234-567-8900",
  "department": "IT Department",
  "position": "Software Developer",
  "bio": "I love coding!",
  "status": "ACTIVE"
}
```
**Note:** Users can only update their own profile (admins can update any)

---

## Report Generation Endpoints

### Base: `/api/reports/`

### 1. Generate Report
```
POST /api/reports/generate/
```
**Body (JSON):**
```json
{
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "unit": "Workshop",
  "title": "Annual Report 2024"
}
```

### 2. List Generated Reports
```
GET /api/reports/
```

### 3. Get Report Details
```
GET /api/reports/{id}/
```

### 4. Export Report to PDF
```
GET /api/reports/{id}/export/?format=pdf
```

### 5. Export Report to Excel
```
GET /api/reports/{id}/export/?format=excel
```

---

## Faculty Activity Endpoints

### Base: `/api/faculty-activities/`

### 1. List Faculty Activities
```
GET /api/faculty-activities/
```

### 2. Create Faculty Activity Record
```
POST /api/faculty-activities/
```
**Body (JSON):**
```json
{
  "faculty": 1,
  "unit": "Computer Science",
  "publications_count": 5,
  "service_hours": 32.5,
  "trainings_attended": 3,
  "period_start": "2024-01-01",
  "period_end": "2024-12-31"
}
```

### 3. Get Activity Details
```
GET /api/faculty-activities/{id}/
```

### 4. Update Activity
```
PATCH /api/faculty-activities/{id}/
```

### 5. Delete Activity
```
DELETE /api/faculty-activities/{id}/
```

---

## Quick Access Guide

### Testing Endpoints

1. **Get JWT Token:**
   ```bash
   POST http://127.0.0.1:8000/api/auth/login/
   ```

2. **Test Documents:**
   ```bash
   GET http://127.0.0.1:8000/api/documents/
   Authorization: Bearer <token>
   ```

3. **Test Tickets:**
   ```bash
   GET http://127.0.0.1:8000/api/tickets/
   Authorization: Bearer <token>
   ```

4. **Test Events:**
   ```bash
   GET http://127.0.0.1:8000/api/events/
   Authorization: Bearer <token>
   ```

5. **Test Users Directory:**
   ```bash
   GET http://127.0.0.1:8000/api/users/
   Authorization: Bearer <token>
   ```

6. **Generate Report:**
   ```bash
   POST http://127.0.0.1:8000/api/reports/generate/
   Authorization: Bearer <token>
   ```

---

## Complete Endpoint List

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Login and get JWT token |
| POST | `/api/auth/refresh/` | Refresh JWT token |
| GET | `/api/auth/me/` | Get current user info |
| GET | `/api/documents/` | List documents |
| POST | `/api/documents/` | Upload document |
| GET | `/api/documents/{id}/` | Get document |
| PATCH | `/api/documents/{id}/` | Update document |
| DELETE | `/api/documents/{id}/` | Delete document |
| GET | `/api/documents/{id}/download/` | Download document |
| GET | `/api/tickets/` | List tickets |
| POST | `/api/tickets/` | Create ticket |
| GET | `/api/tickets/{id}/` | Get ticket |
| PATCH | `/api/tickets/{id}/` | Update ticket |
| DELETE | `/api/tickets/{id}/` | Delete ticket |
| PATCH | `/api/tickets/{id}/assign/` | Assign ticket |
| PATCH | `/api/tickets/{id}/close/` | Close ticket |
| GET | `/api/events/` | List events |
| POST | `/api/events/` | Create event |
| GET | `/api/events/{id}/` | Get event |
| PATCH | `/api/events/{id}/` | Update event |
| DELETE | `/api/events/{id}/` | Delete event |
| GET | `/api/users/` | List users (directory) |
| GET | `/api/users/{id}/` | Get user profile |
| PATCH | `/api/users/{id}/` | Update profile |
| POST | `/api/reports/generate/` | Generate report |
| GET | `/api/reports/` | List reports |
| GET | `/api/reports/{id}/` | Get report |
| GET | `/api/reports/{id}/export/?format=pdf` | Export to PDF |
| GET | `/api/reports/{id}/export/?format=excel` | Export to Excel |
| GET | `/api/faculty-activities/` | List faculty activities |
| POST | `/api/faculty-activities/` | Create activity record |

---

## Accessing the API

### Option 1: Django REST Framework Browsable API

Visit any endpoint in your browser while logged in:
- `http://127.0.0.1:8000/api/documents/`
- `http://127.0.0.1:8000/api/tickets/`
- etc.

### Option 2: Using curl

```bash
# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use the token
curl -X GET http://127.0.0.1:8000/api/documents/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Option 3: Using Postman

1. Create a new request
2. Set method (GET, POST, etc.)
3. Enter URL (e.g., `http://127.0.0.1:8000/api/documents/`)
4. Go to Headers tab
5. Add: `Authorization: Bearer YOUR_TOKEN_HERE`
6. For POST requests, add Body (JSON or form-data)

---

## Important Notes

1. **Root URL (`/`):** There's no endpoint at the root. The API starts at `/api/`

2. **Admin Panel:** Access at `http://127.0.0.1:8000/admin/`

3. **404 Error on Root:** This is normal! There's no endpoint at `/`. Use `/api/...` endpoints instead.

4. **CORS:** Currently configured to allow all origins (development only)

5. **Authentication:** All endpoints except `/api/auth/login/` require JWT token

---

## Testing All Endpoints

You can test all endpoints using the Django REST Framework browsable API:

1. Start server: `python manage.py runserver`
2. Login at: `http://127.0.0.1:8000/api/auth/login/`
3. Copy the `access` token
4. Visit any API endpoint and use the browsable interface

Or use the automated test script:
```bash
python test_documents_api.py
```

