from typing import List
from sqlalchemy.orm import Session
from my_package.My_module.backend.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self) -> List[dict]:
        users = self.db.query(User).all()
        user_dicts = []
        for user in users:
            user_dict = {
                'first_name': user.first_name
            }
            user_dicts.append(user_dict)
        return user_dicts

    def get_by_id(self, id: int) -> User:
        return self.db.query(User).filter(User.idUser == id).first()

    def update(self, id: int, new_user: User) -> User:
        user = self.get_by_id(id)
        user.first_name = new_user.first_name
        user.last_name = new_user.last_name
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, id: int) -> None:
        user = self.get_by_id(id)
        self.db.delete(user)
        self.db.commit()
