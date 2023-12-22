"""
@Project: miniProgress
@File: city.py
@Auth: Bosscal
@Date: 2023/12/21
@Description: 
"""

from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.city import CityService
from const import ErrorCode


class CityStruct:
    name: str


class CityUpdateStruct:
    name: str
    city_id: int


class CityView(HTTPMethodView):

    @openapi.summary("增加一个城市")
    @openapi.tag("City")
    @openapi.definition(body={"application/json": CityService})
    async def post(self, request):
        name = request.json.get("name")
        data = await CityService.add_city(name)
        return response(data)

    @openapi.summary("获取全部城市")
    @openapi.tag("City")
    async def get(self, request):
        data = await CityService.get_all_cities()
        return response(data=data)

    @openapi.summary("更新一个城市")
    @openapi.tag("City")
    @openapi.definition(body={"application/json": CityUpdateStruct})
    async def put(self, request):
        name = request.json.get("name")
        city_id = request.json.get("city_id")
        data = await CityService.update_city(city_id, name)
        return response(data)


city_blueprint = Blueprint("city", url_prefix="/city", version=1)
city_blueprint.add_route(CityView.as_view(), uri="")
