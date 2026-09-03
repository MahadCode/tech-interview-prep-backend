from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Vote
from questions.models import Question

class QuestionVoteView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id, is_deleted=False, status=Question.QuestionStatus.PUBLISHED)

        vote_type = request.data.get("vote_type")

        if vote_type not in Vote.VoteType.values:
            return Response(
                {"error": "Invalid vote type."},
                status=status.HTTP_400_BAD_REQUEST
            )

        vote, created = Vote.objects.get_or_create(
            user=request.user,
            question=question,
            defaults={"vote_type": vote_type}
        )

        if not created:
            if vote.vote_type == vote_type:
                vote.delete()

                return Response(
                    {"message": "Vote removed."},
                    status=status.HTTP_200_OK
                )

            vote.vote_type = vote_type
            vote.save(update_fields=["vote_type"])

        return Response(
            {
                "message": "Vote recorded.",
                "vote_type": vote_type
            },
            status=status.HTTP_200_OK
        )
        

class QuestionVoteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)

        upvotes = Vote.objects.filter(
            question=question,
            vote_type=Vote.VoteType.UPVOTE
        ).count()

        downvotes = Vote.objects.filter(
            question=question,
            vote_type=Vote.VoteType.DOWNVOTE
        ).count()

        score = upvotes - downvotes

        return Response({
            "question_id": question.id,
            "upvotes": upvotes,
            "downvotes": downvotes,
            "score": score
        })
    
    