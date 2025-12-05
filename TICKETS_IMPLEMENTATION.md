# Support Tickets System - Implementation Complete ✅

## Overview
The Support Tickets System has been fully implemented in the backend. This system allows users to create, track, and manage support tickets with auto-generated ticket IDs.

## What Was Implemented

### 1. **Django App: `tickets`**
   - Created complete Django app structure
   - All necessary files (models, views, serializers, URLs, admin)

### 2. **Ticket Model**
   Located in `backend/tickets/models.py`

   **Fields:**
   - `ticket_id` - Auto-generated unique ID (format: TCK-001, TCK-002, etc.)
   - `title` - Ticket title
   - `description` - Detailed description
   - `status` - Choice field: Open, In Progress, Closed
   - `priority` - Choice field: Low, Medium, High, Urgent
   - `created_by` - ForeignKey to User (creator)
   - `assigned_to` - ForeignKey to User (nullable, for assignment)
   - `created_at` - Auto timestamp
   - `updated_at` - Auto timestamp

   **Auto-Generated Ticket IDs:**
   - Format: `TCK-001`, `TCK-002`, `TCK-003`, etc.
   - Automatically increments based on existing tickets
   - Unique and non-editable after creation

### 3. **API Endpoints**

   All endpoints require JWT authentication (access token in header).

   **Base URL:** `/api/tickets/`

   - **GET `/api/tickets/`** - List tickets
     - Query parameters:
       - `search` - Search by title, description, or ticket_id
       - `status` - Filter by status (OPEN, IN_PROGRESS, CLOSED)
       - `priority` - Filter by priority (LOW, MEDIUM, HIGH, URGENT)
       - `assigned_to` - Filter by assignee user ID
   
   - **POST `/api/tickets/`** - Create a new ticket
     - Body (JSON):
       ```json
       {
         "title": "Ticket Title",
         "description": "Ticket description",
         "priority": "MEDIUM"  // Optional: LOW, MEDIUM, HIGH, URGENT
       }
       ```
   
   - **GET `/api/tickets/{id}/`** - Get ticket details
   
   - **PATCH `/api/tickets/{id}/`** - Update ticket (status, priority, etc.)
   
   - **PUT `/api/tickets/{id}/`** - Full update ticket
   
   - **DELETE `/api/tickets/{id}/`** - Delete ticket (admin only)
   
   - **PATCH `/api/tickets/{id}/assign/`** - Assign ticket to a user
     - Body: `{"assigned_to": <user_id>}`
   
   - **PATCH `/api/tickets/{id}/close/`** - Close ticket (set status to CLOSED)

### 4. **Access Control**

   **Permission Rules:**
   - **All authenticated users** can create tickets
   - **Users** can view and update their own tickets
   - **Staff** can view and update all tickets
   - **Admins** have full access (view, update, delete)
   - **Only admins** can delete tickets

### 5. **Features**

   - ✅ Auto-generated ticket IDs (TCK-001 format)
   - ✅ Status tracking (Open, In Progress, Closed)
   - ✅ Priority levels (Low, Medium, High, Urgent)
   - ✅ Ticket assignment to users
   - ✅ Search functionality
   - ✅ Filtering by status, priority, assignee
   - ✅ Role-based access control
   - ✅ Django admin interface

## Next Steps: Running Migrations

To activate the Support Tickets System, you need to create and run migrations:

```bash
cd Division-Information-Management-System/backend
python manage.py makemigrations tickets
python manage.py migrate
```

## Example API Usage

### 1. List Tickets
```bash
GET /api/tickets/
Authorization: Bearer <your_access_token>

# With search
GET /api/tickets/?search=printer

# With filters
GET /api/tickets/?status=OPEN&priority=HIGH
```

### 2. Create Ticket
```bash
POST /api/tickets/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "title": "Printer not working",
  "description": "The printer in Room 101 is not responding",
  "priority": "HIGH"
}
```

