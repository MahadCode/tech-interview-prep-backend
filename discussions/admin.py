from django.contrib import admin
from .models import Comment,Solution,Report

# Register your models here.
admin.site.register(Solution)
admin.site.register(Comment)
admin.site.register(Report)