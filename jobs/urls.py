# jobs/urls.py
from django.urls import path
from .views import (
    JobListCreateView,
    JobDetailView,
    AdminJobListView,
    AdminJobToggleActiveView,
)

urlpatterns = [
    # Lista pública + creación (empresa autenticada)
    # GET /api/jobs/  (AllowAny)
    # POST /api/jobs/ (IsAuthenticated + IsCompany)
    path("jobs/", JobListCreateView.as_view(), name="job-list-create"),

    # Detalle público + update/delete de la empresa dueña
    # GET /api/jobs/<id>/
    # PUT/PATCH/DELETE requieren autenticación y ser la empresa dueña
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job-detail"),

    # Endpoints de administración (panel admin)
    # GET /api/admin/jobs/
    path("admin/jobs/", AdminJobListView.as_view(), name="admin-job-list"),

    # PATCH /api/admin/jobs/<id>/toggle/
    path(
        "admin/jobs/<int:pk>/toggle/",
        AdminJobToggleActiveView.as_view(),
        name="admin-job-toggle",
    ),
]
