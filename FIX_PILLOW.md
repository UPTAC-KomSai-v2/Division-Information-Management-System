# Fix: Install Pillow for ImageField

## Problem
When running migrations, you got this error:
```
accounts.User.avatar: (fields.E210) Cannot use ImageField because Pillow is not installed.
```

## Solution

Pillow is required for Django's `ImageField`. Install it with:

**Since `pip` command is not available, use Python's module form:**

```bash
cd D:\CmSC 135\Division-Information-Management-System\backend
python -m pip install Pillow
```

Or using the requirements file:
```bash
cd D:\CmSC 135\Division-Information-Management-System\backend
python -m pip install -r requirements.txt
```

**Note:** Use `python -m pip` instead of just `pip` when pip command is not recognized.

## After Installation

Once Pillow is installed, you can run migrations again:

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

## What is Pillow?

Pillow is a Python imaging library that Django uses to handle image uploads and processing. It's required whenever you use:
- `ImageField` (for user avatars, document images, etc.)
- Image processing features

## Note

I've already added `Pillow>=10.0.0` to your `requirements.txt` file, so future installations will include it automatically.

