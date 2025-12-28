from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "candidate", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("job__title", "candidate__username")
