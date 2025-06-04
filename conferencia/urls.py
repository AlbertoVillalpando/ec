from django.urls import path
from . import views

urlpatterns = [
    #path('', views.conferencias_view, name='conferencia'),
    path('editar/<int:pk>/', views.editar_conferencia, name='editar_conferencia'),
    path('eliminar/<int:pk>/', views.eliminar_conferencia, name='eliminar_conferencia'),
    path('conferencias/<int:conferencia_id>/autores/', views.autores_disponibles, name='autores_disponibles'),
    path('conferencias/<int:conferencia_id>/invitaciones/', views.ver_invitaciones_conferencia, name='invitaciones_conferencia'),
    path('usuarios/invitaciones/responder/<int:invitacion_id>/<str:estado>/', views.responder_invitacion, name='responder_invitacion'),

    path('conferencias/<int:conferencia_id>/invitar/', views.invitar_autor, name='invitar_autor'),  # Ruta para invitar autor
    path('invitaciones/responder/<int:invitacion_id>/<str:accion>/', views.responder_invitacion, name='responder_invitacion'),


    path('conferencias/crear/', views.crear_conferencia_view, name='crear_conferencia'),
    path('subir_documentos/<int:pk>/', views.subir_documentos_view, name='subir_documentos'),
    path('conferencia/<int:conferencia_id>/evaluar/', views.evaluar_conferencia, name='evaluar_conferencia'),



    path('conferencias/administrador/', views.conferencias_administrador, name='conferencias_administrador'),
    path('conferencias/autor/', views.conferencias_autor, name='conferencias_autor'),
    path('conferencias/revisor/', views.conferencias_revisor, name='conferencias_revisor'),
    path('conferencias/organizador/', views.conferencias_organizador, name='conferencias_organizador'),


    path("enviar_revision/", views.enviar_revision_conferencia, name="enviar_revision_conferencia"),
    path('reportar-trabajo/', views.reportar_trabajo, name='reportar_trabajo'),
    path('eliminar-trabajo/<int:conf_id>/', views.eliminar_trabajo, name='eliminar_trabajo'),

]