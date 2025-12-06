# Calendar/Events System - Implementation Complete ✅

## Overview
The Calendar/Events System has been fully implemented in the backend. This system allows users to create, view, and manage calendar events with date-based filtering.

## What Was Implemented

### 1. **Django App: `calendar`**
   - Created complete Django app structure
   - All necessary files (models, views, serializers, URLs, admin)

### 2. **Event Model**
   Located in `backend/calendar/models.py`

   **Fields:**
   - `title` - Event title
   - `description` - Event description (optional)
   - `date` - Event date (DateField)
   - `start_time` - Start time (TimeField, optional)
   - `end_time` - End time (TimeField, optional)
   - `event_type` - Choice field: Meeting, Workshop, Seminar, Maintenance (optional)
   - `venue` - Event venue/location (optional)
   - `created_by` - ForeignKey to User (creator)
   - `created_at` - Auto timestamp
   - `updated_at` - Auto timestamp

### 3. **API Endpoints**

   All endpoints require JWT authentication (access token in header).

   **Base URL:** `/api/events/`

   - **GET `/api/events/`** - List events
     - Query parameters:
       - `date` - Filter by specific date (format: YYYY-MM-DD or YYYY/MM/DD)
       - `date_from` - Filter events from this date onwards
       - `date_to` - Filter events up to this date
       - `type` - Filter by event type (MEETING, WORKSHOP, SEMINAR, MAINTENANCE)
       - `search` - Search by title, description, or venue
       - `upcoming` - Filter only upcoming events (true/false)
   
   - **POST `/api/events/`** - Create a new event
     - Body (JSON):
       ```json
       {
         "title": "Faculty Meeting",
         "description": "Meeting with department heads",
         "date": "2025-11-25",
         "start_time": "14:00:00",
         "end_time": "16:00:00",
         "event_type": "MEETING",
         "venue": "Conference Room A"
       }
       ```
   
   - **GET `/api/events/{id}/`** - Get event details
   
   - **PATCH `/api/events/{id}/`** - Update event (creator or admin only)
   
   - **PUT `/api/events/{id}/`** - Full update event
   
   - **DELETE `/api/events/{id}/`** - Delete event (creator or admin only)

### 4. **Access Control**

   **Permission Rules:**
   - **All authenticated users** can view events
   - **All authenticated users** can create events
   - **Only creator or admin** can update/delete events

### 5. **Features**

   - ✅ Date-based event management
   - ✅ Optional time tracking (start_time, end_time)
   - ✅ Event types (Meeting, Workshop, Seminar, Maintenance)
   - ✅ Venue/location tracking
   - ✅ Date range filtering
   - ✅ Search functionality
   - ✅ Upcoming events filter
   - ✅ Django admin interface with date hierarchy

## Next Steps: Running Migrations

To activate the Calendar/Events System, you need to create and run migrations:

```bash
cd Division-Information-Management-System/backend
python manage.py makemigrations calendar
python manage.py migrate
```

## Example API Usage

### 1. List All Events
```bash
GET /api/events/
Authorization: Bearer <your_access_token>
```

### 2. List Events for Specific Date
```bash
GET /api/events/?date=2025-11-25
Authorization: Bearer <your_access_token>

# Or with slash format
GET /api/events/?date=2025/11/25
```

### 3. List Events in Date Range
```bash
GET /api/events/?date_from=2025-11-01&date_to=2025-11-30
Authorization: Bearer <your_access_token>
```

### 4. List Upcoming Events Only
```bash
GET /api/events/?upcoming=true
Authorization: Bearer <your_access_token>
```

### 5. Filter by Event Type
```bash
GET /api/events/?type=MEETING
Authorization: Bearer <your_access_token>
```

### 6. Search Events
```bash
GET /api/events/?search=workshop
Authorization: Bearer <your_access_token>
```

