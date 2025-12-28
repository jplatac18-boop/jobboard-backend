from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ("CANDIDATE", "Candidate"),
        ("COMPANY", "Company"),
        ("ADMIN", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="CANDIDATE")

    # para desactivar usuarios sin borrarlos
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="candidate_profile",
    )
    phone = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=255, blank=True)
    resume_url = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    skills = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil candidato: {self.user.username}"
