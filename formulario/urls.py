from django.urls import path
from . import views

urlpatterns = [
    path('crear/<int:conferencia_id>/', views.crear_formulario, name='crear_formulario'),
    path('ver/<int:conferencia_id>/', views.ver_formulario, name='ver_formulario'),
    path('evaluar/<int:conferencia_id>/', views.evaluar_conferencia, name='evaluar_conferencia'),
    path('ver_evaluacion/<int:conferencia_id>/', views.ver_evaluacion, name='ver_evaluacion'),
]
