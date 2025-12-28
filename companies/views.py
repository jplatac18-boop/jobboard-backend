from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CompanyProfile
from .serializers import (
    CompanyProfileSerializer,
    CompanyProfileUpdateSerializer,
)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", "") == "ADMIN"
        )


class IsCompanyUser(permissions.BasePermission):
    """
    Permiso para usuarios con rol COMPANY.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", "") == "COMPANY"
        )


class AdminCompanyListView(generics.ListAPIView):
    queryset = CompanyProfile.objects.select_related("user").order_by("name")
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAdmin]


class AdminCompanyToggleActiveView(generics.UpdateAPIView):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAdmin]
    http_method_names = ["patch"]

    def patch(self, request, *args, **kwargs):
        company = self.get_object()
        company.is_active = not company.is_active
        company.save()

        user = company.user
        user.is_active = company.is_active
        user.save()

        serializer = self.get_serializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyMeView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/companies/me/    -> perfil de la empresa logueada
    PATCH /api/companies/me/   -> actualizar nombre, descripción, website, location
    """

    permission_classes = [IsCompanyUser]

    def get_object(self):
        # Asumimos que el usuario COMPANY siempre tiene CompanyProfile creado
        return self.request.user.company_profile

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return CompanyProfileUpdateSerializer
        return CompanyProfileSerializer


class CompanyPublicDetailView(generics.RetrieveAPIView):
    """
    GET /api/companies/<int:pk>/  -> detalle público de una empresa
    (para usar desde JobDetail o una página pública /companies/:id en el frontend)
    """

    queryset = CompanyProfile.objects.filter(is_active=True).select_related("user")
    serializer_class = CompanyProfileSerializer
    permission_classes = [permissions.AllowAny]
