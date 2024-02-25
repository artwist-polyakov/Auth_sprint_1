from core.base_orjson_model import BaseORJSONModel


class Login(BaseORJSONModel):
    login: str


class Password(BaseORJSONModel):
    password: str


class FirstName(BaseORJSONModel):
    first_name: str = ''


class LastName(BaseORJSONModel):
    last_name: str = ''


class Email(BaseORJSONModel):
    email: str


# наследников надо заполнять в порядке обратном желаемому порядку в схеме
class AuthSchema(LastName, FirstName, Password, Email):
    pass


class UpdateSchema(LastName, FirstName, Email):
    pass
