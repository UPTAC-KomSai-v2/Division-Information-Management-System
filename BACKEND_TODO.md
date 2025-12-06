# Backend Implementation Guide

This document outlines what needs to be implemented in the backend for the Division Information Management System (DIMS).

## Current Status
- ✅ **Authentication**: User model and JWT authentication are implemented
- ❌ **All other features**: Need complete backend implementation

---

## Priority 1: Core Features (Essential for Basic Functionality)

### 1. **Document Management System**
**What the frontend expects:**
- List documents with: name, type, access status
- Upload documents
- Search/filter documents
- Access levels: Public, Permitted, Restricted
- Document types: Publication, Memos, Awards

**Backend tasks:**
1. Create `documents` Django app
2. Create `Document` model with fields:
   - `name` (CharField)
   - `file` (FileField) - store uploaded files
   - `document_type` (CharField with choices: Publication, Memos, Awards)
   - `access_level` (CharField with choices: Public, Permitted, Restricted)
   - `uploaded_by` (ForeignKey to User)
   - `created_at` (DateTimeField)
   - `updated_at` (DateTimeField)
   - `description` (TextField, optional)
3. Create migrations
4. Create API endpoints:
   - `GET /api/documents/` - List documents (with search/filter)
   - `POST /api/documents/` - Upload document
   - `GET /api/documents/{id}/` - Get document details
   - `GET /api/documents/{id}/download/` - Download document
   - `PUT/PATCH /api/documents/{id}/` - Update document
   - `DELETE /api/documents/{id}/` - Delete document
5. Configure file storage (media files)
6. Implement permission checks based on access_level

---

### 2. **Support Tickets System**
**What the frontend expects:**
- Create tickets with: title, description
- List tickets with: ID, title, status, creator, date
- Status values: Open, In Progress, Closed/Resolved
- Search tickets

**Backend tasks:**
1. Create `tickets` Django app
2. Create `Ticket` model with fields:
   - `ticket_id` (CharField, unique) - auto-generated (e.g., "TCK-001")
   - `title` (CharField)
   - `description` (TextField)
   - `status` (CharField with choices: Open, In Progress, Closed)
   - `created_by` (ForeignKey to User)
   - `assigned_to` (ForeignKey to User, nullable)
   - `created_at` (DateTimeField)
   - `updated_at` (DateTimeField)
   - `priority` (CharField, optional: Low, Medium, High, Urgent)
3. Create migrations
4. Create API endpoints:
   - `GET /api/tickets/` - List tickets (filter by status, search)
   - `POST /api/tickets/` - Create ticket
   - `GET /api/tickets/{id}/` - Get ticket details
   - `PATCH /api/tickets/{id}/` - Update ticket (status, assign, etc.)
   - `DELETE /api/tickets/{id}/` - Delete ticket (admin only)

---

### 3. **Calendar/Events System**
**What the frontend expects:**
- List events by date
- Event fields: date, title, description
- Create events
- View events for specific dates

**Backend tasks:**
1. Create `calendar` Django app
2. Create `Event` model with fields:
   - `title` (CharField)
   - `description` (TextField)
   - `date` (DateField)
   - `start_time` (TimeField, optional)
   - `end_time` (TimeField, optional)
   - `created_by` (ForeignKey to User)
   - `created_at` (DateTimeField)
   - `event_type` (CharField, optional: Meeting, Workshop, Seminar, Maintenance)
   - `venue` (CharField, optional)
3. Create migrations
4. Create API endpoints:
   - `GET /api/events/` - List events (filter by date range)
   - `POST /api/events/` - Create event
   - `GET /api/events/{id}/` - Get event details
   - `PUT/PATCH /api/events/{id}/` - Update event
   - `DELETE /api/events/{id}/` - Delete event

---

### 4. **Memo Management System**
**What the frontend expects:**
- List memos with: title, description, author, date
- Create memos
- Manage circulars (similar to memos)
- Search/filter memos and circulars
- Track acknowledgment requirements

