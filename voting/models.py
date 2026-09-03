from django.db import models
from django.conf import settings


class Vote(models.Model):

    class VoteType(models.TextChoices):
        UPVOTE = "upvote", "Upvote"
        DOWNVOTE = "downvote", "Downvote"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votes"
    )

    question = models.ForeignKey(
        "questions.Question",
        on_delete=models.CASCADE,
        related_name="votes"
    )

    vote_type = models.CharField(
        max_length=10,
        choices=VoteType.choices
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "question"],
                name="unique_user_question_vote"
            )
        ]