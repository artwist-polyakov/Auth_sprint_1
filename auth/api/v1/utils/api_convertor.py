from db.models.token_models.access_token_container import AccessTokenContainer
from utils.jwt_toolkit import dict_from_jwt, dict_to_jwt, get_jwt_settings


class APIConvertor:

    @staticmethod
    def map_token_container_to_access_token(token_container: AccessTokenContainer) -> str:
        result = {
            'user_id': token_container.user_id,
            'role': token_container.role,
            'is_superuser': token_container.is_superuser,
            'verified': token_container.verified,
            'subscribed': token_container.subscribed,
            'created_at': token_container.created_at,
            'subscribed_till': token_container.subscribed_till,
            'active_till': (token_container.created_at +
                            get_jwt_settings().access_token_expire_minutes),
            'refresh_id': token_container.refresh_id,
            'refreshed_at': token_container.refreshed_at,
            'user_device_type': token_container.user_device_type
        }

        return dict_to_jwt(result)

    @staticmethod
    def map_token_container_to_refresh_token(token_container: AccessTokenContainer) -> str:
        result = {
            'refresh_id': token_container.refresh_id,
            'user_id': token_container.user_id,
            'active_till': (token_container.created_at +
                            get_jwt_settings().refresh_token_expire_minutes),
            'user_device_type': token_container.user_device_type
        }
        return dict_to_jwt(result)

    @staticmethod
    def refresh_token_to_tuple(refresh_token: str) -> tuple[str, str, int, str] | None:
        result = dict_from_jwt(refresh_token)
        if not result:
            return None
        return (result.get('refresh_id'), result.get('user_id'),
                result.get('active_till'), result.get('user_device_type'))