### 7. Create Event
```bash
POST /api/events/
Authorization: Bearer <your_access_token>
Content-Type: application/json

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

### 8. Get Event Details
```bash
GET /api/events/1/
Authorization: Bearer <your_access_token>
```

### 9. Update Event
```bash
PATCH /api/events/1/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "title": "Updated Meeting Title",
  "venue": "New Venue"
}
```

## Response Format

### List Response
```json
[
  {
    "id": 1,
    "title": "Faculty Meeting",
    "description": "Meeting with department heads",
    "date": "2025-11-25",
    "event_type": "MEETING",
    "creator": "user@example.com"
  }
]
```

### Detail Response
```json
{
  "id": 1,
  "title": "Faculty Meeting",
  "description": "Meeting with department heads",
  "date": "2025-11-25",
  "start_time": "14:00:00",
  "end_time": "16:00:00",
  "event_type": "MEETING",
  "venue": "Conference Room A",
  "created_by": 1,
  "creator": "user@example.com",
  "creator_email": "user@example.com",
  "created_at": "2024-12-05T12:00:00Z",
  "updated_at": "2024-12-05T12:00:00Z"
}
```

## Frontend Integration Notes

The frontend currently uses dummy data. To connect it to the backend:

1. **Update `CalendarPage.vue`:**
   - Replace hardcoded `events` array with API call to `GET /api/events/`
   - Use `date` field from response (format: YYYY-MM-DD)
   - Map date format: Backend uses `YYYY-MM-DD`, frontend uses `YYYY/MM/DD`
   - Filter events by selected date using `?date=YYYY-MM-DD` parameter

2. **Update Event Creation:**
   - Submit form data to `POST /api/events/` with title, description, date
   - Include optional fields: start_time, end_time, event_type, venue
   - Include JWT token in Authorization header

3. **Date Format Conversion:**
   - Backend accepts: `YYYY-MM-DD` or `YYYY/MM/DD`
   - Frontend uses: `YYYY/MM/DD`
   - Convert between formats as needed

4. **Event Type Mapping:**
   - Backend uses: `MEETING`, `WORKSHOP`, `SEMINAR`, `MAINTENANCE`
   - Map to frontend display names as needed

## Files Created/Modified

### New Files:
- `backend/calendar/__init__.py`
- `backend/calendar/apps.py`
- `backend/calendar/models.py`
- `backend/calendar/serializers.py`
- `backend/calendar/views.py`
- `backend/calendar/urls.py`
- `backend/calendar/admin.py`
- `backend/calendar/tests.py`
- `backend/calendar/migrations/__init__.py`

### Modified Files:
- `backend/config/settings.py` - Added calendar app
- `backend/config/urls.py` - Added calendar URLs

## Database Schema

After migrations, the `calendar_event` table will have:
- `id` (Primary Key)
- `title` (VARCHAR)
- `description` (TEXT)
- `date` (DATE)
- `start_time` (TIME, nullable)
- `end_time` (TIME, nullable)
- `event_type` (VARCHAR, nullable)
- `venue` (VARCHAR, nullable)
- `created_by_id` (ForeignKey to accounts_user)
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

## Testing the Implementation

1. **Create migrations:**
   ```bash
   python manage.py makemigrations calendar
   python manage.py migrate
   ```

2. **Test via Django Admin:**
   - Go to `http://localhost:8000/admin/`
   - Events should be available under "CALENDAR"
   - Create an event and verify it appears

3. **Test via API:**
   - Get JWT token from `/api/auth/login/`
   - Create an event via `POST /api/events/`
   - List events filtered by date
   - Verify date filtering works correctly

## Notes

- Date format is flexible: accepts both `YYYY-MM-DD` and `YYYY/MM/DD`
- Events are ordered by date and start_time
- All authenticated users can view all events
- Only creator or admin can modify/delete events
- Optional fields (time, type, venue) can be omitted
- Search works on title, description, and venue
- Date range filtering supports `date_from` and `date_to` parameters

