from sqlalchemy.orm import Session

from . import models

from . import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).offset(skip).limit(limit).all()


def create_user_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = models.Comment(**comment.dict(), owner_id=user_id)
    db.add(db_comment )
    db.commit()
    db.refresh(db_comment)
    return db_comment 