from typing import List
from db.repository.questions import get_a_random_question, list_questions
from apis.v1.route_login import get_current_user
from db.models.user import User
from db.session import get_db
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import status
from schemas.questions import Question
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/questions/random", response_model=Question, status_code=status.HTTP_200_OK)
async def get_random_question(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    question = get_a_random_question(db=db)
    return question

@router.get("/questions/all", response_model=List[Question], status_code=status.HTTP_200_OK)
async def get_all_questions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.is_superuser:
        questions = list_questions(db=db)
        return questions
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
        )