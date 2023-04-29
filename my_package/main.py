from sqlalchemy.orm import Session
from My_module.repositories.userRepository import UserRepository
from My_module.models.user import User,SessionLocal



# create a session to connect to the database
db = SessionLocal()

# create a user repository object
user_repo = UserRepository(db)

# create a user
new_user = User(idUser=4,first_name="Tom", last_name="Doe")
created_user = user_repo.create(new_user)
print(f"Created user: {created_user}")

# get all users
all_users = user_repo.get_all()
print(f"All users: {all_users}")

# get a user by id
user_by_id = user_repo.get_by_id(created_user.idUser)
print(f"User by id: {user_by_id}")

# update a user
updated_user = User(idUser=created_user.idUser, first_name="Jane", last_name="Doe")
updated_user = user_repo.update(created_user.idUser, updated_user)
print(f"Updated user: {updated_user}")

# delete a user
user_repo.delete(created_user.idUser)
print(f"Deleted user with id {created_user.idUser}")