from django.urls import path
from .views import CompanyView, JobRoleView, TagView

urlpatterns = [
    path("companies/", CompanyView.as_view(), name="company-list-create"),
    path("job-roles/", JobRoleView.as_view(), name="jobrole-list-create"),
    path("tags/", TagView.as_view(), name="tag-list-create"),
]