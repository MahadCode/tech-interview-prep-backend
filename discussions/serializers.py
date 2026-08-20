from .models import Solution, Comment
from rest_framework import serializers

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'
        read_only_fields = ['id', 'question', 'author', 'created_at', 'updated_at']
    
            

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'updated_at']
        
    def validate(self, attrs):
        question = attrs.get("question")
        solution = attrs.get("solution")
        reply_to = attrs.get("reply_to")
        if self.instance is None:
            if question and solution:
                raise serializers.ValidationError(
                    "A comment cannot belong to both a question and a solution"
            )

            if question and reply_to:
                raise serializers.ValidationError(
                    "A comment cannot belong to both a question and a comment"
                )

            if solution and reply_to:
                raise serializers.ValidationError(
                    "A comment cannot belong to both a comment and a solution"
                )

            if not solution and not question and not reply_to:
                raise serializers.ValidationError(
                    "A comment must belong to either a question or a solution or a comment"
                )
        else:
            if "question" in attrs or "solution" in attrs or "reply_to" in attrs:
                raise serializers.ValidationError(
                    "Can't Change the Reference Object while editing the comment"
                )
            
        return attrs