from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from api.v1.models.tasks_params import TasksParams

router = APIRouter()


@router.post(
    path='/create',
    response_model=str,
    summary="Send Notification",
    description="Send a notification to users"
)
async def create_task(
        users: list[str] = Query([], alias="users"),
        params: TasksParams = Depends()
) -> JSONResponse:
    if not users:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={'message': 'Users are required'}
        )
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': f'params: {params.model_dump()}, users: {users}'}
    )
