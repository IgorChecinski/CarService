from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)  
    password = Column(String)

    comments = relationship("Comment", back_populates="commentator")



class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    commentator_id = Column(Integer, ForeignKey("users.id"))

    commentator = relationship("User", back_populates="comments")


