from db.models.auth_requests.base_request import BaseRequest


class RoleRequest(BaseRequest):
    uuid: str
    role: str
    resource: str
    verb: str
