# Testing Guide - Document Management System

This guide will help you test if the Document Management System is working correctly.

## 🚀 Quick Start (Fastest Way to Test)

**Option 1: Automated Test Script (Recommended)**
```bash
cd Division-Information-Management-System/backend

# 1. Create migrations and migrate
python manage.py makemigrations documents
python manage.py migrate

# 2. Create a superuser (if needed)
python manage.py createsuperuser
# Email: admin@test.com, Password: testpass123

# 3. Start server (in one terminal)
python manage.py runserver

# 4. Run automated tests (in another terminal)
python test_documents_api.py
```

The script will automatically test all endpoints and show you results!

---

**Option 2: Manual Testing via Django Admin**
```bash
cd Division-Information-Management-System/backend
python manage.py makemigrations documents
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Then visit: `http://127.0.0.1:8000/admin/` and check the Documents section.

---

## Prerequisites

1. Python environment with Django installed
2. Database set up (SQLite3 or PostgreSQL)
3. Virtual environment activated (recommended)

---

## Step 1: Create and Run Migrations

First, create the database tables:

```bash
cd Division-Information-Management-System/backend
python manage.py makemigrations documents
python manage.py migrate
```

**Expected Output:**
- You should see messages about creating migrations
- Migration files created in `documents/migrations/`
- Database tables created successfully

---

## Step 2: Create a Test User (if needed)

If you don't have a user yet, create one:

### Option A: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
- Email: `admin@test.com`
- Password: (choose a password)

### Option B: Create Regular User via Django Shell
```bash
python manage.py shell
```

Then run:
```python
from accounts.models import User

# Create an admin user
admin = User.objects.create_user(
    email='admin@test.com',
    password='testpass123',
    role=User.Role.ADMIN
)

# Create a staff user
staff = User.objects.create_user(
    email='staff@test.com',
    password='testpass123',
    role=User.Role.STAFF
)

# Create a faculty user
faculty = User.objects.create_user(
    email='faculty@test.com',
    password='testpass123',
    role=User.Role.FACULTY
)

print("Users created successfully!")
exit()
```

---

## Step 3: Start the Development Server

```bash
python manage.py runserver
```

Server should start at `http://127.0.0.1:8000/`

---

## Step 4: Testing Methods

### Method 1: Django Admin Interface (Easiest)

1. **Access Admin Panel:**
   - Go to: `http://127.0.0.1:8000/admin/`
   - Login with superuser credentials

2. **Check Documents App:**
   - You should see "DOCUMENTS" section in the admin
   - Click on "Documents" to see the list (will be empty initially)

3. **Create a Test Document:**
   - Click "Add Document"
   - Fill in the form:
     - Name: "Test Document"
     - File: Upload a test file (PDF, DOCX, etc.)
     - Document Type: Choose from dropdown
     - Access Level: Choose from dropdown
     - Description: "This is a test document"
     - Uploaded By: Select a user
   - Click "Save"

4. **Verify:**
   - Document should appear in the list
   - Click on it to see details

**✅ Success Indicator:** You can see and manage documents in admin panel

---

### Method 2: Django REST Framework Browsable API

1. **Get JWT Token:**
   - Go to: `http://127.0.0.1:8000/api/auth/login/`
   - Enter credentials:
     ```json
     {
       "email": "admin@test.com",
       "password": "testpass123"
     }
     ```
   - Click "POST" button
   - **Copy the `access` token** from the response

2. **Test List Documents:**
   - Go to: `http://127.0.0.1:8000/api/documents/`
   - You should see an empty list: `[]`
   - Click "GET" button

3. **Test Upload Document:**
   - Scroll down to "Raw data" or "HTML form"
   - Enter data:
     ```json
     {
       "name": "Test Document",
       "document_type": "PUBLICATION",
       "access_level": "PUBLIC",
       "description": "Test upload via API"
     }
     ```
   - **Note:** File upload requires using the HTML form or a tool like Postman

**✅ Success Indicator:** API endpoints are accessible and returning data

---

### Method 3: Using curl (Command Line)

#### 3.1 Get JWT Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "testpass123"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {...}
}
```

**Save the `access` token!**

#### 3.2 List Documents
```bash
curl -X GET http://127.0.0.1:8000/api/documents/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

