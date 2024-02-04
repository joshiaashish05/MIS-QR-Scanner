import base64
from django.contrib.auth import authenticate
from rest_framework import authentication
from rest_framework import exceptions

class BasicAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_AUTHORIZATION')
        if not username:
            return None
        try:
            username = username.split('Basic ')[1]
            username = base64.b64decode(username).decode('utf-8')
            username, password = username.split(':')
            user = authenticate(request=request, username=username, password=password)
        except (ValueError, TypeError):
            raise exceptions.AuthenticationFailed('Invalid basic authentication header')

        if not user:
            raise exceptions.AuthenticationFailed('Invalid username or password')

        return (user, None)
