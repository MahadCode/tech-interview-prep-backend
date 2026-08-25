from django.db import models
from django.conf import settings


class ModerationReport(models.Model):

    report = models.OneToOneField(
        "discussions.Report",
        on_delete=models.CASCADE,
        related_name="moderation",
    )

    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="moderation_actions",
    )

    class Action(models.TextChoices):
        APPROVE = "approve", "Approve"
        EDIT = "edit", "Edit"
        REMOVE = "remove", "Remove"

    action = models.CharField(
        max_length=20,
        choices=Action.choices,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
