from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    plan = models.JSONField(default=dict, blank=True, null=True)
    api_key = models.TextField(blank=True, null=True)
    api_key_limit = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username
    
    
    def delete(self, using=None, keep_parents=False, soft=True):
        """
        Soft delete by default. Set soft=False for hard delete.
        """
        if soft:
            self.is_deleted = True
            self.is_active = False
            self.deleted_at = timezone.now()
            self.save()
        else:
            super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """
        Restore a soft-deleted object.
        """
        self.is_deleted = False
        self.is_active = True
        self.deleted_at = None
        self.save()