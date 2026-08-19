from django.urls import path
from .views import EditProfileView

urlpatterns = [
    path("manage/", EditProfileView.as_view(), name="manage-profile")
]