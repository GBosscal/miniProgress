"""
@Project: miniProgress
@File: point.py
@Auth: Bosscal
@Date: 2023/12/21
@Description: 
"""

from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.point import PointService


class AddPointStruct:
    name: str
    pic: str
    stamp_id: int


class UpdatePointStruct:
    name: str
    pic: str
    stamp_id: int
    point_id: int


class PointView(HTTPMethodView):

    @openapi.summary("新增一个打卡点")
    @openapi.tag("point")
    @openapi.definition(body={"application/json": AddPointStruct})
    async def post(self, request):
        name = request.json.get("name")
        pic = request.json.get("pic")
        stamp_id = request.json.get("stamp_id")
        data = await PointService.add_point(name, pic, stamp_id)
        return response(data)

    @openapi.summary("更新一个打卡点")
    @openapi.tag("point")
    @openapi.definition(body={"application/json": UpdatePointStruct})
    async def put(self, request):
        name = request.json.get("name")
        pic = request.json.get("pic")
        point_id = request.json.get("point_id")
        stamp_id = request.json.get("stamp_id")
        data = await PointService.update_point(name, pic, stamp_id, point_id)
        return response(data)


point_blueprint = Blueprint("point", url_prefix="/point")
point_blueprint.add_route(PointView.as_view(), uri="")
