# Register your models here.

from django.contrib import admin
from .models import PreparationGoal

@admin.register(PreparationGoal)
class PreparationGoalAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "metric", "target_value", "target_tag", "target_company", "deadline", "created_at")

