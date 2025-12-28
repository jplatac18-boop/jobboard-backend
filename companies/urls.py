# companies/urls.py
from django.urls import path
from .views import (
    AdminCompanyListView,
    AdminCompanyToggleActiveView,
    CompanyMeView,
    CompanyPublicDetailView,
)
from jobs.views import CompanyJobsPublicListView

urlpatterns = [
    # Admin
    path("admin/companies/", AdminCompanyListView.as_view(), name="admin-companies"),
    path(
        "admin/companies/<int:pk>/toggle/",
        AdminCompanyToggleActiveView.as_view(),
        name="admin-company-toggle",
    ),

    # Perfil de empresa autenticada (para /company/profile en React)
    path("companies/me/", CompanyMeView.as_view(), name="company-me"),

    # Detalle público de empresa (para /companies/:id en React)
    path(
        "companies/<int:pk>/",
        CompanyPublicDetailView.as_view(),
        name="company-detail",
    ),

    # Jobs públicos de la empresa
    path(
        "companies/<int:pk>/jobs/",
        CompanyJobsPublicListView.as_view(),
        name="company-jobs-public",
    ),
]
