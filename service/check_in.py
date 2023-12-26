"""
@Project: miniProgress
@File: check_in.py
@Auth: Bosscal
@Date: 2023/12/22
@Description: 
"""

from const import ErrorCode
from model.check_in_point import CheckInPoint
from model.point import Point


class CheckInPointService:

    @classmethod
    async def add_point(cls, user_id: int, pic: str, point_id: int, latitude, longitude):
        # 判断打卡点是否存在
        if not Point.get_point_by_id(point_id):
            return ErrorCode.PointNotExists
        # 判断距离是否足够小
        if not Point.checking_radius_for_point(point_id, latitude, longitude):
            return ErrorCode.CheckInPointTooFar
        mark = CheckInPoint.add_check_in_point(user_id, pic, point_id)
        return ErrorCode.Success if mark else ErrorCode.CheckInPointAddError

    @classmethod
    async def get_point_by_user_id(cls, user_id: int):
        points = CheckInPoint.get_points_by_user_id(user_id)
        return [point.to_dict() for point in points]
