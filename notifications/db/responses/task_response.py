from db.responses.base_response import BaseResponse


class TaskResponse(BaseResponse):
    id: int
    title: str
    sended_messages: int
    total_messages: int
    type: str
    created_at: int
    is_launched: bool
