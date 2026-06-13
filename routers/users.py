from fastapi import APIRouter,Depends,HTTPException,status
from schemas import UserResponse
from database import get_db
from models import User
from sqlalchemy.orm import Session
from dependencies import get_current_user,require_admin
router=APIRouter(
    tags=["Users"],
    prefix="/users"
)
@router.get("/",response_model=list[UserResponse])
def get_users(admin:User=Depends(require_admin),db:Session=Depends(get_db)):
    return db.query(User).all()
@router.get("/me",response_model=UserResponse)
def get_me(current_user:User=Depends(get_current_user)):
    return current_user
@router.delete("/{id}",status_code=204)
def delete_user(id:int,admin:User=Depends(require_admin),db:Session=Depends(get_db)):
    db_user=db.query(User).filter(id==User.id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
@router.patch("/{id}/role")
def change_role(id:int,role:str,admin:User=Depends(require_admin),db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.id==id).first()
    db_user.role=role
    db.commit()
    return db_user