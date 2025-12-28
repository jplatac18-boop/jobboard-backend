from django.db import models
from companies.models import CompanyProfile


class Job(models.Model):
    # Empresa dueña de la oferta
    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name="jobs",
        db_index=True,  # FK ya viene indexada, pero lo dejamos explícito
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(
        max_length=255,
        db_index=True,          # búsquedas/filtrado por ubicación
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,          # orden por fecha de creación
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,          # muy usado para listar solo activas
    )

    class Meta:
        indexes = [
            # Listar ofertas activas por ubicación
            models.Index(
                fields=["is_active", "location"],
                name="job_active_location_idx",
            ),
            # Listar ofertas de una empresa, solo activas
            models.Index(
                fields=["company", "is_active"],
                name="job_company_active_idx",
            ),
            # Listar recientes primero
            models.Index(
                fields=["-created_at"],
                name="job_created_at_desc_idx",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.company.name}"
