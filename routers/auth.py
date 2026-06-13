from fastapi import APIRouter,Depends,HTTPException,status
from schemas import UserCreate,UserResponse
from database import get_db
from passlib.context import CryptContext
from models import User
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime,timedelta,timezone
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from jose import jwt
import os
router=APIRouter(
    tags=["Authorization"],
    prefix="/auth"
)
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_MINUTES=os.getenv("ACCESS_TOKEN_MINUTES")
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(password:str):
    return pwd_context.hash(password)
def verify_password(plain:str,hashed:str):
    return pwd_context.verify(plain,hashed)
def create_token(data:dict):
    to_encode=data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_MINUTES))
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
@router.post("/register",response_model=UserResponse,status_code=201)
def registration(user:UserCreate,db:Session=Depends(get_db)):
    user_email=db.query(User).filter(user.email==User.email).first()
    if user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email alkready taken")
    new_user={
        "email":user.email,
        "hashed_password":hash_password(user.password),
        "role":"user",
        "is_active":True
    }
    new_user_model=User(**new_user)
    db.add(new_user_model)
    db.commit()
    db.refresh(new_user_model)
    return new_user_model
@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    db_user=db.query(User).filter(form_data.username==User.email).first()
    if not db_user or not verify_password(form_data.password,db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong email or password")
    token=create_token({"sub":str(db_user.id),"role":db_user.role})
    return {"access_token":token,"token_type":"bearer"}
