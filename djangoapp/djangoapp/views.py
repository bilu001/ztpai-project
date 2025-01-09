import os
import uuid
from datetime import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Player, User
from django.contrib.auth.hashers import make_password,check_password

@csrf_exempt
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
def change_password(request):
    if request.method == 'POST':
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

        is_default = check_password("default", user.password)

        if is_default:
            if current_password != "default":
                return JsonResponse({'error': "Current password is incorrect"}, status=401)
        else:
            if not check_password(current_password, user.password):
                return JsonResponse({'error': "Current password is incorrect"}, status=401)

        user.password = make_password(new_password)
        user.changed_password = True
        user.save()

        return JsonResponse({'message': 'Password changed successfully'}, status=200)

    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def list_players(request):
    if request.method == 'GET':
        all_players = Player.objects.all().values()
        return JsonResponse(list(all_players), safe=False)
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def remove_player(request, player_id):
    if request.method == 'DELETE':
        User.objects.filter(player_id=player_id).delete()

        qs = Player.objects.filter(player_id=player_id)
        if not qs.exists():
            return JsonResponse({"error": "Player not found"}, status=404)
        qs.delete()

        return JsonResponse({"message": "Player removed successfully"}, status=200)
    return HttpResponseNotAllowed(['DELETE'])