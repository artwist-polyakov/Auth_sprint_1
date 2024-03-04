from django.db import models
import uuid
from datetime import datetime


class RefreshToken(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='refresh_tokens')
    active_till = models.BigIntegerField()
    created_at = models.DateTimeField(default=datetime.utcnow)
    user_device_type = models.TextField()

    def __str__(self):
        return f'<RefreshToken {self.uuid}>'
