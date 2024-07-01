from sqlalchemy import Column, Integer, String, Float, Text
from db.base_class import Base

class QuestionBase(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    preview = Column(Text, nullable=False)
    difficulty_name = Column(String, nullable=False)
    max_score = Column(Integer, nullable=False)
    success_ratio = Column(Float)
    skill = Column(String)
    link = Column(String, nullable=False)
