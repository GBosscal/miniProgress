"""
@Project: miniProgress
@File: stamp.py
@Auth: Bosscal
@Date: 2023/12/21
@Description: 
"""

from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.stamp import StampService
from const import ErrorCode


class AddStampStruct:
    name: str
    pic: str
    city_id: int


class UpdateStampStruct:
    name: str
    pic: str
    city_id: int
    stamp_id: int


class StampView(HTTPMethodView):

    @openapi.summary("新增一个集邮册")
    @openapi.tag("stamp")
    @openapi.definition(body={"application/json": AddStampStruct})
    async def post(self, request):
        name = request.json.get("name")
        pic = request.json.get("pic")
        city_id = request.json.get("city_id")
        data = await StampService.add_stamp(name, pic, city_id)
        return response(data)

    @openapi.summary("更新一个集邮册")
    @openapi.tag("stamp")
    @openapi.definition(body={"application/json": UpdateStampStruct})
    async def put(self, request):
        name = request.json.get("name")
        pic = request.json.get("pic")
        city_id = request.json.get("city_id")
        stamp_id = request.json.get("stamp_id")
        data = await StampService.update_stamp(name, pic, city_id, stamp_id)
        return response(data)


class PersonalStampSummaryView(HTTPMethodView):

    @openapi.summary("获取个人的集邮进度")
    @openapi.tag("stamp")
    @openapi.parameter("user_id", location="query")
    async def get(self, request):
        user_id = request.args.get("user_id")
        data = await StampService.get_stamp_summary(user_id)
        return response(data=data)


class PersonalEachStampView(HTTPMethodView):

    @openapi.summary("获取个人的每个集邮册")
    @openapi.tag("stamp")
    @openapi.parameter("user_id", location="query")
    async def get(self, request):
        user_id = request.args.get("user_id")
        data = await StampService.get_each_stamp(user_id)
        return response(data=data)


class PersonalSingleStampView(HTTPMethodView):

    @openapi.summary("获取个人的指定集邮册")
    @openapi.tag("stamp")
    @openapi.parameter("user_id", location="query")
    @openapi.parameter("stamp_id", location="query")
    async def get(self, request):
        user_id = request.args.get("user_id")
        stamp_id = request.args.get("stamp_id")
        data = await StampService.get_one_stamp(stamp_id, user_id)
        return response(data=data)


stamp_blueprint = Blueprint("stamp", url_prefix="/stamp")
stamp_blueprint.add_route(StampView.as_view(), uri="")
stamp_blueprint.add_route(PersonalEachStampView.as_view(), uri="/personal")
stamp_blueprint.add_route(PersonalStampSummaryView.as_view(), uri="/personal/summary")
stamp_blueprint.add_route(PersonalSingleStampView.as_view(), uri="/personal/single")