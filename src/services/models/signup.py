import re

from pydantic import BaseModel, EmailStr, ValidationError, constr, field_validator

MIN_PASS_LENGTH = 5

LoginStr = constr(
    pattern=r'^\S+$',
    min_length=3,
    max_length=255,
    strip_whitespace=True,
    to_lower=True
)

NameStr = constr(
    strip_whitespace=True,
    min_length=2,
    max_length=100
)


class PasswordModel(BaseModel):
    password: str

    @field_validator("password")
    def check_pass(cls, value):
        value = str(value)
        if len(value) < MIN_PASS_LENGTH:
            raise ValueError(f"Password must have at least {MIN_PASS_LENGTH} characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")
        if ' ' in value:
            raise ValueError("Password must not contain spaces")
        return value


class LoginModel(BaseModel):
    login: str = LoginStr


class EmailModel(BaseModel):
    email: EmailStr | None


class SignupModel(LoginModel, EmailModel, PasswordModel):
    first_name: str = NameStr
    last_name: str = NameStr
