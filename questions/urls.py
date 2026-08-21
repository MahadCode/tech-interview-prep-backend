from django.urls import path
from .views import QuestionCreateView, QuestionDetailView, CompanyWiseQuestionView, QuestionStatusDetailView

urlpatterns = [
    path("", QuestionCreateView.as_view(), name="post-question"),
    path("<int:id>/", QuestionDetailView.as_view(), name="manage-question"),
    path("company/<int:company_id>/", CompanyWiseQuestionView.as_view(), name="company-questions"),
    path("<int:id>/status/", QuestionStatusDetailView.as_view(), name="manage-question-progress-status")
]
