# logout.py
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request, *args, **kwargs):
        """
        Destroys the session for the logged-in user.
        """
        request.session.flush()  # remove session data
        return JsonResponse({'message': 'Logged out successfully'}, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return 405 for GET requests if you only allow POST.
        """
        return JsonResponse({'error': 'Method not allowed'}, status=405)
