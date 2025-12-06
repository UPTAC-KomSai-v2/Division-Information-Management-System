# How to Run (Backend + Frontend)

This project uses Django/Channels for the backend and Quasar/Vue for the frontend. Real-time chat relies on Redis for the channel layer.

## Prerequisites
- Python 3.x (venv located at `backend/.venv`)
- Node.js + npm (Quasar CLI installed via `npm i -g @quasar/cli`)
- Redis accessible at `127.0.0.1:6379` (change host/port in `backend/config/settings.py` if different)
- Git (optional for code fetch)

## Backend (Django + Channels)
1) Open a terminal and go to the backend:
   ```bash
   cd backend
   ```
2) Activate the virtual environment:
   ```bash
   .\.venv\Scripts\Activate.ps1   # Windows PowerShell
   # or source .venv/bin/activate # macOS/Linux
   ```
3) Install dependencies (first time or after updates):
   ```bash
   pip install -r requirements.txt
   ```
4) Ensure Redis is running (example with Docker):
   ```bash
   docker run -p 6379:6379 redis:7
   ```
5) Run the ASGI server (exposes API + WebSockets):
   ```bash
   daphne -b 0.0.0.0 -p 8000 config.asgi:application
   ```
   - Backend base URL: `http://192.168.1.76:8000`
   - WebSocket base: `ws://192.168.1.76:8000`
   - If the host/IP changes, update:
     - `ALLOWED_HOSTS` and `CHANNEL_LAYERS` host in `backend/config/settings.py`
     - `frontend/src/boot/axios.js` baseURL
     - `frontend/src/pages/MessagesPage.vue` `apiBase` / `wsBase`

## Frontend (Quasar/Vue)
1) Open a second terminal and go to the frontend:
   ```bash
   cd frontend
   ```
2) Install dependencies (first time):
   ```bash
   npm install
   ```
3) Run the dev server:
   ```bash
   quasar dev
   ```
   - Quasar will print a dev URL (commonly `http://localhost:9000`). From other laptops on the same network, use `http://192.168.1.76:<quasar-port>`.

## Login and Real-Time Chat
- Login endpoint: `/api/auth/login/` (email + password) handled by Django.
- Tokens stored in `localStorage` as `access` / `refresh`.
- Messages page opens WebSockets to `ws://192.168.1.76:8000/ws/messages/<room>/?token=<access>`.

## Quick Checks
- Backend up: open `http://192.168.1.76:8000/api/auth/me/` with Authorization header `Bearer <access>`.
- WebSocket: connect to `ws://192.168.1.76:8000/ws/messages/1_2/?token=<access>` (replace IDs) and send `{"text":"hello"}`.

## Common Issues
- If chat doesn’t update across laptops: verify Redis is running and `CHANNEL_LAYERS` points to it.
- CORS/hosts: ensure `ALLOWED_HOSTS` includes the backend host/IP and frontend uses the same host for HTTP/WS.
- Firewall: allow inbound on backend port (8000) and Redis port (6379) if remote.
