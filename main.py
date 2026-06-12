from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
fake_users_db = []
counter_users = 0
SECRET_KEY = "fjkhsdfjksdhfjhjwefj02ru0239rjewlf"
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
app = FastAPI()
class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=2)
class UserResponse(BaseModel):
    id: int
    email: str
class Token(BaseModel):
    access_token: str
    token_type: str
def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
def create_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    for us in fake_users_db:
        if int(user_id) == us["id"]:  # приводим типы
            return us
    raise HTTPException(status_code=404, detail="User not found")
@app.post("/auth/register", status_code=201, response_model=UserResponse)
def register(user: UserCreate):
    global counter_users
    for us in fake_users_db:
        if us["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already taken")
    counter_users += 1
    new_user = {
        "id": counter_users,
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "role": "admin"
    }
    fake_users_db.append(new_user)
    return new_user
@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = None
    for us in fake_users_db:
        if us["email"] == form_data.username:
            user = us
            break
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Wrong email or password")
    token = create_token({"sub": str(user["id"]), "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}
@app.get("/users/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
@app.get("/users/admin")
def admin_page(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return {"message": f"Welcome admin — {current_user['email']}"}