from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_and_ocr, name='upload'),
    path('', views.home_view, name='home'),
]
