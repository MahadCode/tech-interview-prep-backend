from .models import Question, UserQuestionStatus
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from accounts.serializers import UserSerializer
from taxonomy.serializers import CompanySerializer, JobRoleSerializer, TagSerializer

class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    company_full = CompanySerializer(source="company", many=True, read_only=True)
    job_role_full = JobRoleSerializer(source="job_role", read_only=True)
    tag_full = TagSerializer(source="tag", many=True, read_only=True)
    class Meta:
        model = Question
        fields = [
            "id",
            "company",
            "author",
            "job_role",
            "difficulty_level",
            "title",
            "tag",
            "description",
            "status",
            "is_deleted",
            "company_full",
            "job_role_full",
            "tag_full"
        ]
        
        read_only_fields = ["id", "status", "is_deleted"]
        
class UserQuestionStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserQuestionStatus
        fields = '__all__'
        read_only_fields = ["id", "user", "question", "created_at", "updated_at"]
        
    