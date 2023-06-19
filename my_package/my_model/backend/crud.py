from sqlalchemy.orm import Session
from .models import User, Comment
from .schemas import UserCreate, CommentCreate


def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_comment(db: Session, comment: CommentCreate, user_id: int):
    db_comment = Comment(content=comment, commentator_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments(db: Session):
    return db.query(Comment, User).join(User, Comment.commentator_id == User.id).all()

