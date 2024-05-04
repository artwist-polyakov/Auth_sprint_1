from models.base_orjson_model import BaseORJSONModel


class EnrichingMessageTask(BaseORJSONModel):
    id: int
    title: str
    content: str
    user_id: str
    type: str
    created_at: int
