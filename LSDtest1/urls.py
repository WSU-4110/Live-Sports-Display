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
  #  path('run-ssh/', views.run_ssh, name='run_ssh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
