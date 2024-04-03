from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('user-logout')

    def test_logout_success(self):
        self.client.cookies['jwt'] = 'testtoken'
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.cookies['jwt'].value, '')
        self.assertEqual(response.data['message'], 'success')

    
    def test_logout_response_structure(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'success')
