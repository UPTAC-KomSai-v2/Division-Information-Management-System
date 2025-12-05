# Communications System Documentation

## Overview

The Communications System replaces the old "Documents" system with a more comprehensive parent-child model structure. This allows for better organization and management of different communication types (Circulars, Memos, Events, and Documents) in a single unified system.

## Architecture

### Parent Model: Communication
The `Communication` model serves as the parent table for all communication types.

**Fields:**
- `communicationID` - Primary key (auto-increment)
- `type` - Dropdown: CIRCULAR, MEMO, EVENT, DOCUMENT
- `title` - Communication title
- `description` - Communication description
- `created_by` - Foreign key to User (author)
- `created_at` - Timestamp when created
- `published_at` - Timestamp when published (nullable)
- `target_department` - Target department (optional)
- `target_roles` - JSON array of target roles (e.g., ['ADMIN', 'STAFF', 'FACULTY'])

### Child Models

#### 1. Memo
- `commID` - OneToOne Foreign Key to Communication
- `reqs_ack` - Boolean: Requires Acknowledgment

#### 2. Circular
- `commID` - OneToOne Foreign Key to Communication
- `reqs_ack` - Boolean: Requires Acknowledgment

#### 3. CommunicationDocument
- `commID` - OneToOne Foreign Key to Communication
- `document_ID` - Document identifier
- `route_to` - Routing information

#### 4. CommunicationEvent
- `commID` - OneToOne Foreign Key to Communication
- `start_date` - Event start date/time
- `end_date` - Event end date/time
- `location` - Event location

## Database Structure

```
Communication (Parent)
├── communicationID (PK)
├── type
├── title
├── description
├── created_by (FK → User)
├── created_at
├── published_at
├── target_department
└── target_roles (JSON)

Memo (Child)
├── commID (PK, FK → Communication)
└── reqs_ack

Circular (Child)
├── commID (PK, FK → Communication)
└── reqs_ack

CommunicationDocument (Child)
├── commID (PK, FK → Communication)
├── document_ID
└── route_to

CommunicationEvent (Child)
├── commID (PK, FK → Communication)
├── start_date
├── end_date
└── location
```

## API Endpoints

### Base URL
All endpoints are under `/api/communications/`

### List Communications
```
GET /api/communications/
```

**Query Parameters:**
- `search` - Search in title, description, department
- `type` - Filter by type (CIRCULAR, MEMO, EVENT, DOCUMENT)
- `department` - Filter by target department
- `role` - Filter by target role
- `published` - Filter by published status (true/false)
- `date_from` - Filter from date (YYYY-MM-DD)
- `date_to` - Filter to date (YYYY-MM-DD)

### Get Communication Details
```
GET /api/communications/{communicationID}/
```

### Create Communication
```
POST /api/communications/
```

**Request Body Example (Memo):**
```json
{
  "type": "MEMO",
  "title": "Important Memo",
  "description": "This is a memo",
  "target_department": "IT Department",
  "target_roles": ["ADMIN", "STAFF"],
  "reqs_ack": true
}
```

**Request Body Example (Circular):**
```json
{
  "type": "CIRCULAR",
  "title": "General Circular",
  "description": "This is a circular",
  "target_department": "All Departments",
  "target_roles": ["ADMIN", "STAFF", "FACULTY"],
  "reqs_ack": false
}
```

**Request Body Example (Document):**
```json
{
  "type": "DOCUMENT",
  "title": "Policy Document",
  "description": "New policy document",
  "target_department": "HR",
  "target_roles": ["ADMIN", "STAFF"],
  "document_ID": "DOC-2025-001",
  "route_to": "HR Department"
}
```

**Request Body Example (Event):**
```json
{
  "type": "EVENT",
  "title": "Division Meeting",
  "description": "Monthly division meeting",
  "target_department": "All Departments",
  "target_roles": ["ADMIN", "STAFF"],
  "start_date": "2025-12-10T09:00:00Z",
  "end_date": "2025-12-10T11:00:00Z",
  "location": "Conference Room A"
}
```

### Update Communication
```
PUT /api/communications/{communicationID}/
PATCH /api/communications/{communicationID}/
```

### Delete Communication
```
DELETE /api/communications/{communicationID}/
```

### Publish Communication
```
POST /api/communications/{communicationID}/publish/
```

### Unpublish Communication
```
POST /api/communications/{communicationID}/unpublish/
```

## Django Admin

All models are registered in the Django admin:

1. **Communications** - Main parent table
2. **Memos** - Child table for memos
3. **Circulars** - Child table for circulars
4. **Communication Documents** - Child table for documents
5. **Communication Events** - Child table for events

## Usage Notes

1. **One-to-One Relationship**: Each Communication can have exactly ONE child record of its type (one Memo, or one Circular, etc.)

2. **Type-Specific Data**: When creating a communication, provide the appropriate child model fields:
   - Memo/Circular: `reqs_ack`
   - Document: `document_ID`, `route_to`
   - Event: `start_date`, `end_date`, `location`

3. **Publishing**: Communications can be created as drafts and published later using the `/publish/` endpoint.

4. **Target Audience**: Use `target_department` for department filtering and `target_roles` (JSON array) for role-based targeting.

5. **Automatic Creation**: When creating a communication, the system automatically creates the appropriate child record based on the `type` field.

## Migration from Old Documents System

The old `documents` app remains in the system but is now separate. To migrate:

1. The new `communications` app uses a different structure
2. Old documents remain accessible via `/api/documents/`
3. New communications are available via `/api/communications/`
4. You can gradually migrate data or run both systems in parallel

