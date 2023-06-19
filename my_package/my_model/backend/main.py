from fastapi import (
    Depends, FastAPI, HTTPException, Request, status, Form, Response
)
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from . import crud, models
from . import schemas
from .database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from starlette.middleware.sessions import SessionMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware for session management
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Constants for token generation
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Templates and static files configuration
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



#FUNCTIONS!

# Function to create an access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to authenticate a user
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

# Dependency to get the optional current user from the session
def get_optional_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get('user_id')
    if user_id is not None:
        user = db.query(models.User).get(user_id)
        if user is not None:
            return user
    return None

#not exacly sure why we need to implement those 2 functions, after finishing everything i'll try to delete on and implement the other function in the place of some endpoints

# Dependency to get the current user from the session
def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return None

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None

    return user

# Save sum to user endpoint, this endpointis only creatted for identyfing that the current user picked services and the sum of those services were added to his account(this is onlt=y a message it does not do that in db)
@app.post("/save_sum")
async def save_sum(
    request: Request,
    current_user: models.User = Depends(get_optional_current_user)
):
    if not current_user:
        return RedirectResponse(url="/login_successful")
   
    return {"message": "Total sum added to user"}


##ENDPOINTS!

# Root endpoint
@app.get("/")
def read_root(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_optional_current_user)
):
    return templates.TemplateResponse("home.html", {"request": request, "user": current_user})


# Add comment endpoint for creating a comment
@app.post("/add_comment")
async def add_comment(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    form_data = await request.form()
    comment = form_data.get("comment")
    users = crud.get_users(db)

    if comment:
        db_comment = crud.create_comment(db=db, comment=comment, user_id=current_user.id)

        return templates.TemplateResponse("index.html", {"request": request, "users": users})

    else:
        # Handle the case when the comment is not provided
        error_message = "Comment is required"
        return templates.TemplateResponse("index.html", {"request": request, "users": users,"error_message": error_message})



# Comment endpoint
@app.get("/comments/")
def read_comments(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: models.User = Depends(get_optional_current_user)):
    users = crud.get_users(db)
    user = current_user if current_user else None
    return templates.TemplateResponse("index.html", {"request": request, "users": users, "user": user})


# Service endpoint
@app.get("/services/")
def read_services(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_optional_current_user)
):
    services = [
        {"name": "Service 1", "description": "This is service 1", "price": 100},
        {"name": "Service 2", "description": "This is service 2", "price": 200},
        {"name": "Service 3", "description": "This is service 3", "price": 300},
    ]
    return templates.TemplateResponse("service.html", {"request": request, "services": services, "user": current_user})

# Token-based login endpoint, 
@app.post("/token")
def login_for_access_token(
    request: Request,
    db: Session = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...),
):
    user = authenticate_user(db, username, password)
    if not user:
        error_message = "Incorrect username or password."
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error_message": error_message}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    request.session['user_id'] = user.id
    return RedirectResponse(url='/login_successful', status_code=303)

# Login successful endpoint
@app.get("/login_successful")
def login_successful(request: Request):
    user_id = request.session.get('user_id')
    if not user_id:
        error_message = "You are not logged in."
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error_message": error_message}
        )
    return templates.TemplateResponse("login_successful.html", {"request": request})

# Login GET
@app.get("/login", response_class=HTMLResponse)
def open_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error_message": ""})

# Login successful page GET
@app.get("/login_successful", response_class=HTMLResponse)
def login_successful(request: Request):
    return templates.TemplateResponse("login_successful.html", {"request": request})

# Logout endpoint
@app.get("/logout")
def logout(request: Request, current_user: models.User = Depends(get_optional_current_user)):
    request.session.pop('user_id', None)
    return RedirectResponse(url="/")

# Register page endpoint
@app.get("/register")
def register_get(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("create_account.html", {"request": request})

# Register user endpoint
from fastapi import Form, HTTPException

@app.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        error_message = "Username already exists. Please choose a different username."
        return templates.TemplateResponse(
            "create_account.html",
            {"request": request, "error_message": error_message}
        )
    if password != confirm_password:
        error_message = "Password and Confirm Password do not match."
        return templates.TemplateResponse(
            "create_account.html",
            {"request": request, "error_message": error_message}
        )

    hashed_password = pwd_context.hash(password)
    user_data = schemas.UserCreate(username=username, password=hashed_password)
    db = crud.create_user(db, user_data)
    return templates.TemplateResponse("correctRegister.html", {"request": request})
