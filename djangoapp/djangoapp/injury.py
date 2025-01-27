from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from djangoapp.models import Injury, Player
import json

@method_decorator(csrf_exempt, name='dispatch')
class ReportInjuryView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            player_id = data.get("player_id")
            injury_type = data.get("type")
            location = data.get("location")
            description = data.get("description")
            feelings = data.get("feelings")
            next_visit = data.get("next_visit")

            if not all([player_id, injury_type, location, description]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            player = Player.objects.get(player_id=player_id)
            Injury.objects.create(
                player=player,
                type=injury_type,
                location=location,
                description=description,
                feelings=feelings,
                next_visit=next_visit
            )

            return JsonResponse({"message": "Injury reported successfully"}, status=201)
        except Player.DoesNotExist:
            return JsonResponse({"error": "Player not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
