from pydantic import BaseModel


class Question(BaseModel):
    id: int
    name: str
    preview: str
    difficulty_name: str
    max_score: float
    success_ratio: float
    skill: str | None = None
    link: str

    class Config:
        orm_mode = True
