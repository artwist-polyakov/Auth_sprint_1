import http
import json

import bcrypt
import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        url = settings.AUTH_API_LOGIN_URL

        # todo

        payload = {'email': email, 'password': password}
        response = requests.post(url, data=json.dumps(payload))
        if response.status_code != http.HTTPStatus.OK:
            return None

        data = response.json()

        try:
            user, created = User.objects.get_or_create(uuid=data['uuid'],)
            user.email = data.get('email')
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.is_superuser = data.get('is_superuser')
            user.role = data.get('role')
            user.is_verified = data.get('is_verified')
            user.save()
        except Exception:
            return None

        return user

    def get_user(self, user_uuid):
        try:
            return User.objects.get(pk=user_uuid)
        except User.DoesNotExist:
            return None