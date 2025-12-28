from django.test import TestCase
from django.contrib.auth import get_user_model

from companies.models import CompanyProfile
from jobs.models import Job

User = get_user_model()

class JobModelTest(TestCase):
    def setUp(self):
        self.company_user = User.objects.create_user(
            username='empresa_test',
            email='empresa@test.com',
            password='Prueba123!',
            role='COMPANY'
        )
        self.company_profile = CompanyProfile.objects.create(
            user=self.company_user,
            company_name='Empresa Test',
            location='Colombia'
        )

    def test_create_job(self):
        job = Job.objects.create(
            company=self.company_profile,
            title='Backend Developer',
            description='Trabajo con Django y DRF.',
            salary_min=3000000,
            salary_max=5000000,
            modality='REMOTE',
            job_type='FULL_TIME',
            location='Colombia',
            level='Junior',
            status='ACTIVE',
        )
        self.assertEqual(job.title, 'Backend Developer')
        self.assertEqual(job.company, self.company_profile)
