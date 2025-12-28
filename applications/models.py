# applications/models.py
from django.db import models
from django.conf import settings
from jobs.models import Job


class Application(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
        db_index=True,  # consultas por oferta
    )
    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
        db_index=True,  # consultas por candidato
    )
    cover_letter = models.TextField(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,  # ordenar por fecha
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
        db_index=True,  # filtros por estado
    )

    class Meta:
        unique_together = ("job", "candidate")
        indexes = [
            # Postulaciones de una oferta por estado
            models.Index(
                fields=["job", "status"],
                name="app_job_status_idx",
            ),
            # Postulaciones de un candidato por estado
            models.Index(
                fields=["candidate", "status"],
                name="app_candidate_status_idx",
            ),
            # Postulaciones recientes por oferta
            models.Index(
                fields=["job", "-created_at"],
                name="app_job_created_desc_idx",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.candidate.username} -> {self.job.title}"
