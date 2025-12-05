# How to Install Pillow

## Problem
You tried `pip install Pillow` but got:
```
'pip' is not recognized as an internal or external command
```

## Solution

Since you can run `python manage.py` successfully, Python is installed. Use Python's module form instead:

### Option 1: Using Python Module (Recommended)
```bash
python -m pip install Pillow
```

### Option 2: Check Your Python Installation
If that doesn't work, try:
```bash
python3 -m pip install Pillow
```

Or check which Python you have:
```bash
python --version
python -m pip --version
```

## After Installation

Once Pillow is installed, verify it:
```bash
python -c "import PIL; print(PIL.__version__)"
```

Then run migrations:
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

## Note

- `pip` is Python's package installer
- `npm` is Node.js package manager (won't work for Python packages)
- Use `python -m pip` when `pip` command is not available
- Pillow is a Python library, so it must be installed with pip (not npm)

