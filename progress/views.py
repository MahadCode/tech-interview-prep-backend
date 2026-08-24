from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import PreparationGoal
from .serializers import PreparationGoalSerializer, PreparationStatisticsSerializer


class PreparationGoalListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        goals = PreparationGoal.objects.filter(user=request.user).select_related(
            "target_tag", "target_company"
        )

        serializer = PreparationGoalSerializer(goals, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PreparationGoalSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PreparationGoalDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, id):
        return get_object_or_404(PreparationGoal, id=id, user=request.user)

    def get(self, request, id):
        goal = self.get_object(request, id)

        serializer = PreparationGoalSerializer(goal)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        goal = self.get_object(request, id)

        serializer = PreparationGoalSerializer(goal, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        goal = self.get_object(request, id)

        goal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PreparationStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PreparationStatisticsSerializer(instance=request.user, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)
