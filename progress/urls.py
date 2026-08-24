from django.urls import path

from .views import PreparationGoalListCreateView, PreparationGoalDetailView, PreparationStatisticsView

urlpatterns = [
    path("goals/", PreparationGoalListCreateView.as_view(), name="goal-list-create"),
    path("goals/<int:id>/", PreparationGoalDetailView.as_view(), name="goal-detail"),
    path("statistics/", PreparationStatisticsView.as_view(), name="goals-statistics"),
]