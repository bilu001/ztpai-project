import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from djangoapp.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    """
    Handle user login via POST method.
    """

    def options(self, request, *args, **kwargs):
        """
        Handle the preflight CORS request by returning the CORS headers.
        """
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def post(self, request, *args, **kwargs):
        """
        Handle user login and return user details or error response.
        """
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except (ValueError, KeyError):
            return self._error_response('Invalid JSON or missing fields', 400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return self._error_response('Invalid username or password', 401)

        if not check_password(password, user.password):
            return self._error_response('Invalid username or password', 401)
        request.session['user_id'] = user.user_id
        request.session['role'] = user.role

        return JsonResponse({
            'message': 'Login successful',
            'user': {
                'id': user.user_id,
                'username': user.username,
                'role': user.role,
                'changed_password': user.changed_password
            }
        }, status=200)

    def _error_response(self, message, status):
        """
        Return a standardized error response with CORS headers.
        """
        response = JsonResponse({'error': message}, status=status)
        response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def get(self, request, *args, **kwargs):
        """
        Handle invalid GET requests for login.
        """
        return self._error_response('Use POST method for login', 405)