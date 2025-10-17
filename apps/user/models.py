from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    plan = models.JSONField(default=dict, blank=True, null=True)
    api_key = models.TextField(blank=True, null=True)
    api_key_limit = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username