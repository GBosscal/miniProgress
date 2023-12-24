"""
@Project: miniProgress
@File: point.py
@Auth: Bosscal
@Date: 2023/12/20
@Description: 
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR, text
from sqlalchemy import func
from sqlalchemy import SavepointClause
from geoalchemy2 import Geometry

from model.base import BaseModel
from const import DeleteOrNot
from utils.orm_mysql import create_db_session


class Point(BaseModel):
    __tablename__ = "point"

    name = Column(VARCHAR(32), nullable=False)  # 打卡点ID
    pic = Column(VARCHAR(128), nullable=True)  # 打卡点图片
    stamp_id = Column(Integer, nullable=False)  # 集邮册ID
    location = Column(Geometry('POINT'), default="Point(0 0)")

    # latitude = Column(DECIMAL(10, 8))  # 打卡点的纬度
    # longitude = Column(DECIMAL(11, 8))  # 打卡点的经度

    def __init__(self, name, pic, stamp_id, location, **kwargs):
        self.name = name
        self.pic = pic
        self.stamp_id = stamp_id
        self.location = location

    @staticmethod
    def create_location(latitude, longitude):
        location = func.ST_GeomFromText(f'Point({longitude} {latitude})', 4326)
        return location

    @classmethod
    def get_latitude_longitude(cls, case_id: int):
        with create_db_session() as session:
            latitude, longitude = session.query(func.ST_Y(cls.location), func.ST_X(cls.location)).filter(
                cls.id == case_id).first()
            return latitude, longitude

    def to_dict(self):
        data = {
            "stamp_id": self.stamp_id, "name": self.name,
            "pic": self.pic, "id": self.id
        }
        latitude, longitude = self.get_latitude_longitude(self.id)
        data.update({"latitude": latitude, "longitude": longitude})
        return data

    @classmethod
    def get_point_by_stamp_ids(cls, stamp_ids: list):
        with create_db_session() as session:
            return session.query(cls).filter(cls.id.in_(stamp_ids)).filter_by(
                is_deleted=DeleteOrNot.NotDeleted.value).all()

    @classmethod
    def add_point(cls, name: str, pic: str, stamp_id: int, latitude, longitude):
        with create_db_session() as session:
            new_point = Point(name, pic, stamp_id, cls.create_location(latitude, longitude))
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
    def query_point_by_latitude(cls, stamp_ids: list, latitude, longitude):
        location = cls.create_location(latitude, longitude)
        radius = 1000  # 距离设定为1000米内
        with create_db_session() as session:
            results = session.query(cls).filter(
                cls.stamp_id.in_(stamp_ids),
                func.ST_Distance_Sphere(cls.location, location) <= radius
            ).all()
            return results

    @classmethod
    def update_point(cls, point_info, name: str, pic: str, stamp_id: int, latitude, longitude):
        with create_db_session() as session:
            point_info.name = name
            point_info.pic = pic
            point_info.stamp_id = stamp_id
            point_info.location = cls.create_location(latitude, longitude)
            try:
                session.merge(point_info)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                return False
