from django.db import models
from commons.models.baseModel import BaseModel
from ..form.models import Form  # ✅ Optional: only if needed for migrations (safe circular import)

class Feedback(BaseModel):
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    sentiment = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ("positive", "Positive"),
            ("neutral", "Neutral"),
            ("negative", "Negative"),
        ],
        help_text="AI-detected sentiment based on message and rating."
    )

    sentiment_score = models.FloatField(
        blank=True,
        null=True,
        help_text="A numeric score between 0 (negative) and 1 (positive)."
    )

    summary = models.TextField(blank=True, null=True)
    suggestions = models.JSONField(default=list, blank=True, null=True)

    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=1,
        help_text="User-provided rating from 1 to 5."
    )

    def __str__(self):
        form_title = getattr(self.form, "title", "Unknown Form")
        return f"Feedback from {self.name or 'Anonymous'} on {form_title}"
