# companies/signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CompanyProfile

UserModel = settings.AUTH_USER_MODEL  # cadena "users.User"


@receiver(post_save, sender=UserModel)
def create_company_profile(sender, instance, created, **kwargs):
    if not created:
        return

    # Ajusta "role" y el valor "COMPANY" a como lo tengas en tu modelo User
    if getattr(instance, "role", "") == "COMPANY":
        CompanyProfile.objects.create(
            user=instance,
            name=getattr(instance, "username", str(instance)),
        )
