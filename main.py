from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from my_package.My_module.backend.repositories.userRepository import UserRepository
from my_package.My_module.backend.models.user import User, SessionLocal
import os

app = FastAPI()


# Get the absolute path to the templates directory
templates_directory = os.path.join(os.path.dirname(__file__), 'my_package', 'My_module', 'frontend', 'templates')

# Create Jinja2Templates with the templates directory
templates = Jinja2Templates(directory=templates_directory)

# create a session to connect to the database
db = SessionLocal()

# create a user repository object
user_repo = UserRepository(db)




@app.get('/index/', response_class=HTMLResponse)
def index(request: Request):
    users = user_repo.get_all()
    context = {'request': request, 'users': users}
    return templates.TemplateResponse("index.html", context)



# create a user
# new_user = User(idUser=7, first_name="Greg", last_name="Doe")
# created_user = user_repo.create(new_user)
# print(f"Created user: {created_user}")



# # get a user by id
# user_by_id = user_repo.get_by_id(created_user.idUser)
# print(f"User by id: {user_by_id}")

# # update a user
# updated_user = User(idUser=created_user.idUser, first_name="Jane", last_name="Doe")
# updated_user = user_repo.update(created_user.idUser, updated_user)
# print(f"Updated user: {updated_user}")

# # delete a user
# user_repo.delete(created_user.idUser)
