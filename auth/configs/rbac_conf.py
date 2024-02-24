from aiocache import cached
from aiocache.serializers import JsonSerializer
from services.role_service import get_role_service

RBAC_CONF = {
    'admin': {
        'films': ['read', 'write', 'delete'],
        'genres': ['read', 'write', 'delete'],
        'persons': ['read', 'write', 'delete'],
        'users': ['read', 'write', 'delete'],
    },
    'user': {
        'films': ['read'],
        'genres': ['read'],
        'persons': ['read'],
        'users': ['read', 'write', 'delete'],
    }
}


@cached(serializer=JsonSerializer())
async def get_rbac_conf():
    return await get_role_service().get_roles()


EXСLUDED_PATHS = ['docs', 'openapi.json', 'auth/openapi', 'auth/openapi.json']
