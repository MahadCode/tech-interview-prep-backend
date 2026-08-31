from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Company, JobRole, Tag
from .serializers import CompanySerializer, JobRoleSerializer, TagSerializer
from moderation.permissions import IsModeratorOrAdmin


class CompanyView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsModeratorOrAdmin()]
        return [AllowAny()]

    def get(self, request):
        companies = Company.objects.filter(is_active=True)
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobRoleView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsModeratorOrAdmin()]
        return [AllowAny()]

    def get(self, request):
        job_roles = JobRole.objects.filter(is_active=True)
        serializer = JobRoleSerializer(job_roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsModeratorOrAdmin()]
        return [AllowAny()]

    def get(self, request):
        tags = Tag.objects.filter(is_active=True)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)