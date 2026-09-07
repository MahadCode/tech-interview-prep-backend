from rest_framework.permissions import BasePermission

class IsVerifiedUser(BasePermission):
    message = "You must be logged in and have a verified email address to perform this action"

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.account_status == "active"
        )