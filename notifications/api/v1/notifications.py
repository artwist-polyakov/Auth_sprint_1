from http import HTTPStatus

from api.v1.models.task_result import TaskResult
from api.v1.models.tasks_params import TasksParams
from api.v1.utils.convertors import TaskResponseConvertor
from db.requests.task_request import GetTaskInfo, TaskRequest
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from service.tasks_service import TasksService, get_tasks_service

router = APIRouter()


@router.post(
    path='/create',
    response_model=TaskResult,
    summary="Send Notification",
    description="Send a notification to users"
)
async def create_task(
        user_ids: list[str] = Query(...),
        params: TasksParams = Depends(),
        tasks_service: TasksService = Depends(get_tasks_service)
) -> TaskResult | JSONResponse:
    task = TaskRequest(
        title=params.title,
        content=params.content,
        user_ids=user_ids,
        type=params.type,
        scenario=params.scenario
    )
    result = await tasks_service.handle_task_request(task)
    if not result:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={'message': 'Task creation failed'}
        )
    return TaskResponseConvertor.convert_to_response(result)


@router.get(
    path='/info',
    response_model=TaskResult,
    summary="Get task information",
    description="Get information about the task by its id"
)
async def get_task_info(
        task_id: int = Query(..., alias="task_id"),
        tasks_service: TasksService = Depends(get_tasks_service)
) -> TaskResult | JSONResponse:
    request = GetTaskInfo(task_id=task_id)
    result = await tasks_service.handle_task_request(request)
    if not result:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': 'Task not found'}
        )
    return TaskResponseConvertor.convert_to_response(result)
