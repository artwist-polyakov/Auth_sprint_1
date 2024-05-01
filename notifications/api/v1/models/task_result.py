from api.v1.models.tasks_params import MessageType
from core.base_orjson_model import BaseORJSONModel


class TaskResult(BaseORJSONModel):
    id: int
    title: str
    sended_messages: int
    total_messages: int
    with_errors: int
    type: MessageType
    created_at: int
    is_launched: bool
