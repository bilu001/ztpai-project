import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from djangoapp.models import User
from django.contrib.auth.hashers import check_password

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def options(self, request, *args, **kwargs):
        """
        Handle the preflight request by returning the CORS headers.
        """
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        #response['Access-Control-Allow-Credentials'] = 'true'
        return response

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except (ValueError, KeyError):
            response = JsonResponse({'error': 'Invalid JSON'}, status=400)
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            response = JsonResponse({'error': 'Invalid username or password'}, status=401)
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

        if not check_password(password, user.password):
            response = JsonResponse({'error': 'Invalid username or password'}, status=401)
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

        if user.role != 'coach':
            request.session['user_id'] = user.user_id
            request.session['role'] = user.role

            response = JsonResponse({
                'message': 'User logged',
                'user_id': user.user_id,
                'role': user.role
            }, status=200)
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

        request.session['user_id'] = user.user_id
        request.session['role'] = user.role

        response = JsonResponse({
            'message': 'Login successful',
            'user_id': user.user_id,
            'role': user.role
        }, status=200)
        response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def get(self, request, *args, **kwargs):
        """
        If someone tries GET, return method not allowed (405),
        but still attach CORS headers so the browser doesn't complain.
        """
        response = JsonResponse({'error': 'Use POST method for login'}, status=405)
        response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
