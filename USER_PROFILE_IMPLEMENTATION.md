# User Profile/Directory System - Implementation Complete ✅

## Overview
The User Profile/Directory System has been fully implemented. User profiles have been extended with additional fields, and directory listing/management APIs are available.

## What Was Implemented

### 1. **Extended User Model**
   Located in `backend/accounts/models.py`

   **New Profile Fields Added:**
   - `first_name` - User's first name
   - `last_name` - User's last name
   - `phone` - Phone number (optional)
   - `department` - Department/Unit (optional)
   - `position` - Job position/title (optional)
   - `avatar` - Profile picture (ImageField, optional)
   - `bio` - Biography/description (optional)
   - `status` - User status: Active, Inactive, On Leave
   - `date_joined` - Account creation date

   **Helper Methods:**
   - `get_full_name()` - Returns full name or email
   - `get_short_name()` - Returns first name or email
   - `initials` - Property that generates initials (e.g., "JD" for John Doe)

### 2. **API Endpoints**

   All endpoints require JWT authentication (access token in header).

   **Base URL:** `/api/users/`

   - **GET `/api/users/`** - List all users (directory)
     - Query parameters:
       - `search` - Search by email, name, department, or position
       - `role` - Filter by role (ADMIN, STAFF, FACULTY)
       - `status` - Filter by status (ACTIVE, INACTIVE, ON_LEAVE)
       - `department` - Filter by department
   
   - **GET `/api/users/{id}/`** - Get user profile details
   
   - **PATCH `/api/users/{id}/`** - Update user profile (own profile or admin only)
   
   - **PUT `/api/users/{id}/`** - Full update user profile

   **Existing Endpoint (Enhanced):**
   - **GET `/api/auth/me/`** - Get own profile (now includes all profile fields)

### 3. **Access Control**

   **Permission Rules:**
   - **All authenticated users** can view directory (list users)
   - **All authenticated users** can view individual user profiles
   - **Users** can update their own profile
   - **Admins** can update any user's profile
   - **Only admins** can delete users (via admin interface)

### 4. **Features**

   - ✅ Extended user profiles with personal information
   - ✅ Avatar/photo upload support
   - ✅ Directory listing with search and filters
   - ✅ User status tracking (Active, Inactive, On Leave)
   - ✅ Automatic initials generation
   - ✅ Full name display
   - ✅ Enhanced Django admin interface

## Next Steps: Running Migrations

To activate the User Profile extensions, you need to create and run migrations:

```bash
cd Division-Information-Management-System/backend
python manage.py makemigrations accounts
python manage.py migrate
```

**Note:** This will add new fields to existing users. All new fields are optional, so existing users won't be affected.

## Example API Usage

### 1. List Users (Directory)
```bash
GET /api/users/
Authorization: Bearer <your_access_token>

# With search
GET /api/users/?search=john

# With filters
GET /api/users/?role=STAFF&status=ACTIVE

# Filter by department
GET /api/users/?department=IT
```

### 2. Get User Profile
```bash
GET /api/users/1/
Authorization: Bearer <your_access_token>
```

### 3. Get Own Profile
```bash
GET /api/auth/me/
Authorization: Bearer <your_access_token>
```

### 4. Update Profile
```bash
PATCH /api/users/1/
Authorization: Bearer <your_access_token>
Content-Type: application/json

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

### 5. Upload Avatar
```bash
PATCH /api/users/1/
Authorization: Bearer <your_access_token>
Content-Type: multipart/form-data

{
  "avatar": <image_file>
}
```

## Response Format

### List Response (Directory)
```json
[
  {
    "id": 1,
    "email": "john.doe@example.com",
    "name": "John Doe",
    "initials": "JD",
    "role": "STAFF",
    "position": "Software Developer",
    "status": "ACTIVE",
    "avatar_url": "http://localhost:8000/media/avatars/1/profile.jpg"
  }
]
```

### Detail Response
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "name": "John Doe",
  "full_name": "John Doe",
  "initials": "JD",
  "role": "STAFF",
  "phone": "+1-234-567-8900",
  "department": "IT Department",
  "position": "Software Developer",
  "avatar": "/media/avatars/1/profile.jpg",
  "avatar_url": "http://localhost:8000/media/avatars/1/profile.jpg",
  "bio": "I love coding!",
  "status": "ACTIVE",
  "is_active": true
}
```

## Frontend Integration Notes

The frontend currently uses dummy data. To connect it to the backend:

1. **Update `DirectoryPage.vue`:**
   - Replace hardcoded `rows` array with API call to `GET /api/users/`
   - Use `name` field from response (automatically generated from first_name + last_name)
   - Use `initials` field from response for avatar display
   - Use `status` field from response
   - Use `role` field and map to display names
   - Use `avatar_url` if available, otherwise use initials with color

2. **Update `UserProfilePage.vue`:**
   - Fetch profile from `GET /api/auth/me/` or `GET /api/users/{id}/`
   - Display all profile fields
   - Allow editing and submit to `PATCH /api/users/{id}/`

3. **Status Mapping:**
   - Frontend uses: "Active", "Inactive", "On Leave"
   - Backend uses: "ACTIVE", "INACTIVE", "ON_LEAVE"
   - Map accordingly in frontend code

4. **Role Mapping:**
   - Backend: "ADMIN", "STAFF", "FACULTY"
   - Map to display names as needed

## Files Created/Modified

### Modified Files:
- `backend/accounts/models.py` - Added profile fields to User model
- `backend/accounts/serializers.py` - Extended serializers with profile fields
- `backend/accounts/views.py` - Added UserViewSet for directory and profile management
- `backend/accounts/admin.py` - Updated admin interface to show profile fields
- `backend/accounts/urls.py` - Created URL routing for user endpoints
- `backend/config/urls.py` - Added accounts URLs

## Database Schema Changes

After migrations, the `accounts_user` table will have new columns:
- `first_name` (VARCHAR, nullable)
- `last_name` (VARCHAR, nullable)
- `phone` (VARCHAR, nullable)
- `department` (VARCHAR, nullable)
- `position` (VARCHAR, nullable)
- `avatar` (VARCHAR, nullable) - file path
- `bio` (TEXT, nullable)
- `status` (VARCHAR) - defaults to "ACTIVE"
- `date_joined` (DATETIME)

## Testing the Implementation

1. **Create migrations:**
   ```bash
   python manage.py makemigrations accounts
   python manage.py migrate
   ```

2. **Test via Django Admin:**
   - Go to `http://localhost:8000/admin/`
   - Users should show new profile fields
   - Edit a user and add profile information

3. **Test via API:**
   - Get JWT token from `/api/auth/login/`
   - List users via `GET /api/users/`
   - Update profile via `PATCH /api/users/{id}/`
   - Verify search and filtering work

## Notes

- All new profile fields are optional
- Existing users will have empty/null values for new fields
- Avatar uploads are stored in `media/avatars/{user_id}/`
- Status defaults to "ACTIVE" for new users
- Users can only update their own profiles (admins can update any)
- Directory listing only shows active users by default
- Search works across email, name, department, and position

