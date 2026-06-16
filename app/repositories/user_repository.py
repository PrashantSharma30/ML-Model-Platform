from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users import User

from sqlalchemy import select

def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.scalar(stmt)


def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.scalar(stmt)


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user: User) -> User:
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()

def get_all_users(db: Session) -> list[User]:
    stmt = select(User)
    return list(db.scalars(stmt).all())

def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)