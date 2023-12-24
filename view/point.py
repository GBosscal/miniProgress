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
from const import ErrorCode


class AddPointStruct:
    name: str
    pic: str
    stamp_id: int
    latitude: str
    longitude: str


class UpdatePointStruct:
    name: str
    pic: str
    stamp_id: int
    point_id: int
    latitude: str
    longitude: str


class PointView(HTTPMethodView):

    @openapi.summary("新增一个打卡点")
    @openapi.tag("point")
    @openapi.definition(body={"application/json": AddPointStruct})
    async def post(self, request):
        name = request.json.get("name")
        pic = request.json.get("pic")
        stamp_id = request.json.get("stamp_id")
        latitude = request.json.get("latitude")
        longitude = request.json.get("longitude")
        data = await PointService.add_point(name, pic, stamp_id, latitude, longitude)
        return response(data)

    @openapi.summary("更新一个打卡点")
    @openapi.tag("point")
    @openapi.definition(body={"application/json": UpdatePointStruct})
    async def put(self, request):
        name = request.json.get("name")
        pic = request.json.get("pic")
        point_id = request.json.get("point_id")
        stamp_id = request.json.get("stamp_id")
        latitude = request.json.get("latitude")
        longitude = request.json.get("longitude")
        data = await PointService.update_point(name, pic, stamp_id, point_id, latitude, longitude)
        return response(data)


class CityFuzzyPointView(HTTPMethodView):

    @openapi.summary("获取当前城市在当前经纬度附近的打卡点")
    @openapi.tag("point")
    @openapi.parameter("city_name", location="query")
    @openapi.parameter("latitude", location="query")
    @openapi.parameter("longitude", location="query")
    async def get(self, request):
        city_name = request.args.get("city_name")
        latitude = request.args.get("latitude")
        longitude = request.args.get("longitude")
        data = await PointService.fuzzy_query_point(city_name, latitude, longitude)
        return response(data) if isinstance(data, ErrorCode) else response(data=data)


class CityPointView(HTTPMethodView):

    @openapi.summary("获取当前城市的打卡点")
    @openapi.tag("point")
    @openapi.parameter("city_name", location="query")
    async def get(self, request):
        city_name = request.args.get("city_name")
        data = await PointService.query_point_by_city_name(city_name)
        return response(data) if isinstance(data, ErrorCode) else response(data=data)


point_blueprint = Blueprint("point", url_prefix="/point")
point_blueprint.add_route(PointView.as_view(), uri="")
point_blueprint.add_route(CityFuzzyPointView.as_view(), uri="/fuzzy")
point_blueprint.add_route(CityPointView.as_view(), uri="/city")
