from django.urls import path
from djangoapp.login import LoginView
from djangoapp.views import add_player, change_password, list_players, remove_player, get_player_id_by_username, get_injury_count
from django.conf import settings
from django.conf.urls.static import static
from djangoapp.logout import LogoutView
from djangoapp.injury import ReportInjuryView
from djangoapp.swagger import schema_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('api/add_player/', add_player, name='add_player'),
    path('api/players/', list_players, name='list_players'),
    path('change_password/', change_password, name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/remove_player/<int:player_id>/', remove_player, name='remove_player'),
    path('api/report_injury/', ReportInjuryView.as_view(), name='report_injury'),
    path('api/get-player-id-by-username/<str:username>/', get_player_id_by_username, name='get_player_id_by_username'),
    path('api/injury-count/', get_injury_count, name='injury_count'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # Optional alternative UI
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)