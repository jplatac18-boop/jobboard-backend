from django.test import TestCase
from django.contrib.auth import get_user_model

from companies.models import CompanyProfile
from jobs.models import Job
from applications.models import Application
from users.models import CandidateProfile

User = get_user_model()

class ApplicationModelTest(TestCase):
    def setUp(self):
        self.company_user = User.objects.create_user(
            username='empresa_test2',
            email='empresa2@test.com',
            password='Prueba123!',
            role='COMPANY'
        )
        self.company_profile = CompanyProfile.objects.create(
            user=self.company_user,
            company_name='Empresa Test 2',
            location='Colombia'
        )
        self.job = Job.objects.create(
            company=self.company_profile,
            title='Frontend Developer',
            description='Trabajo con React.',
            salary_min=2000000,
            salary_max=4000000,
            modality='REMOTE',
            job_type='FULL_TIME',
            location='Colombia',
            level='Junior',
            status='ACTIVE',
        )

        self.candidate_user = User.objects.create_user(
            username='candidato_test',
            email='candidato@test.com',
            password='Prueba123!',
            role='CANDIDATE'
        )
        self.candidate_profile = CandidateProfile.objects.create(
            user=self.candidate_user,
            location='Colombia'
        )

    def test_create_application(self):
        application = Application.objects.create(
            job=self.job,
            candidate=self.candidate_profile,
            status='APPLIED',
            cover_letter='Me interesa la vacante.'
        )
        self.assertEqual(application.job, self.job)
        self.assertEqual(application.candidate, self.candidate_profile)
