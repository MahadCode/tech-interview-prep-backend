from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField()
    is_active = models.BooleanField(default=True)
    created_at = models.BigAutoField(auto_now_add=True)

class JobRole(models.Model):
    name = models.CharField()
    is_active = models.BooleanField(default=True)
    created_at = models.BigAutoField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField()
    is_active = models.BooleanField(default=True)
    created_at = models.BigAutoField(auto_now_add=True)
    
    
