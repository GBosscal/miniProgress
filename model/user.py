"""
@Project: miniProgress
@File: user.py.py
@Auth: Bosscal
@Date: 2023/12/20
@Description: 
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR

from model.base import BaseModel
from const import DeleteOrNot
from utils.orm_mysql import create_db_session


class User(BaseModel):
    __tablename__ = "user"

    user_name = Column(VARCHAR(32), nullable=False)  # 用户名称
    user_avatar = Column(VARCHAR(128), nullable=False)  # 用户头像
    user_open_id = Column(VARCHAR(64), nullable=False)  # 用户的开放ID

    def __init__(self, user_name: str, user_avatar: str, user_open_id: str, **kwargs):
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.user_open_id = user_open_id

    def to_dict(self):
        return {
            "user_name": self.user_name, "user_avatar": self.user_avatar, "user_open_id": self.user_open_id,
            "created_time": self.created_time, "updated_time": self.updated_time
        }

    @classmethod
    def query_user_by_open_id(cls, open_id: str):
        with create_db_session() as session:
            return session.query(cls).filter_by(user_open_id=open_id, is_deleted=DeleteOrNot.NotDeleted.value).first()

    @classmethod
    def query_user_by_user_id(cls, user_id: int):
        with create_db_session() as session:
            return session.query(cls).filter_by(id=user_id, is_deleted=DeleteOrNot.NotDeleted.value).first()

    @classmethod
    def add_user(cls, name: str, avatar: str, open_id: str):
        with create_db_session() as session:
            new_user = User(name, avatar, open_id)
            try:
                session.add(new_user)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                return False

    @classmethod
    def update_user(cls, user_info, name: str, avatar: str):
        with create_db_session() as session:
            user_info.user_name = name
            user_info.user_avatar = avatar
            try:
                session.merge(user_info)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                session.rollback()
                return False

    @classmethod
    def delete_user(cls, user_id: int = None, user_open_id: str = None):
        if user_id is None and user_open_id is None:
            print("delete user must by user_id or user_open_id")
            return False
        with create_db_session() as session:
            if user_id:
                session.query(cls).filter_by(id=user_id).delete()
            if user_open_id:
                session.query(cls).filter_by(user_open_id=user_open_id).delete()
            try:
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                session.rollback()
                return False