#### 3.3 Upload Document
```bash
curl -X POST http://127.0.0.1:8000/api/documents/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -F "name=Test Document" \
  -F "file=@/path/to/your/file.pdf" \
  -F "document_type=PUBLICATION" \
  -F "access_level=PUBLIC" \
  -F "description=Uploaded via curl"
```

Replace:
- `YOUR_ACCESS_TOKEN_HERE` with the token from step 3.1
- `/path/to/your/file.pdf` with actual file path

#### 3.4 Get Document Details
```bash
curl -X GET http://127.0.0.1:8000/api/documents/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

#### 3.5 Download Document
```bash
curl -X GET http://127.0.0.1:8000/api/documents/1/download/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  --output downloaded_file.pdf
```

**✅ Success Indicator:** Commands execute without errors and return JSON/data

---

### Method 4: Using Python Requests (Script)

Create a test script `test_documents.py`:

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Step 1: Login
print("1. Logging in...")
login_response = requests.post(
    f"{BASE_URL}/api/auth/login/",
    json={
        "email": "admin@test.com",
        "password": "testpass123"
    }
)
token = login_response.json()["access"]
print(f"✓ Token obtained: {token[:20]}...")

headers = {
    "Authorization": f"Bearer {token}"
}

# Step 2: List Documents
print("\n2. Listing documents...")
list_response = requests.get(
    f"{BASE_URL}/api/documents/",
    headers=headers
)
print(f"✓ Found {len(list_response.json())} documents")
print(json.dumps(list_response.json(), indent=2))

# Step 3: Upload Document
print("\n3. Uploading document...")
with open("test_file.txt", "w") as f:
    f.write("This is a test file content")

upload_data = {
    "name": "Test Document from Python",
    "document_type": "MEMOS",
    "access_level": "PUBLIC",
    "description": "Uploaded via Python script"
}
files = {
    "file": ("test_file.txt", open("test_file.txt", "rb"), "text/plain")
}

upload_response = requests.post(
    f"{BASE_URL}/api/documents/",
    headers=headers,
    data=upload_data,
    files=files
)
doc_id = upload_response.json()["id"]
print(f"✓ Document uploaded with ID: {doc_id}")

# Step 4: Get Document Details
print(f"\n4. Getting document {doc_id} details...")
detail_response = requests.get(
    f"{BASE_URL}/api/documents/{doc_id}/",
    headers=headers
)
print("✓ Document details:")
print(json.dumps(detail_response.json(), indent=2))

# Step 5: Test Search
print("\n5. Testing search...")
search_response = requests.get(
    f"{BASE_URL}/api/documents/?search=Test",
    headers=headers
)
print(f"✓ Found {len(search_response.json())} documents matching 'Test'")

print("\n✅ All tests completed successfully!")
```

Run it:
```bash
cd Division-Information-Management-System/backend
python test_documents.py
```

**✅ Success Indicator:** Script runs without errors and prints success messages

---

### Method 5: Using Postman

1. **Setup:**
   - Import or create a new request collection
   - Set base URL: `http://127.0.0.1:8000`

2. **Get Token:**
   - POST to `/api/auth/login/`
   - Body (raw JSON):
     ```json
     {
       "email": "admin@test.com",
       "password": "testpass123"
     }
     ```
   - Save the `access` token as an environment variable

3. **Create Request Collection:**
   
   **Request 1: List Documents**
   - Method: GET
   - URL: `{{base_url}}/api/documents/`
   - Headers:
     - `Authorization: Bearer {{access_token}}`

   **Request 2: Upload Document**
   - Method: POST
   - URL: `{{base_url}}/api/documents/`
   - Headers:
     - `Authorization: Bearer {{access_token}}`
   - Body: form-data
     - `name`: "Test Document"
     - `file`: [Select File]
     - `document_type`: "PUBLICATION"
     - `access_level`: "PUBLIC"
     - `description`: "Test upload"

   **Request 3: Get Document**
   - Method: GET
   - URL: `{{base_url}}/api/documents/1/`
   - Headers:
     - `Authorization: Bearer {{access_token}}`

   **Request 4: Download Document**
   - Method: GET
   - URL: `{{base_url}}/api/documents/1/download/`
   - Headers:
     - `Authorization: Bearer {{access_token}}`

