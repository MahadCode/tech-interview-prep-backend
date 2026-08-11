from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True, null=True)
    class UserRole(models.TextChoices):
        USER = "user", "User"
        MODERATOR = "moderator", "Moderator"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    class AccountStatus(models.TextChoices):
        PENDING_VERIFICATION = "pending_verification", "Pending_Verfication"
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"

    account_status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.PENDING_VERIFICATION,

    )

    def __str__(self):
        return self.username