from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt
import json

def validate_access_token(token, request_data):
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None, JsonResponse({"error": "Unauthenticated"}, status=400)
    except jwt.DecodeError:
        return None, JsonResponse({"error": "Invalid or expired token"}, status=400)
    
    user = User.objects.filter(id=payload['id']).first()
    request_email = request_data.get("email")
    if request_email is None:
        return None, JsonResponse({"error": "email parameter should be exist in request body"}, status=400)
        # return None, "email parameter should be exist in request body"
    elif request_email != user.email:
        return None, JsonResponse({"error": "Token and user doesn't match"}, status=400)
    return user, ""

def get_token_from_cookie(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    except jwt.DecodeError:
        raise AuthenticationFailed('"Invalid or expired token"')

    user = User.objects.filter(id=payload['id']).first()
    if user is None:
       raise AuthenticationFailed("Invalid or expired token")
    return token


class TokenAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'PATCH':
            try:
                token = get_token_from_cookie(request)
            except AuthenticationFailed as ex:
                return JsonResponse({"error": ex.detail}, status=401)
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')
            except jwt.DecodeError:
                return JsonResponse({"error": "Authorization token is required"}, status=401)
            user, error_response = validate_access_token(token, json.loads(request.body))
            if not user:
                return error_response
                # return JsonResponse({"error": detail}, status=401)
            request.user = user
            return None
