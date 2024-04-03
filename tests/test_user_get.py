from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from account.models import User
import jwt
from datetime import datetime, timedelta

class UserViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_view_url = reverse('user-get')
        self.user = User.objects.create_user(
            email='kandemirozenc1@gmail.com', 
            name='Ozenc', 
            surname='Kandemir', 
            password='password123',
            phone='1234567890'
        )
        self.secret = 'secret'
        
    def generate_jwt(self, user_id, expired=False):
        payload = {
            'id': user_id,
            'exp': datetime.now() + timedelta(days=(-1 if expired else 1)),
            'iat': datetime.now().timestamp()
        }
        token = jwt.encode(payload, self.secret, algorithm='HS256')
        return token

    def test_user_data_retrieval_success(self):
        token = self.generate_jwt(self.user.id)
        self.client.cookies['jwt'] = token
        response = self.client.get(self.user_view_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_user_data_retrieval_unauthenticated_no_token(self):
        response = self.client.get(self.user_view_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Unauthenticated', str(response.data))

    def test_user_data_retrieval_unauthenticated_expired_token(self):
        expired_token = self.generate_jwt(self.user.id, expired=True)
        self.client.cookies['jwt'] = expired_token
        response = self.client.get(self.user_view_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Unauthenticated', str(response.data))

    def test_user_data_retrieval_unauthenticated_expired_token(self):
        expired_token = self.generate_jwt(self.user.id, expired=True)
        self.client.cookies['jwt'] = expired_token
        response = self.client.get(self.user_view_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Unauthenticated', str(response.data))
