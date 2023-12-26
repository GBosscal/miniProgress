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
    city_name: str
    latitude: str
    longitude: str


class UpdateStampStruct:
    name: str
    pic: str
    city_name: str
    stamp_id: int
    latitude: str
    longitude: str


class StampView(HTTPMethodView):

    @openapi.summary("新增一个集邮册")
    @openapi.tag("stamp")
    @openapi.definition(body={"application/json": AddStampStruct})
    async def post(self, request):
        name = request.json.get("name")
        pic = request.json.get("pic")
        city_name = request.json.get("city_name")
        latitude = request.json.get("latitude")
        longitude = request.json.get("longitude")
        data = await StampService.add_stamp(name, pic, city_name, latitude, longitude)
        return response(data)

    @openapi.summary("更新一个集邮册")
    @openapi.tag("stamp")
    @openapi.definition(body={"application/json": UpdateStampStruct})
    async def put(self, request):
        name = request.json.get("name")
        pic = request.json.get("pic")
        city_name = request.json.get("city_name")
        stamp_id = request.json.get("stamp_id")
        latitude = request.json.get("latitude")
        longitude = request.json.get("longitude")
        data = await StampService.update_stamp(name, pic, city_name, stamp_id, latitude, longitude)
        return response(data)


class PersonalStampSummaryView(HTTPMethodView):

    @openapi.summary("获取个人的集邮进度总结")
    @openapi.description(
        "如果传入了city_name，则只返回city_name城市的集邮册以及集邮进度。否则返回全部城市的。（只会已经获得的集邮册数量，已经打卡点的个数，探索的地区数量）")
    @openapi.tag("stamp")
    @openapi.parameter("user_id", location="query")
    @openapi.parameter("city_name", location="query")
    async def get(self, request):
        user_id = request.args.get("user_id")
        city_name = request.args.get("city_name")
        data = await StampService.get_stamp_summary(user_id, city_name)
        return response(data=data)


class PersonalEachStampView(HTTPMethodView):

    @openapi.summary("获取个人的每个集邮册")
    @openapi.description("如果传入了city_name，则只返回city_name城市的集邮册以及集邮进度。否则返回全部城市的。")
    @openapi.tag("stamp")
    @openapi.parameter("user_id", location="query")
    @openapi.parameter("city_name", location="query")
    async def get(self, request):
        user_id = request.args.get("user_id")
        city_name = request.args.get("city_name")
        data = await StampService.get_each_stamp(user_id, city_name)
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


class CityFuzzyStampView(HTTPMethodView):

    @openapi.summary("获取当前城市，当前位置附近的集邮册")
    @openapi.tag("stamp")
    @openapi.parameter("city_name", location="query")
    @openapi.parameter("user_id", location="query")
    @openapi.parameter("latitude", location="query")
    @openapi.parameter("longitude", location="query")
    async def get(self, request):
        city_name = request.args.get("city_name")
        user_id = request.args.get("user_id")
        longitude = request.args.get("longitude")
        latitude = request.args.get("latitude")
        data = await StampService.fuzzy_query_stamp(user_id, city_name, latitude, longitude)
        return response(data=data)


stamp_blueprint = Blueprint("stamp", url_prefix="/stamp")
stamp_blueprint.add_route(StampView.as_view(), uri="")
stamp_blueprint.add_route(PersonalEachStampView.as_view(), uri="/personal")
stamp_blueprint.add_route(PersonalStampSummaryView.as_view(), uri="/personal/summary")
stamp_blueprint.add_route(PersonalSingleStampView.as_view(), uri="/personal/single")
stamp_blueprint.add_route(CityFuzzyStampView.as_view(), uri="/city/fuzzy")
