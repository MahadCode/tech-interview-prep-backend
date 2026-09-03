from django.urls import path
from .views import RegisterView, EmailVerificationView, LoginView, LogoutView, PasswordRecoveryLink, PasswordChangeView, CurrentUserView, get_csrf_token, EditProfileView, ResendVerificationEmail, PasswordResetView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/<str:token>/", EmailVerificationView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("recover-password/", PasswordRecoveryLink.as_view(), name="recover-password"),
    path("reset-password/<str:token>/", PasswordResetView.as_view(), name="reset-password"),
    path("change-password/", PasswordChangeView.as_view(), name="change-password"),
    path("current-user/", CurrentUserView.as_view(), name="current-user"),
    path("csrf/", get_csrf_token, name="csrf"),
    path("edit-profile/", EditProfileView.as_view(), name='edit-profile'),
    path("resend-verification/", ResendVerificationEmail.as_view(), name="resend-verification"),
]