from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
import jwt
from datetime import datetime, timedelta

User = get_user_model()

class UserViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='kandemirozenc1@gmail.com', name='Ozenc', surname='Kandemir', phone='1234567890')
        self.update_url = reverse('user-get')
        self.secret = "secret"

    def generate_jwt(self, user_id, expired=False):
        payload = {
            'id': user_id,
            'exp': datetime.now() + timedelta(days=(-1 if expired else 1)),
            'iat': datetime.now().timestamp()
        }
        token = jwt.encode(payload, self.secret, algorithm='HS256')
        return token

    def test_update_user_success(self):
        data = {
            "email": "kandemirozenc1@gmail.com",
            "store_url": "http://www.url.com",
            "platform": "Amazon"
        }
        token = self.generate_jwt(self.user.id)
        self.client.cookies['jwt'] = token
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.update_url, data, format='json')
        
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.platform, 'Amazon')

    def test_update_non_existent_user(self):
        data = {
            "email": "non_exist@example.com",
            "store_url": "http://www.url.com",
            "platform": "Amazon"
        }
        token = self.generate_jwt(self.user.id)
        self.client.cookies['jwt'] = token
        response = self.client.patch(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_with_disallowed_fields(self):
        data = {
            'email': 'kandemirozenc1@gmail.com',
            'store_url': 'http://forbidden.com',
            "platform": "Amazqwen"
        }
        token = self.generate_jwt(self.user.id)
        self.client.cookies['jwt'] = token
        response = self.client.patch(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_non_exist_user(self):
        data = {
            'email': 'test1@example.com',
            'store_url': 'http://forbidden.com',
            "platform": "Amazqwen"
        }
        token = self.generate_jwt(self.user.id)
        self.client.cookies['jwt'] = token
        response = self.client.patch(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
