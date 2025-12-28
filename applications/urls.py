# applications/urls.py
from django.urls import path
from .views import (
    ApplicationCreateView,
    ApplicationListView,
    MyApplicationsListView,
    ApplicationStatusUpdateView,
)

urlpatterns = [
    path(
        "applications/",
        ApplicationCreateView.as_view(),
        name="application-create",
    ),
    path(
        "applications/list/",
        ApplicationListView.as_view(),
        name="application-list-by-job",
    ),
    path(
        "applications/me/",
        MyApplicationsListView.as_view(),
        name="my-applications",
    ),
    path(
        "applications/<int:pk>/",
        ApplicationStatusUpdateView.as_view(),
        name="application-status-update",
    ),
]
