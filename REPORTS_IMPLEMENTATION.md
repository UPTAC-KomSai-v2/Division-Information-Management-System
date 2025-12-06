# Report Generation System - Implementation Complete ✅

## Overview
The Report Generation System has been fully implemented. This system allows users to generate faculty activity reports with date range filtering and export to PDF/Excel formats.

## What Was Implemented

### 1. **Django App: `reports`**
   - Created complete Django app structure
   - All necessary files (models, views, serializers, URLs, admin)

### 2. **Models**

   **FacultyActivity Model** (`backend/reports/models.py`):
   - Tracks faculty activity metrics for reporting
   - Fields: faculty, unit, publications_count, service_hours, trainings_attended
   - Period tracking (period_start, period_end)
   
   **Report Model** (`backend/reports/models.py`):
   - Stores generated reports metadata
   - Fields: report_type, title, date_from, date_to, unit_filter
   - Stores report data as JSON (optional caching)

### 3. **Report Generation Logic**

   The system generates reports by aggregating data from:
   - **Publications**: Count of PUBLICATION documents uploaded by faculty
   - **Service Hours**: Estimated from events created/attended by faculty
   - **Trainings Attended**: Count of WORKSHOP/SEMINAR events
   - **Unit**: Department/unit from user profile

### 4. **API Endpoints**

   All endpoints require JWT authentication.

   **Base URL:** `/api/reports/`

   - **POST `/api/reports/generate/`** - Generate a new report
     - Body (JSON):
       ```json
       {
         "date_from": "2024-01-01",
         "date_to": "2024-12-31",
         "unit": "Meeting",  // Optional: filter by event type
         "title": "Q1 2024 Report"  // Optional
       }
       ```
   
   - **GET `/api/reports/`** - List generated reports
   
   - **GET `/api/reports/{id}/`** - Get report details with data
   
   - **GET `/api/reports/{id}/export/?format=pdf`** - Export to PDF
   
   - **GET `/api/reports/{id}/export/?format=excel`** - Export to Excel

### 5. **Export Functionality**

   **PDF Export:**
   - Uses ReportLab library
   - Formatted tables with headers
   - Includes report title and metadata
   - Requires: `pip install reportlab`

   **Excel Export:**
   - Uses openpyxl library
   - Formatted spreadsheets with headers
   - Includes report title and metadata
   - Requires: `pip install openpyxl`

### 6. **Features**

   - ✅ Date range filtering
   - ✅ Unit/event type filtering
   - ✅ Aggregates data from documents and events
   - ✅ PDF export support
   - ✅ Excel export support
   - ✅ Report data caching (JSON storage)
   - ✅ Django admin interface

## Next Steps: Installation & Setup

### 1. Register App & Run Migrations

```bash
cd Division-Information-Management-System/backend
python manage.py makemigrations reports
python manage.py migrate
```

### 2. Install Export Libraries (Optional)

For PDF export:
```bash
python -m pip install reportlab
```

For Excel export:
```bash
python -m pip install openpyxl
```

**Note:** Export features will still work without these libraries, but will return helpful error messages prompting installation.

## Example API Usage

### 1. Generate Report
```bash
POST /api/reports/generate/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "unit": "Workshop",
  "title": "Annual Faculty Activity Report 2024"
}
```

**Response:**
```json
{
  "report": {
    "id": 1,
    "report_type": "FACULTY_ACTIVITY",
    "title": "Annual Faculty Activity Report 2024",
    "date_from": "2024-01-01",
    "date_to": "2024-12-31",
    "unit_filter": "Workshop",
    "generated_by": 1,
    "generated_at": "2024-12-05T12:00:00Z"
  },
  "data": [
    {
      "facultyName": "John Doe",
      "unit": "Computer Science",
      "publications": 5,
      "serviceHours": 32.0,
      "trainingsAttended": 3,
      "faculty_id": 1
    }
  ]
}
```

### 2. List Reports
```bash
GET /api/reports/
Authorization: Bearer <your_access_token>
```

### 3. Get Report Details
```bash
GET /api/reports/1/
Authorization: Bearer <your_access_token>
```

### 4. Export to PDF
```bash
GET /api/reports/1/export/?format=pdf
Authorization: Bearer <your_access_token>
```

### 5. Export to Excel
```bash
GET /api/reports/1/export/?format=excel
Authorization: Bearer <your_access_token>
```

## Report Data Structure

The report data array contains objects with:
- `facultyName` - Full name of faculty member
- `unit` - Department/unit name
- `publications` - Number of publications (from documents)
- `serviceHours` - Estimated service hours (from events)
- `trainingsAttended` - Number of trainings attended (from events)
- `faculty_id` - User ID of faculty member

## How Data is Calculated

1. **Publications**: Count of documents with type=PUBLICATION uploaded by faculty in date range
2. **Service Hours**: Estimated from events (default: 2 hours per event)
3. **Trainings Attended**: Count of events with type=WORKSHOP or SEMINAR
4. **Unit**: User's department or position field

## Frontend Integration Notes

The frontend expects this data structure. To connect:

1. **Update `DashPage.vue`:**
   - Replace hardcoded `rows` array with API call to `POST /api/reports/generate/`
   - Use `data` array from response for table rows
   - Handle date_from and date_to from form inputs
   - Handle unit filter from dropdown

2. **Report Generation:**
   - Submit form data to `POST /api/reports/generate/`
   - Display report data in the table
   - Show report preview with generated data

3. **Export Buttons:**
   - PDF button: Link to `/api/reports/{id}/export/?format=pdf`
   - Excel button: Link to `/api/reports/{id}/export/?format=excel`

## Files Created/Modified

### New Files:
- `backend/reports/__init__.py`
- `backend/reports/apps.py`
- `backend/reports/models.py`
- `backend/reports/serializers.py`
- `backend/reports/views.py`
- `backend/reports/urls.py`
- `backend/reports/admin.py`
- `backend/reports/tests.py`
- `backend/reports/migrations/__init__.py`

### Modified Files:
- `backend/config/settings.py` - Added reports app
- `backend/config/urls.py` - Added reports URLs
- `backend/requirements.txt` - Added optional export libraries

## Database Schema

After migrations, two new tables:

**`reports_facultyactivity`**:
- `id`, `faculty_id`, `unit`, `publications_count`, `service_hours`, `trainings_attended`
- `period_start`, `period_end`, `created_at`, `updated_at`

**`reports_report`**:
- `id`, `report_type`, `title`, `date_from`, `date_to`, `unit_filter`
- `generated_by_id`, `generated_at`, `report_data` (JSON)

## Testing the Implementation

1. **Create migrations:**
   ```bash
   python manage.py makemigrations reports
   python manage.py migrate
   ```

2. **Test via API:**
   - Get JWT token
   - Generate a report with date range
   - Verify report data is returned correctly
   - Test export endpoints (after installing libraries)

## Notes

- Report generation aggregates data from existing models (Documents, Events)
- Service hours are estimated (2 hours per event) - can be customized
- Unit filter filters by event type when calculating metrics
- PDF/Excel export requires additional libraries (install as needed)
- Report data is cached in JSON field for faster retrieval
- Faculty must have role=FACULTY to appear in reports

## Future Enhancements

- Add manual FacultyActivity entries via admin
- More accurate service hours calculation
- Additional report types
- Scheduled report generation
- Email report delivery
- Custom report templates

