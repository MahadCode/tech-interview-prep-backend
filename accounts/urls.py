from django.urls import path
from .views import RegisterView, EmailVerificationView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/<str:token>/", EmailVerificationView.as_view(), name="verify-email")
]