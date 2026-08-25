from django.urls import path
from .views import (
    ModerationReportListView,
    ModerationReportDetailView,
    PendingQuestionListView,
    QuestionModerationDetailView,
)

urlpatterns = [
    path(
        "reports/",
        ModerationReportListView.as_view(),
        name="moderation-report-list",
    ),
    path(
        "reports/<int:id>/",
        ModerationReportDetailView.as_view(),
        name="moderation-report-detail",
    ),
    path(
        "questions/",
        PendingQuestionListView.as_view(),
        name="pending-question-list",
    ),
    path(
        "questions/<int:id>/",
        QuestionModerationDetailView.as_view(),
        name="question-moderation-detail",
    ),
]
