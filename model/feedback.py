"""
@Project: miniProgress
@File: feedback.py
@Auth: Bosscal
@Date: 2023/12/20
@Description: 
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR, Text, desc

from model.base import BaseModel
from const import DeleteOrNot
from utils.orm_mysql import create_db_session
from utils import format_datetime_to_string


class Feedback(BaseModel):
    __tablename__ = "feedback"

    user_id = Column(Integer, nullable=False)  # 用户ID
    msg = Column(Text, nullable=False)  # 反馈的信息

    def __init__(self, user_id: int, msg: str, **kwargs):
        self.user_id = user_id
        self.msg = msg

    def to_dict(self):
        return {"msg": self.msg, "user_id": self.user_id, "created_time": format_datetime_to_string(self.created_time)}

    @classmethod
    def add_feedback(cls, user_id: int, msg: str):
        with create_db_session() as session:
            new_feedback = Feedback(user_id, msg)
            try:
                session.add(new_feedback)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                session.rollback()
                return False

    @classmethod
    def query_feedback(cls, feedback_id: int = None):
        with create_db_session() as session:
            if feedback_id is not None:
                return session.query(cls).filter_by(id=feedback_id, is_deleted=DeleteOrNot.NotDeleted.value).all()
            return session.query(cls).filter_by(is_deleted=DeleteOrNot.NotDeleted.value).order_by(
                desc(cls.created_time)).all()
