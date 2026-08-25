from django.contrib import admin
from .models import ModerationReport
# Register your models here.
@admin.register(ModerationReport)
class ModerationReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'report', 'moderator', 'action']
