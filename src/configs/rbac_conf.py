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

EXСLUDED_PATHS = ['docs', 'openapi.json']
