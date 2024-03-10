import uuid
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from users.managers.user_manager import UserManager


class User(AbstractBaseUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=255, default='unauthorized')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.utcnow)

    last_login = None

    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        return True

    objects = UserManager()

    def __str__(self):
        return f'{self.email} {self.uuid}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        managed = False
        db_table = 'users\".\"users'
