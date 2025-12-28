from django.urls import path
from .views import (
    JobListCreateView,
    JobDetailView,
    AdminJobListView,
    AdminJobToggleActiveView,
)

urlpatterns = [
    path("jobs/", JobListCreateView.as_view(), name="job-list-create"),
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job-detail"),

    path("admin/jobs/", AdminJobListView.as_view(), name="admin-job-list"),
    path(
        "admin/jobs/<int:pk>/toggle/",
        AdminJobToggleActiveView.as_view(),
        name="admin-job-toggle",
    ),
]
