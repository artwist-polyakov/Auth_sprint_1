from pydantic_settings import BaseSettings


class JWTSecuritySettings(BaseSettings):
    jwt_access_token_expires: int = 3600
    # jwt_secret_key: str = 'secret'
    # jwt_token_location: set[str] = {'cookies'}
    jwt_cookie_csrf_protect: bool = False
    openssl_key: str = ...
    algorithm: str = 'HS256'

    class Config:
        env_file = '.env'
