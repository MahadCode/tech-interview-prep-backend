from django.urls import path
from .views import PostQuestionView, QuestionDetailView, CompanyWiseQuestionView

urlpatterns = [
    path("", PostQuestionView.as_view(), name="post-question"),
    path("<int:id>/", QuestionDetailView.as_view(), name="manage-question"),
    path("company/<int:company_id>/", CompanyWiseQuestionView.as_view(), name="company-questions")
]