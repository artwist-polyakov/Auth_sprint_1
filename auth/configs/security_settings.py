from pydantic_settings import BaseSettings


class JWTSecuritySettings(BaseSettings):
    access_token_expire_minutes: int = 60*60
    refresh_token_expire_minutes: int = 500*60
    # jwt_secret_key: str = 'secret'
    # jwt_token_location: set[str] = {'cookies'}
    jwt_cookie_csrf_protect: bool = False
    openssl_key: str = ...
    algorithm: str = 'HS256'

    class Config:
        env_file = '.env'
