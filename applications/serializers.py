# applications/serializers.py
from rest_framework import serializers
from django.db import IntegrityError
from .models import Application
from jobs.models import Job
from users.models import User


class CandidateMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


class JobMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id", "title", "location"]


class ApplicationSerializer(serializers.ModelSerializer):
    # Solo para lectura en las respuestas
    candidate = CandidateMiniSerializer(read_only=True)
    job = JobMiniSerializer(read_only=True)

    # Campo extra de solo escritura para recibir el id del job
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), write_only=True, source="job"
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "job",       # salida (anidado)
            "job_id",    # entrada (id)
            "candidate",
            "cover_letter",
            "created_at",
            "status",
        ]
        read_only_fields = ["id", "candidate", "created_at", "job"]

    def create(self, validated_data):
        request = self.context["request"]
        try:
            return Application.objects.create(candidate=request.user, **validated_data)
        except IntegrityError:
            # Ya existe una postulación para (job, candidate)
            raise serializers.ValidationError(
                {"non_field_errors": ["Ya te has postulado a esta oferta."]}
            )
