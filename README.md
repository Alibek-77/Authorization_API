# 🔐 Auth API
 
JWT authentication system built with FastAPI and PostgreSQL. Supports registration, login, role-based access control, and token validation.
 
## Tech Stack
 
- **FastAPI** — REST API framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **python-jose** — JWT tokens
- **passlib + bcrypt** — password hashing
- **python-dotenv** — environment config
## Project Structure
 
```
auth_api/
├── main.py            # app entry point
├── database.py        # database connection
├── models.py          # SQLAlchemy models
├── schemas.py         # Pydantic schemas
├── dependencies.py    # auth dependencies
└── routers/
    ├── auth.py        # register + login
    └── users.py       # user management
```
 
## Setup
 
**1. Clone and install**
```bash
git clone https://github.com/your-username/auth-api.git
cd auth-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
 
**2. Create database**
```sql
CREATE DATABASE auth_db;
```
 
**3. Create `.env`**
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/auth_db
SECRET_KEY=your_secret_key_min_32_chars
ALGORITHM=HS256
ACCESS_TOKEN_MINUTES=30
```
 
**4. Run**
```bash
uvicorn main:app --reload
```
 
## Endpoints
 
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register new user | — |
| POST | `/auth/login` | Login, get JWT token | — |
| GET | `/users/me` | Get current user | ✓ |
| GET | `/users/` | List all users | Admin |
| PATCH | `/users/{id}/role` | Change user role | Admin |
| DELETE | `/users/{id}` | Delete user | Admin |
 
## Roles
 
- `user` — default role, access to own data only
- `admin` — full access to all endpoints
To make a user admin, update directly in database:
```sql
UPDATE users SET role = 'admin' WHERE email = 'your@email.com';
```
 
## How JWT Works
 
```
1. Register  → password is hashed with bcrypt
2. Login     → server returns JWT token (30 min)
3. Request   → send token in Authorization header
4. Server    → validates token, returns user data
```
 
## Documentation
 
Swagger UI: `http://localhost:8000/docs`