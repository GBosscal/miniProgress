"""
@Project: miniProgress
@File: feedback.py
@Auth: Bosscal
@Date: 2023/12/20
@Description: 
"""

from const import ErrorCode
from model.feedback import Feedback


class FeedbackService:

    @classmethod
    async def add_feedback(cls, user_id: int, msg: str):
        """增加一条新的反馈"""
        mark = Feedback.add_feedback(user_id, msg)
        if not mark:
            return ErrorCode.FeedbackAddError
        return ErrorCode.Success

    @classmethod
    async def get_feedback(cls, feedback_id: int = None):
        """获取一个反馈或者获取全部的反馈"""
        all_feedback = Feedback.query_feedback(feedback_id)
        all_feedback = [feedback.to_dict() for feedback in all_feedback]
        return {"feedback": all_feedback, "total": len(all_feedback)}
