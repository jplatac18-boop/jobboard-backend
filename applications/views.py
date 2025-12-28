# applications/views.py
from rest_framework import generics, permissions

from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsCandidate


class ApplicationCreateView(generics.CreateAPIView):
    """
    Candidatos crean una postulación (POST /api/applications/)
    Body: { "job_id": <id>, "cover_letter": "..." }
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]


class ApplicationListView(generics.ListAPIView):
    """
    Empresa ve postulaciones de sus ofertas.
    GET /api/applications/list/?job=<id>&status=PENDING|ACCEPTED|REJECTED
    - Si no se manda status, se usa PENDING por defecto.
    """
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Incluimos company para evitar N+1 y poder filtrar
        qs = Application.objects.select_related("job__company", "candidate")

        # Solo empresas pueden ver postulaciones de sus ofertas
        if getattr(user, "role", None) == "COMPANY":
            company = getattr(user, "company_profile", None)
            if company is None:
                return Application.objects.none()
            qs = qs.filter(job__company=company)
        else:
            return Application.objects.none()

        job_id = self.request.query_params.get("job")
        if job_id:
            qs = qs.filter(job_id=job_id)

        status_param = self.request.query_params.get("status", "PENDING")
        if status_param:
            qs = qs.filter(status=status_param)

        return qs.order_by("-created_at")


class MyApplicationsListView(generics.ListAPIView):
    """
    Candidato ve sus propias postulaciones.
    GET /api/applications/me/?status=PENDING|ACCEPTED|REJECTED
    - Si no se manda status, devuelve todas.
    """
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get_queryset(self):
        user = self.request.user
        qs = (
            Application.objects.select_related("job__company")
            .filter(candidate=user)
        )

        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)

        return qs.order_by("-created_at")


class ApplicationStatusUpdateView(generics.UpdateAPIView):
    """
    Empresa cambia el estado de una postulación.
    PATCH /api/applications/<id>/ { "status": "ACCEPTED" | "REJECTED" }
    """
    queryset = Application.objects.select_related("job__company", "candidate")
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch"]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) != "COMPANY":
            return Application.objects.none()

        company = getattr(user, "company_profile", None)
        if company is None:
            return Application.objects.none()

        # Solo postulaciones de sus propios jobs
        return super().get_queryset().filter(job__company=company)
