# API Endpoints - Quick Reference

## Base URL
All API endpoints start with: `http://127.0.0.1:8000/api/`

**Note:** The root URL (`/`) shows a 404 error - this is normal! All endpoints are under `/api/`

---

## Quick Access URLs

### Authentication
- `POST /api/auth/login/` - Login (get JWT token)
- `POST /api/auth/refresh/` - Refresh token
- `GET /api/auth/me/` - Get current user

### Documents
- `GET /api/documents/` - List documents
- `POST /api/documents/` - Upload document
- `GET /api/documents/{id}/download/` - Download file

### Tickets
- `GET /api/tickets/` - List tickets
- `POST /api/tickets/` - Create ticket
- `GET /api/tickets/{id}/` - Get ticket details

### Events
- `GET /api/events/` - List events
- `POST /api/events/` - Create event
- `GET /api/events/?date=2025-11-25` - Get events for specific date

### Users/Directory
- `GET /api/users/` - List users (directory)
- `GET /api/users/{id}/` - Get user profile
- `PATCH /api/users/{id}/` - Update profile

### Reports
- `POST /api/reports/generate/` - Generate report
- `GET /api/reports/` - List reports
- `GET /api/reports/{id}/export/?format=pdf` - Export PDF
- `GET /api/reports/{id}/export/?format=excel` - Export Excel

---

## How to Test

### Step 1: Get JWT Token
Visit in browser:
```
http://127.0.0.1:8000/api/auth/login/
```
Enter email and password, click POST.

### Step 2: Copy the Access Token
From the response, copy the `access` token value.

### Step 3: Test Any Endpoint
Visit in browser (you'll need to authenticate):
```
http://127.0.0.1:8000/api/documents/
http://127.0.0.1:8000/api/tickets/
http://127.0.0.1:8000/api/events/
http://127.0.0.1:8000/api/users/
```

---

## Full Documentation

See `API_ENDPOINTS.md` for complete documentation with:
- All endpoints listed
- Request/response examples
- Query parameters
- Authentication details

