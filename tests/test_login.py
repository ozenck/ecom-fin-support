from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('user-login')

        self.user = User.objects.create_user(email='kandemirozenc@gmail.com', name='Ozenc', surname='Kandemir', phone='1234567890')
        self.test_user_password = User.objects.filter(email=self.user.email).first().password

    def test_successful_login(self):
        response = self.client.post(self.login_url, {'email': self.user.email, 'password': self.test_user_password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('jwt' in response.data)

    def test_login_incorrect_password(self):
        response = self.client.post(self.login_url, {'email': self.user.email, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Incorrect password!')

    def test_login_nonexistent_user(self):
        response = self.client.post(self.login_url, {'email': 'nonexistent@example.com', 'password': 'somepassword'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'User not found!')

    def test_login_missing_fields(self):
        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Please check email and password')

        response = self.client.post(self.login_url, {'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.login_url, {'password': 'somepassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
