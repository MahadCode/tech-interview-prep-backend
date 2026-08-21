from django.contrib import admin
from .models import Question, UserQuestionStatus
# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "difficulty_level"]

@admin.register(UserQuestionStatus)
class UserQuestionStatus(admin.ModelAdmin):
    list_display = ["id", "user", "question", "status"]