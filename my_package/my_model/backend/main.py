from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

from . import crud, models
from . import schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/comments/")
def read_comments(request: Request, db: Session = Depends(get_db)):
    comments = crud.get_comments(db)
    return templates.TemplateResponse("index.html", {"request": request, "comments": comments})



@app.post("/add_comment")
def add_comment(comment_data: schemas.CommentCreate, db: Session = Depends(get_db)):
    user_id = 1  # Replace with the actual user ID
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_comment = crud.create_user_comment(db=db, comment=comment_data, user_id=user_id)
    return db_comment

#trzeba stworzyc services w bazie( z jakiegos powodu hard code nie dziala)
@app.get("/services/")
def read_services(request: Request, db: Session = Depends(get_db)):
    services = [
        {"name": "Service 1", "description": "This is service 1", "price": "$100"},
        {"name": "Service 2", "description": "This is service 2", "price": "$200"},
        {"name": "Service 3", "description": "This is service 3", "price": "$300"},
    ]
    return templates.TemplateResponse("service.html", {"request": request, "service": services})

# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.get("/comments/", response_model=list[schemas.Comment])
# def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     comments = crud.get_comments(db, skip=skip, limit=limit)
#     return comments


# # Define a request body model for creating a comment
# class CommentCreateRequest(BaseModel):
#     user_id: int
#     content: str


# @app.post("/comments", response_model=schemas.Comment)
# def create_comment(comment_data: CommentCreateRequest, db: Session = Depends(get_db)):
#     user_id = comment_data.user_id
#     content = comment_data.content
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     comment = schemas.CommentCreate(content=content)
#     db_comment = crud.create_user_comment(db=db, comment=comment, user_id=user_id)
#     return db_comment
