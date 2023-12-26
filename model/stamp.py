"""
@Project: miniProgress
@File: stamp.py
@Auth: Bosscal
@Date: 2023/12/20
@Description: 
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR, func
from geoalchemy2 import Geometry

from model.base import BaseModel
from const import DeleteOrNot
from utils.orm_mysql import create_db_session


class Stamp(BaseModel):
    __tablename__ = "stamp"

    name = Column(VARCHAR(32), nullable=False)  # 集邮册名称
    pic = Column(VARCHAR(128), nullable=True)  # 集邮册图片
    city_name = Column(VARCHAR(64), nullable=False)  # 城市名称
    location = Column(Geometry('POINT'))

    def __init__(self, name, pic, city_name, location, **kwargs):
        self.name = name
        self.pic = pic
        self.city_name = city_name
        self.location = location

    @staticmethod
    def create_location(latitude, longitude):
        location = func.ST_GeomFromText(f'Point({longitude} {latitude})', 4326)
        return location

    @classmethod
    def get_latitude_longitude(cls, stamp_id: int):
        with create_db_session() as session:
            latitude, longitude = session.query(func.ST_Y(cls.location), func.ST_X(cls.location)).filter(
                cls.id == stamp_id).first()
            return latitude, longitude

    def to_dict(self):
        data = {
            "city_name": self.city_name, "name": self.name, "pic": self.pic, "id": self.id
        }
        latitude, longitude = self.get_latitude_longitude(self.id)
        data.update({"latitude": latitude, "longitude": longitude})
        return data

    @classmethod
    def get_all_stamp(cls):
        with create_db_session() as session:
            return session.query(cls).filter_by(is_deleted=DeleteOrNot.NotDeleted.value).all()

    @classmethod
    def get_one_stamp(cls, stamp_id: int):
        with create_db_session() as session:
            return session.query(cls).filter_by(id=stamp_id, is_deleted=DeleteOrNot.NotDeleted.value).first()

    @classmethod
    def query_stamp_by_city_name(cls, city_name: str):
        with create_db_session() as session:
            return session.query(cls).filter_by(city_name=city_name, is_deleted=DeleteOrNot.NotDeleted.value).all()

    @classmethod
    def add_stamp(cls, name: str, pic: str, city_name: str, latitude, longitude):
        with create_db_session() as session:
            new_stamp = Stamp(name, pic, city_name, cls.create_location(latitude, longitude))
            try:
                session.add(new_stamp)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                return False

    @classmethod
    def update_stamp(cls, stamp_info, name: str, pic: str, city_name: str, latitude, longitude):
        location = cls.create_location(latitude, longitude)
        with create_db_session() as session:
            stamp_info.name = name
            stamp_info.pic = pic
            stamp_info.city_name = city_name
            stamp_info.location = location
            try:
                session.merge(stamp_info)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                return False

    @classmethod
    def query_stamp_by_latitude(cls, city_name: str, latitude, longitude):
        location = cls.create_location(latitude, longitude)
        radius = 1000  # 距离设定为1000米内
        with create_db_session() as session:
            results = session.query(cls, func.ST_Distance_Sphere(cls.location, location).label('distance')).filter(
                cls.city_name == city_name,
                func.ST_Distance_Sphere(cls.location, location) <= radius
            ).all()
            return results
