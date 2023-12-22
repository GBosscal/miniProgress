"""
@Project: miniProgress
@File: point.py
@Auth: Bosscal
@Date: 2023/12/22
@Description: 
"""

from model.point import Point
from const import ErrorCode


class PointService:

    @classmethod
    async def add_point(cls, name: str, pic: str, stamp_id: int):
        """新增一个打卡点"""
        mark = Point.add_point(name, pic, stamp_id)
        return ErrorCode.Success if mark else ErrorCode.PointAddError

    @classmethod
    async def update_point(cls, name: str, pic: str, stamp_id: int, point_id: int):
        """更新一个打卡点"""
        point_info = Point.get_point_by_id(point_id)
        if not point_info:
            return ErrorCode.PointNotExists
        mark = Point.update_point(point_info, name, pic, stamp_id)
        return ErrorCode.Success if mark else ErrorCode.PointUpdateError
