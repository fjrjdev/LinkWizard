from django.db import models
import uuid


class Link(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    label = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="link"
    )
