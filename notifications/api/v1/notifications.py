from http import HTTPStatus

from api.v1.models.task_result import TaskResult
from api.v1.models.tasks_params import TasksParams
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post(
    path='/create',
    response_model=TaskResult,
    summary="Send Notification",
    description="Send a notification to users"
)
async def create_task(
        users: list[str] = Query([], alias="users"),
        params: TasksParams = Depends()
) -> TaskResult | JSONResponse:
    if not users:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={'message': 'Users are required'}
        )
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': f'params: {params.model_dump()}, users: {users}'}
    )


@router.get(
    path='/info',
    response_model=TaskResult,
    summary="Get task information",
    description="Get information about the task by its id"
)
async def get_task_info(
        task_id: int = Query(..., alias="task_id")
) -> TaskResult | JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': f'Task info: {task_id}'}
    )
