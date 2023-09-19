from django.contrib import admin
from django.urls import path

from apps.games.views import GameView


urlpatterns = [
    path('admin/', admin.site.urls),
    *GameView.as_my_view('game')
]
