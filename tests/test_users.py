from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from account.models import User

class UsersViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.users_url = reverse('all-users-get')
        User.objects.create_user(email='kandemirozenc1@gmail.com', name='Ozenc', surname='Kandemir 1', password='test12345')
        User.objects.create_user(email='kandemirozenc2@gmail.com', name='Ozenc', surname='Kandemir 2', password='test12345')

    def test_get_all_users(self):
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        self.assertIn('kandemirozenc1@gmail.com', str(response.data))
        self.assertIn('kandemirozenc2@gmail.com', str(response.data))
