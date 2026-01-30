# Project Refresh – 21-realstate-backend

This is a quick “get back up to speed” document for the current Django/DRF backend implementation.

## Stack / tooling

- Django + Django REST Framework
- JWT auth via `rest_framework_simplejwt` (with refresh-token rotation + blacklist)
- API docs via `drf-spectacular` (Swagger UI + OpenAPI schema)
- CORS via `django-cors-headers`
- Postgres connection via `DATABASE_URL`

## High-level routing

- Swagger UI: `GET /`
- OpenAPI schema: `GET /api/schema/`
- Django admin: `/admin/`
- Auth APIs: `/api/auth/` (users app)
- Customer APIs: `/api/customer/` (users app)
- Core APIs: `/api/` (core app, DRF router)

Notes:
- Endpoints use trailing slashes.
- Global DRF default permission is `IsAuthenticated`, but many core `GET` endpoints override this to be public.

## Auth & roles

- Custom user model: email-based login (`AUTH_USER_MODEL = users.User`).
- Roles are in `apps.core.choices.UserRoles`:
  - `customer`, `developer`, `content_creator`, `staff`, `manager`, `superuser`
- JWT settings (from settings):
  - access token lifetime: 1 day
  - refresh token lifetime: 30 days
  - refresh rotation enabled + blacklist after rotation

### Token claims

Login/register tokens include additional claims:
- `user_id`, `email`, `role`, `full_name`

## Implemented data models (summary)

### Users app

- `User`
  - `email` (unique), `full_name`, `phone` (validated), `role`, `profile_image`, `is_active`, timestamps
- `CustomerInquiry`
  - `customer` FK to `User`
  - `phone`, `message`, `interested_in`
  - `project_id` and `unit_id` are stored as integers (there are no project/unit models wired to this yet)

### Core app

- `Country` (webp image required)
- `City` (webp image required, FK to Country)
- `Slider` (jpg/jpeg/png/webp allowed)
- `Ad` (jpg/jpeg/png/webp allowed) + `appear_place` choice
- `Feature`
- `Article` (webp image required; markdown content fields + simple markdown validation)

### Developers / Units / Projects apps (status)

- `apps.developers.models.Developer` exists (not exposed via API routes yet).
- `apps.units.models.UnitType` exists (not exposed via API routes yet).
- `apps.projects.models` is currently empty.

## Endpoints (complete list from current URL config)

### System

- `GET /` — Swagger UI
- `GET /api/schema/` — OpenAPI schema
- `/admin/` — Django admin site

### Auth (`/api/auth/`)

- `POST /api/auth/register/` — public
  - creates a user (defaults to role `customer`)
  - returns tokens + token expiry fields + user payload
- `POST /api/auth/login/` — public
  - returns tokens + token expiry fields + user payload
- `POST /api/auth/refresh/` — public (SimpleJWT)
- `POST /api/auth/logout/` — authenticated
  - blacklists refresh token (requires `refresh` in body)
- `GET /api/auth/me/` — authenticated
- `PATCH /api/auth/me/` — authenticated
- `PUT /api/auth/me/` — authenticated

### Customer (`/api/customer/`)

- `GET /api/customer/inqury/` — staff/manager/superuser
  - lists all inquiries
- `POST /api/customer/inqury/` — customer only
  - creates an inquiry for the authenticated customer

Note: the path is spelled `inqury` in code.


### Core (`/api/`)

All of these are DRF `ModelViewSet`s, so they expose the standard actions.

#### Countries (`/api/countries/`)

- `GET /api/countries/` — public
- `POST /api/countries/` — staff/manager/superuser
- `GET /api/countries/{id}/` — public
- `PUT/PATCH /api/countries/{id}/` — staff/manager/superuser
- `DELETE /api/countries/{id}/` — manager/superuser

#### Cities (`/api/cities/`)

- `GET /api/cities/` — public
- `POST /api/cities/` — staff/manager/superuser
- `GET /api/cities/{id}/` — public
- `PUT/PATCH /api/cities/{id}/` — staff/manager/superuser
- `DELETE /api/cities/{id}/` — manager/superuser

#### Sliders (`/api/sliders/`)

- `GET /api/sliders/` — public
- `POST /api/sliders/` — staff/manager/superuser
- `GET /api/sliders/{id}/` — public
- `PUT/PATCH /api/sliders/{id}/` — staff/manager/superuser
- `DELETE /api/sliders/{id}/` — manager/superuser

#### Ads (`/api/ads/`)

- `GET /api/ads/` — public
- `POST /api/ads/` — staff/manager/superuser
- `GET /api/ads/{id}/` — public
- `PUT/PATCH /api/ads/{id}/` — staff/manager/superuser
- `DELETE /api/ads/{id}/` — manager/superuser

#### Features (`/api/features/`)

- `GET /api/features/` — public
- `POST /api/features/` — staff/manager/superuser
- `GET /api/features/{id}/` — public
- `PUT/PATCH /api/features/{id}/` — staff/manager/superuser
- `DELETE /api/features/{id}/` — manager/superuser

#### Articles (`/api/articles/`)

- `GET /api/articles/` — public
- `POST /api/articles/` — content_creator OR manager OR superuser
- `GET /api/articles/{id}/` — public
- `PUT/PATCH /api/articles/{id}/` — content_creator OR manager OR superuser
- `DELETE /api/articles/{id}/` — content_creator OR manager OR superuser

### Unit Types (`/api/unit/types/`)

- `GET /api/unit/types/` — public
- `GET /api/unit/types/{id}/` — public
- `POST /api/unit/types/` — staff/manager/superuser
- `PUT/PATCH /api/unit/types/{id}/` — staff/manager/superuser
- `DELETE /api/unit/types/{id}/` — manager/superuser
## Where to look next

- Deeper request/response examples are already documented in `docs/FRONTEND_API_REFERENCE.md`.
- Role behavior and intended access model is summarized in `docs/Auth&permissionssystem.md`.
- URL entrypoint: `config/urls.py`.
