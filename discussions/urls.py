from django.urls import path
from .views import CommentCreateView, CommentDetailView, SolutionCreateView, SolutionDetailView

urlpatterns = [
    path("questions/<int:id>/solutions/", SolutionCreateView.as_view(), name="create-solution"),
    path("solutions/<int:id>/", SolutionDetailView.as_view(), name="manage-solution"),
    path("comments/", CommentCreateView.as_view(), name="create-comment"),
    path("comments/<int:id>/", CommentDetailView.as_view(), name="manage-comment")
]