import jwt
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseForbidden

class JWTValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.session.get('jwt_token')
        
        if token:
            try:
                # Use your actual secret key or public key for verification
                decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])  # Use your secret key here

                # Store decoded user info in the request object
                request.jwt_user = decoded

            except jwt.ExpiredSignatureError:
                # Token expired, log out the user
                logout(request)
                request.session.flush()
                return HttpResponseForbidden('Session expired. Please log in again.')
            except jwt.InvalidTokenError:
                # Token is invalid or malformed
                logout(request)
                request.session.flush()
                return HttpResponseForbidden('Invalid token. Please log in again.')
        
        return self.get_response(request)
