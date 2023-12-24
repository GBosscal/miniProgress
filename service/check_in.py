"""
@Project: miniProgress
@File: check_in.py
@Auth: Bosscal
@Date: 2023/12/22
@Description: 
"""

from const import ErrorCode
from model.check_in_point import CheckInPoint


class CheckInPointService:

    @classmethod
    async def add_point(cls, user_id: int, pic: str, point_id: int):
        mark = CheckInPoint.add_check_in_point(user_id, pic, point_id)
        return ErrorCode.Success if mark else ErrorCode.CheckInPointAddError

    @classmethod
    async def get_point_by_user_id(cls, user_id: int):
        points = CheckInPoint.get_points_by_user_id(user_id)
        return [point.to_dict() for point in points]
