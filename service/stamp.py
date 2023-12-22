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
    async def add_stamp(cls, name: str, pic: str, city_id: int):
        mark = Stamp.add_stamp(name, pic, city_id)
        return ErrorCode.Success if mark else ErrorCode.StampAddError

    @classmethod
    async def update_stamp(cls, name: str, pic: str, city_id: int, stamp_id: int):
        stamp_info = Stamp.get_one_stamp(stamp_id)
        if not stamp_info:
            return ErrorCode.StampNotExists
        mark = Stamp.update_stamp(stamp_info, name, pic, city_id)
        return ErrorCode.Success if mark else ErrorCode.StampUpdateError

    @classmethod
    async def get_stamp_progress(cls, user_id: int) -> list:
        """获取个人的集邮进度"""
        # 获取全部的集邮册
        all_stamps = Stamp.get_all_stamp()
        stamp_ids = [stamp.id for stamp in all_stamps]
        city_ids = [stamp.city_id for stamp in all_stamps]
        # 获取全部的城市
        all_city = City.get_city_by_ids(city_ids)
        all_city = {str(city.id): city.city_name for city in all_city}
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
        stamp_data = []
        # 处理打卡点和集邮册之间的关系
        for stamp in all_stamps:
            stamp_info = stamp.to_dict()
            stamp_info["city_name"] = all_city.get(str(stamp.city_id)) or ""
            stamp_info["points"] = stamp_points.get(str(stamp.id)) or []
            c_i_p = [point["id"] for point in stamp_info["points"] if point["check_in"] is True]
            stamp_info["percent"] = round(len(c_i_p) / len(stamp_info["points"]), 4) if len(
                stamp_info["points"]) != 0 else 0
            stamp_info["check_in_points"] = c_i_p
            stamp_data.append(stamp_info)
        return stamp_data

    @staticmethod
    def checking_get_stamp(stamp: dict):
        if len(stamp["check_in_points"]) == len(stamp["points"]) and len(stamp["points"]) != 0:
            return True
        return False

    @classmethod
    async def get_stamp_summary(cls, user_id: int):
        """获取个人的集邮总结"""
        stamp_data = await cls.get_stamp_progress(user_id)
        result = {"point_num": 0, "stamp_num": 0, "area_num": 0, "area_list": []}
        for stamp in stamp_data:
            if stamp["city_name"] not in result["area_list"]:
                result["area_list"].append(stamp["city_name"])
            result["point_num"] += len(stamp["check_in_points"])
            if cls.checking_get_stamp(stamp):
                result["stamp_num"] += 1
        return result

    @classmethod
    async def get_each_stamp(cls, user_id: int):
        """展示个人的每一个集邮册"""
        stamp_data = await cls.get_stamp_progress(user_id)
        all_cities_stamps = {}
        for stamp in stamp_data:
            # 获取城市的全部集邮册
            if stamp["city_name"] not in all_cities_stamps:
                city_stamp = {
                    "city_name": stamp["city_name"],
                    "city_stamp_num": 0,
                    "stamps": []
                }
            else:
                city_stamp = all_cities_stamps[stamp["city_name"]]
            # 校验该集邮册是否获得
            if cls.checking_get_stamp(stamp):
                city_stamp["city_stamp_num"] += 1
            city_stamp["stamps"].append(stamp)
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
