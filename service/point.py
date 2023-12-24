"""
@Project: miniProgress
@File: point.py
@Auth: Bosscal
@Date: 2023/12/22
@Description: 
"""

from model.point import Point
from model.stamp import Stamp
from const import ErrorCode


class PointService:

    @classmethod
    async def add_point(cls, name: str, pic: str, stamp_id: int, latitude, longitude):
        """新增一个打卡点"""
        # 判断当前集邮册是否存在重名的打卡点
        mark = Point.checking_point_dup_name(stamp_id, name)
        if mark:
            return ErrorCode.PointDupName
        mark = Point.add_point(name, pic, stamp_id, latitude, longitude)
        return ErrorCode.Success if mark else ErrorCode.PointAddError

    @classmethod
    async def update_point(cls, name: str, pic: str, stamp_id: int, point_id: int, latitude, longitude):
        """更新一个打卡点"""
        point_info = Point.get_point_by_id(point_id)
        if not point_info:
            return ErrorCode.PointNotExists
        mark = Point.checking_point_dup_name(stamp_id, name)
        if mark:
            return ErrorCode.PointDupName
        mark = Point.update_point(point_info, name, pic, stamp_id, latitude, longitude)
        return ErrorCode.Success if mark else ErrorCode.PointUpdateError

    @classmethod
    async def fuzzy_query_point(cls, city_name: str, latitude, longitude):
        """根据城市ID以及经纬度模糊查询打卡点"""
        stamps = Stamp.query_stamp_by_city_name(city_name)
        if not stamps:
            return ErrorCode.StampNotExistsInCity
        stamp_ids = [stamp.id for stamp in stamps]
        points = Point.query_point_by_latitude(stamp_ids, latitude, longitude)
        return [point.to_dict() for point in points]

    @classmethod
    async def query_point_by_city_name(cls, city_name: str):
        """根据城市名称查询打卡点"""
        stamps = Stamp.query_stamp_by_city_name(city_name)
        if not stamps:
            return ErrorCode.StampNotExistsInCity
        stamp_ids = [stamp.id for stamp in stamps]
        points = Point.get_point_by_stamp_ids(stamp_ids)
        return [point.to_dict() for point in points]
