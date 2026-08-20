from .models import Question
from rest_framework import serializers

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
        
        
    