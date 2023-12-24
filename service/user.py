"""
@Project: miniProgress
@File: user.py
@Auth: Bosscal
@Date: 2023/12/20
@Description: 
"""
from model.user import User
from const import ErrorCode
from utils import days_since_given_date_by_datetime


class UserService:

    @staticmethod
    def format_user_info(user_info: User):
        return {
            "name": user_info.user_name,
            "party_time": days_since_given_date_by_datetime(user_info.created_time),
            "avatar": user_info.user_avatar,
            "user_id": user_info.id
        }

    @classmethod
    async def user_registry(cls, name: str, avatar: str, user_open_id: str):
        """用户注册的函数"""
        user_info = User.query_user_by_open_id(user_open_id)
        if user_info:
            return ErrorCode.UserExists
        # 用户还没注册
        mark = User.add_user(name, avatar, user_open_id)
        if not mark:
            return ErrorCode.UserUpdateError
        user_info = User.query_user_by_open_id(user_open_id)
        return cls.format_user_info(user_info)

    @classmethod
    async def user_info(cls, user_open_id: str):
        """获取用户信息"""
        user_info = User.query_user_by_open_id(user_open_id)
        if not user_info:
            return ErrorCode.UserNotExists
        user_info = cls.format_user_info(user_info)
        return user_info

    @classmethod
    async def update_user_info(cls, user_id: int, name: str, avatar: str):
        """更新用户信息"""
        user_info = User.query_user_by_user_id(user_id)
        if not user_info:
            return ErrorCode.UserNotExists
        mark = User.update_user(user_info, name, avatar)
        if not mark:
            return ErrorCode.UserUpdateError
        return ErrorCode.Success

    @classmethod
    async def delete_user_by_open_id(cls, user_open_id: str):
        """通过open——id删除用户"""
        mark = User.delete_user(user_open_id=user_open_id)
        return ErrorCode.Success if mark else ErrorCode.UserDeleteError
