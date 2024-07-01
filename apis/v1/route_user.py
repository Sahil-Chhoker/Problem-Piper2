from db.models.user import User
from db.repository.user import create_new_user, delete_user
from apis.v1.route_login import get_current_user
from db.session import get_db
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import status
from schemas.user import ShowUser
from schemas.user import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/user/register", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user

@router.get("/user/profile", response_model=ShowUser)
def get_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user


@router.delete("/user/{user_id}")
def delete_current_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    if user_id != current_user.id:
        raise HTTPException(
            detail="Only the owner can delete the user.",
            status_code=status.HTTP_403_FORBIDDEN
        )
    message = delete_user(user_id=user_id, db=db)
    if message.get("error"):
        raise HTTPException(
            detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"message": f"User deleted successfully with id {user_id}"}

