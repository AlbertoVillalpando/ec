import os
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Conferencia
from django.http import HttpResponseRedirect
from .forms import ConferenciaForm
from django.contrib.auth.models import Group
from django.http import JsonResponse
from usuarios.models import CustomUser
from notificaciones.models import Notificacion
from .models import InvitacionRevisor, Conferencia
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import json


@login_required
def conferencias_administrador(request):
    conferencias = Conferencia.objects.all()
    return render(request, 'conferencia/conferencias_administrador.html', {
        'conferencias': conferencias,
        'es_autor': False,
        'es_revisor': False,
    })

@login_required
def conferencias_autor(request):
    conferencias = Conferencia.objects.filter(autor=request.user)
    return render(request, 'conferencia/conferencias_autor.html', {'conferencias': conferencias})

@login_required
def conferencias_revisor(request):
    conferencias = request.user.conferencias_como_revisor
    return render(request, 'conferencia/conferencias_revisor.html', {'conferencias': conferencias})


@login_required
def conferencias_organizador(request):
    conferencias = Conferencia.objects.all()  # o con más filtros según permisos
    return render(request, 'conferencia/conferencias_organizador.html', {'conferencias': conferencias})

@login_required
def evaluar_conferencia(request, conferencia_id):
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    preguntas = conferencia.preguntas.all()  # si usas related_name='preguntas'

    return render(request, 'conferencia/evaluar_conferencia.html', {
        'conferencia': conferencia,
        'preguntas': preguntas,
    })

@login_required
def subir_documentos_view(request, pk):
    conferencia = get_object_or_404(Conferencia, pk=pk)

    if request.method == 'POST':
        archivo = request.FILES.get('archivo')

        if not archivo:
            return redirect(request.path)

        if not archivo.name.endswith('.zip'):
            return redirect(request.path)

        conferencia.archivo_zip = archivo
        conferencia.save()

        return redirect('conferencias_autor')

    return render(request, 'conferencia/subir_documentos.html', {'conferencia': conferencia})

@login_required
def crear_conferencia_view(request):
    if request.method == 'POST':
        form = ConferenciaForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('conferencias_administrador')
    else:
        form = ConferenciaForm()

    return render(request, 'conferencia/crear_conferencia.html', {'form': form})



@login_required
def editar_conferencia(request, pk):
    conferencia = get_object_or_404(Conferencia, pk=pk)
    if request.method == 'POST':
        form = ConferenciaForm(request.POST, instance=conferencia)
        if form.is_valid():
            form.save()
            return redirect('conferencias_administrador')
    else:
        form = ConferenciaForm(instance=conferencia)
    return render(request, 'conferencia/editar.html', {'form': form})


@login_required
def eliminar_conferencia(request, pk):
    conferencia = get_object_or_404(Conferencia, pk=pk)
    conferencia.delete()
    return redirect('conferencias_administrador')


@login_required
def autores_disponibles(request, conferencia_id):
    autores = CustomUser.objects.filter(groups__name='Autor')
    invitados_ids = InvitacionRevisor.objects.filter(conferencia_id=conferencia_id).values_list('autor_id', flat=True)
    disponibles = autores.exclude(id__in=invitados_ids)

    data = [
        {"id": autor.id, "nombre": f"{autor.nombre} {autor.apellidos}", "email": autor.email}
        for autor in disponibles
    ]
    return JsonResponse(data, safe=False)


@login_required
def ver_invitaciones_conferencia(request, conferencia_id):
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    invitaciones = InvitacionRevisor.objects.filter(conferencia=conferencia)
    
    # Filtrar autores disponibles (que no hayan sido invitados aún)
    autores_disponibles = CustomUser.objects.exclude(id__in=invitaciones.values('autor_id'))
    
    return render(request, 'conferencia/invitaciones_conferencia.html', {
        'conferencia': conferencia,
        'invitaciones': invitaciones,
        'autores_disponibles': autores_disponibles,
    })


@login_required
def responder_invitacion(request, invitacion_id, accion):
    invitacion = get_object_or_404(InvitacionRevisor, id=invitacion_id, autor=request.user)

    accion_lower = accion.lower()
    if accion_lower == 'aceptar':
        invitacion.estado = 'aceptado'
        invitacion.save()

        autor = invitacion.autor
        revisor_group, _ = Group.objects.get_or_create(name='Revisor')
        autor.groups.add(revisor_group)

    elif accion_lower == 'rechazar':
        invitacion.estado = 'rechazado'
        invitacion.save()

    return redirect('invitaciones_conferencia', conferencia_id=invitacion.conferencia.id)



@login_required
def invitar_autor(request, conferencia_id):
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    
    if request.method == 'POST':
        autor_id = request.POST.get('autor')
        autor = get_object_or_404(CustomUser, id=autor_id)
        
        # Crear la invitación para el autor
        invitacion = InvitacionRevisor(conferencia=conferencia, autor=autor)
        invitacion.save()
        
        return redirect('invitaciones_conferencia', conferencia_id=conferencia.id)


    # Para el caso en que la petición sea GET, obtener todos los autores disponibles.
    autores_disponibles = CustomUser.objects.filter(groups__name='Autor')  # Solo autores

    # Obtener las invitaciones ya enviadas para esta conferencia
    invitaciones = InvitacionRevisor.objects.filter(conferencia=conferencia)

    return render(request, 'conferencia/invitar_autor.html', {
        'conferencia': conferencia,
        'autores_disponibles': autores_disponibles,
        'invitaciones': invitaciones
    })

@csrf_exempt
@login_required
def enviar_revision_conferencia(request):
    if request.method == "POST":
        data = json.loads(request.body)
        conferencia_id = data.get("conferencia_id")
        decision = data.get("decision")

        conferencia = Conferencia.objects.get(id=conferencia_id)
        conferencia.estado_revision = decision  # campo nuevo en el modelo
        conferencia.save()

        # Crear notificación
        mensaje = f"Tu conferencia '{conferencia.nombre}' ha sido {decision}."
        Notificacion.objects.create(
            usuario=conferencia.autor,
            mensaje=mensaje,
            leida=False
        )

        return JsonResponse({"estado": decision})
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def reportar_trabajo(request):
    if request.method == "POST":
        data = json.loads(request.body)
        conferencia_id = data.get("conferencia_id")
        conferencia = Conferencia.objects.get(id=conferencia_id)
        conferencia.trabajo_reportado = True
        conferencia.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})

@csrf_exempt
def eliminar_trabajo(request, conf_id):
    conferencia = Conferencia.objects.get(id=conf_id)
    if conferencia.trabajo_reportado and conferencia.archivo_zip:
        path = conferencia.archivo_zip.path
        if os.path.exists(path):
            os.remove(path)
        conferencia.archivo_zip = None
        conferencia.trabajo_reportado = False
        conferencia.save()
    return redirect('conferencias_administrador')  # Ajusta si tu nombre de URL es diferente