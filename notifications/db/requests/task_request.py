from db.requests.base_request import BaseRequest


class TaskRequest(BaseRequest):
    title: str
    content: str
    user_ids: list[str]
    type: str
    scenario: str


class GetTaskInfo(BaseRequest):
    task_id: int


class PostTask(TaskRequest):
    pass
