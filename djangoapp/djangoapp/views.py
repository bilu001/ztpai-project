import json
from datetime import datetime
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Player, User, Injury
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@csrf_exempt
@api_view(['POST'])
@swagger_auto_schema(
    operation_description="Add a new player to the team. Requires name, surname, role, and contract end date.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='First name of the player'),
            'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Last name of the player'),
            'role': openapi.Schema(type=openapi.TYPE_STRING, description='Role of the player (e.g., striker)'),
            'contract_end': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Contract end date in YYYY-MM-DD format'),
        },
        required=['name', 'surname', 'role'],
    ),
    responses={
        201: openapi.Response(description="Player added successfully"),
        400: openapi.Response(description="Invalid request data"),
    }
)
def add_player(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        role = request.POST.get('role')
        contract_end = request.POST.get('contract_end') 
        contract_end_date = None
        if contract_end:
            try:
                contract_end_date = datetime.strptime(contract_end, '%Y-%m-%d').date()
            except ValueError:
                pass

        new_player = Player.objects.create(
            name=name,
            surname=surname,
            position=role,
            contract_ends=contract_end_date,
        )


        username = (name[0] + surname).lower() if (name and surname) else "player"
        hashed_default = make_password("default")
        User.objects.create(
            username=username,
            password=hashed_default,
            role='player',
            changed_password=False,
            player_id=new_player.player_id
        )
        return JsonResponse({
            'message': 'Player added successfully',
            'player': {
                'id': new_player.player_id,
                'name': new_player.name,
                'surname': new_player.surname,
                'role': new_player.position,
                'contract_ends': str(new_player.contract_ends) if new_player.contract_ends else None,
            }
        }, status=201)

    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
@api_view(['PUT'])
@swagger_auto_schema(
    operation_description="Change the password for the logged-in user. Requires current and new passwords.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'current_password': openapi.Schema(type=openapi.TYPE_STRING, description='The current password of the user'),
            'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='The new password to set'),
        },
        required=['current_password', 'new_password'],
    ),
    responses={
        200: openapi.Response(description="Password changed successfully"),
        401: openapi.Response(description="Not logged in or incorrect password"),
        400: openapi.Response(description="Invalid request data"),
    }
)
def change_password(request):
    if request.method == 'PUT':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'Not logged in'}, status=401)

        try:
            data = json.loads(request.body)
        except (ValueError, KeyError):
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if check_password("default", user.password):
            if current_password != "default":
                return JsonResponse({'error': "Current password is incorrect"}, status=401)
        else:
            if not check_password(current_password, user.password):
                return JsonResponse({'error': "Current password is incorrect"}, status=401)

        if new_password.strip() == "":
            return JsonResponse({'error': "New password cannot be empty"}, status=400)

        user.password = make_password(new_password)
        user.changed_password = True
        user.save()

        return JsonResponse({'message': 'Password changed successfully'}, status=200)

    return HttpResponseNotAllowed(['PUT'])

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Retrieve a list of all players in the team.",
    responses={
        200: openapi.Response(description="List of players retrieved successfully"),
    }
)
def list_players(request):
    if request.method == 'GET':
        all_players = Player.objects.all().values()
        return JsonResponse(list(all_players), safe=False)
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
@api_view(['DELETE'])
@swagger_auto_schema(
    operation_description="Remove a player by their ID.",
    responses={
        200: openapi.Response(description="Player removed successfully"),
        404: openapi.Response(description="Player not found"),
    }
)
def remove_player(request, player_id):
    if request.method == 'DELETE':
        User.objects.filter(player_id=player_id).delete()
        qs = Player.objects.filter(player_id=player_id)
        if not qs.exists():
            return JsonResponse({"error": "Player not found"}, status=404)
        qs.delete()

        return JsonResponse({"message": "Player removed successfully"}, status=200)
    return HttpResponseNotAllowed(['DELETE'])

@csrf_exempt
@api_view(['GET'])  # Register the HTTP method with DRF
@swagger_auto_schema(
    operation_description="Retrieve the player_id for a given username.",
    responses={
        200: openapi.Response(
            description="Player ID retrieved successfully",
            examples={
                "application/json": {"player_id": 1}
            }
        ),
        404: openapi.Response(description="User not found"),
        400: openapi.Response(description="Unexpected error"),
    }
)
def get_player_id_by_username(request, username):
    if request.method == 'GET':
        try:
            print(f"Looking up username: {username}") 
            user = User.objects.get(username=username)
            print(f"Found user: {user}")

            return JsonResponse({"player_id": user.player_id}, status=200) 
        except User.DoesNotExist:
            print(f"User not found for username: {username}")
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Retrieve the total number of reported injuries.",
    responses={
        200: openapi.Response(description="Injury count retrieved successfully"),
    }
)
def get_injury_count(request):
    if request.method == 'GET':
        try:
            injury_count = Injury.objects.count()  # Count all injuries in the table
            return JsonResponse({"injury_count": injury_count}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)