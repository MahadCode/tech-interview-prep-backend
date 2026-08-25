from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import ModerationReport
from .serializers import ModerationReportSerializer, ModerationActionSerializer, QuestionModerationSerializer
from .permissions import IsModeratorOrAdmin
from discussions.models import Report
from questions.models import Question
from questions.serializers import QuestionSerializer

class ModerationReportListView(APIView):

    permission_classes = [IsModeratorOrAdmin]
    def get(self, request):
        reports = Report.objects.filter(status=Report.Status.PENDING)
        
        for report in reports:
            ModerationReport.objects.get_or_create(report=report)
            
        moderation_reports = ModerationReport.objects.filter(report__status=Report.Status.PENDING)
        serializer = ModerationReportSerializer(moderation_reports, many=True)
        
        return Response(serializer.data)
    

class ModerationReportDetailView(APIView):

    permission_classes = [IsModeratorOrAdmin]
    
    def approve(self, moderation_report, moderator):
        report = moderation_report.report

        report.status = Report.Status.DISMISSED
        report.reviewed_by = moderator
        report.resolved_at = timezone.now()
        report.save()

        moderation_report.action = ModerationReport.Action.APPROVE
        moderation_report.moderator = moderator
        moderation_report.reviewed_at = timezone.now()
        moderation_report.save()
    
    def edit(self, moderation_report, moderator, data):

        report = moderation_report.report

        if report.question:
            question = report.question
            
            if "title" in data:
                question.title = data["title"]
            if "description" in data:
                question.description = data["description"]

            question.save()

        elif report.solution:
            solution = report.solution

            if "content" in data:
                solution.content = data["content"]

            solution.save()

        elif report.comment:
            comment = report.comment

            if "content" in data:
                comment.content = data["content"]

            comment.save()

        report.status = Report.Status.ACTIONED
        report.reviewed_by = moderator
        report.resolved_at = timezone.now()
        report.save()

        moderation_report.action = ModerationReport.Action.EDIT
        moderation_report.moderator = moderator
        moderation_report.reviewed_at = timezone.now()
        moderation_report.save()
    
    def remove(self, moderation_report, moderator):
        report = moderation_report.report

        if report.question:
            question = report.question
            question.status = Question.QuestionStatus.REMOVED
            question.save(update_fields=["status"])
        elif report.solution:
            report.solution.delete()
        elif report.comment:
            report.comment.delete()

        report.status = Report.Status.ACTIONED
        report.reviewed_by = moderator
        report.resolved_at = timezone.now()
        report.save()

        moderation_report.action = ModerationReport.Action.REMOVE
        moderation_report.moderator = moderator
        moderation_report.reviewed_at = timezone.now()
        moderation_report.save()

    def get(self, request, id):
        moderation_report = get_object_or_404(ModerationReport, id=id, report__status=Report.Status.PENDING)
        serializer = ModerationReportSerializer(moderation_report)
        return Response(serializer.data)

    def patch(self, request, id):
        moderation_report = get_object_or_404(ModerationReport, id=id, report__status=Report.Status.PENDING)
        serializer = ModerationActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data["action"]

        if action == ModerationReport.Action.APPROVE:
            self.approve(moderation_report, request.user)
        elif action == ModerationReport.Action.EDIT:
            self.edit(moderation_report, request.user, serializer.validated_data)
        elif action == ModerationReport.Action.REMOVE:
            self.remove(moderation_report, request.user)

        moderation_report.refresh_from_db()
        response_serializer = ModerationReportSerializer(moderation_report)
        return Response(response_serializer.data)
    
class PendingQuestionListView(APIView):
    permission_classes = [IsModeratorOrAdmin]

    def get(self, request):

        questions = Question.objects.filter(status=Question.QuestionStatus.PENDING_REVIEW, is_deleted=False)
        serializer = QuestionSerializer(questions, many=True)
        
        return Response(serializer.data)

class QuestionModerationDetailView(APIView):
    permission_classes = [IsModeratorOrAdmin]

    def patch(self, request, id):

        question = get_object_or_404(Question, id=id, status=Question.QuestionStatus.PENDING_REVIEW, is_deleted=False)

        serializer = QuestionModerationSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data["action"]

        if action == "publish":
            question.status = Question.QuestionStatus.PUBLISHED

        elif action == "remove":
            question.status = Question.QuestionStatus.REMOVED

        question.save(update_fields=["status"])

        return Response(QuestionSerializer(question).data, status=status.HTTP_200_OK)