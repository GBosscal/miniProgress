"""
@Project: miniProgress
@File: check_in_point.py
@Auth: Bosscal
@Date: 2023/12/20
@Description: 
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR, and_

from model.base import BaseModel
from const import DeleteOrNot
from utils.orm_mysql import create_db_session


class CheckInPoint(BaseModel):
    __tablename__ = "check_in_point"

    user_id = Column(Integer, nullable=False)  # 用户的ID
    pic = Column(VARCHAR(128), nullable=True)  # 打卡的图片
    point_id = Column(Integer, nullable=False)  # 打卡点ID

    def __init__(self, user_id, pic, point_id, **kwargs):
        self.user_id = user_id
        self.pic = pic
        self.point_id = point_id

    def to_dict(self):
        return {"point_id": self.point_id, "user_id": self.user_id, "pic": self.pic, "id": self.id}

    @classmethod
    def get_check_in_point_by_user_id(cls, user_id: int, point_ids: list):
        with create_db_session() as session:
            return session.query(cls).filter(
                and_(
                    cls.user_id == user_id,
                    cls.point_id.in_(point_ids),
                    cls.is_deleted == DeleteOrNot.NotDeleted.value
                )
            ).all()

    @classmethod
    def get_points_by_user_id(cls, user_id:int):
        with create_db_session() as session:
            return session.query(cls).filter(
                and_(
                    cls.user_id == user_id,
                    cls.is_deleted == DeleteOrNot.NotDeleted.value
                )
            ).all()

    @classmethod
    def add_check_in_point(cls, user_id: int, pic: str, point_id: int):
        with create_db_session() as session:
            new_point = CheckInPoint(user_id, pic, point_id)
            try:
                session.add(new_point)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                return False
