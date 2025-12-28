# jobs/models.py
from django.db import models
from companies.models import CompanyProfile


class Job(models.Model):
    # Empresa dueña de la oferta
    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name="jobs",
        db_index=True,
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(
        max_length=255,
        db_index=True,
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["is_active", "location"],
                name="job_active_location_idx",
            ),
            models.Index(
                fields=["company", "is_active"],
                name="job_company_active_idx",
            ),
            models.Index(
                fields=["-created_at"],
                name="job_created_at_desc_idx",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} - {self.company.name}"
