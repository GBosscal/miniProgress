"""
@Project: miniProgress
@File: feedback.py
@Auth: Bosscal
@Date: 2023/12/21
@Description: 
"""

from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.feedback import FeedbackService
from const import ErrorCode


class FeedBackStruct:
    user_id: int
    msg: str


class FeedbackView(HTTPMethodView):

    @openapi.summary("新增一条反馈")
    @openapi.tag("Feedback")
    @openapi.definition(body={"application/json": FeedBackStruct})
    async def post(self, request):
        user_id = request.json.get("user_id")
        msg = request.json.get("msg")
        data = await FeedbackService.add_feedback(user_id, msg)
        return response(data)

    @openapi.summary("获取反馈,如果feedback_id不传则获取全部反馈")
    @openapi.tag("Feedback")
    @openapi.parameter("feedback_id", location="query")
    async def get(self, request):
        feedback_id = request.args.get("feedback_id")
        data = await FeedbackService.get_feedback(feedback_id)
        return response(data=data)


feedback_blueprint = Blueprint("feedback", url_prefix="/feedback", version=1)
feedback_blueprint.add_route(FeedbackView.as_view(), uri="")
