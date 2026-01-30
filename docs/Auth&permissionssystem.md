# Authorization System & Permission Roles – Plan

This project uses a **single authentication system** with **multiple user roles**, all sharing the **same login endpoint**.
Authorization is enforced through **role-based permissions**.

---

## 1. User Roles & Access Levels

### Anonymous User

* Can view public content only:

  * Units
  * Projects
  * Cities
  * Countries
  * All publicly available pages
* Cannot submit inquiries
* Cannot access any dashboard or protected endpoint

---

### Customer

* All registered accounts start as **Customer** by default
* Can view all public content
* Can submit inquiries **only when logged in**
* Cannot access dashboard pages
* Role can be upgraded only by **Manager or Superuser**

---

### Developer

* Can access **only their own projects and units**
* Can:

  * Create new projects
  * Add units to their projects
  * Edit or delete their own projects and units
* All create/update/delete actions are marked as **Pending**

  * Pending content is hidden from public views
  * Requires approval by **Manager or Staff**
* Can edit developer profile data:

  * Name
  * Logo
  * Company information
* If `is_active = false`, login is denied
* Access is limited to the **Developer Portal (frontend)** only

---

### Content Creator

* Has access **only to Articles**
* Can:

  * Create articles
  * Edit articles
  * Delete articles
* Can view other dashboard sections in read-only mode
* No access to projects, units, or system settings

---

### Staff

* Full access to all dashboard sections
* Can:

  * Create and edit all resources
* **Cannot delete any data**
* Can review and approve pending developer content
* Has activity tracking enabled

---

### Manager

* Has full system access, equivalent to Superuser
* Can:

  * Create, edit, delete all resources
  * Approve or reject pending content
* **Cannot access Django Admin panel**
* Has activity tracking enabled

---

### Superuser

* Full system access without restrictions
* Can:

  * Perform all actions
  * Access Django Admin panel
* **Excluded from audit tracking**

---

## 2. Tracking Systems

### Audit Tracking (Actions Log)

* Enabled for:

  * Manager
  * Staff
  * Content Creator
  * Developer
  * Customer
* Tracks:

  * User identity
  * Role
  * Action performed
  * Target resource
  * Timestamp
* **Superuser actions are not tracked**

---

### Session Tracking (Analytics)

* Enabled only for:

  * Customers
  * Developers
* Tracks:

  * Page or endpoint accessed
  * Session duration
  * Activity timeline
* Used for analytics and behavior insights

---

## 3. User Model (Single Model for All Roles)

All users share the same user model with the following fields:

* Full name
* Email (unique)
* Password
* Phone number
* Role (default: `customer`)
* `is_active`
* Profile image (optional)

Each **Developer account is linked to its developer entity** to allow access to its own data in the developer portal.

---

## 4. Authentication System

All roles use the same authentication endpoints, based on **JWT**.

### Authentication Endpoints

* `POST /auth/register`
  * Registers a new **Customer** by default

* `POST /auth/login`
* `POST /auth/logout`
* `POST /auth/refresh`
* `GET /auth/me`

JWT tokens include:

* User ID
* User role

---

## 5. Permissions Layer

* Permissions are implemented inside `core.permissions`
* All authorization rules are enforced at the **view level**
* No permission logic is placed inside serializers

---

## 6. Core Models CRUD

After authentication and permissions are complete:

* Implement CRUD operations for core models
* Apply role-based permissions to each endpoint
* Ensure delete operations are restricted according to role rules

---

## Summary

* One user model
* One login system
* Role-based permissions
* Dual tracking systems
* Secure, scalable, and production-ready design

