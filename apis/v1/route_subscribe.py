from typing import List
from db.repository.subscription import subscribe_to_service, unsubscribe_to_service
from apis.v1.route_login import get_current_user
from db.models.user import User
from db.session import get_db
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import status
from schemas.questions import Question
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/subscribe", status_code=status.HTTP_200_OK)
async def subscribe(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message = subscribe_to_service(user=current_user, db=db)
    return message

@router.get("/unsubscribe", status_code=status.HTTP_200_OK)
async def unsubscribe(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message = unsubscribe_to_service(user=current_user, db=db)
    return message

