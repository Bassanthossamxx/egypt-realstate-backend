# Authentication System - API Documentation

---

##  Authentication Endpoints

All auth endpoints are prefixed with `/auth/`

### 1. Register (POST /auth/register/)
**Description**: Create a new user account (defaults to Customer role)

**Request Body**:
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone": "+1234567890",
  "password": "securePassword123",
  "password_confirm": "securePassword123",
  "profile_image": null
}
```

**Response (201 Created)**:
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "phone": "+1234567890",
    "role": "customer",
    "profile_image": null,
    "is_active": true,
    "created_at": "2025-12-25T22:00:00Z",
    "updated_at": "2025-12-25T22:00:00Z"
  }
}
```

---

### 2. Login (POST /auth/login/)
**Description**: Login with email and password, returns JWT tokens with user role

**Request Body**:
```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Response (200 OK)**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "admin@example.com",
    "full_name": "Super Admin",
    "role": "superadmin",
    "phone": null,
    "profile_image": null
  }
}
```

**JWT Payload includes**:
- `user_id`: User ID
- `email`: User email
- `role`: User role (customer, developer, staff, manager, superadmin, content_creator)
- `full_name`: User's full name

---

### 3. Logout (POST /auth/logout/)
**Description**: Logout by blacklisting the refresh token
**Auth Required**: Yes (Bearer token)

**Request Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (205 Reset Content)**:
```json
{
  "message": "Successfully logged out"
}
```

---

### 4. Refresh Token (POST /auth/refresh/)
**Description**: Get a new access token using refresh token

**Request Body**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK)**:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 5. Get Current User (GET /auth/me/)
**Description**: Get or update current user profile
**Auth Required**: Yes (Bearer token)

**Request Headers**:
```
Authorization: Bearer <access_token>
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "email": "admin@example.com",
  "full_name": "Super Admin",
  "phone": null,
  "role": "superadmin",
  "profile_image": null,
  "is_active": true,
  "created_at": "2025-12-25T22:00:00Z",
  "updated_at": "2025-12-25T22:00:00Z"
}
```

**Update Profile (PATCH /auth/me/)**: Same endpoint, send fields to update

---

## 👥 User Roles

All registered users start as **Customer** by default. Roles can be upgraded by Manager or Superadmin.

| Role | Value | Description |
|------|-------|-------------|
| Customer | `customer` | Default role, can submit inquiries when logged in |
| Developer | `developer` | Access to own projects/units, requires approval |
| Content Creator | `content_creator` | Access to article management |
| Staff | `staff` | Full read/write access, cannot delete |
| Manager | `manager` | Full system access, can approve content |
| Superadmin | `superadmin` | Full system access including Django admin |

---

## JWT Configuration

- **Access Token Lifetime**: 15 minutes
- **Refresh Token Lifetime**: 7 days
- **Token Rotation**: Enabled (new refresh token on each refresh)
- **Blacklist After Rotation**: Enabled (old tokens are blacklisted)
- **Auth Header Type**: Bearer

---

## User Model Fields

```python
- id: Integer (auto)
- email: Email (unique, required) - used for login
- full_name: String (required)
- phone: String (optional)
- role: Choice field (default: customer)
- profile_image: ImageField (optional)
- is_active: Boolean (default: True)
- is_staff: Boolean (default: False)
- is_superuser: Boolean (default: False)
- created_at: DateTime (auto)
- updated_at: DateTime (auto)
```

---

## Testing Instructions

### Test Superuser Credentials
```
Email: admin@example.com
Password: admin123
Role: superadmin
```

### Quick Test with cURL

**1. Login**:
```bash
curl -X POST http://127.0.0.1:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

**2. Register new user**:
```bash
curl -X POST http://127.0.0.1:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "full_name":"Test User",
    "phone":"+1234567890",
    "password":"testPass123",
    "password_confirm":"testPass123"
  }'
```

**3. Get current user** (replace TOKEN with access token from login):
```bash
curl -X GET http://127.0.0.1:8000/auth/me/ \
  -H "Authorization: Bearer TOKEN"
```
---

