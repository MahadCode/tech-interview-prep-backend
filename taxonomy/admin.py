from django.contrib import admin
from .models import Company,Tag,JobRole

# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
