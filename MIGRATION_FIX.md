# Fix: Migration Default Value for date_joined

## Problem
When running migrations, Django asks:
```
It is impossible to add the field 'date_joined' with 'auto_now_add=True' to user without providing a default.
```

## Solution

You're at a prompt asking you to choose. Here's what to do:

### Step 1: Select Option 1
At the prompt, type:
```
1
```
Then press Enter.

### Step 2: Provide Default Value
Django will then ask for a default value. Type:
```
timezone.now
```
Then press Enter.

This will set the `date_joined` field to the current time for all existing users.

## Alternative: Use a Specific Date

If you want all existing users to have the same date (e.g., when you started the system), you can enter:
```
2024-12-01 00:00:00
```
(Replace with your preferred date)

## After Migration Completes

Once the migration finishes, you can continue with:
```bash
python manage.py migrate
```

## Why This Happened

When adding a new required field to an existing model that already has data:
- Django needs to know what value to put in that field for existing rows
- `auto_now_add=True` only works for NEW rows, not existing ones
- So we provide a one-time default for the migration

## Note

I've updated the model to use `default=timezone.now` instead of `auto_now_add=True` which is better for migrations, but you still need to complete the current migration prompt first.

