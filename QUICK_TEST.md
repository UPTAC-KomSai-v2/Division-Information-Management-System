# Quick Test - Document Management System

## The Fastest Way to Test (5 Steps)

### Step 1: Navigate to Backend
```bash
cd Division-Information-Management-System/backend
```

### Step 2: Create Database Tables
```bash
python manage.py makemigrations documents
python manage.py migrate
```

**Expected:** You should see messages like:
- `Migrations for 'documents': ...`
- `Applying documents.0001_initial... OK`

### Step 3: Create Admin User (if you don't have one)
```bash
python manage.py createsuperuser
```
Enter:
- Email: `admin@test.com`
- Password: `testpass123` (or your choice)

### Step 4: Start the Server

**Terminal 1:**
```bash
python manage.py runserver
```

Wait for: `Starting development server at http://127.0.0.1:8000/`

### Step 5: Run Automated Tests

**Terminal 2** (open a new terminal):
```bash
cd Division-Information-Management-System/backend
python test_documents_api.py
```

---

## ✅ Success Indicators

### If Everything Works:

1. **Migrations:**
   ```
   ✓ Creating migrations...
   ✓ Applying migrations...
   ```

2. **Server:**
   ```
   ✓ Starting development server at http://127.0.0.1:8000/
   ✓ Quit the server with CTRL-BREAK.
   ```

3. **Test Script Output:**
   ```
   ============================================================
     Document Management System - API Test Suite
   ============================================================
   
   ============================================================
     1. Testing Login
   ============================================================
   ✓ Login successful!
   
   ============================================================
     2. Testing List Documents
   ============================================================
   ✓ List documents successful!
   ✓ Found 0 document(s)
   
   ============================================================
     3. Testing Upload Document
   ============================================================
   ✓ Document uploaded successfully!
   ✓ Document ID: 1
   
   ... (more tests) ...
   
   ✅ All tests passed! Document Management System is working correctly.
   ```

---

## 🧪 Alternative: Manual Browser Test

### Test 1: Django Admin

1. Keep server running (Terminal 1)
2. Open browser: `http://127.0.0.1:8000/admin/`
3. Login with your superuser credentials
4. Click on **"Documents"** under DOCUMENTS section
5. Click **"Add Document"** button
6. Fill in the form and upload a file
7. Click **"Save"**

**✅ Success:** Document appears in the list!

### Test 2: API Browser

1. Get token:
   - Go to: `http://127.0.0.1:8000/api/auth/login/`
   - Enter email and password
   - Click POST button
   - Copy the `access` token

2. List documents:
   - Go to: `http://127.0.0.1:8000/api/documents/`
   - You should see an empty list: `[]`

**✅ Success:** API responds with empty list (no error)!

---

## 🔧 Troubleshooting

### Error: "No module named 'django'"
```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
```

### Error: "No such table: documents_document"
```bash
python manage.py makemigrations documents
python manage.py migrate
```

### Error: "Cannot connect to server"
- Make sure server is running in Terminal 1
- Check if port 8000 is available
- Try: `python manage.py runserver 8001` (use different port)

### Error: "401 Unauthorized"
- Check your email/password
- Make sure you're using the correct token
- Token expires after 30 minutes - get a new one

### Error: "403 Forbidden"
- Check document access_level
- Verify user role has permission
- Only owner/admin can edit/delete

---

## 📝 What Gets Tested

The automated test script checks:

1. ✅ User login and JWT token generation
2. ✅ Listing documents (empty initially)
3. ✅ Uploading a document
4. ✅ Retrieving document details
5. ✅ Searching documents
6. ✅ Filtering documents by type and access
7. ✅ Downloading document files

---

## 🎯 Next Steps After Testing

Once tests pass:

1. **Connect Frontend:**
   - Update `DocumentsPage.vue` to use API
   - Update `DocUploadPage.vue` to upload files
   - Replace dummy data with real API calls

2. **Add Validation:**
   - File size limits
   - File type restrictions
   - Better error messages

3. **Enhance Features:**
   - Pagination for large lists
   - Document categories/tags
   - Version control
   - Document preview

---

## 📚 More Details

- Full testing guide: `TESTING_GUIDE.md`
- API documentation: `DOCUMENTS_IMPLEMENTATION.md`
- Backend TODO: `BACKEND_TODO.md`