### 3. Get Ticket Details
```bash
GET /api/tickets/1/
Authorization: Bearer <your_access_token>
```

### 4. Update Ticket Status
```bash
PATCH /api/tickets/1/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "status": "IN_PROGRESS"
}
```

### 5. Assign Ticket
```bash
PATCH /api/tickets/1/assign/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "assigned_to": 2
}
```

### 6. Close Ticket
```bash
PATCH /api/tickets/1/close/
Authorization: Bearer <your_access_token>
```

## Response Format

### List Response
```json
[
  {
    "id": 1,
    "ticket_id": "TCK-001",
    "title": "Printer not working",
    "status": "OPEN",
    "priority": "HIGH",
    "creator": "user@example.com",
    "date": "2024-12-05",
    "created_at": "2024-12-05T12:00:00Z"
  }
]
```

### Detail Response
```json
{
  "id": 1,
  "ticket_id": "TCK-001",
  "title": "Printer not working",
  "description": "The printer in Room 101 is not responding",
  "status": "OPEN",
  "priority": "HIGH",
  "created_by": 1,
  "creator": "user@example.com",
  "creator_email": "user@example.com",
  "assigned_to": null,
  "assignee": null,
  "assignee_email": null,
  "created_at": "2024-12-05T12:00:00Z",
  "date": "2024-12-05",
  "updated_at": "2024-12-05T12:00:00Z"
}
```

## Frontend Integration Notes

The frontend currently uses dummy data. To connect it to the backend:

1. **Update `TicketsPage.vue`:**
   - Replace hardcoded `events` array with API call to `GET /api/tickets/`
   - Use `ticket_id` from response (matches format like 'TCK-001')
   - Map status values: `OPEN`, `IN_PROGRESS`, `CLOSED`
   - Use `creator` field for creator display

2. **Update Ticket Creation:**
   - Submit form data to `POST /api/tickets/` with title and description
   - Include JWT token in Authorization header

3. **Status Mapping:**
   - Frontend uses: "Open", "In Progress", "Closed"
   - Backend uses: "OPEN", "IN_PROGRESS", "CLOSED"
   - Map accordingly in frontend code

## Files Created/Modified

### New Files:
- `backend/tickets/__init__.py`
- `backend/tickets/apps.py`
- `backend/tickets/models.py`
- `backend/tickets/serializers.py`
- `backend/tickets/views.py`
- `backend/tickets/urls.py`
- `backend/tickets/admin.py`
- `backend/tickets/tests.py`
- `backend/tickets/migrations/__init__.py`

### Modified Files:
- `backend/config/settings.py` - Added tickets app
- `backend/config/urls.py` - Added tickets URLs

## Database Schema

After migrations, the `tickets_ticket` table will have:
- `id` (Primary Key)
- `ticket_id` (VARCHAR, unique) - Auto-generated
- `title` (VARCHAR)
- `description` (TEXT)
- `status` (VARCHAR)
- `priority` (VARCHAR)
- `created_by_id` (ForeignKey to accounts_user)
- `assigned_to_id` (ForeignKey to accounts_user, nullable)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

## Testing the Implementation

1. **Create migrations:**
   ```bash
   python manage.py makemigrations tickets
   python manage.py migrate
   ```

2. **Test via Django Admin:**
   - Go to `http://localhost:8000/admin/`
   - Tickets should be available under "TICKETS"
   - Create a ticket and verify auto-generated ticket_id

3. **Test via API:**
   - Get JWT token from `/api/auth/login/`
   - Create a ticket via `POST /api/tickets/`
   - Verify ticket_id is auto-generated (TCK-001)
   - List tickets and verify they appear

## Notes

- Ticket IDs are auto-generated and cannot be edited after creation
- First ticket will be TCK-001, second will be TCK-002, etc.
- Status can be updated by creator, assignee, staff, or admin
- Only admins can delete tickets
- Search works on title, description, and ticket_id
- Filtering supports multiple query parameters simultaneously

