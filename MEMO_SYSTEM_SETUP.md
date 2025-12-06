# Memo Management System - Setup Guide

## ✅ Implementation Complete

The Memo Management System has been successfully implemented! This includes both **Memos** and **Circulars** management.

## What Was Implemented

### 1. **Memo Model**
- Auto-generated `memo_id` (MEMO-001, MEMO-002, etc.)
- Title, description
- Created by (author)
- Requires acknowledgment (`reqs_ack`)
- Target department and roles
- Published at timestamp
- Created/updated timestamps

### 2. **Circular Model**
- Auto-generated `circular_id` (CIRC-001, CIRC-002, etc.)
- Same structure as Memo
- Separate management from Memos

### 3. **API Endpoints**

#### Memos:
- `GET /api/memos/` - List all memos (with filtering)
- `POST /api/memos/` - Create new memo
- `GET /api/memos/{id}/` - Get memo details
- `PUT/PATCH /api/memos/{id}/` - Update memo
- `DELETE /api/memos/{id}/` - Delete memo
- `POST /api/memos/{id}/publish/` - Publish memo
- `POST /api/memos/{id}/unpublish/` - Unpublish memo

#### Circulars:
- `GET /api/circulars/` - List all circulars (with filtering)
- `POST /api/circulars/` - Create new circular
- `GET /api/circulars/{id}/` - Get circular details
- `PUT/PATCH /api/circulars/{id}/` - Update circular
- `DELETE /api/circulars/{id}/` - Delete circular
- `POST /api/circulars/{id}/publish/` - Publish circular
- `POST /api/circulars/{id}/unpublish/` - Unpublish circular

### 4. **Filtering & Search**

**Query Parameters:**
- `search` - Search in title, description, ID, department
- `department` - Filter by target department
- `role` - Filter by target role (ADMIN, STAFF, FACULTY)
- `reqs_ack` - Filter by acknowledgment requirement (true/false)
- `published` - Filter by published status (true/false)
- `date_from` - Filter from date (YYYY-MM-DD)
- `date_to` - Filter to date (YYYY-MM-DD)

### 5. **Django Admin**
- Both Memos and Circulars are registered in admin
- Checkbox interface for Target Roles
- Full CRUD operations
- Search and filtering capabilities

## Next Steps: Create Migrations

Run these commands to create database tables:

```bash
cd D:\CmSC 135\Division-Information-Management-System\backend
python manage.py makemigrations memos
python manage.py migrate
```

**Expected Output:**
```
Migrations for 'memos':
  memos/migrations/0001_initial.py
    - Create model Memo
    - Create model Circular

Running migrations:
  Applying memos.0001_initial... OK
```

## Verify Installation

### 1. Check Admin Panel
1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with your admin account
3. You should see:
   - **MEMOS** section with:
     - Memos
     - Circulars

### 2. Test API Endpoints

#### List Memos
```
GET http://127.0.0.1:8000/api/memos/
Authorization: Bearer YOUR_TOKEN
```

#### Create a Memo
```
POST http://127.0.0.1:8000/api/memos/
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
  "title": "Important Memo",
  "description": "This is an important memo",
  "target_department": "IT Department",
  "target_roles": ["ADMIN", "STAFF"],
  "reqs_ack": true
}
```

#### Create a Circular
```
POST http://127.0.0.1:8000/api/circulars/
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
  "title": "General Announcement",
  "description": "This is a circular announcement",
  "target_department": "All Departments",
  "target_roles": ["ADMIN", "STAFF", "FACULTY"],
  "reqs_ack": false
}
```

## Features

1. **Auto-Generated IDs**: Memos get MEMO-001, MEMO-002, etc. Circulars get CIRC-001, CIRC-002, etc.
2. **Acknowledgment Tracking**: Track which memos/circulars require acknowledgment
3. **Targeting**: Specify target department and roles
4. **Publishing Control**: Draft and published states
5. **Search & Filter**: Comprehensive filtering options
6. **Permission Control**: Only creator or admin can modify
7. **Admin Interface**: User-friendly Django admin with checkboxes for roles

## Database Tables

After migration, you'll have:
- `memos_memo` - Memo records
- `memos_circular` - Circular records

## Notes

- All endpoints require JWT authentication
- Target roles are stored as JSON array (e.g., ["ADMIN", "STAFF"])
- Published status is based on `published_at` timestamp
- Auto-generated IDs cannot be manually set

