from django.shortcuts import render, redirect, get_object_or_404
from conferencia.models import Conferencia
from .models import Pregunta, Evaluacion, Respuesta
from django.contrib.auth.decorators import login_required
from notificaciones.models import Notificacion

@login_required
def evaluar_conferencia(request, conferencia_id):
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    preguntas = Pregunta.objects.filter(conferencia=conferencia)

    evaluacion, _ = Evaluacion.objects.get_or_create(conferencia=conferencia, revisor=request.user)

    # Diccionario pregunta.id -> puntaje
    respuestas = {r.pregunta.id: r.puntaje for r in evaluacion.respuestas.all()}

    if request.method == 'POST':
        evaluacion.retroalimentacion = request.POST.get('retroalimentacion', '')
        evaluacion.save()

        evaluacion.respuestas.all().delete()

        for pregunta in preguntas:
            key = f'respuesta_{pregunta.id}'
            puntaje = request.POST.get(key)
            if puntaje:
                Respuesta.objects.create(
                    evaluacion=evaluacion,
                    pregunta=pregunta,
                    puntaje=int(puntaje)
                )
        
        # Crear notificación para el autor
        autor = conferencia.autor  # Cambia esto si es otra relación
        mensaje = f"Tu conferencia '{conferencia.nombre}' ha sido evaluada."
        Notificacion.objects.create(usuario=autor, mensaje=mensaje, leida=False)

        return redirect('conferencias_revisor')  # Ajusta esta URL a la que uses

    # Pasamos las preguntas y los puntajes para marcar radios
    preguntas_con_puntajes = [(pregunta, respuestas.get(pregunta.id)) for pregunta in preguntas]

    return render(request, 'formulario/evaluar_conferencia.html', {
        'conferencia': conferencia,
        'preguntas_con_puntajes': preguntas_con_puntajes,
        'evaluacion': evaluacion,
    })


@login_required
def ver_evaluacion(request, conferencia_id):
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    evaluaciones = conferencia.evaluacion_set.all()

    context = {
        'conferencia': conferencia,
        'evaluaciones': evaluaciones,
    }
    return render(request, 'formulario/ver_evaluacion.html', context)

@login_required
def crear_formulario(request, conferencia_id):
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)

    if request.method == 'POST':
        preguntas = request.POST.getlist('preguntas')
        for texto in preguntas:
            if texto.strip():
                Pregunta.objects.create(conferencia=conferencia, texto=texto.strip())
        return redirect('conferencia')

    preguntas_existentes = conferencia.preguntas.all()  # related_name

    return render(request, 'formulario/crear_formulario.html', {
        'conferencia': conferencia,
        'preguntas_existentes': preguntas_existentes
    })

@login_required
def ver_formulario(request, conferencia_id):
    conferencia = get_object_or_404(Conferencia, id=conferencia_id)
    preguntas = Pregunta.objects.filter(conferencia=conferencia)

    if request.method == 'POST':
        for pregunta in preguntas:
            puntaje = request.POST.get(f"respuesta_{pregunta.id}")
            if puntaje:
                Respuesta.objects.create(
                    pregunta=pregunta,
                    puntaje=int(puntaje)
                )
        return redirect('conferencia')  # Redirige a donde prefieras

    return render(request, 'formulario/ver_formulario.html', {
        'conferencia': conferencia,
        'preguntas': preguntas
    })