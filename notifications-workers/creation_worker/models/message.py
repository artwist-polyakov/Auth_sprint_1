from models.base_orjson_model import BaseORJSONModel


class Message(BaseORJSONModel):
    id: int
    title: str
    content: str
    user_ids: list[str]
    type: str
    created_at: int
    scenario: str
