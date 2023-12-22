"""
@Project: miniProgress
@File: stamp.py
@Auth: Bosscal
@Date: 2023/12/20
@Description: 
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR

from model.base import BaseModel
from const import DeleteOrNot
from utils.orm_mysql import create_db_session


class Stamp(BaseModel):
    __tablename__ = "stamp"

    name = Column(VARCHAR(32), nullable=False)  # 集邮册名称
    pic = Column(VARCHAR(128), nullable=True)  # 集邮册图片
    city_id = Column(Integer, nullable=False)  # 城市ID

    def __init__(self, name, pic, city_id, **kwargs):
        self.name = name
        self.pic = pic
        self.city_id = city_id

    def to_dict(self):
        return {"city_id": self.city_id, "name": self.name, "pic": self.pic, "id": self.id}

    @classmethod
    def get_all_stamp(cls):
        with create_db_session() as session:
            return session.query(cls).filter_by(is_deleted=DeleteOrNot.NotDeleted.value).all()

    @classmethod
    def get_one_stamp(cls, stamp_id: int):
        with create_db_session() as session:
            return session.query(cls).filter_by(id=stamp_id, is_deleted=DeleteOrNot.NotDeleted.value).first()

    @classmethod
    def add_stamp(cls, name: str, pic: str, city_id: int):
        with create_db_session() as session:
            new_stamp = Stamp(name, pic, city_id)
            try:
                session.add(new_stamp)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                return False

    @classmethod
    def update_stamp(cls, stamp_info, name: str, pic: str, city_id: int):
        with create_db_session() as session:
            stamp_info.name = name
            stamp_info.pic = pic
            stamp_info.city_id = city_id
            try:
                session.merge(stamp_info)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                return False
