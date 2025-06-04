from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    invitaciones_autor_view,
    responder_invitacion_revisor_view,
)

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('autor/', views.vistaAutor, name='vistaAutor'),
    path('organizador/', views.vistaOrganizador, name='vistaOrganizador'),
    path('revisor/', views.vistaRevisor, name='vistaRevisor'),
    path('adminis/', views.vistaAdmin, name='vistaAdmin'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('actualizar-roles/', views.actualizar_roles, name='actualizar_roles'),
    path('logout/', views.logout_view, name='logout'),
    path('panel-organizador/', views.vista_organizador, name='vistaOrganizador'),
    path('invitaciones/', invitaciones_autor_view, name='invitaciones_autor'),
    path('invitaciones/responder/<int:invitacion_id>/', responder_invitacion_revisor_view, name='responder_invitacion'),



    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]