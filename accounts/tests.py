from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer, RegisterSerializer


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_custom_user_creation(self):
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.first_name, self.user_data['first_name'])
        self.assertEqual(self.user.last_name, self.user_data['last_name'])
        self.assertTrue(self.user.check_password(self.user_data['password']))

    def test_custom_user_str_method(self):
        self.assertEqual(str(self.user), self.user_data['username'])


class RegisterSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_serialize_user(self):
        serializer = RegisterSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_duplicate_email(self):
        CustomUser.objects.create_user(
            username='user1',
            email=self.user_data['email'],
            password='password123'
        )

        serializer = RegisterSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


class CustomUserSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )

    def test_serializer_contains_expected_fields(self):
        serializer = CustomUserSerializer(instance=self.user)
        expected_fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'first_name', 'last_name']
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))


class RegisterViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, self.user_data['username'])

    def test_register_user_with_existing_email(self):
        CustomUser.objects.create_user(
            username='user1',
            email=self.user_data['email'],
            password='password123'
        )

        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class ListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('list')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )

    def test_list_requires_authentication(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_with_authentication(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)