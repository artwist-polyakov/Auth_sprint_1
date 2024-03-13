import logging
import secrets
import string

from pydantic import BaseModel, EmailStr, constr, field_validator

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
    max_length=100,

)


class ValidateEmail(EmailStr):
    @classmethod
    def validate(cls, value):
        try:
            cls._validate(value)
        except ValueError:
            raise ValueError("Email is not valid")
        return value


class CustomValueError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class PasswordModel(BaseModel):
    password: str

    @staticmethod
    def generate_password() -> str:

        # todo использовать check_pass для проверки пароля

        alphabet = string.ascii_letters + string.digits
        while True:
            password = ''.join(secrets.choice(alphabet) for _ in range(10))
            try:
                PasswordModel.check_pass(password)
            except CustomValueError:
                logging.warning(f"Generated password: {password} is invalind")
                continue
            else:
                logging.warning(f"Generated password: {password} is valid")
                break
        logging.warning(f"Generated password: {password} returned to the user")
        return password

    @field_validator("password")
    def check_pass(cls, value):
        value = str(value)
        if len(value) < MIN_PASS_LENGTH:
            raise CustomValueError(f"Password must have at least {MIN_PASS_LENGTH} characters")
        if not any(c.isupper() for c in value):
            raise CustomValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise CustomValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise CustomValueError("Password must have at least one digit")
        if ' ' in value:
            raise CustomValueError("Password must not contain spaces")
        return value


class EmailModel(BaseModel):
    email: str

    @field_validator("email")
    def check_email(cls, value):
        try:
            ValidateEmail.validate(value)
        except ValueError:
            raise CustomValueError("Email is not valid")
        return value.lower()


class SignupModel(EmailModel, PasswordModel):
    first_name: str = NameStr
    last_name: str = NameStr


class ProfileModel(EmailModel):
    first_name: str = NameStr
    last_name: str = NameStr
    uuid: str
