from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from account.models import User

class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user-create')
        self.valid_payload = {
            'name': 'Ozenc',
            'surname': 'Kandemir',
            'email': 'kandemirozenc@gmail.com',
            'phone': '1234567890'
        }
        self.invalid_payload = {
            'name': '',
            'surname': 'Kandemir',
            'email': 'kandemirozenc@gmail.com',
            'phone': '1234567890'
        }
        self.invalid_payload2 = {
            "name": "Ozenc",
            "surname": "Kandemir",
            "email": "kandemirozenc5@gmail.com",
            "phone": "1234567",
            "store_url": "http://www.url.com",
            "platform": "Amazon"
        }
    
    def test_register_with_valid_payload(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'Ozenc')
        
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # same email can not be inserted

    def test_register_with_invalid_payload(self):
        response = self.client.post(self.register_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_existing_email(self):
        User.objects.create(**self.valid_payload)
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(User.objects.count(), 1)
    
    def test_register_notvalid_data(self):
        response = self.client.post(self.register_url, self.invalid_payload2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(User.objects.count(), 1)
        # self.assertEqual(User.objects.get().name, 'Ozenc')
        
        # response = self.client.post(self.register_url, self.valid_payload, format='json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # same email can not be inserted
