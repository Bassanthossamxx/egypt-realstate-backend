# 21-realstate-backend

Django + DRF backend for a real estate API (auth, core resources) with JWT authentication and Swagger (drf-spectacular).

Frontend integration doc: `docs/FRONTEND_API_REFERENCE.md`

## Project structure

```
.
├─ manage.py
├─ requirements.txt
├─ config/
│  ├─ settings.py        # Django settings (reads .env)
│  ├─ urls.py            # Main routes (admin, auth, core, swagger)
│  ├─ asgi.py / wsgi.py
│  └─ __init__.py
├─ apps/
│  ├─ core/
│  │  ├─ models.py
│  │  ├─ serializers.py
│  │  ├─ views.py
│  │  ├─ urls.py         # /api/...
│  │  ├─ permissions.py
│  │  └─ migrations/
│  ├─ users/
│  │  ├─ models.py       # Custom user model
│  │  ├─ serializers.py
│  │  ├─ views.py
│  │  ├─ urls.py         # /api/auth/...
│  │  └─ migrations/
│  └─ units/
│     ├─ models.py
│     ├─ views.py
│     └─ migrations/
└─ docs/
	 ├─ API_AUTHENTICATION.md
	 └─ Auth&permissionssystem.md
```

## Main endpoints

- Swagger UI: `/` (root)
- OpenAPI schema: `/api/schema/`
- Admin: `/admin/`
- Auth (users app): `/api/auth/`
	- `POST /api/auth/register/`
	- `POST /api/auth/login/`
	- `POST /api/auth/logout/`
	- `POST /api/auth/refresh/`
	- `GET  /api/auth/me/`
- Core API (core app): `/api/`
	- `/api/countries/`, `/api/cities/`, `/api/sliders/`, `/api/ads/`, `/api/features/`, `/api/articles/`

## Setup (Windows / PowerShell)

1) Create & activate a virtual environment

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

2) Install dependencies

```powershell
pip install -r requirements.txt
```

3) Create a `.env` file in the project root (same folder as `manage.py`)

4) Run migrations

```powershell
python manage.py migrate
```

5) Create an admin user (optional)

```powershell
python manage.py createsuperuser
```

6) Start the server

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for Swagger UI.

## Environment variables (.env)

This project uses `python-dotenv` to load environment variables from a `.env` file.

Create a file named `.env` in the project root:

```dotenv
# Required
DATABASE_URL=postgres://postgres:postgres@localhost:5432/realstate_db

# Recommended
SECRET_KEY=change-me-in-production
DEBUG=True

# Comma-separated list
ALLOWED_HOSTS=127.0.0.1,localhost

# CORS
CORS_ALLOW_ALL_ORIGINS=True
```

Notes:

- `DATABASE_URL` must be a valid PostgreSQL URL.
- `DEBUG` and `CORS_ALLOW_ALL_ORIGINS` are read as strings (`True`/`False`).
- `ALLOWED_HOSTS` is split by commas.