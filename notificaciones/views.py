# notificaciones/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notificacion
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST


@login_required
def dropdown_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')[:5]
    return render(request, 'notificaciones/_dropdown.html', {
        'notificaciones': notificaciones
    })


@csrf_exempt
@login_required
def marcar_notificaciones_leidas(request):
    if request.method == 'POST':
        Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


