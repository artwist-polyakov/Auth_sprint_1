from core.base_orjson_model import BaseORJSONModel


class Role(BaseORJSONModel):
    role: str


class Resource(BaseORJSONModel):
    resource: str


class Verb(BaseORJSONModel):
    verb: str


class RoleSchema(Role, Resource, Verb):
    pass
