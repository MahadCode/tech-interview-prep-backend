from django.db import models
from django.conf import settings
# Create your models here.
class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    question = models.ForeignKey("questions.Question", on_delete=models.SET_NULL, null=True)
    solution = models.ForeignKey("discussions.Solution", on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey("discussions.Comment", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)