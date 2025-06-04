# notificaciones/context_processors.py
from .models import Notificacion

def notificaciones_usuario(request):
    from .models import Notificacion
    if request.user.is_authenticated:
        no_leidas = Notificacion.objects.filter(usuario=request.user, leida=False).count()
        notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha')[:5]  # últimas 5
    else:
        no_leidas = 0
        notificaciones = []
    return {
        'notificaciones_no_leidas': no_leidas,
        'notificaciones_usuario': notificaciones
    }