**Backend tasks:**
1. Create `memos` Django app
2. Create `Memo` model with fields:
   - `memo_id` (CharField, unique) - auto-generated identifier
   - `title` (CharField)
   - `description` (TextField)
   - `created_by` (ForeignKey to User)
   - `created_at` (DateTimeField)
   - `updated_at` (DateTimeField)
   - `reqs_ack` (BooleanField) - requires acknowledgment
   - `target_department` (CharField, optional)
   - `target_roles` (JSONField, optional) - list of target roles
   - `published_at` (DateTimeField, optional)
3. Create `Circular` model (similar structure to Memo):
   - `circular_id` (CharField, unique)
   - `title` (CharField)
   - `description` (TextField)
   - `created_by` (ForeignKey to User)
   - `created_at` (DateTimeField)
   - `updated_at` (DateTimeField)
   - `reqs_ack` (BooleanField)
   - `target_department` (CharField, optional)
   - `target_roles` (JSONField, optional)
   - `published_at` (DateTimeField, optional)
4. Create migrations
5. Create API endpoints:
   - `GET /api/memos/` - List memos (with search/filter)
   - `POST /api/memos/` - Create memo
   - `GET /api/memos/{id}/` - Get memo details
   - `PUT/PATCH /api/memos/{id}/` - Update memo
   - `DELETE /api/memos/{id}/` - Delete memo
   - `GET /api/circulars/` - List circulars (with search/filter)
   - `POST /api/circulars/` - Create circular
   - `GET /api/circulars/{id}/` - Get circular details
   - `PUT/PATCH /api/circulars/{id}/` - Update circular
   - `DELETE /api/circulars/{id}/` - Delete circular
6. Implement permission checks (creator or admin can modify)
7. Add filtering by department, role, date range

---

## Priority 2: User & Communication Features

### 4. **User Profile/Directory System**
**What the frontend expects:**
- List users with: name, email, role, status
- User status: Active, Inactive, On Leave
- Search users
- Avatar/initials support

**Backend tasks:**
1. Extend `User` model in `accounts` app (or create `Profile` model):
   - `first_name` (CharField)
   - `last_name` (CharField)
   - `phone` (CharField, optional)
   - `department` (CharField, optional)
   - `position` (CharField, optional)
   - `avatar` (ImageField, optional)
   - `status` (CharField: Active, Inactive, On Leave)
   - `bio` (TextField, optional)
2. Create migrations
3. Create API endpoints:
   - `GET /api/users/` - List users (directory)
   - `GET /api/users/{id}/` - Get user profile
   - `PATCH /api/users/{id}/` - Update profile (own profile or admin)
   - `GET /api/users/me/` - Get own profile (already have `/api/auth/me/` - may need to extend)

---

### 5. **Messaging System**
**What the frontend expects:**
- Private chats (one-on-one)
- Group chats
- Starred conversations
- Contact list
- Message settings (privacy, notifications)

**Backend tasks:**
1. Create `messages` Django app
2. Create models:
   - `Conversation` model:
     - `conversation_type` (CharField: private, group)
     - `participants` (ManyToMany to User)
     - `created_at` (DateTimeField)
     - `updated_at` (DateTimeField)
   - `Message` model:
     - `conversation` (ForeignKey to Conversation)
     - `sender` (ForeignKey to User)
     - `content` (TextField)
     - `created_at` (DateTimeField)
     - `read_at` (DateTimeField, nullable)
   - `ConversationMember` (optional - for starred, muted, etc.):
     - `conversation` (ForeignKey)
     - `user` (ForeignKey)
     - `is_starred` (BooleanField)
     - `muted_until` (DateTimeField, nullable)
3. Create migrations
4. Create API endpoints:
   - `GET /api/conversations/` - List user's conversations
   - `POST /api/conversations/` - Create conversation
   - `GET /api/conversations/{id}/` - Get conversation with messages
   - `POST /api/conversations/{id}/messages/` - Send message
   - `PATCH /api/conversations/{id}/star/` - Star/unstar conversation
   - WebSocket support (optional, for real-time messaging)

