# Fix: timezone is not defined

## Problem
You're getting this error:
```
NameError: name 'timezone' is not defined
```

## Solution

The import is already in the file, but the server may need to be restarted. 

### Step 1: Save the File
Make sure `accounts/models.py` is saved. The import should be:
```python
from django.utils import timezone
```

### Step 2: Restart the Server
Stop the Django server (Ctrl+C) and restart it:
```bash
python manage.py runserver
```

### Step 3: Clear Python Cache (if still having issues)
If the error persists, delete Python cache files:
```bash
# Delete all __pycache__ directories
find . -type d -name __pycache__ -exec rm -r {} +
```

Or manually delete:
- `backend/accounts/__pycache__/`
- `backend/__pycache__/`

Then restart the server.

## Verification

The import should be at the top of `accounts/models.py`:
```python
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone  # ← This line should be here
import os
```

## Alternative Fix (if import is missing)

If for some reason the import is missing, add it:
```python
from django.utils import timezone
```

This should be after the other Django imports and before using `timezone.now`.