---

## Step 5: Test Access Control

Test that permissions work correctly:

### Test Case 1: Public Access
1. Login as Faculty user
2. Create a document with `access_level: PUBLIC`
3. Login as Staff user
4. Try to GET the document → Should succeed ✅
5. Try to DELETE the document → Should fail (not owner) ❌

### Test Case 2: Permitted Access
1. Login as Staff user
2. Create a document with `access_level: PERMITTED`
3. Login as Faculty user
4. Try to GET the document → Should fail ❌
5. Login as Admin user
6. Try to GET the document → Should succeed ✅

### Test Case 3: Restricted Access
1. Login as Faculty user
2. Create a document with `access_level: RESTRICTED`
3. Login as Staff user
4. Try to GET the document → Should fail ❌
5. Login as Faculty user (owner)
6. Try to GET the document → Should succeed ✅
7. Login as Admin user
8. Try to GET the document → Should succeed ✅

---

## Step 6: Test Search and Filtering

### Test Search:
```bash
curl -X GET "http://127.0.0.1:8000/api/documents/?search=research" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test Type Filter:
```bash
curl -X GET "http://127.0.0.1:8000/api/documents/?type=PUBLICATION" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test Access Filter:
```bash
curl -X GET "http://127.0.0.1:8000/api/documents/?access=PUBLIC" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test Combined Filters:
```bash
curl -X GET "http://127.0.0.1:8000/api/documents/?type=PUBLICATION&access=PUBLIC&search=test" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Step 7: Verify File Storage

1. **Check Media Directory:**
   ```bash
   cd Division-Information-Management-System/backend
   ls -la media/documents/
   ```
   
   You should see folders organized by user ID:
   ```
   media/
     documents/
       1/          # User ID 1's documents
          file1.pdf
          file2.docx
       2/          # User ID 2's documents
          file3.pdf
   ```

2. **Verify Files:**
   - Upload a document via API
   - Check if file exists in `media/documents/{user_id}/`
   - File should be accessible

---

## Common Issues and Solutions

### Issue 1: "ModuleNotFoundError: No module named 'django'"
**Solution:** Activate your virtual environment or install Django
```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
```

### Issue 2: "No such table: documents_document"
**Solution:** Run migrations
```bash
python manage.py makemigrations documents
python manage.py migrate
```

### Issue 3: "401 Unauthorized" when accessing endpoints
**Solution:** 
- Check if you included the Authorization header
- Verify the token is valid (not expired)
- Login again to get a new token

### Issue 4: "403 Forbidden" when accessing documents
**Solution:**
- Check document access_level
- Verify user role has permission
- Check if user is the document owner

### Issue 5: Files not uploading
**Solution:**
- Check file size limits
- Verify media directory exists and is writable
- Check Django settings for MEDIA_ROOT and MEDIA_URL

### Issue 6: "Cannot find path" for media files
**Solution:**
- Ensure `MEDIA_ROOT` is set in settings.py
- Create the media directory if it doesn't exist:
  ```bash
  mkdir -p backend/media/documents
  ```

---

## Quick Test Checklist

- [ ] Migrations created and applied
- [ ] Server starts without errors
- [ ] Can login and get JWT token
- [ ] Can list documents (empty initially)
- [ ] Can upload a document
- [ ] Can retrieve document details
- [ ] Can download document file
- [ ] Can search documents
- [ ] Can filter by type
- [ ] Can filter by access level
- [ ] Access control works (public/permitted/restricted)
- [ ] Only owner/admin can edit/delete
- [ ] Files stored in correct location
- [ ] Django admin shows documents

---

## Success Criteria

✅ **System is working if:**
1. All API endpoints respond correctly
2. Documents can be uploaded and retrieved
3. Files are stored and downloadable
4. Access control works as expected
5. Search and filtering work
6. No errors in server logs

---

## Next Steps

Once testing is successful:
1. Connect frontend to these APIs
2. Replace dummy data in Vue components
3. Test end-to-end user flows
4. Add file validation (size, type)
5. Consider adding pagination for large document lists

