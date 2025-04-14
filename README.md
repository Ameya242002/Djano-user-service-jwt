# Fast api -user-service-jwt
Absolutely! Here's a polished `README.md` file for your FastAPI Authentication Service based on everything you shared. It's organized, styled, and ready for GitHub:

---

# 🛡️ FastAPI Authentication Service

A robust authentication and role-based access control system built using FastAPI, SQLAlchemy, and JWT.

---

## 📁 Project Structure

```
fastapi-auth-service/
├── alembic/              # Database migrations
├── venv/                 # Virtual environment
├── main.py               # Main FastAPI app
├── models.py             # SQLAlchemy models
├── schemas.py            # Pydantic schemas
├── database.py           # DB connection/config
├── auth_routes.py        # Auth-related endpoints
├── role_routes.py        # Role management endpoints
├── config.py             # Environment/config settings
├── requirements.txt      # Project dependencies
└── .env                  # Environment variables
```

---

## 🧪 Environment Setup

### 1. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables (`.env`)

```env
DATABASE_URL=postgresql://username:password@localhost:5432/fastapi_auth
SECRET_KEY=your_super_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_MINUTES=1440
```

---

## 🛢️ Database Configuration

- Loads `.env` variables
- Creates SQLAlchemy engine and session
- `get_db()` dependency for route-level DB access

```python
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

---

## 🧱 Models

### 👤 User Model

```python
class User(Base):
    __tablename__ = 'users'
    ...
```

### 📦 Role Model

```python
class Role(Base):
    __tablename__ = 'roles'
    ...
```

### 🏷️ Enum for Roles

```python
class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"
    STAFF = "staff"
```

---

## 🧾 Pydantic Schemas

### UserCreate / UserOut / UserLogin

```python
class UserCreate(BaseModel): ...
class UserOut(BaseModel): ...
class UserLogin(BaseModel): ...
```

### RoleCreate

```python
class RoleCreate(BaseModel): ...
```

---

## 🔑 Authentication Endpoints (`auth_routes.py`)

| Method | Endpoint         | Description         |
|--------|------------------|---------------------|
| POST   | `/auth/signup`   | Register new user   |
| POST   | `/auth/login`    | Login user          |
| GET    | `/auth/refresh`  | Refresh token       |
| GET    | `/auth/validate` | Validate token      |

---

## 🧑‍💼 Role Management (`role_routes.py`)

| Method | Endpoint                            | Description               |
|--------|-------------------------------------|---------------------------|
| POST   | `/roles/`                           | Create new role           |
| PUT    | `/roles/users/{user_id}/role/{role_id}` | Assign role to user   |

---

## 🧰 Database Operations

### Create Database

```bash
psql -U postgres -c "CREATE DATABASE fastapi_auth"
```

### Run Migrations

```bash
alembic upgrade head
```

### Initialize Default Roles

```python
def init_roles():
    roles = [
        {"name": RoleEnum.ADMIN, "description": "Administrator"},
        ...
    ]
```

---

## 🔍 API Testing Flow

### 1. Register

```http
POST /auth/signup
```

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

### 2. Login

```http
POST /auth/login
```

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

### 3. Assign Role

```http
PUT /roles/users/1/role/1
Authorization: Bearer <access_token>
```

---

## 🔐 Security Features

- **Password Hashing:** bcrypt via `passlib`
- **JWT Token Handling:** Access & Refresh tokens with expiry

---

## ▶️ Running the App

### Development

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 📘 API Documentation

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ⚠️ Error Handling

| Status | Reason           |
|--------|------------------|
| 401    | Unauthorized     |
| 403    | Forbidden        |
| 404    | Not Found        |

---

🔁 FastAPI Auth Flow – Step-by-Step

1. **User Registers** → Hashes password → Saves to DB
2. **User Logs In** → Verifies creds → Returns JWT tokens
3. **User Accesses Protected Routes** with access token
4. **Refresh Token** used to get new access token
5. **Create Role** (admin only)
6. **Assign Role to User**
7. **Validate Token** for auth check

---

## ✅ Auth Flow Summary

| Action         | Method & Endpoint                 | Requires Auth        |
|----------------|-----------------------------------|----------------------|
| Register       | POST `/auth/signup`               | ❌ No                |
| Login          | POST `/auth/login`                | ❌ No                |
| Refresh Token  | GET `/auth/refresh`               | ✅ Refresh Token     |
| Validate Token | GET `/auth/validate`              | ✅ Access Token      |
| Create Role    | POST `/roles/`                    | ✅ Admin             |
| Assign Role    | PUT `/roles/users/{user_id}/role/{role_id}` | ✅ Admin   |

---

## 🔐 JWT Token Overview

| Token Type   | Used For                | Lifetime   | Sent With         |
|--------------|-------------------------|------------|-------------------|
| Access Token | Authenticated requests  | 30 minutes | Every API call    |
| Refresh Token| Renew access token      | 24 hours   | `/auth/refresh`   |

