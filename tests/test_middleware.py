from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from account.middleware import TokenAuthenticationMiddleware
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
import json
import jwt

User = get_user_model()

class TokenAuthenticationMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = TokenAuthenticationMiddleware(lambda x: JsonResponse({"message": "success"}))

    @patch('account.middleware.get_token_from_cookie')
    @patch('account.middleware.validate_access_token')
    def test_valid_token_authentication(self, mock_validate_access_token, mock_get_token_from_cookie):
        mock_get_token_from_cookie.return_value = 'validtoken'
        mock_user = User.objects.create_user(email='kandemirozenc1@gmail.com', password='password123')
        mock_validate_access_token.return_value = (mock_user, None)

        data = {
            "email": "kandemirozenc1@gmail.com",
            "store_url": "http://www.url.com",
            "platform": "Amazon"
        }

        request = self.factory.patch('/user/', data=json.dumps(data))
        response = self.middleware.process_request(request)
        
        self.assertIsNone(response)  # Middleware should not return a response for valid authentication
        self.assertEqual(request.user, mock_user)

    @patch('account.middleware.get_token_from_cookie')
    def test_missing_token(self, mock_get_token_from_cookie):
        mock_get_token_from_cookie.side_effect = AuthenticationFailed('Unauthenticated!')
        request = self.factory.patch('/user/')
        response = self.middleware.process_request(request)
        
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 401)

    @patch('account.middleware.get_token_from_cookie')
    def test_expired_jwt(self, mock_get_token_from_cookie):
        mock_get_token_from_cookie.side_effect = jwt.ExpiredSignatureError
        request = self.factory.patch('/user/', HTTP_AUTHORIZATION='Bearer expiredtoken')

        with self.assertRaises(AuthenticationFailed) as context:
            self.middleware.process_request(request)
        self.assertEqual(str(context.exception), 'Unauthenticated!')
    
    @patch('account.middleware.get_token_from_cookie')
    def test_jwt_decode_error(self, mock_get_token_from_cookie):
        mock_get_token_from_cookie.side_effect = jwt.DecodeError
        request = self.factory.patch('/user/', HTTP_AUTHORIZATION='Bearer expiredtoken')

        with self.assertRaises(AuthenticationFailed) as context:
            self.middleware.process_request(request)
        self.assertEqual(str(context.exception), 'Authorization token is required!')