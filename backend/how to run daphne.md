cd backend
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install daphne
daphne -b 0.0.0.0 -p 8000 config.asgi:application
