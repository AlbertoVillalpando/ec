# notificaciones/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dropdown/', views.dropdown_notificaciones, name='dropdown_notificaciones'),
    path('marcar-como-leidas/', views.marcar_notificaciones_leidas, name='marcar_notificaciones_leidas'),
]
