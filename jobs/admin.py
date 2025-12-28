# jobs/admin.py
from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "company", "location", "created_at", "is_active")
    list_filter = ("company", "is_active", "created_at")
    search_fields = ("title", "company__username", "location")
