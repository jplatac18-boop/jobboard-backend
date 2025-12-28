from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from companies.models import CompanyProfile
from jobs.models import Job
from users.models import CandidateProfile
from applications.models import Application

User = get_user_model()

class AuthAndJobApplicationTests(APITestCase):

    def setUp(self):
        # usuario empresa
        self.company_user = User.objects.create_user(
            username='empresa_api',
            email='empresa_api@test.com',
            password='Prueba123!',
            role='COMPANY'
        )
        self.company_profile = CompanyProfile.objects.create(
            user=self.company_user,
            company_name='Empresa API',
            location='Colombia'
        )

        # usuario candidato
        self.candidate_user = User.objects.create_user(
            username='candidato_api',
            email='candidato_api@test.com',
            password='Prueba123!',
            role='CANDIDATE'
        )
        self.candidate_profile = CandidateProfile.objects.create(
            user=self.candidate_user,
            location='Colombia'
        )

    def get_token(self, username, password):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': username, 'password': password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_login_jwt(self):
        token = self.get_token('empresa_api', 'Prueba123!')
        self.assertTrue(len(token) > 0)

    def test_create_job_as_company(self):
        token = self.get_token('empresa_api', 'Prueba123!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = '/api/jobs/'
        data = {
            "company": self.company_profile.id,
            "title": "Job API Test",
            "description": "Creado desde test.",
            "salary_min": "3000000",
            "salary_max": "5000000",
            "modality": "REMOTE",
            "job_type": "FULL_TIME",
            "location": "Colombia",
            "level": "Junior",
            "status": "ACTIVE"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)

    def test_apply_to_job_as_candidate(self):
        # crear job primero
        job = Job.objects.create(
            company=self.company_profile,
            title='Job para aplicar',
            description='Prueba de aplicación.',
            salary_min=3000000,
            salary_max=5000000,
            modality='REMOTE',
            job_type='FULL_TIME',
            location='Colombia',
            level='Junior',
            status='ACTIVE',
        )

        token = self.get_token('candidato_api', 'Prueba123!')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = '/api/applications/'
        data = {
            "job": job.id,
            "status": "APPLIED",
            "cover_letter": "Test desde APITestCase",
            "cv_url_override": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
