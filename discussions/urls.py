from django.urls import path
from .views import CommentCreateView, CommentDetailView, SolutionCreateView, SolutionDetailView, ReportListCreateView, ReportDetailView, QuestionCommentListView

urlpatterns = [
    path("questions/<int:id>/solutions/", SolutionCreateView.as_view(), name="create-solution"),
    path("solutions/<int:id>/", SolutionDetailView.as_view(), name="manage-solution"),
    path("comments/", CommentCreateView.as_view(), name="create-comment"),
    path("comments/<int:id>/", CommentDetailView.as_view(), name="manage-comment"),
    path("reports/", ReportListCreateView.as_view(), name="report-list-create"),
    path("reports/<int:id>/", ReportDetailView.as_view(), name="report-detail"),
    path("questions/<int:id>/comments/", QuestionCommentListView.as_view(), name="question-comments"),
]
