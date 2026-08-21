from .models import Question, UserQuestionStatus
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = [
            "id",
            "company",
            "job_role",
            "difficulty_level",
            "title",
            "tag",
            "description",
            "status",
            "is_deleted"
        ]
        
        read_only_fields = ["id", "status", "is_deleted"]
        
class UserQuestionStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserQuestionStatus
        fields = '__all__'
        read_only_fields = ["id", "user", "question", "created_at", "updated_at"]
        
    