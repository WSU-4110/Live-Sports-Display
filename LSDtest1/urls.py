from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#import django_toolbar
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('LiveStats/', include('LiveStats.urls')),
  #  path("__debug__/", include("debug_toolbar.urls")),
    path('upload/', views.upload_and_ocr, name='upload'),
    path('', views.home_view, name='home'),
    path('stats_page/', views.stats_page, name='stats_page'),
    path('league_standings/', views.Get_League_Standings, name='league_standings'),
    path('game_schedule/', views.Get_Game_Schedule, name='game_schedule'),
    path('live_team_stats/', views.Get_Live_Team_Stats, name='live_team_stats'),
    path('live_game_stats/', views.Get_Live_Game_Stats, name='live_game_stats'),
    path('live_player_stats/', views.Get_Live_Player_Stats, name='live_player_stats'),
    path('run-ssh/', views.run_ssh, name='run_ssh'),
    path('run-single-display/', views.run_single_display, name='run_single_display'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
