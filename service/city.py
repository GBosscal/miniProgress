"""
@Project: miniProgress
@File: city.py
@Auth: Bosscal
@Date: 2023/12/21
@Description: 
"""

from const import ErrorCode
from model.city import City


class CityService:

    @classmethod
    async def add_city(cls, name: str):
        """新增一个城市"""
        cities = City.get_city_by_name(name)
        if cities:
            return ErrorCode.CityExists
        mark = City.add_city(name)
        return ErrorCode.Success if mark else ErrorCode.CityAddError

    @classmethod
    async def update_city(cls, city_id: int, name: str):
        """更新一个城市"""
        city_info = City.get_city_by_id(city_id)
        if not city_info:
            return ErrorCode.CityNotExists
        mark = City.update_city(city_info, name)
        return ErrorCode.Success if mark else ErrorCode.CityUpdateError

    @classmethod
    async def get_all_cities(cls):
        """获取所有城市"""
        cities = City.get_cities()
        result = [city.to_dict() for city in cities]
        return result
