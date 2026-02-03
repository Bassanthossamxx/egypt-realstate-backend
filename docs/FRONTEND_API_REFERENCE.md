# Frontend API Reference - Complete Guide

> **Comprehensive API documentation for Egypt Real Estate Platform**  
---

## Table of Contents

1. [Overview](#overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Website/App Endpoints (Public & Customer)](#websiteapp-endpoints)
4. [Dashboard Endpoints (Staff & Management)](#dashboard-endpoints)
5. [User Roles & Permissions Matrix](#user-roles--permissions-matrix)
6. [Common Patterns & Best Practices](#common-patterns--best-practices)

---

## Overview

### Base URLs
- **Production**: Your DigitalOcean App Platform URL
- **Swagger UI**: `/` (interactive API documentation)
- **OpenAPI Schema**: `/api/schema/`

### Important Conventions
- All endpoints use trailing slashes (`/`)
- All media URLs returned as absolute URLs
- All timestamps in ISO 8601 format (UTC)
- Use `multipart/form-data` for file uploads
- Use `application/json` for JSON data

### Response Codes
| Code | Meaning |
|------|---------|
| `200 OK` | Successful request |
| `201 Created` | Resource created successfully |
| `204 No Content` | Resource deleted successfully |
| `400 Bad Request` | Validation error or malformed request |
| `401 Unauthorized` | Authentication required or token invalid |
| `403 Forbidden` | Insufficient permissions |
| `404 Not Found` | Resource not found |
| `500 Internal Server Error` | Server error |

---

## Authentication & Authorization

### User Roles

| Role | Description | Primary Use Case |
|------|-------------|------------------|
| `customer` | Regular website/app users | Browse listings, submit inquiries |
| `developer` | Property developers "PORTAL" | Manage their projects and units |
| `content_creator` | Content managers | Create and manage articles |
| `staff` | Staff members | Dashboard CRUD operations (no delete) |
| `manager` | Managers | Full dashboard access (cannot see superusers) |
| `superuser` | System administrators "Our Team" | Complete system access |

### JWT Authentication

#### Header Format
```
Authorization: Bearer <access_token>
```

#### Token Lifecycle
- **Access Token**: 24 hours (short-lived)
- **Refresh Token**: 30 days (long-lived)
- **Token Claims**: `user_id`, `email`, `role`, `full_name`

---

## Website/App Endpoints

Public-facing endpoints for website and mobile app users.

---

### Authentication (`/api/auth/`)

#### Register User

Create a new customer account.

**Endpoint**: `POST /api/auth/register/`  
**Authentication**: None (Public)  
**Role**: Assigns `customer` role automatically

**Request Body** (`application/json` or `multipart/form-data`)

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `email` | string |  Yes | Unique, valid email format |
| `full_name` | string |  Yes | Max 255 characters |
| `password` | string |  Yes | Min 8 characters |
| `password_confirm` | string | Yes | Must match `password` |
| `phone` | string | Optional | Digits with optional `+` prefix |
| `profile_image` | file | Optional | Image file |

**Example Request**

```json
{
  "email": "customer@example.com",
  "full_name": "John Doe",
  "phone": "+201234567890",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!"
}
```

**Success Response** `201 Created`

```json
{
  "message": "User registered successfully",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "access_expires_at": "2026-02-04T14:00:00+00:00",
  "refresh_expires_at": "2026-03-05T14:00:00+00:00",
  "access_expires_in": 86400,
  "refresh_expires_in": 2592000,
  "user": {
    "id": 1,
    "email": "customer@example.com",
    "full_name": "John Doe",
    "phone": "+201234567890",
    "role": "customer",
    "profile_image": null,
    "is_active": true,
    "created_at": "2026-02-03T14:00:00Z",
    "updated_at": "2026-02-03T14:00:00Z"
  }
}
```

**Error Responses**

```json
// 400 - Email already exists
{"email": ["A user with this email already exists."]}

// 400 - Password mismatch
{"password": ["Password fields didn't match."]}

// 400 - Weak password
{"password": ["This password is too short. It must contain at least 8 characters."]}
```

---

#### Login

Authenticate with email and password.

**Endpoint**: `POST /api/auth/login/`  
**Authentication**: None (Public)

**Request Body**

| Field | Type | Required |
|-------|------|----------|
| `email` | string |  Yes |
| `password` | string |  Yes |

**Example Request**

```json
{
  "email": "customer@example.com",
  "password": "SecurePass123!"
}
```

**Success Response** `200 OK`

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "access_expires_at": "2026-02-04T14:00:00+00:00",
  "refresh_expires_at": "2026-03-05T14:00:00+00:00",
  "access_expires_in": 86400,
  "refresh_expires_in": 2592000,
  "user": {
    "id": 1,
    "email": "customer@example.com",
    "full_name": "John Doe",
    "role": "customer",
    "phone": "+201234567890",
    "profile_image": "http://127.0.0.1:8000/media/users/profiles/profile.jpg"
  }
}
```

**Error Response**

```json
// 401 - Invalid credentials
{"detail": "No active account found with the given credentials"}
```

---

#### Refresh Token

Get a new access token using refresh token.

**Endpoint**: `POST /api/auth/refresh/`  
**Authentication**: None (Public)

**Request Body**

| Field | Type | Required |
|-------|------|----------|
| `refresh` | string |  Yes |

**Example Request**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

**Success Response** `200 OK`

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

**Error Response**

```json
// 401 - Invalid or expired
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

---

#### Get Current User Profile

Retrieve authenticated user's profile.

**Endpoint**: `GET /api/auth/me/`  
**Authentication**: Required (Any authenticated user)

**Success Response** `200 OK`

```json
{
  "id": 1,
  "email": "customer@example.com",
  "full_name": "John Doe",
  "phone": "+201234567890",
  "role": "customer",
  "profile_image": "http://127.0.0.1:8000/media/users/profiles/profile.jpg",
  "is_active": true,
  "created_at": "2026-02-03T14:00:00Z",
  "updated_at": "2026-02-03T14:00:00Z"
}
```

---

#### Update Current User Profile

Update authenticated user's profile.

**Endpoints**:  
- `PATCH /api/auth/me/` (partial update)  
- `PUT /api/auth/me/` (full update)

**Authentication**: Required (Any authenticated user)

**Request Body** (All optional for PATCH)

| Field | Type | Editable |
|-------|------|----------|
| `full_name` | string |  Yes |
| `phone` | string | Yes |
| `profile_image` | file |  Yes |
| `email` | string | No (read-only) |
| `role` | string |  No (read-only) |

**Example Request**

```json
{
  "full_name": "John Smith",
  "phone": "+201234567899"
}
```

**Success Response** `200 OK`

---

#### Logout

Blacklist refresh token to logout.

**Endpoint**: `POST /api/auth/logout/`  
**Authentication**: Required

**Request Body**

| Field | Type | Required |
|-------|------|----------|
| `refresh` | string |  Yes |

**Example Request**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

**Success Response** `205 Reset Content`

```json
{
  "message": "Successfully logged out"
}
```

---

### Countries (`/api/countries/`)

#### List Countries

**Endpoint**: `GET /api/countries/`  
**Authentication**: None (Public)

**Query Parameters**

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `appear_on_home_page` | string | `true` | `true`, `false`, `all` |
| `search` | string | - | Search in `name_en` or `name_ar` |

**Example Requests**

```
GET /api/countries/
GET /api/countries/?appear_on_home_page=all
GET /api/countries/?search=egypt
```

**Success Response** `200 OK`

```json
[
  {
    "id": 1,
    "name_en": "Egypt",
    "name_ar": "مصر",
    "image": "http://127.0.0.1:8000/media/countries/egypt.webp",
    "appear_on_home_page": true,
    "created_at": "2026-02-01T10:00:00Z"
  }
]
```

---

#### Get Country Details

**Endpoint**: `GET /api/countries/{id}/`  
**Authentication**: None (Public)

**Success Response** `200 OK`

```json
{
  "id": 1,
  "name_en": "Egypt",
  "name_ar": "مصر",
  "image": "http://127.0.0.1:8000/media/countries/egypt.webp",
  "appear_on_home_page": true,
  "created_at": "2026-02-01T10:00:00Z"
}
```

---

### Cities (`/api/cities/`)

#### List Cities

**Endpoint**: `GET /api/cities/`  
**Authentication**: None (Public)

**Query Parameters**

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `appear_on_home_page` | string | `true` | `true`, `false`, `all` |
| `search` | string | - | Search in `name_en` or `name_ar` |

**Success Response** `200 OK`

```json
[
  {
    "id": 1,
    "country": 1,
    "country_name": "Egypt",
    "name_en": "Cairo",
    "name_ar": "القاهرة",
    "image": "http://127.0.0.1:8000/media/cities/cairo.webp",
    "appear_on_home_page": true,
    "created_at": "2026-02-01T10:00:00Z",
    "updated_at": "2026-02-01T10:00:00Z"
  }
]
```

---

#### Get City Details

**Endpoint**: `GET /api/cities/{id}/`  
**Authentication**: None (Public)

**Success Response** `200 OK`

```json
{
  "id": 1,
  "country": 1,
  "country_name": "Egypt",
  "name_en": "Cairo",
  "name_ar": "القاهرة",
  "image": "http://127.0.0.1:8000/media/cities/cairo.webp",
  "appear_on_home_page": true,
  "created_at": "2026-02-01T10:00:00Z",
  "updated_at": "2026-02-01T10:00:00Z"
}
```

---

### Sliders (`/api/sliders/`)

Home page slider images.

#### List Sliders

**Endpoint**: `GET /api/sliders/`  
**Authentication**: None (Public)

**Query Parameters**

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `appear_on_home_page` | string | `true` | `true`, `false`, `all` |

**Success Response** `200 OK`

```json
[
  {
    "id": 1,
    "image": "http://127.0.0.1:8000/media/sliders/slider1.jpg",
    "appear_on_home_page": true,
    "index": 0,
    "created_at": "2026-02-01T10:00:00Z"
  },
  {
    "id": 2,
    "image": "http://127.0.0.1:8000/media/sliders/slider2.jpg",
    "appear_on_home_page": true,
    "index": 1,
    "created_at": "2026-02-01T10:00:00Z"
  }
]
```

---

#### Get Slider Details

**Endpoint**: `GET /api/sliders/{id}/`  
**Authentication**: None (Public)

**Success Response** `200 OK`

```json
{
  "id": 1,
  "image": "http://127.0.0.1:8000/media/sliders/slider1.jpg",
  "appear_on_home_page": true,
  "index": 0,
  "created_at": "2026-02-01T10:00:00Z"
}
```

---

### Advertisements (`/api/ads/`)

#### List Ads

**Endpoint**: `GET /api/ads/`  
**Authentication**: None (Public)

**Success Response** `200 OK`

```json
[
  {
    "id": 1,
    "image": "http://127.0.0.1:8000/media/ads/ad1.webp",
    "appear_place": "home",
    "created_at": "2026-02-01T10:00:00Z"
  },
  {
    "id": 2,
    "image": "http://127.0.0.1:8000/media/ads/ad2.webp",
    "appear_place": "projects",
    "created_at": "2026-02-01T10:00:00Z"
  }
]
```

**Appear Place Options**: `home`, `projects`, `units`, `other`

---

#### Get Ad Details

**Endpoint**: `GET /api/ads/{id}/`  
**Authentication**: None (Public)

**Success Response** `200 OK`

```json
{
  "id": 1,
  "image": "http://127.0.0.1:8000/media/ads/ad1.webp",
  "appear_place": "home",
  "created_at": "2026-02-01T10:00:00Z"
}
```

---

### Features (`/api/features/`)

Property features (pool, gym, parking, etc.)

#### List Features

**Endpoint**: `GET /api/features/`  
**Authentication**: None (Public)

**Query Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search in `name_en` or `name_ar` |

**Success Response** `200 OK`

```json
[
  {"id": 1, "name_en": "Swimming Pool", "name_ar": "حمام سباحة"},
  {"id": 2, "name_en": "Gym", "name_ar": "صالة رياضية"},
  {"id": 3, "name_en": "Parking", "name_ar": "موقف سيارات"},
  {"id": 4, "name_en": "Garden", "name_ar": "حديقة"}
]
```

---

#### Get Feature Details

**Endpoint**: `GET /api/features/{id}/`  
**Authentication**: None (Public)

**Success Response** `200 OK`

```json
{
  "id": 1,
  "name_en": "Swimming Pool",
  "name_ar": "حمام سباحة"
}
```

---

### Articles (`/api/articles/`)

Blog articles and news.

#### List Articles

**Endpoint**: `GET /api/articles/`  
**Authentication**: None (Public)

**Query Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search in `title_en` or `title_ar` |

**Success Response** `200 OK`

```json
[
  {
    "id": 1,
    "title_en": "Top 10 Real Estate Investment Tips",
    "title_ar": "أفضل 10 نصائح للاستثمار العقاري",
    "content_en_md": "# Introduction\n\nReal estate investment...",
    "content_ar_md": "# مقدمة\n\nالاستثمار العقاري...",
    "meta": {
      "author": "John Doe",
      "category": "Investment"
    },
    "image": "http://127.0.0.1:8000/media/articles/article1.webp",
    "created_at": "2026-02-01T10:00:00Z",
    "updated_at": "2026-02-01T10:00:00Z"
  }
]
```

---

#### Get Article Details

**Endpoint**: `GET /api/articles/{id}/`  
**Authentication**: None (Public)

**Success Response** `200 OK`

```json
{
  "id": 1,
  "title_en": "Top 10 Real Estate Investment Tips",
  "title_ar": "أفضل 10 نصائح للاستثمار العقاري",
  "content_en_md": "# Introduction\n\nReal estate investment is one of...",
  "content_ar_md": "# مقدمة\n\nالاستثمار العقاري هو أحد...",
  "meta": {
    "author": "John Doe",
    "category": "Investment",
    "tags": ["investment", "real estate", "tips"]
  },
  "image": "http://127.0.0.1:8000/media/articles/article1.webp",
  "created_at": "2026-02-01T10:00:00Z",
  "updated_at": "2026-02-01T10:00:00Z"
}
```

---

### Unit Types (`/api/unit/types/`)

Types of properties (apartment, villa, office, etc.)

#### List Unit Types

**Endpoint**: `GET /api/unit/types/`  
**Authentication**: None (Public)

**Query Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search in `name_en` or `name_ar` |

**Success Response** `200 OK`

```json
[
  {"id": 1, "name_en": "Apartment", "name_ar": "شقة"},
  {"id": 2, "name_en": "Villa", "name_ar": "فيلا"},
  {"id": 3, "name_en": "Office", "name_ar": "مكتب"},
  {"id": 4, "name_en": "Shop", "name_ar": "محل تجاري"},
  {"id": 5, "name_en": "Land", "name_ar": "أرض"}
]
```

---

#### Get Unit Type Details

**Endpoint**: `GET /api/unit/types/{id}/`  
**Authentication**: None (Public)

**Success Response** `200 OK`

```json
{
  "id": 1,
  "name_en": "Apartment",
  "name_ar": "شقة"
}
```

---

### Developers (`/api/developers/`)

Real estate development companies.

#### List Developers

**Endpoint**: `GET /api/developers/`  
**Authentication**: None (Public)

**Query Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search in `name_en` or `name_ar` |

**Success Response** `200 OK`

```json
[
  {
    "id": 1,
    "name_en": "Emaar Properties",
    "name_ar": "إعمار العقارية",
    "description_en": "Leading real estate developer in the Middle East.",
    "description_ar": "شركة عقارية رائدة في الشرق الأوسط.",
    "logo": "http://127.0.0.1:8000/media/developers/logos/emaar.jpg",
    "website_url": "https://www.emaar.com",
    "created_at": "2026-02-01T10:00:00Z",
    "updated_at": "2026-02-01T10:00:00Z"
  }
]
```

---

#### Get Developer Details

**Endpoint**: `GET /api/developers/{id}/`  
**Authentication**: None (Public)

**Success Response** `200 OK`

```json
{
  "id": 1,
  "name_en": "Emaar Properties",
  "name_ar": "إعمار العقارية",
  "description_en": "Leading real estate developer in the Middle East with projects across multiple countries.",
  "description_ar": "شركة عقارية رائدة في الشرق الأوسط مع مشاريع في عدة دول.",
  "logo": "http://127.0.0.1:8000/media/developers/logos/emaar.jpg",
  "website_url": "https://www.emaar.com",
  "created_at": "2026-02-01T10:00:00Z",
  "updated_at": "2026-02-01T10:00:00Z"
}
```

---

### Customer Inquiries (`/api/customer/inqury/`)

Submit inquiries about properties.

#### Create Inquiry

**Endpoint**: `POST /api/customer/inqury/`  
**Authentication**: Required (Customer role only)

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `phone` | string |  Yes | Contact phone number |
| `message` | string | Yes | Inquiry message |
| `interested_in` | integer | Yes | Unit type ID |
| `project_id` | integer | Conditional | Project ID (at least one of project_id or unit_id required) |
| `unit_id` | integer | Conditional | Unit ID (at least one of project_id or unit_id required) |

**Example Request**

```json
{
  "phone": "+201234567890",
  "message": "I'm interested in learning more about the available apartments in this project.",
  "interested_in": 1,
  "project_id": 5,
  "unit_id": null
}
```

**Success Response** `201 Created`

```json
{
  "id": 10,
  "customer_id": 1,
  "phone": "+201234567890",
  "message": "I'm interested in learning more about the available apartments in this project.",
  "interested_in": 1,
  "interested_in_name_en": "Apartment",
  "interested_in_name_ar": "شقة",
  "project_id": 5,
  "unit_id": null,
  "is_contacted": false,
  "created_at": "2026-02-03T14:00:00Z"
}
```

**Error Responses**

```json
// 400 - Missing interested_in
{"interested_in": ["This field is required."]}

// 400 - No project or unit specified
{"non_field_errors": ["Provide project_id and/or unit_id."]}

// 403 - Not a customer
{"detail": "You do not have permission to perform this action."}
```

---

## Dashboard Endpoints

Admin panel endpoints for staff, managers, content creators, and superusers.

---

### User Management (`/api/dashboard/users/`)

**Permissions**:
- **Manager**: Can see all users EXCEPT superusers
- **Superuser**: Can see ALL users including other superusers

#### List Users

**Endpoint**: `GET /api/dashboard/users/`  
**Authentication**: Required (Manager or Superuser)

**Success Response** `200 OK`

```json
[
  {
    "id": 1,
    "email": "manager@example.com",
    "full_name": "Jane Manager",
    "phone": "+201234567890",
    "role": "manager",
    "developer_id": null,
    "developer_name_en": null,
    "developer_name_ar": null,
    "developer_logo": null,
    "profile_image": "http://127.0.0.1:8000/media/users/profiles/jane.jpg",
    "is_active": true,
    "created_at": "2026-01-15T10:00:00Z",
    "updated_at": "2026-02-01T10:00:00Z"
  },
  {
    "id": 3,
    "email": "developer@example.com",
    "full_name": "Developer User",
    "phone": "+201234567892",
    "role": "developer",
    "developer_id": 1,
    "developer_name_en": "Emaar Properties",
    "developer_name_ar": "إعمار العقارية",
    "developer_logo": "http://127.0.0.1:8000/media/developers/logos/emaar.jpg",
    "profile_image": null,
    "is_active": true,
    "created_at": "2026-01-25T10:00:00Z",
    "updated_at": "2026-01-25T10:00:00Z"
  }
]
```

---

#### Get User Details

**Endpoint**: `GET /api/dashboard/users/{id}/`  
**Authentication**: Required (Manager or Superuser)

**Success Response** `200 OK`

```json
{
  "id": 1,
  "email": "manager@example.com",
  "full_name": "Jane Manager",
  "phone": "+201234567890",
  "role": "manager",
  "developer_id": null,
  "developer_name_en": null,
  "developer_name_ar": null,
  "developer_logo": null,
  "profile_image": "http://127.0.0.1:8000/media/users/profiles/jane.jpg",
  "is_active": true,
  "created_at": "2026-01-15T10:00:00Z",
  "updated_at": "2026-02-01T10:00:00Z"
}
```

---

#### Create User

**Endpoint**: `POST /api/dashboard/users/`  
**Authentication**: Required (Manager or Superuser)

**Request Body** (`multipart/form-data` for file upload)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Unique email |
| `full_name` | string | Yes | User's full name |
| `password` | string | Yes | Password (min 8 chars) |
| `password_confirm` | string | Yes | Must match password |
| `role` | string | Yes | `customer`, `developer`, `content_creator`, `staff`, `manager`, `superuser` |
| `phone` | string | Optional | Phone number |
| `developer_id` | integer | Conditional | Required if role is `developer` |
| `profile_image` | file |  Optional | Profile image |
| `is_active` | boolean | Optional | Default: `true` |

**Example Request**

```json
{
  "email": "newstaff@example.com",
  "full_name": "New Staff Member",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "role": "staff",
  "phone": "+201234567893",
  "is_active": true
}
```

**Success Response** `201 Created`

```json
{
  "id": 15,
  "email": "newstaff@example.com",
  "full_name": "New Staff Member",
  "phone": "+201234567893",
  "role": "staff",
  "developer_id": null,
  "developer_name_en": null,
  "developer_name_ar": null,
  "developer_logo": null,
  "profile_image": null,
  "is_active": true,
  "created_at": "2026-02-03T14:00:00Z",
  "updated_at": "2026-02-03T14:00:00Z"
}
```

**Error Responses**

```json
// 400 - Developer role without developer_id
{"developer_id": ["Developer is required when role is developer."]}

// 400 - Email already exists
{"email": ["A user with this email already exists."]}
```

---

#### Update User

**Endpoints**:  
- `PATCH /api/dashboard/users/{id}/` (partial)  
- `PUT /api/dashboard/users/{id}/` (full)

**Authentication**: Required (Manager or Superuser)

**Request Body** (All optional for PATCH)

| Field | Type | Description |
|-------|------|-------------|
| `full_name` | string | User's full name |
| `phone` | string | Phone number |
| `role` | string | User role |
| `developer_id` | integer | Required if changing role to `developer` |
| `profile_image` | file | Profile image |
| `is_active` | boolean | Account status |
| `new_password` | string | New password |
| `new_password_confirm` | string | Required if `new_password` provided |

**Example Request**

```json
{
  "full_name": "Updated Staff Member",
  "role": "manager",
  "is_active": true
}
```

**Success Response** `200 OK`

---

#### Delete User

**Endpoint**: `DELETE /api/dashboard/users/{id}/`  
**Authentication**: Required (Manager or Superuser)

**Success Response** `204 No Content`

---

### Countries Management (Dashboard)

#### Create Country

**Endpoint**: `POST /api/countries/`  
**Authentication**: Required (Staff, Manager, or Superuser)

**Request Body** (`multipart/form-data`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name_en` | string |  Yes | English name (unique) |
| `name_ar` | string |  Yes | Arabic name (unique) |
| `image` | file | Yes | Country image (.webp format  only accepted) |
| `appear_on_home_page` | boolean | Optional | Default: `false` |

**Success Response** `201 Created`

```json
{
  "id": 3,
  "name_en": "Saudi Arabia",
  "name_ar": "المملكة العربية السعودية",
  "image": "http://127.0.0.1:8000/media/countries/saudi.webp",
  "appear_on_home_page": false,
  "created_at": "2026-02-03T14:00:00Z"
}
```

---

#### Update Country

**Endpoints**:  
- `PATCH /api/countries/{id}/` (partial)  
- `PUT /api/countries/{id}/` (full)

**Authentication**: Required (Staff, Manager, or Superuser)

**Success Response** `200 OK`

---

#### Delete Country

**Endpoint**: `DELETE /api/countries/{id}/`  
**Authentication**: Required (Manager or Superuser only)

**Success Response** `204 No Content`

---

### Cities Management (Dashboard)

#### Create City

**Endpoint**: `POST /api/cities/`  
**Authentication**: Required (Staff, Manager, or Superuser)

**Request Body** (`multipart/form-data`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `country` | integer |  Yes | Country ID |
| `name_en` | string |  Yes | English name |
| `name_ar` | string | Yes | Arabic name |
| `image` | file | Yes | City image (.webp format only accepted) |
| `appear_on_home_page` | boolean | Optional | Default: `false` |

**Success Response** `201 Created`

```json
{
  "id": 5,
  "country": 1,
  "country_name": "Egypt",
  "name_en": "Giza",
  "name_ar": "الجيزة",
  "image": "http://127.0.0.1:8000/media/cities/giza.webp",
  "appear_on_home_page": false,
  "created_at": "2026-02-03T14:00:00Z",
  "updated_at": "2026-02-03T14:00:00Z"
}
```

---

#### Update City

**Endpoints**:  
- `PATCH /api/cities/{id}/` (partial)  
- `PUT /api/cities/{id}/` (full)

**Authentication**: Required (Staff, Manager, or Superuser)

**Success Response** `200 OK`

---

#### Delete City

**Endpoint**: `DELETE /api/cities/{id}/`  
**Authentication**: Required (Manager or Superuser only)

**Success Response** `204 No Content`

---

### Sliders Management (Dashboard)

#### Create Slider

**Endpoint**: `POST /api/sliders/`  
**Authentication**: Required (Staff, Manager, or Superuser)

**Request Body** (`multipart/form-data`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | file | Yes | Slider image "accept any img type" |
| `appear_on_home_page` | boolean | Optional | Default: `true` |
| `index` | integer | Optional | Display order (default: `0`) |

**Note**: If index conflicts with existing slider, the existing one will be auto-reassigned.

**Success Response** `201 Created`

```json
{
  "id": 4,
  "image": "http://127.0.0.1:8000/media/sliders/slider4.jpg",
  "appear_on_home_page": true,
  "index": 0,
  "created_at": "2026-02-03T14:00:00Z"
}
```

---

#### Update Slider

**Endpoints**:  
- `PATCH /api/sliders/{id}/` (partial)  
- `PUT /api/sliders/{id}/` (full)

**Authentication**: Required (Staff, Manager, or Superuser)

**Success Response** `200 OK`

---

#### Delete Slider

**Endpoint**: `DELETE /api/sliders/{id}/`  
**Authentication**: Required (Manager or Superuser only)

**Success Response** `204 No Content`

---

### 📢 Ads Management (Dashboard)

#### Create Ad

**Endpoint**: `POST /api/ads/`  
**Authentication**: Required (Staff, Manager, or Superuser)

**Request Body** (`multipart/form-data`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | file | Yes | Ad image (.webp format  only accepted) |
| `appear_place` | string | Yes | `home`, `projects`, `units`, or `other` |

**Success Response** `201 Created`

```json
{
  "id": 3,
  "image": "http://127.0.0.1:8000/media/ads/ad3.webp",
  "appear_place": "units",
  "created_at": "2026-02-03T14:00:00Z"
}
```

---

#### Update Ad

**Endpoints**:  
- `PATCH /api/ads/{id}/` (partial)  
- `PUT /api/ads/{id}/` (full)

**Authentication**: Required (Staff, Manager, or Superuser)

**Success Response** `200 OK`

---

#### Delete Ad

**Endpoint**: `DELETE /api/ads/{id}/`  
**Authentication**: Required (Manager or Superuser only)

**Success Response** `204 No Content`

---

### Features Management (Dashboard)

#### Create Feature

**Endpoint**: `POST /api/features/`  
**Authentication**: Required (Staff, Manager, or Superuser)

**Request Body**

| Field | Type | Required |
|-------|------|----------|
| `name_en` | string | Yes |
| `name_ar` | string | Yes |

**Example Request**

```json
{
  "name_en": "Balcony",
  "name_ar": "شرفة"
}
```

**Success Response** `201 Created`

```json
{
  "id": 5,
  "name_en": "Balcony",
  "name_ar": "شرفة"
}
```

---

#### Update Feature

**Endpoints**:  
- `PATCH /api/features/{id}/` (partial)  
- `PUT /api/features/{id}/` (full)

**Authentication**: Required (Staff, Manager, or Superuser)

**Success Response** `200 OK`

---

#### Delete Feature

**Endpoint**: `DELETE /api/features/{id}/`  
**Authentication**: Required (Manager or Superuser only)

**Success Response** `204 No Content`

---

### Articles Management (Dashboard)

#### Create Article

**Endpoint**: `POST /api/articles/`  
**Authentication**: Required (Content Creator, Manager, or Superuser)

**Request Body** (`multipart/form-data`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title_en` | string | Yes | English title |
| `title_ar` | string | Yes | Arabic title |
| `content_en_md` | string | Yes | English content (Markdown only format accepted) |
| `content_ar_md` | string | Yes | Arabic content (Markdown only format accepted) |
| `image` | file | Yes | Article image (.webp format only accepted) |
| `meta` | object | Optional | JSON metadata |

**Example Request**

```json
{
  "title_en": "Future of Real Estate in Egypt",
  "title_ar": "مستقبل العقارات في مصر",
  "content_en_md": "# Introduction\n\nThe real estate market in Egypt...",
  "content_ar_md": "# مقدمة\n\nسوق العقارات في مصر...",
  "meta": {
    "author": "Jane Doe",
    "category": "Market Analysis",
    "tags": ["egypt", "real estate", "market"]
  }
}
```

**Success Response** `201 Created`

```json
{
  "id": 3,
  "title_en": "Future of Real Estate in Egypt",
  "title_ar": "مستقبل العقارات في مصر",
  "content_en_md": "# Introduction\n\nThe real estate market in Egypt...",
  "content_ar_md": "# مقدمة\n\nسوق العقارات في مصر...",
  "meta": {
    "author": "Jane Doe",
    "category": "Market Analysis",
    "tags": ["egypt", "real estate", "market"]
  },
  "image": "http://127.0.0.1:8000/media/articles/article3.webp",
  "created_at": "2026-02-03T14:00:00Z",
  "updated_at": "2026-02-03T14:00:00Z"
}
```

---

#### Update Article

**Endpoints**:  
- `PATCH /api/articles/{id}/` (partial)  
- `PUT /api/articles/{id}/` (full)

**Authentication**: Required (Content Creator, Manager, or Superuser)

**Success Response** `200 OK`

---

#### Delete Article

**Endpoint**: `DELETE /api/articles/{id}/`  
**Authentication**: Required (Content Creator, Manager, or Superuser)

**Success Response** `204 No Content`

---

### Unit Types Management (Dashboard)

#### Create Unit Type

**Endpoint**: `POST /api/unit/types/`  
**Authentication**: Required (Staff, Manager, or Superuser)

**Request Body**

| Field | Type | Required |
|-------|------|----------|
| `name_en` | string |  Yes (unique) |
| `name_ar` | string |  Yes (unique) |

**Example Request**

```json
{
  "name_en": "Penthouse",
  "name_ar": "بنتهاوس"
}
```

**Success Response** `201 Created`

```json
{
  "id": 6,
  "name_en": "Penthouse",
  "name_ar": "بنتهاوس"
}
```

---

#### Update Unit Type

**Endpoints**:  
- `PATCH /api/unit/types/{id}/` (partial)  
- `PUT /api/unit/types/{id}/` (full)

**Authentication**: Required (Staff, Manager, or Superuser)

**Success Response** `200 OK`

---

#### Delete Unit Type

**Endpoint**: `DELETE /api/unit/types/{id}/`  
**Authentication**: Required (Manager or Superuser only)

**Success Response** `204 No Content`

---

### Developers Management (Dashboard)

#### Create Developer

**Endpoint**: `POST /api/developers/`  
**Authentication**: Required (Staff, Manager, or Superuser)

**Request Body** (`multipart/form-data`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name_en` | string | Yes | English name |
| `name_ar` | string | Yes | Arabic name |
| `description_en` | string | Yes | English description |
| `description_ar` | string | Yes | Arabic description |
| `logo` | file | Yes | Developer logo |
| `website_url` | string | Optional | Website URL (http/https) |

**Success Response** `201 Created`

```json
{
  "id": 3,
  "name_en": "Sodic",
  "name_ar": "سوديك",
  "description_en": "One of the region's leading real estate development companies.",
  "description_ar": "واحدة من الشركات الرائدة في تطوير العقارات في المنطقة.",
  "logo": "http://127.0.0.1:8000/media/developers/logos/sodic.jpg",
  "website_url": "https://www.sodic.com",
  "created_at": "2026-02-03T14:00:00Z",
  "updated_at": "2026-02-03T14:00:00Z"
}
```

---

#### Update Developer

**Endpoints**:  
- `PATCH /api/developers/{id}/` (partial)  
- `PUT /api/developers/{id}/` (full)

**Authentication**: Required (Staff, Manager, or Superuser)

**Success Response** `200 OK`

---

#### Delete Developer

**Endpoint**: `DELETE /api/developers/{id}/`  
**Authentication**: Required (Manager or Superuser only)

**Important**: All users linked to this developer will be converted to `customer` role.

**Success Response** `204 No Content`

---

### Customer Inquiries Management (Dashboard)

#### List All Inquiries

**Endpoint**: `GET /api/customer/inqury/`  
**Authentication**: Required (Staff, Manager, or Superuser)

**Success Response** `200 OK`

```json
[
  {
    "id": 10,
    "customer_id": 5,
    "phone": "+201234567890",
    "message": "I'm interested in learning more about the available apartments.",
    "interested_in": 1,
    "interested_in_name_en": "Apartment",
    "interested_in_name_ar": "شقة",
    "project_id": 5,
    "unit_id": null,
    "is_contacted": false,
    "created_at": "2026-02-03T14:00:00Z"
  },
  {
    "id": 9,
    "customer_id": 3,
    "phone": "+201234567891",
    "message": "What is the price range for villas?",
    "interested_in": 2,
    "interested_in_name_en": "Villa",
    "interested_in_name_ar": "فيلا",
    "project_id": 3,
    "unit_id": 12,
    "is_contacted": true,
    "created_at": "2026-02-02T10:00:00Z"
  }
]
```

---

#### Mark Inquiry as Contacted

**Endpoint**: `PATCH /api/customer/inqury/{id}/contacted/`  
**Authentication**: Required (Staff, Manager, or Superuser)

**Request Body**

| Field | Type | Required |
|-------|------|----------|
| `is_contacted` | boolean | Yes |

**Example Request**

```json
{
  "is_contacted": true
}
```

**Success Response** `200 OK`

```json
{
  "is_contacted": true
}
```

---

## User Roles & Permissions Matrix

### Complete Permission Table

| Endpoint | Public | Customer | Developer | Content Creator | Staff | Manager | Superuser |
|----------|--------|----------|-----------|-----------------|-------|---------|-----------|
| **Authentication** |
| Register | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Login | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Refresh Token | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Me (GET/PATCH) | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Logout | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Public Resources (GET)** |
| Countries | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Cities | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Sliders | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ads | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Features | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Articles | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Unit Types | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Developers | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Dashboard CRUD** |
| Countries (POST/PATCH) | - | - | - | - | ✅ | ✅ | ✅ |
| Countries (DELETE) | - | - | - | - | - | ✅ | ✅ |
| Cities (POST/PATCH) | - | - | - | - | ✅ | ✅ | ✅ |
| Cities (DELETE) | - | - | - | - | - | ✅ | ✅ |
| Sliders (POST/PATCH) | - | - | - | - | ✅ | ✅ | ✅ |
| Sliders (DELETE) | - | - | - | - | - | ✅ | ✅ |
| Ads (POST/PATCH) | - | - | - | - | ✅ | ✅ | ✅ |
| Ads (DELETE) | - | - | - | - | - | ✅ | ✅ |
| Features (POST/PATCH) | - | - | - | - | ✅ | ✅ | ✅ |
| Features (DELETE) | - | - | - | - | - | ✅ | ✅ |
| Articles (POST/PATCH/DELETE) | - | - | - | ✅ | - | ✅ | ✅ |
| Unit Types (POST/PATCH) | - | - | - | - | ✅ | ✅ | ✅ |
| Unit Types (DELETE) | - | - | - | - | - | ✅ | ✅ |
| Developers (POST/PATCH) | - | - | - | - | ✅ | ✅ | ✅ |
| Developers (DELETE) | - | - | - | - | - | ✅ | ✅ |
| **Customer Features** |
| Inquiry (POST) | - | ✅ | - | - | - | - | - |
| Inquiries (GET) | - | - | - | - | ✅ | ✅ | ✅ |
| Inquiry Contact (PATCH) | - | - | - | - | ✅ | ✅ | ✅ |
| **User Management** |
| Users (GET) | - | - | - | - | - | ✅ | ✅ |
| Users (POST/PATCH/DELETE) | - | - | - | - | - | ✅ | ✅ |

### Role Hierarchy

```
superuser (Complete system access)
    ↓
manager (Dashboard full access, CANNOT see superusers)
    ↓
staff (Dashboard CRUD, no delete permissions)
    ↓
content_creator (Article management only)
    ↓
developer (Developer-specific features)
    ↓
customer (Public access + inquiry submission)
```

---

## Common Patterns & Best Practices

### File Uploads

**Image Format Requirements**:
- **WebP only**: Countries, Cities, Ads, Articles
- **Any image format**: Sliders, Developer logos, User profile images

**Upload Headers**:
```
Content-Type: multipart/form-data
Authorization: Bearer <access_token>
```

### Search Functionality

Most list endpoints support text search via `?search=query`:

**Searchable Fields by Resource**:
- Countries/Cities: `name_en`, `name_ar`
- Features: `name_en`, `name_ar`
- Unit Types: `name_en`, `name_ar`
- Articles: `title_en`, `title_ar`
- Developers: `name_en`, `name_ar`

**Example**:
```
GET /api/countries/?search=egypt
GET /api/articles/?search=investment
```

### Filtering

**Homepage Visibility**:
```
GET /api/countries/?appear_on_home_page=true   # Show only homepage items
GET /api/countries/?appear_on_home_page=false  # Show non-homepage items
GET /api/countries/?appear_on_home_page=all    # Show all items
```

### Pagination

API responses may include pagination:

```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/countries/?page=2",
  "previous": null,
  "results": [...]
}
```

## Swagger UI Integration

Access interactive API documentation at: `/`

**Features**:
- Try endpoints directly from browser
- View all request/response schemas
- Test authentication with JWT tokens

**Authorization in Swagger**:
1. Click **Authorize** button
2. Enter: `Bearer <your_access_token>`
3. Click **Authorize**
4. All requests will include the token

---

## Contact & Support

- **Swagger Documentation**: `/`
or talk with me @bassanthossamxx & bassanthosamm1@outlook.com