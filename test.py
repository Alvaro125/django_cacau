import io
import json
import unittest
from datetime import datetime, date
from unittest.mock import patch, MagicMock, ANY

from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer, RegisterSerializer
from accounts.views import RegisterView, ListView, VerifyTokenView

from profiles.models import Profile, Skill, Language, Experience, Course, Certificate, Degree, Project
from profiles.serializers import (
    ProfileSerializer, SkillSerializer, LanguageSerializer, ExperienceSerializer,
    CourseSerializer, CertificateSerializer, DegreeSerializer, ProjectSerializer
)
from profiles.views import (
    ProfileViewSet, SkillViewSet, LanguageViewSet, ExperienceViewSet,
    CourseViewSet, CertificateViewSet, DegreeViewSet, ProjectViewSet
)

from cvitae.models import CVitae
from cvitae.views import MarkdownCreateView


class VerifyTokenViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.verify_token_url = reverse('verify-token')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )

    def test_verify_token_requires_authentication(self):
        """Test that verify token view requires authentication"""
        response = self.client.get(self.verify_token_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_token_with_authentication(self):
        """Test verify token view with authentication"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.verify_token_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_valid'])
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio',
            linkedin='https://linkedin.com/test',
            github='https://github.com/test',
            website='https://test.com'
        )

    def test_profile_creation(self):
        """Test Profile model creation"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.bio, 'Test bio')
        self.assertEqual(self.profile.linkedin, 'https://linkedin.com/test')
        self.assertEqual(self.profile.github, 'https://github.com/test')
        self.assertEqual(self.profile.website, 'https://test.com')

    def test_profile_str_method(self):
        """Test Profile __str__ method"""
        self.assertEqual(str(self.profile), f"Profile of {self.user.username}")


class SkillModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.skill = Skill.objects.create(
            profile=self.profile,
            name='Python',
            proficiency='Advanced'
        )

    def test_skill_creation(self):
        """Test Skill model creation"""
        self.assertEqual(self.skill.profile, self.profile)
        self.assertEqual(self.skill.name, 'Python')
        self.assertEqual(self.skill.proficiency, 'Advanced')

    def test_skill_str_method(self):
        """Test Skill __str__ method"""
        self.assertEqual(str(self.skill), 'Python (Advanced)')


class LanguageModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.language = Language.objects.create(
            profile=self.profile,
            name='English',
            level='Fluent'
        )

    def test_language_creation(self):
        """Test Language model creation"""
        self.assertEqual(self.language.profile, self.profile)
        self.assertEqual(self.language.name, 'English')
        self.assertEqual(self.language.level, 'Fluent')

    def test_language_str_method(self):
        """Test Language __str__ method"""
        self.assertEqual(str(self.language), 'English (Fluent)')


class ExperienceModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.experience = Experience.objects.create(
            profile=self.profile,
            company='Test Company',
            title='Developer',
            description='Developed amazing things',
            start_date=date(2020, 1, 1),
            end_date=date(2022, 1, 1)
        )

    def test_experience_creation(self):
        """Test Experience model creation"""
        self.assertEqual(self.experience.profile, self.profile)
        self.assertEqual(self.experience.company, 'Test Company')
        self.assertEqual(self.experience.title, 'Developer')
        self.assertEqual(self.experience.description, 'Developed amazing things')
        self.assertEqual(self.experience.start_date, date(2020, 1, 1))
        self.assertEqual(self.experience.end_date, date(2022, 1, 1))

    def test_experience_str_method(self):
        """Test Experience __str__ method"""
        self.assertEqual(str(self.experience), 'Developer at Test Company')


class CourseModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.course = Course.objects.create(
            profile=self.profile,
            title='Python Course',
            institution='Test Institution',
            completion_date=date(2021, 1, 1)
        )

    def test_course_creation(self):
        """Test Course model creation"""
        self.assertEqual(self.course.profile, self.profile)
        self.assertEqual(self.course.title, 'Python Course')
        self.assertEqual(self.course.institution, 'Test Institution')
        self.assertEqual(self.course.completion_date, date(2021, 1, 1))

    def test_course_str_method(self):
        """Test Course __str__ method"""
        self.assertEqual(str(self.course), 'Python Course (Test Institution)')


class CertificateModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.certificate = Certificate.objects.create(
            profile=self.profile,
            name='Python Certificate',
            issuer='Test Issuer',
            issue_date=date(2021, 1, 1)
        )

    def test_certificate_creation(self):
        """Test Certificate model creation"""
        self.assertEqual(self.certificate.profile, self.profile)
        self.assertEqual(self.certificate.name, 'Python Certificate')
        self.assertEqual(self.certificate.issuer, 'Test Issuer')
        self.assertEqual(self.certificate.issue_date, date(2021, 1, 1))

    def test_certificate_str_method(self):
        """Test Certificate __str__ method"""
        self.assertEqual(str(self.certificate), 'Python Certificate issued by Test Issuer')


class DegreeModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.degree = Degree.objects.create(
            profile=self.profile,
            title='Computer Science',
            institution='Test University',
            start_date=date(2018, 1, 1),
            completion_date=date(2022, 1, 1)
        )

    def test_degree_creation(self):
        """Test Degree model creation"""
        self.assertEqual(self.degree.profile, self.profile)
        self.assertEqual(self.degree.title, 'Computer Science')
        self.assertEqual(self.degree.institution, 'Test University')
        self.assertEqual(self.degree.start_date, date(2018, 1, 1))
        self.assertEqual(self.degree.completion_date, date(2022, 1, 1))

    def test_degree_str_method(self):
        """Test Degree __str__ method"""
        self.assertEqual(str(self.degree), 'Computer Science at Test University')


class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.project = Project.objects.create(
            profile=self.profile,
            title='Test Project',
            description='A project for testing',
            project_url='https://github.com/test/project'
        )

    def test_project_creation(self):
        """Test Project model creation"""
        self.assertEqual(self.project.profile, self.profile)
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.description, 'A project for testing')
        self.assertEqual(self.project.project_url, 'https://github.com/test/project')

    def test_project_str_method(self):
        """Test Project __str__ method"""
        self.assertEqual(str(self.project), 'Test Project')


class CVitaeModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.cvitae = CVitae.objects.create(
            user=self.user,
            url='https://example.com/cv',
            content='Test job description'
        )

    def test_cvitae_creation(self):
        """Test CVitae model creation"""
        self.assertEqual(self.cvitae.user, self.user)
        self.assertEqual(self.cvitae.url, 'https://example.com/cv')
        self.assertEqual(self.cvitae.content, 'Test job description')
        self.assertIsNotNone(self.cvitae.created)

    def test_cvitae_str_method(self):
        """Test CVitae __str__ method"""
        self.assertEqual(str(self.cvitae), f"Profile of {self.user.username}")


class ProfileViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio',
            linkedin='https://linkedin.com/test',
            github='https://github.com/test',
            website='https://test.com'
        )
        self.client.force_authenticate(user=self.user)
        self.profile_list_url = reverse('profile-list')
        self.profile_detail_url = reverse('profile-detail', kwargs={'pk': self.profile.pk})

    def test_profile_list(self):
        """Test getting a list of profiles (should only return the user's profile)"""
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.profile.id)
        self.assertEqual(response.data['bio'], self.profile.bio)

    def test_profile_detail(self):
        """Test getting profile details"""
        response = self.client.get(self.profile_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.profile.id)
        self.assertEqual(response.data['bio'], self.profile.bio)

    def test_profile_update(self):
        """Test updating a profile"""
        update_data = {
            'bio': 'Updated bio',
            'linkedin': 'https://linkedin.com/updated',
            'github': 'https://github.com/updated',
            'website': 'https://updated.com'
        }
        response = self.client.put(self.profile_detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, update_data['bio'])
        self.assertEqual(self.profile.linkedin, update_data['linkedin'])
        self.assertEqual(self.profile.github, update_data['github'])
        self.assertEqual(self.profile.website, update_data['website'])

    def test_profile_create(self):
        """Test creating a profile (should fail if one already exists)"""
        # Clean up existing profile
        self.profile.delete()

        create_data = {
            'bio': 'New bio',
            'linkedin': 'https://linkedin.com/new',
            'github': 'https://github.com/new',
            'website': 'https://new.com'
        }
        response = self.client.post(self.profile_list_url, create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 1)
        new_profile = Profile.objects.first()
        self.assertEqual(new_profile.bio, create_data['bio'])

    def test_profile_not_found(self):
        """Test handling when profile is not found"""
        # Create a second user without a profile
        user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword123'
        )
        self.client.force_authenticate(user=user2)
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SkillViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.skill = Skill.objects.create(
            profile=self.profile,
            name='Python',
            proficiency='Advanced'
        )
        self.client.force_authenticate(user=self.user)
        self.skill_list_url = reverse('skill-list')
        self.skill_detail_url = reverse('skill-detail', kwargs={'pk': self.skill.pk})

    def test_skill_list(self):
        """Test getting a list of skills"""
        response = self.client.get(self.skill_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.skill.name)

    def test_skill_detail(self):
        """Test getting skill details"""
        response = self.client.get(self.skill_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.skill.name)
        self.assertEqual(response.data['proficiency'], self.skill.proficiency)

    def test_skill_create(self):
        """Test creating a skill"""
        create_data = {
            'name': 'JavaScript',
            'proficiency': 'Intermediate'
        }
        response = self.client.post(self.skill_list_url, create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skill.objects.count(), 2)
        new_skill = Skill.objects.get(name='JavaScript')
        self.assertEqual(new_skill.proficiency, 'Intermediate')
        self.assertEqual(new_skill.profile, self.profile)

    def test_skill_update(self):
        """Test updating a skill"""
        update_data = {
            'name': 'Python',
            'proficiency': 'Expert'
        }
        response = self.client.put(self.skill_detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.proficiency, 'Expert')

    def test_skill_delete(self):
        """Test deleting a skill"""
        response = self.client.delete(self.skill_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Skill.objects.count(), 0)

    def test_skill_create_without_profile(self):
        """Test creating a skill when user has no profile"""
        # Create a second user without a profile
        user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword123'
        )
        self.client.force_authenticate(user=user2)
        create_data = {
            'name': 'JavaScript',
            'proficiency': 'Intermediate'
        }
        response = self.client.post(self.skill_list_url, create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LanguageViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.language = Language.objects.create(
            profile=self.profile,
            name='English',
            level='Fluent'
        )
        self.client.force_authenticate(user=self.user)
        self.language_list_url = reverse('language-list')
        self.language_detail_url = reverse('language-detail', kwargs={'pk': self.language.pk})

    def test_language_list(self):
        """Test getting a list of languages"""
        response = self.client.get(self.language_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.language.name)

    def test_language_detail(self):
        """Test getting language details"""
        response = self.client.get(self.language_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.language.name)
        self.assertEqual(response.data['level'], self.language.level)

    def test_language_create(self):
        """Test creating a language"""
        create_data = {
            'name': 'Spanish',
            'level': 'Intermediate'
        }
        response = self.client.post(self.language_list_url, create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Language.objects.count(), 2)
        new_language = Language.objects.get(name='Spanish')
        self.assertEqual(new_language.level, 'Intermediate')
        self.assertEqual(new_language.profile, self.profile)


class ExperienceViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.experience = Experience.objects.create(
            profile=self.profile,
            company='Test Company',
            title='Developer',
            description='Developed amazing things',
            start_date=date(2020, 1, 1),
            end_date=date(2022, 1, 1)
        )
        self.client.force_authenticate(user=self.user)
        self.experience_list_url = reverse('experience-list')
        self.experience_detail_url = reverse('experience-detail', kwargs={'pk': self.experience.pk})

    def test_experience_list(self):
        """Test getting a list of experiences"""
        response = self.client.get(self.experience_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['company'], self.experience.company)

    def test_experience_detail(self):
        """Test getting experience details"""
        response = self.client.get(self.experience_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company'], self.experience.company)
        self.assertEqual(response.data['title'], self.experience.title)


class CourseViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.course = Course.objects.create(
            profile=self.profile,
            title='Python Course',
            institution='Test Institution',
            completion_date=date(2021, 1, 1)
        )
        self.client.force_authenticate(user=self.user)
        self.course_list_url = reverse('course-list')
        self.course_detail_url = reverse('course-detail', kwargs={'pk': self.course.pk})

    def test_course_list(self):
        """Test getting a list of courses"""
        response = self.client.get(self.course_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.course.title)
