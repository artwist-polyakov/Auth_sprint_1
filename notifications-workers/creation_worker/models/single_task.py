from models.base_orjson_model import BaseORJSONModel


class SingleTask(BaseORJSONModel):
    notification_id: int = 0
    task_id: int = 0
    title: str
    content: str
    user_id: str = ""
    type: str
    created_at: int
    scenario: str
