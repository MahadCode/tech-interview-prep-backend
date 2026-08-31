from rest_framework import serializers
from .models import Company, JobRole, Tag


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]


class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = ["id", "name", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]