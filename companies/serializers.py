from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CompanyProfile

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = CompanyProfile
        fields = (
            "id",
            "name",
            "description",
            "website",
            "location",
            "is_active",
            "user",
        )
        read_only_fields = ("id", "is_active", "user")


class CompanyProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para que la empresa actualice sólo sus propios datos
    desde /companies/me/ (sin poder tocar usuario ni is_active).
    """

    class Meta:
        model = CompanyProfile
        fields = (
            "name",
            "description",
            "website",
            "location",
        )
