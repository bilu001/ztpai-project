from django.urls import path
from djangoapp.login import LoginView
from djangoapp.views import add_player, change_password, list_players, remove_player
from django.conf import settings
from django.conf.urls.static import static
from djangoapp.logout import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('api/add_player/', add_player, name='add_player'),
    path('api/players/', list_players, name='list_players'),
    path('change_password/', change_password, name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/remove_player/<int:player_id>/', remove_player, name='remove_player')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)