# Setup Communications System

## Steps to Set Up

### 1. Register the App (Already Done ✅)
The `communications` app has been added to `INSTALLED_APPS` in `settings.py`.

### 2. Create Migrations

Run these commands to create database tables:

```bash
cd D:\CmSC 135\Division-Information-Management-System\backend
python manage.py makemigrations communications
```

**Expected Output:**
```
Migrations for 'communications':
  communications/migrations/0001_initial.py
    - Create model Communication
    - Create model Memo
    - Create model Circular
    - Create model CommunicationDocument
    - Create model CommunicationEvent
```

### 3. Apply Migrations

```bash
python manage.py migrate
```

**Expected Output:**
```
Running migrations:
  Applying communications.0001_initial... OK
```

### 4. Restart Django Server

If your server is running, restart it:

```bash
# Stop the server (Ctrl+C)
# Then restart:
python manage.py runserver
```

## Verify Installation

### 1. Check Admin Panel

1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with your admin account
3. You should see:
   - **COMMUNICATIONS** section with:
     - Communications
     - Memos
     - Circulars
     - Communication Documents
     - Communication Events

### 2. Test API Endpoints

#### List Communications
```
GET http://127.0.0.1:8000/api/communications/
```

#### Create a Memo
```
POST http://127.0.0.1:8000/api/communications/
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
  "type": "MEMO",
  "title": "Test Memo",
  "description": "This is a test memo",
  "target_department": "IT",
  "target_roles": ["ADMIN", "STAFF"],
  "reqs_ack": true
}
```

## Database Tables Created

After migration, you'll have these tables:
- `communications_communication` (parent table)
- `communications_memo` (child table)
- `communications_circular` (child table)
- `communications_communicationdocument` (child table)
- `communications_communicationevent` (child table)

## Troubleshooting

### Issue: Migration errors
**Solution**: Make sure you've activated your virtual environment and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Module not found
**Solution**: Ensure the `communications` app is in `INSTALLED_APPS` in `settings.py`

### Issue: URLs not working
**Solution**: Check that `path('api/', include('communications.urls'))` is in `config/urls.py`

## Next Steps

1. Test creating communications of each type (Memo, Circular, Document, Event)
2. Test filtering and search functionality
3. Test publishing/unpublishing communications
4. Migrate existing documents if needed

