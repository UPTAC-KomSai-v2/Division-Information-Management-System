# Fix: events_event table doesn't exist

## Problem
You're getting this error:
```
OperationalError: no such table: events_event
```

## Cause
The database table for the Events model hasn't been created yet. You need to create and run migrations.

## Solution - Run These Commands

### Step 1: Create Migrations for Events
```bash
cd D:\CmSC 135\Division-Information-Management-System\backend
python manage.py makemigrations events
```

**Expected Output:**
```
Migrations for 'events':
  events/migrations/0001_initial.py
    - Create model Event
```

### Step 2: Apply Migrations
```bash
python manage.py migrate
```

**Expected Output:**
```
Running migrations:
  Applying events.0001_initial... OK
```

### Step 3: Restart Server (if running)
After migrations, restart your Django server.

## Complete All Missing Migrations

You might also need migrations for other apps. Run all at once:

```bash
# Create migrations for all apps
python manage.py makemigrations

# Apply all migrations
python manage.py migrate
```

This will create and apply migrations for:
- events
- tickets
- reports
- accounts (if there are new changes)

## Verify It Works

After migrations, try accessing:
```
http://127.0.0.1:8000/admin/events/event/
```

The error should be gone!

## Quick Fix (All Apps at Once)

Run these commands to fix all migration issues:

```bash
cd D:\CmSC 135\Division-Information-Management-System\backend
python manage.py makemigrations
python manage.py migrate
```

This will create and apply migrations for ALL apps that need them.
