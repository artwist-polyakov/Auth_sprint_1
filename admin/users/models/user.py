from django.db import models
import uuid
from datetime import datetime


class User(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=255, default='unauthorized')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f'<User {self.email}>'

    class Meta:
        db_table = 'users'
