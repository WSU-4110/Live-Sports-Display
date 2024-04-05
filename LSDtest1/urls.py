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
    path('team_stats/', views.Get_Team_Stats, name='team_stats'),
    path('live_stats/', views.Get_Live_Stats, name='live_stats'),
    path('run-ssh/', views.run_ssh, name='run_ssh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
