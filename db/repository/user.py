from core.hashing import Hasher
from db.models.user import User
from schemas.user import ShowUser, UserCreate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session):
    user = User(
        email=user.email,
        password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id: int, db: Session):
    user_in_db = db.query(User).filter(User.id == user_id).first()
    if not user_in_db:
        return {"error": f"User not found with id {user_id}"}
    db.delete(user_in_db)
    db.commit()
    return {"message": f"Deleted User with id {user_id}"}
    