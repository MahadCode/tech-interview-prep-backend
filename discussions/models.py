from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


# Create your models here.
class Solution(models.Model):
    question = models.ForeignKey(
        "questions.Question",
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    question = models.ForeignKey(
        "questions.Question",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )
    solution = models.ForeignKey(
        "Solution", on_delete=models.CASCADE, related_name="comments", null=True, blank=True
    )
    reply_to = models.ForeignKey(
        "Comment", on_delete=models.CASCADE, related_name="replies", null=True, blank=True
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.question and self.solution:
            raise ValidationError(
                "A comment cannot belong to both a question and a solution"
            )

        if self.question and self.reply_to:
            raise ValidationError(
                "A comment cannot belong to both a question and a comment"
            )

        if self.solution and self.reply_to:
            raise ValidationError(
                "A comment cannot belong to both a comment and a solution"
            )

        if not self.solution and not self.question and not self.reply_to:
            raise ValidationError(
                "A comment must belong to either a question or a solution or a comment"
            )


class Report(models.Model):
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reporter",
        null=True,
    )
    
    question = models.ForeignKey(
        "questions.Question", on_delete=models.SET_NULL, null=True
    )
    solution = models.ForeignKey("Solution", on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey("Comment", on_delete=models.SET_NULL, null=True)
    
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reviewer",
        null=True,
    )

    reason = models.TextField()

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEWED = "reviewed", "Reviewed"
        ACTIONED = "actioned", "Actioned"
        DISMISSED = "dismissed", "Dismissed"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField()
