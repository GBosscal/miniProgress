"""
@Project: miniProgress
@File: stamp.py
@Auth: Bosscal
@Date: 2023/12/21
@Description: 
"""
from model.city import City
from model.stamp import Stamp
from model.point import Point
from model.check_in_point import CheckInPoint
from const import ErrorCode


class StampService:

    @classmethod
    async def add_stamp(cls, name: str, pic: str, city_name: str, latitude, longitude):
        mark = Stamp.add_stamp(name, pic, city_name, latitude, longitude)
        return ErrorCode.Success if mark else ErrorCode.StampAddError

    @classmethod
    async def update_stamp(cls, name: str, pic: str, city_name: str, stamp_id: int, latitude, longitude):
        stamp_info = Stamp.get_one_stamp(stamp_id)
        if not stamp_info:
            return ErrorCode.StampNotExists
        mark = Stamp.update_stamp(stamp_info, name, pic, city_name, latitude, longitude)
        return ErrorCode.Success if mark else ErrorCode.StampUpdateError

    @classmethod
    def _format_stamp_data(cls, stamp: Stamp, stamp_points: dict):
        """处理已经打卡的打卡点和打卡点之间的关系"""
        stamp_info = stamp.to_dict()
        stamp_info["points"] = stamp_points.get(str(stamp.id)) or []
        c_i_p = [point["id"] for point in stamp_info["points"] if point["check_in"] is True]
        stamp_info["check_in_points"] = c_i_p
        stamp_info["check_in_point_num"] = len(c_i_p)
        stamp_info["point_num"] = len(stamp_info["points"])
        if stamp_info["point_num"] != 0:
            stamp_info["percent"] = round(stamp_info["check_in_point_num"] / stamp_info["point_num"], 4)
        else:
            stamp_info["percent"] = 0.0000
        return stamp_info

    @classmethod
    def _stamp_and_point(cls, user_id: int, stamp_ids: list):
        """处理集邮册和打卡点之间的关系"""
        # 获取全部的打卡点
        all_points = Point.get_point_by_stamp_ids(stamp_ids)
        point_ids = [point.id for point in all_points]
        # 获取用户已经打卡的打卡点
        check_in_points = CheckInPoint.get_check_in_point_by_user_id(user_id, point_ids) or []
        check_in_points = {str(point.point_id): point for point in check_in_points}
        # 处理打卡点和已打卡点之间的关系
        stamp_points = {str(stamp_id): [] for stamp_id in stamp_ids}
        for point in all_points:
            point_info = point.to_dict()
            point_info["check_in"] = True if str(point.id) in check_in_points else False
            stamp_points[str(point.stamp_id)].append(point_info)
        return stamp_points

    @classmethod
    async def get_stamp_progress(cls, user_id: int) -> list:
        """获取个人的集邮进度"""
        # 获取全部的集邮册
        all_stamps = Stamp.get_all_stamp()
        stamp_ids = [stamp.id for stamp in all_stamps]
        stamp_points = cls._stamp_and_point(user_id, stamp_ids)
        stamp_data = [cls._format_stamp_data(stamp, stamp_points) for stamp in all_stamps]
        return stamp_data

    @staticmethod
    def checking_get_stamp(stamp: dict):
        if len(stamp["check_in_points"]) == len(stamp["points"]) and len(stamp["points"]) != 0:
            return True
        return False

    @classmethod
    async def get_stamp_summary(cls, user_id: int, city_name: str):
        """获取个人的集邮总结"""
        stamp_data = await cls.get_stamp_progress(user_id)
        result = {"check_in_point_num": 0, "stamp_num": 0, "area_num": 0, "area_list": []}
        for stamp in stamp_data:
            if city_name and city_name != stamp["city_name"]:
                # 只获取指定城市的
                continue
            result["check_in_point_num"] += len(stamp["check_in_points"])
            if cls.checking_get_stamp(stamp):
                result["stamp_num"] += 1
                if stamp["city_name"] not in result["area_list"]:
                    result["area_list"].append(stamp["city_name"])
        result["area_num"] = len(result["area_list"])
        return result

    @classmethod
    async def get_each_stamp(cls, user_id: int, city_name: str):
        """展示个人的每一个集邮册"""
        stamp_data = await cls.get_stamp_progress(user_id)
        all_cities_stamps = {}
        for stamp in stamp_data:
            # 获取指定城市的集邮册
            if city_name and stamp["city_name"] != city_name:
                continue
            # 获取城市的全部集邮册
            if stamp["city_name"] not in all_cities_stamps:
                city_stamp = {
                    "city_name": stamp["city_name"],
                    "city_stamp_num": 0,
                    "stamps": [],
                    "city_point_num": 0
                }
            else:
                city_stamp = all_cities_stamps[stamp["city_name"]]
            # 校验该集邮册是否获得
            if cls.checking_get_stamp(stamp):
                city_stamp["city_stamp_num"] += 1
            city_stamp["stamps"].append(stamp)
            city_stamp["city_point_num"] += stamp["point_num"]
            all_cities_stamps[stamp["city_name"]] = city_stamp
        # 从字典转换为列表
        result = [data for _, data in all_cities_stamps.items()]
        return result

    @classmethod
    async def get_one_stamp(cls, stamp_id: int, user_id: int):
        """展示单个集邮册"""
        # 获取特定的集邮册
        stamp_info = Stamp.get_one_stamp(stamp_id)
        if not stamp_info:
            return ErrorCode.StampNotExists
        # 获取集邮册的所有打卡点
        all_points = Point.get_point_by_stamp_ids([stamp_id])
        point_ids = [point.id for point in all_points]
        # 获取已经打卡的打卡点
        c_i_p = CheckInPoint.get_check_in_point_by_user_id(user_id, point_ids) or []
        c_i_p = {str(point.point_id): point for point in c_i_p}
        result = stamp_info.to_dict()
        result["points"] = []
        c_percent = 0
        for point in all_points:
            point_info = point.to_dict()
            point_info["check_in"] = False
            if str(point.id) in c_i_p:
                c_percent += 1
                point_info["check_in"] = True
            result["points"].append(point_info)
        result["percent"] = round(c_percent / len(c_i_p), 4) if len(c_i_p) != 0 else 0
        return result

    @classmethod
    async def fuzzy_query_stamp(cls, user_id: int, city_name: str, latitude, longitude):
        """根据城市ID以及经纬度模糊查询集邮册以及返回集邮册进度"""
        stamps = Stamp.query_stamp_by_latitude(city_name, latitude, longitude)
        stamp_ids = [stamp[0].id for stamp in stamps]
        stamp_points = cls._stamp_and_point(user_id, stamp_ids)
        all_data = []
        for stamp in stamps:
            data = cls._format_stamp_data(stamp[0], stamp_points)
            data["distance"] = stamp[1]
            all_data.append(data)
        return all_data
