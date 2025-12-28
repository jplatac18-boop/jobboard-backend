# jobs/serializers.py
from rest_framework import serializers
from .models import Job
from companies.models import CompanyProfile
from companies.serializers import CompanyProfileSerializer


class CompanyMinimalSerializer(serializers.ModelSerializer):
    """
    Versión ligera del perfil de empresa para usar dentro de Job.
    """

    class Meta:
        model = CompanyProfile
        fields = ("id", "name", "location", "website")


class JobSerializer(serializers.ModelSerializer):
    # Devuelve los datos de la empresa anidados (solo lectura)
    company = CompanyMinimalSerializer(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "location",
            "salary",
            "created_at",
            "is_active",
            "company",
        ]
        read_only_fields = ["id", "created_at", "is_active", "company"]
