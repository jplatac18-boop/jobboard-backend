# jobs/views.py
from rest_framework import generics, permissions, filters, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Job
from .serializers import JobSerializer
from .permissions import IsCompany
from companies.models import CompanyProfile


class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "location"]  # buscar por título / ubicación

    def get_queryset(self):
        # Incluimos select_related para evitar N+1 con company
        qs = Job.objects.select_related("company").filter(is_active=True).order_by(
            "-created_at"
        )
        user = self.request.user

        mine = self.request.query_params.get("mine")
        if (
            mine == "true"
            and user.is_authenticated
            and getattr(user, "role", None) == "COMPANY"
        ):
            # Ahora Job.company apunta a CompanyProfile, no al usuario
            company = getattr(user, "company_profile", None)
            if company is None:
                # Si por algún motivo el usuario COMPANY no tiene perfil, devolvemos vacío
                return Job.objects.none()
            qs = qs.filter(company=company)

        return qs

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsCompany()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user

        # si la empresa está bloqueada, no publica
        if not getattr(user, "is_active", True):
            raise PermissionDenied("Tu cuenta está bloqueada por el administrador.")

        # Asignar la empresa correcta (CompanyProfile) a la Job
        try:
            company = user.company_profile
        except CompanyProfile.DoesNotExist:
            raise PermissionDenied(
                "No tienes un perfil de empresa configurado para publicar ofertas."
            )

        serializer.save(company=company)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.select_related("company").filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        job = self.get_object()
        user = self.request.user

        # Solo la empresa dueña puede actualizar
        company = getattr(user, "company_profile", None)
        if not user.is_authenticated or company is None or job.company != company:
            raise PermissionDenied("No puedes modificar esta oferta.")

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        company = getattr(user, "company_profile", None)
        if not user.is_authenticated or company is None or instance.company != company:
            raise PermissionDenied("No puedes eliminar esta oferta.")
        instance.delete()


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", "") == "ADMIN"
        )


class AdminJobListView(generics.ListAPIView):
    queryset = Job.objects.select_related("company").order_by("-created_at")
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]


class AdminJobToggleActiveView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]
    http_method_names = ["patch"]

    def patch(self, request, *args, **kwargs):
        job = self.get_object()
        job.is_active = not job.is_active
        job.save()
        serializer = self.get_serializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyJobsPublicListView(generics.ListAPIView):
    """
    Jobs públicos de una empresa concreta.
    GET /api/companies/<id>/jobs/
    """
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        company_id = self.kwargs.get("pk")
        return (
            Job.objects.select_related("company")
            .filter(is_active=True, company_id=company_id)
            .order_by("-created_at")
        )
