"""
@Project: miniProgress
@File: city.py
@Auth: Bosscal
@Date: 2023/12/20
@Description: 
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR

from model.base import BaseModel
from const import DeleteOrNot
from utils.orm_mysql import create_db_session


class City(BaseModel):
    __tablename__ = "city"

    city_name = Column(VARCHAR(32), nullable=False)  # 城市名称

    def __init__(self, city_name, **kwargs):
        self.city_name = city_name

    def to_dict(self):
        return {"city_name": self.city_name, "id": self.id}

    @classmethod
    def add_city(cls, name):
        with create_db_session() as session:
            new_city = City(city_name=name)
            try:
                session.add(new_city)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                session.rollback()
                return False

    @classmethod
    def update_city(cls, city_info, name: str):
        city_info.city_name = name
        with create_db_session() as session:
            try:
                session.merge(city_info)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                session.rollback()
                return False

    @classmethod
    def get_cities(cls):
        with create_db_session() as session:
            return session.query(cls).all()

    @classmethod
    def get_city_by_name(cls, name: str):
        with create_db_session() as session:
            return session.query(cls).filter_by(city_name=name, is_deleted=DeleteOrNot.NotDeleted.value).first()

    @classmethod
    def get_city_by_id(cls, city_id: int):
        with create_db_session() as session:
            return session.query(cls).filter_by(id=city_id, is_deleted=DeleteOrNot.NotDeleted.value).first()

    @classmethod
    def get_city_by_ids(cls, city_ids: list):
        with create_db_session() as session:
            return session.query(cls).filter(cls.id.in_(city_ids)).filter_by(
                is_deleted=DeleteOrNot.NotDeleted.value).all()
