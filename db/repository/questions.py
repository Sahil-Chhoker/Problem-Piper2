from core.hashing import Hasher
from db.models.questions import QuestionBase
from schemas.questions import Question
from sqlalchemy.orm import Session
from sqlalchemy import func


def get_a_random_question(db: Session):
    result = db.query(QuestionBase).order_by(func.random()).first()
    return result

def list_questions(db: Session):
    result = db.query(QuestionBase).all()
    return result