from django.shortcuts import render
from .models import Question, UserQuestionStatus
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import QuestionSerializer, UserQuestionStatusSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from accounts.permissions import IsVerifiedUser

# Create your views here.
class QuestionCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsVerifiedUser]

        return [permission() for permission in permission_classes]

    def get(self, request):
        questions = Question.objects.filter(is_deleted=False, status=Question.QuestionStatus.PUBLISHED).select_related("author","job_role").prefetch_related("company","tag")
        question_serializer = QuestionSerializer(questions, many=True)
        return Response(question_serializer.data)
        
    def post(self, request):
        question_serializer = QuestionSerializer(data = request.data) 
        question_serializer.is_valid(raise_exception=True)
        question_serializer.save(author = request.user)
        return Response(question_serializer.data, status=status.HTTP_201_CREATED)
    
class QuestionDetailView(APIView):
    permission_classes = [IsVerifiedUser]
    
    def get(self, request, id):
        question = get_object_or_404( Question.objects.select_related("author", "job_role").prefetch_related("company", "tag"), id=id, is_deleted=False)
        if question.status == Question.QuestionStatus.PUBLISHED:
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        return Response({"message": "Question hasn't been published yet"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        question = get_object_or_404( Question.objects.select_related("author", "job_role").prefetch_related("company", "tag"), id=id, is_deleted=False)
        
        if request.user.id != question.author.id:
            return Response({"message": "You are not author of the post"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = QuestionSerializer(
            question,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        question = get_object_or_404( Question.objects.select_related("author", "job_role").prefetch_related("company", "tag"), id=id)   
         
        if request.user.id != question.author.id:
            return Response({"message": "You are not author of the post"}, status=status.HTTP_403_FORBIDDEN)
        
        if question.is_deleted == True:
            return Response({"message": "This post has already deleted."}, status=status.HTTP_404_NOT_FOUND)
        
        question.is_deleted = True
        question.save(update_fields=["is_deleted"])
        return Response({"message": "Successful Deletion"})
    
class CompanyWiseQuestionView(APIView):
    
    def get(self, request, company_id):
        questions = Question.objects.filter(company__id=company_id, is_deleted=False)
        if not questions:
            return Response({"message": "No questions found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
        

class QuestionStatusDetailView(APIView):
    permission_classes = [IsVerifiedUser]
    
    def get(self, request, id):
        question = get_object_or_404(Question, id=id, is_deleted = False)
        question_status = get_object_or_404(UserQuestionStatus, question=question, user=request.user)
        serializer = UserQuestionStatusSerializer(question_status)
        return Response(serializer.data)
        
    def post(self, request, id):
        question = get_object_or_404(Question, id=id, is_deleted = False)
        
        serializer = UserQuestionStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user = request.user, question = question)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, id):
        question = get_object_or_404(Question, id=id, is_deleted = False)
        question_status = get_object_or_404(UserQuestionStatus, question=question, user=request.user)
        serializer = UserQuestionStatusSerializer(question_status, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        question = get_object_or_404(Question, id=id, is_deleted = False)
        question_status = get_object_or_404(UserQuestionStatus, question=question, user=request.user)
        question_status.delete()
        return Response({"message": "Successful Deletion"})
        

class UserQuestionStatusListView(APIView):
    permission_classes = [IsVerifiedUser]
    
    def get(self, request):
        question_status = request.user.questions_progress_status.filter(
            question__status = Question.QuestionStatus.PUBLISHED,
            question__is_deleted = False
        ).exclude(
            status = UserQuestionStatus.StatusChoices.UNSOLVED
        ).select_related("question")
        
        serializer = UserQuestionStatusSerializer(question_status, many=True)
        return Response(serializer.data)
        
        
    
    
        
        
        
        
        
        
    
    
        
    
    
    
