"""
@Project: miniProgress
@File: check_in.py.py
@Auth: Bosscal
@Date: 2023/12/22
@Description: 
"""

from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.check_in import CheckInPointService


class AddCheckInPointStruct:
    user_id: int
    point_id: int
    latitude: str
    longitude: str


class CheckInPointView(HTTPMethodView):

    @openapi.summary("打卡一个打卡点")
    @openapi.tag("check-in-point")
    @openapi.definition(body={"application/json": AddCheckInPointStruct})
    async def post(self, request):
        user_id = request.json.get("user_id")
        pic = request.json.get("pic")
        point_id = request.json.get("point_id")
        latitude = request.json.get("latitude")
        longitude = request.json.get("longitude")
        data = await CheckInPointService.add_point(user_id, pic, point_id, latitude, longitude)
        return response(data)

    @openapi.summary("获取用户全部已打卡的打卡点")
    @openapi.tag("check-in-point")
    @openapi.parameter("user_id", location="query")
    async def get(self, request):
        user_id = request.args.get("user_id")
        data = await CheckInPointService.get_point_by_user_id(user_id)
        return response(data=data)


check_in_point_blueprint = Blueprint("check_in_point", url_prefix="/point/check-in")
check_in_point_blueprint.add_route(CheckInPointView.as_view(), uri="")
