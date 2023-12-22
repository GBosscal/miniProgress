"""
@Project: miniProgress
@File: user.py
@Auth: Bosscal
@Date: 2023/12/21
@Description: 
"""
from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.user import UserService
from const import ErrorCode


class UserRegistry:
    name: str
    avatar: str
    user_open_id: str


class UserUpdate:
    name: str
    avatar: str
    user_id: int


class UserView(HTTPMethodView):

    @openapi.summary("用户注册")
    @openapi.tag("User")
    @openapi.definition(body={"application/json": UserRegistry})
    async def post(self, request):
        name = request.json.get("name")
        avatar = request.json.get("avatar")
        user_open_id = request.json.get("user_open_id")
        data = await UserService.user_registry(name, avatar, user_open_id)
        if isinstance(data, ErrorCode):
            return response(data)
        return response(data=data)

    @openapi.summary("获取用户信息")
    @openapi.tag("User")
    @openapi.parameter("user_open_id", location="query")
    async def get(self, request):
        user_open_id = request.args.get("user_open_id")
        data = await UserService.user_info(user_open_id)
        return response(data) if isinstance(data, ErrorCode) else response(data=data)

    @openapi.summary("更新用户信息")
    @openapi.tag("User")
    @openapi.definition(body={"application/json": UserUpdate})
    async def put(self, request):
        name = request.json.get("name")
        avatar = request.json.get("avatar")
        user_id = request.json.get("user_id")
        data = await UserService.update_user_info(user_id, name, avatar)
        return response(data)


user_blueprint = Blueprint("user", url_prefix="/user", version=1)
user_blueprint.add_route(UserView.as_view(), uri="")
