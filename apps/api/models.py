from django.db import models
from django.conf import settings
from commons.models.baseModel import BaseModel
# Create your models here.

class ApiLog(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='api_log'
        )
    name = models.CharField(max_length=255)
    end_point = models.TextField(blank=True,null=True)
    method = models.TextField(blank=True,null=True)
    status_code = models.IntegerField(blank=True,null=True)
    message = models.TextField(blank=True,null=True)
    response_time = models.FloatField(blank=True,null=True)


    def __str__(self):
        return f"{self.name} - {self.status_code}"

