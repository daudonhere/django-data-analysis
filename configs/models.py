from django.db import models
from django.utils import timezone
import uuid

class IngestionData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.JSONField()
    source = models.TextField()
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ingested from {self.source} at {self.createdAt}"
