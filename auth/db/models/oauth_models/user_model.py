from core.base_orjson_model import BaseORJSONModel


class OAuthUserModel(BaseORJSONModel):
    """
    Приходит набор данных вида

    {'id': '111814111',
    'login': 'login',
    'client_id': 'edwefwrfds12313',
    'display_name': 'name',
    'real_name': 'Real Name',
    'first_name': 'Name',
    'last_name': 'Name',
    'sex': None,
    'default_email': 'a@ea.ru',
    'emails': ['a@ea.ru'],
    'birthday': 'YYYY-MM-DD',
    'default_avatar_id': '21377/enc-dfsfddsgsg',
    'is_avatar_empty': False,
    'default_phone':
        {'id': 123123123,
        'number': '+79666666666'},
    'psuid': '1.dgdsfsdg'}


    """

    default_email: str
    first_name: str
    last_name: str
