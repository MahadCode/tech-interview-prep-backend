from django.contrib import admin
from .models import Comment,Solution,Report

# Register your models here.
@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'question', 'content']

@admin.register(Comment)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'question', 'solution', 'reply_to', 'content']
    
admin.site.register(Report)