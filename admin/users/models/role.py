from django.db import models
import uuid


class Role(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=255)
    resource = models.CharField(max_length=255)
    verb = models.CharField(max_length=255)

    def __str__(self):
        return f'<Role {self.role}>'

    class Meta:
        db_table = 'roles'
