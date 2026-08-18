from django.urls import path
from .views import RegisterView, EmailVerificationView, LoginView, LogoutView, PasswordRecoveryLink, PasswordChangeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/<str:token>/", EmailVerificationView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("recover-password/", PasswordRecoveryLink.as_view(), name="recover-password"),
    path("change-password/<str:token>/", PasswordChangeView.as_view(), name="change-password")
]