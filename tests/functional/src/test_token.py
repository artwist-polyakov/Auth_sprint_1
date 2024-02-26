from http import HTTPStatus

import pytest
from configs.test_settings import settings


# POST
# /auth/v1/users/refresh
# Refresh access token via refresh token

# POST
# /auth/v1/users/logout
# Logout from current session

# POST
# /auth/v1/users/logout_all_devices
# Logout from all devices

# GET
# /auth/v1/users/history
# Get login history

# GET
# /auth/v1/users/check_permissions
# Check permissions

