from django.urls import path
from .views import QuestionVoteView, QuestionVoteDetailView

urlpatterns = [
    path("questions/<int:question_id>/vote/", QuestionVoteView.as_view(), name="vote-question"),
    path("questions/<int:question_id>/votes/", QuestionVoteDetailView.as_view(), name="question-votes")
]