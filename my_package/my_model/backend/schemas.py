from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentCreate(BaseModel):
    content: str
    commentator_id: int


class Comment(BaseModel):
    content: str


class UserBase(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    comments: list[Comment] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    

    
