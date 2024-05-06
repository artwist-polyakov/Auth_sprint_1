from api.v1.models.task_result import TaskResult
from db.responses.task_response import TaskResponse


class TaskResponseConvertor:
    @staticmethod
    def convert_to_response(task: TaskResponse) -> TaskResult:
        return TaskResult(
            id=task.id,
            title=task.title,
            sended_messages=task.sended_messages,
            total_messages=task.total_messages,
            with_errors=task.with_errors,
            type=task.type,
            created_at=task.created_at,
            is_launched=task.is_launched,
            scenario=task.scenario
        )