---

## Priority 3: Reporting & Analytics

### 6. **Report Generation System**
**What the frontend expects:**
- Generate reports with date range
- Filter by unit (Meeting, Workshop, Seminar, Maintenance)
- Report fields: Faculty Name, Unit, Publications, Service Hours, Trainings Attended
- Export to PDF/Excel

**Backend tasks:**
1. Create `reports` Django app (or add to existing app)
2. Create models (if storing reports):
   - `Report` model:
     - `report_type` (CharField)
     - `date_from` (DateField)
     - `date_to` (DateField)
     - `unit` (CharField)
     - `generated_by` (ForeignKey to User)
     - `generated_at` (DateTimeField)
     - `data` (JSONField, optional - store report data)
3. Create API endpoints:
   - `POST /api/reports/generate/` - Generate report
   - `GET /api/reports/` - List generated reports
   - `GET /api/reports/{id}/` - Get report details
   - `GET /api/reports/{id}/export/?format=pdf` - Export to PDF
   - `GET /api/reports/{id}/export/?format=excel` - Export to Excel
4. Integrate PDF generation library (e.g., ReportLab, WeasyPrint)
5. Integrate Excel generation library (e.g., openpyxl, pandas)

---

## Additional Backend Tasks okay po

### 7. **User Management Enhancements**
- Add user registration endpoint (if needed)
- Add password reset functionality
- Add user activation/deactivation
- Admin endpoints for user management

### 8. **File Upload Configuration**
- Configure Django settings for media files:
  - `MEDIA_URL = '/media/'`
  - `MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`
- Set up file storage (local or cloud)
- Implement file validation (type, size limits)
 
### 9. **Permission System**
- Create custom permissions for each model
- Implement role-based access control (RBAC)
- Add permission checks in views/viewsets

### 10. **API Documentation**
- Set up Django REST Framework's browsable API
- Add API documentation (using drf-spectacular or similar)
- Document all endpoints with request/response examples

### 11. **Search Functionality**
- Implement full-text search (using PostgreSQL full-text search or Django SearchVector)
- Add search endpoints for documents, tickets, users, etc.

### 12. **Caching**
- Implement caching for frequently accessed data
- Cache user sessions, document lists, etc.

### 13. **Testing**
- Write unit tests for models
- Write API endpoint tests
- Write integration tests

### 14. **Error Handling**
- Custom exception handlers
- Consistent error response format
- Logging setup

---

## Recommended Implementation Order

1. **Start with Documents** - Most visible feature, relatively straightforward
2. **Then Tickets** - Essential for support functionality
3. **Calendar/Events** - Simple model, good for practice
4. **Memos** - Essential for managing Circulars/Memos in the Web App
5. **User Profiles** - Extend existing User model
6. **Directory** - Build on user profiles
7. **Messages** - More complex, requires WebSockets for real-time
8. **Reports** - Requires data from other models, export functionality

---

## Quick Start: Creating a New Feature

For each new feature, follow this pattern:

1. **Create Django app:**
   ```bash
   python manage.py startapp <app_name>
   ```

2. **Add to INSTALLED_APPS** in `settings.py`

3. **Create models** in `models.py`

4. **Create serializers** in `serializers.py`

5. **Create views/viewsets** in `views.py`

6. **Create URL routing** in `urls.py`

7. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Test endpoints** using Django REST Framework browsable API

---

## Database Considerations

Currently configured for PostgreSQL but SQLite3 file exists. Consider:
- Setting up PostgreSQL database (`dims_db`)
- Or continue with SQLite3 for development
- Use migrations for all schema changes
- Consider database indexes for frequently queried fields

---

## Notes

- All endpoints should use JWT authentication (already configured)
- Use Django REST Framework's ViewSets for CRUD operations
- Implement proper pagination for list endpoints
- Add filtering and ordering capabilities
- Use serializers for request/response validation
- Follow RESTful API conventions

