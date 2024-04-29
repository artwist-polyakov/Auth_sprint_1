from http import HTTPStatus

from api.v1.models.tasks_params import TasksParams
from fastapi import APIRouter, Depends, Query

router = APIRouter()


@router.post(
    path='/create',
    response_model=str,
    summary="Send Notification",
    description="Send a notification to users"
)
async def send_notification(
        users: list[str] = Query([], alias="users"),
        params: TasksParams = Depends()
) -> str:
    return "Notification sent successfully"
