from django.db import models
from django.conf import settings
from commons.models.baseModel import BaseModel
import uuid

class Form(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use this instead of auth.User
        on_delete=models.CASCADE,
        related_name='forms'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True)
    redirect_url = models.URLField(max_length=200, blank=True, null=True)
    theme = models.JSONField(default=dict, blank=True, null=True)
    widget_theme = models.JSONField(default=dict, blank=True, null=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
