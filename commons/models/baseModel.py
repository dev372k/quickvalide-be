from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    """
    Abstract base model to provide common fields for all models.
    Supports soft delete.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

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
