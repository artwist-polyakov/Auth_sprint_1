from pydantic import BaseModel


class TaskResult(BaseModel):
    id: int
    title: str
    content: str
    user_ids: list[str]
    type: str
    created_at: int
    is_launched: bool
