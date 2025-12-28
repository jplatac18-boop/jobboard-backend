# users/management/commands/seed_jobboard.py

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from jobs.models import Job
from companies.models import CompanyProfile


User = get_user_model()


class Command(BaseCommand):
    help = "Crea datos iniciales para el Job Board (usuarios, empresas y ofertas)."

    def handle(self, *args, **options):
        # Admin
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "role": "ADMIN",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password("admin123")
            admin.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Superusuario admin creado (admin/admin123)"
                )
            )
        else:
            self.stdout.write("Superusuario admin ya existe")

        # Empresa
        company_user, created = User.objects.get_or_create(
            username="empresa_demo",
            defaults={
                "email": "empresa@example.com",
                "role": "COMPANY",
            },
        )
        if created:
            company_user.set_password("empresa123")
            company_user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Usuario empresa creado (empresa_demo/empresa123)"
                )
            )
        else:
            self.stdout.write("Usuario empresa ya existe")

        company_profile, _ = CompanyProfile.objects.get_or_create(
            user=company_user,
            defaults={
                "name": "Empresa Demo S.A.S.",
                "website": "https://empresa-demo.com",
                "description": "Empresa de ejemplo para el Job Board.",
                "location": "Cartagena, Colombia",
                "is_active": True,
            },
        )

        # Candidato
        candidate_user, created = User.objects.get_or_create(
            username="candidato_demo",
            defaults={
                "email": "candidato@example.com",
                "role": "CANDIDATE",
            },
        )
        if created:
            candidate_user.set_password("candidato123")
            candidate_user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Usuario candidato creado (candidato_demo/candidato123)"
                )
            )
        else:
            self.stdout.write("Usuario candidato ya existe")

        # Ofertas de trabajo
        jobs_data = [
            {
                "title": "Desarrollador Full Stack Junior",
                "description": "Stack: React, Django REST, PostgreSQL.\nTrabajo híbrido en Cartagena.",
                "location": "Cartagena, Colombia",
                # Usa Decimal o float simple, sin puntos de miles ni texto
                "salary": Decimal("4000000.00"),
            },
            {
                "title": "Frontend Developer React",
                "description": "Proyecto SPA con TypeScript y Tailwind.\nEquipo 100% remoto.",
                "location": "Remoto",
                "salary": Decimal("3500000.00"),
            },
            {
                "title": "Backend Developer Django",
                "description": "APIs REST con Django REST Framework y JWT.\nExperiencia con PostgreSQL.",
                "location": "Bogotá, Colombia",
                "salary": Decimal("5000000.00"),
            },
        ]

        created_count = 0
        for data in jobs_data:
            job, created_job = Job.objects.get_or_create(
                title=data["title"],
                company=company_user,
                defaults={
                    "description": data["description"],
                    "location": data["location"],
                    "salary": data["salary"],
                    "is_active": True,
                },
            )
            if created_job:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed completado. Nuevas ofertas creadas: {created_count}."
            )
        )
