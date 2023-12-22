"""
@Project: miniProgress
@File: point.py
@Auth: Bosscal
@Date: 2023/12/20
@Description: 
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR

from model.base import BaseModel
from const import DeleteOrNot
from utils.orm_mysql import create_db_session


class Point(BaseModel):
    __tablename__ = "point"

    name = Column(VARCHAR(32), nullable=False)  # 打卡点ID
    pic = Column(VARCHAR(128), nullable=True)  # 打卡点图片
    stamp_id = Column(Integer, nullable=False)  # 集邮册ID

    def __init__(self, name, pic, stamp_id, **kwargs):
        self.name = name
        self.pic = pic
        self.stamp_id = stamp_id

    def to_dict(self):
        return {"stamp_id": self.stamp_id, "name": self.name, "pic": self.pic, "id": self.id}

    @classmethod
    def get_point_by_stamp_ids(cls, stamp_ids: list):
        with create_db_session() as session:
            return session.query(cls).filter(cls.id.in_(stamp_ids)).filter_by(
                is_deleted=DeleteOrNot.NotDeleted.value).all()

    @classmethod
    def add_point(cls, name: str, pic: str, stamp_id: int):
        with create_db_session() as session:
            new_point = Point(name, pic, stamp_id)
            try:
                session.add(new_point)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                return False

    @classmethod
    def get_point_by_id(cls, point_id: int):
        with create_db_session() as session:
            return session.query(cls).filter_by(id=point_id, is_deleted=DeleteOrNot.NotDeleted.value).first()

    @classmethod
    def update_point(cls, point_info, name: str, pic: str, stamp_id: int):
        with create_db_session() as session:
            point_info.name = name
            point_info.pic = pic
            point_info.stamp_id = stamp_id
            try:
                session.merge(point_info)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                return False