from fastapi import APIRouter
from http import HTTPStatus

router = APIRouter()


@router.post(
    path='/create',
    response_model=str,
    summary="Send Notification",
    description="Send a notification to users"
)
async def send_notification() -> str:
    return "Notification sent successfully"
