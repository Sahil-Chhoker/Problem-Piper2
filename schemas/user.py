from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class ShowUser(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:  # tells pydantic to convert even non dict obj to json
        orm_mode = True
