from uuid import UUID

from db.models.oauth_models.oauth_token import OAuthToken
from db.models.oauth_models.user_model import OAuthUserModel


class OAuthDBModel(OAuthToken, OAuthUserModel):
    uuid: UUID
    user_id: str
    oauth_method: str
